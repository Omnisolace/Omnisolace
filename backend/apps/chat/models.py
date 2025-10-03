"""
聊天相关模型
"""
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
import uuid
import json

User = get_user_model()


class ChatSession(models.Model):
    """
    聊天会话模型
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_sessions')
    
    title = models.CharField(max_length=200, verbose_name='会话标题', default='新的对话')
    summary = models.TextField(verbose_name='会话摘要', blank=True)
    
    # 会话状态
    is_active = models.BooleanField(default=True, verbose_name='是否活跃')
    is_archived = models.BooleanField(default=False, verbose_name='是否归档')
    is_emergency = models.BooleanField(default=False, verbose_name='紧急会话')
    
    # 统计信息
    message_count = models.PositiveIntegerField(default=0, verbose_name='消息数量')
    duration_minutes = models.PositiveIntegerField(default=0, verbose_name='持续时间(分钟)')
    
    # 时间戳
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    last_message_at = models.DateTimeField(null=True, blank=True, verbose_name='最后消息时间')
    
    # 数据脱敏
    is_desensitized = models.BooleanField(default=False, verbose_name='已脱敏')
    desensitized_at = models.DateTimeField(null=True, blank=True, verbose_name='脱敏时间')
    
    class Meta:
        verbose_name = '聊天会话'
        verbose_name_plural = '聊天会话'
        db_table = 'chat_sessions'
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['user', 'is_active']),
            models.Index(fields=['created_at']),
            models.Index(fields=['is_emergency']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"
    
    def update_last_message_time(self):
        """更新最后消息时间"""
        self.last_message_at = timezone.now()
        self.save(update_fields=['last_message_at', 'updated_at'])
    
    def increment_message_count(self):
        """增加消息计数"""
        self.message_count += 1
        self.save(update_fields=['message_count'])
    
    def generate_title(self):
        """根据首条消息生成标题"""
        first_user_message = self.messages.filter(
            sender_type='user'
        ).first()
        
        if first_user_message:
            content = first_user_message.content[:50]
            self.title = content + ('...' if len(first_user_message.content) > 50 else '')
            self.save(update_fields=['title'])
    
    def schedule_desensitization(self):
        """安排数据脱敏"""
        from datetime import timedelta
        from django.conf import settings
        
        days = getattr(settings, 'CHAT_DESENSITIZATION_DAYS', 7)
        target_time = self.created_at + timedelta(days=days)
        
        # 这里可以添加定时任务来执行脱敏
        return target_time


class ChatMessage(models.Model):
    """
    聊天消息模型
    """
    class SenderType(models.TextChoices):
        USER = 'user', '用户'
        AI = 'ai', 'AI助手'
        SYSTEM = 'system', '系统'
    
    class MessageType(models.TextChoices):
        TEXT = 'text', '文本'
        AUDIO = 'audio', '语音'
        IMAGE = 'image', '图片'
        SYSTEM_NOTICE = 'system_notice', '系统通知'
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    
    # 消息内容
    content = models.TextField(verbose_name='消息内容')
    message_type = models.CharField(
        max_length=20,
        choices=MessageType.choices,
        default=MessageType.TEXT,
        verbose_name='消息类型'
    )
    sender_type = models.CharField(
        max_length=10,
        choices=SenderType.choices,
        verbose_name='发送者类型'
    )
    
    # 媒体文件
    audio_file = models.FileField(upload_to='chat/audio/%Y/%m/', null=True, blank=True, verbose_name='语音文件')
    image_file = models.ImageField(upload_to='chat/images/%Y/%m/', null=True, blank=True, verbose_name='图片文件')
    
    # 消息元数据
    metadata = models.JSONField(default=dict, verbose_name='元数据')
    
    # 情绪信息
    emotion_data = models.JSONField(null=True, blank=True, verbose_name='情绪数据')
    
    # 危机检测
    crisis_detected = models.BooleanField(default=False, verbose_name='检测到危机')
    crisis_keywords = models.JSONField(default=list, verbose_name='危机关键词')
    
    # AI回复相关
    ai_model = models.CharField(max_length=50, verbose_name='AI模型', blank=True)
    ai_confidence = models.FloatField(null=True, blank=True, verbose_name='AI置信度')
    processing_time = models.FloatField(null=True, blank=True, verbose_name='处理时间(秒)')
    
    # 时间戳
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    # 数据脱敏
    original_content = models.TextField(null=True, blank=True, verbose_name='原始内容')
    is_desensitized = models.BooleanField(default=False, verbose_name='已脱敏')
    
    class Meta:
        verbose_name = '聊天消息'
        verbose_name_plural = '聊天消息'
        db_table = 'chat_messages'
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['session', 'created_at']),
            models.Index(fields=['sender_type']),
            models.Index(fields=['crisis_detected']),
        ]
    
    def __str__(self):
        return f"{self.get_sender_type_display()} - {self.content[:50]}"
    
    def save(self, *args, **kwargs):
        # 保存消息时更新会话信息
        super().save(*args, **kwargs)
        
        if self.session:
            self.session.update_last_message_time()
            self.session.increment_message_count()
            
            # 如果是首条用户消息，生成标题
            if self.sender_type == self.SenderType.USER and self.session.message_count == 1:
                self.session.generate_title()
    
    def desensitize_content(self):
        """脱敏处理消息内容"""
        if not self.is_desensitized and self.content:
            self.original_content = self.content
            
            # 脱敏处理逻辑
            desensitized = self.content
            
            # 替换手机号
            import re
            desensitized = re.sub(r'1[3-9]\d{9}|1\d{10}', '1****', desensitized)
            
            # 替换身份证号
            desensitized = re.sub(r'\d{17}[\dXx]', '****', desensitized)
            
            # 替换邮箱
            desensitized = re.sub(r'\w+@\w+\.\w+', '****@****.***', desensitized)
            
            # 替换姓名（简单处理，实际可能需要更复杂的NLP）
            # 这里可以添加更多脱敏规则
            
            self.content = desensitized
            self.is_desensitized = True
            self.save(update_fields=['content', 'original_content', 'is_desensitized'])
    
    def get_emotion_summary(self):
        """获取情绪摘要"""
        if not self.emotion_data:
            return None
        
        return {
            'primary_emotion': self.emotion_data.get('label', 'neutral'),
            'confidence': self.emotion_data.get('confidence', 0),
            'score': self.emotion_data.get('score', 50)
        }


class ChatFeedback(models.Model):
    """
    聊天反馈模型
    """
    class FeedbackType(models.TextChoices):
        POSITIVE = 'positive', '正反馈'
        NEGATIVE = 'negative', '负反馈'
    
    class PositiveCategory(models.TextChoices):
        ACCURATE = 'accurate', '准确有效'
        COMPREHENSIVE = 'comprehensive', '回答全面'
        CORRECT_STANCE = 'correctStance', '立场正确'
        STANDARD_FORMAT = 'standardFormat', '格式规范'
    
    class NegativeCategory(models.TextChoices):
        # 针对回答的负反馈
        FACTUAL_ERROR = 'factualError', '事实错误'
        INCOMPLETE_CONTENT = 'incompleteContent', '内容不完整'
        CALCULATION_ERROR = 'calculationError', '计算错误'
        REASONING_ERROR = 'reasoningError', '推理错误'
        UNPROFESSIONAL_CONTENT = 'unprofessionalContent', '内容不专业'
        ILLEGAL_HARMFUL = 'illegalHarmful', '违法有害'
        
        # 针对格式的负反馈
        FORMAT_ERROR = 'formatError', '格式错误'
        REPETITIVE_CONTENT = 'repetitiveContent', '内容重复'
        GARBLED_TEXT = 'garbledText', '乱码错误'
        NEEDS_DIAGRAM = 'needsDiagram', '需画图但生成文本'
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_feedbacks')
    message = models.ForeignKey(ChatMessage, on_delete=models.CASCADE, related_name='feedbacks')
    
    # 反馈类型和分类
    feedback_type = models.CharField(
        max_length=20,
        choices=FeedbackType.choices,
        verbose_name='反馈类型'
    )
    positive_category = models.CharField(
        max_length=20,
        choices=PositiveCategory.choices,
        null=True,
        blank=True,
        verbose_name='正反馈分类'
    )
    negative_category = models.CharField(
        max_length=25,
        choices=NegativeCategory.choices,
        null=True,
        blank=True,
        verbose_name='负反馈分类'
    )
    
    # 详细反馈内容
    additional_feedback = models.TextField(verbose_name='额外反馈', blank=True)
    
    # 评分（保留原有字段以兼容）
    rating = models.PositiveSmallIntegerField(
        choices=[(i, f'{i}星') for i in range(1, 6)],
        null=True,
        blank=True,
        verbose_name='评分'
    )
    
    # 时间戳
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        verbose_name = '聊天反馈'
        verbose_name_plural = '聊天反馈'
        db_table = 'chat_feedbacks'
        unique_together = ['user', 'message']
        indexes = [
            models.Index(fields=['feedback_type']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.get_feedback_type_display()}"
    
    def get_category_display(self):
        """获取分类显示名称"""
        if self.feedback_type == self.FeedbackType.POSITIVE and self.positive_category:
            return dict(self.PositiveCategory.choices).get(self.positive_category, '')
        elif self.feedback_type == self.FeedbackType.NEGATIVE and self.negative_category:
            return dict(self.NegativeCategory.choices).get(self.negative_category, '')
        return ''
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': str(self.id),
            'feedback_type': self.feedback_type,
            'positive_category': self.positive_category,
            'negative_category': self.negative_category,
            'additional_feedback': self.additional_feedback,
            'rating': self.rating,
            'created_at': self.created_at.isoformat(),
            'category_display': self.get_category_display()
        }


class ChatTemplate(models.Model):
    """
    聊天模板 - 预设回复模板
    """
    class TemplateType(models.TextChoices):
        GREETING = 'greeting', '问候语'
        ENCOURAGEMENT = 'encouragement', '鼓励语'
        CRISIS_RESPONSE = 'crisis_response', '危机回应'
        CLOSURE = 'closure', '结束语'
        AGE_SPECIFIC = 'age_specific', '年龄段专用'
    
    name = models.CharField(max_length=100, verbose_name='模板名称')
    template_type = models.CharField(
        max_length=20,
        choices=TemplateType.choices,
        verbose_name='模板类型'
    )
    content = models.TextField(verbose_name='模板内容')
    
    # 使用条件
    age_groups = models.JSONField(default=list, verbose_name='适用年龄段')
    emotion_triggers = models.JSONField(default=list, verbose_name='情绪触发条件')
    keywords = models.JSONField(default=list, verbose_name='关键词')
    
    # 统计信息
    usage_count = models.PositiveIntegerField(default=0, verbose_name='使用次数')
    effectiveness_score = models.FloatField(default=0.0, verbose_name='效果评分')
    
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '聊天模板'
        verbose_name_plural = '聊天模板'
        db_table = 'chat_templates'
    
    def __str__(self):
        return f"{self.name} - {self.get_template_type_display()}"
    
    def increment_usage(self):
        """增加使用计数"""
        self.usage_count += 1
        self.save(update_fields=['usage_count'])
    
    def update_effectiveness(self, score):
        """更新效果评分"""
        # 使用简单的移动平均算法
        if self.effectiveness_score == 0:
            self.effectiveness_score = score
        else:
            self.effectiveness_score = (self.effectiveness_score * 0.9 + score * 0.1)
        self.save(update_fields=['effectiveness_score'])
