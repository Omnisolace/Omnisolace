"""
情绪分析相关模型
"""
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
import uuid
import json

User = get_user_model()


class EmotionLog(models.Model):
    """
    情绪日志模型
    """
    class EmotionLabel(models.TextChoices):
        HAPPY = 'happy', '开心'
        SAD = 'sad', '难过'
        ANGRY = 'angry', '愤怒'
        ANXIOUS = 'anxious', '焦虑'
        FEAR = 'fear', '恐惧'
        SURPRISED = 'surprised', '惊讶'
        DISGUSTED = 'disgusted', '厌恶'
        NEUTRAL = 'neutral', '平静'
        EXCITED = 'excited', '兴奋'
        DEPRESSED = 'depressed', '抑郁'
        CONFUSED = 'confused', '困惑'
        HOPEFUL = 'hopeful', '充满希望'
        LONELY = 'lonely', '孤独'
        STRESSED = 'stressed', '压力'
        CALM = 'calm', '冷静'
    
    class AnalysisSource(models.TextChoices):
        TEXT = 'text', '文本分析'
        VOICE = 'voice', '语音分析'
        BEHAVIOR = 'behavior', '行为分析'
        MANUAL = 'manual', '手动标注'
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='emotion_logs')
    chat_message = models.ForeignKey(
        'chat.ChatMessage', 
        on_delete=models.CASCADE, 
        related_name='emotion_logs',
        null=True,
        blank=True
    )
    
    # 情绪信息
    emotion_label = models.CharField(
        max_length=20,
        choices=EmotionLabel.choices,
        verbose_name='情绪标签'
    )
    confidence = models.FloatField(verbose_name='置信度', help_text='0.0-1.0')
    intensity = models.PositiveSmallIntegerField(
        verbose_name='强度',
        help_text='0-100, 0为最低强度，100为最高强度'
    )
    
    # 分析信息
    analysis_source = models.CharField(
        max_length=20,
        choices=AnalysisSource.choices,
        verbose_name='分析来源'
    )
    raw_data = models.JSONField(verbose_name='原始分析数据', default=dict)
    keywords = models.JSONField(verbose_name='情绪关键词', default=list)
    
    # 上下文信息
    context = models.JSONField(verbose_name='上下文信息', default=dict)
    session_emotion_trend = models.JSONField(verbose_name='会话情绪趋势', default=list)
    
    # 危机检测
    crisis_indicators = models.JSONField(verbose_name='危机指标', default=list)
    risk_level = models.PositiveSmallIntegerField(
        default=0,
        verbose_name='风险等级',
        help_text='0-5, 0为无风险，5为极高风险'
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        verbose_name = '情绪日志'
        verbose_name_plural = '情绪日志'
        db_table = 'emotion_logs'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['emotion_label']),
            models.Index(fields=['risk_level']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.get_emotion_label_display()} ({self.intensity}%)"
    
    @property
    def is_negative_emotion(self):
        """是否为负面情绪"""
        negative_emotions = [
            self.EmotionLabel.SAD,
            self.EmotionLabel.ANGRY,
            self.EmotionLabel.ANXIOUS,
            self.EmotionLabel.FEAR,
            self.EmotionLabel.DEPRESSED,
            self.EmotionLabel.LONELY,
            self.EmotionLabel.STRESSED,
        ]
        return self.emotion_label in negative_emotions
    
    @property
    def is_crisis_risk(self):
        """是否存在危机风险"""
        return self.risk_level >= 3
    
    def calculate_emotion_trend(self, days=7):
        """计算情绪趋势"""
        from datetime import timedelta
        from django.db.models import Avg
        
        start_date = self.created_at - timedelta(days=days)
        
        trend_data = EmotionLog.objects.filter(
            user=self.user,
            created_at__gte=start_date
        ).values('emotion_label').annotate(
            avg_intensity=Avg('intensity'),
            count=models.Count('id')
        )
        
        return list(trend_data)
    
    def get_similar_emotions(self, threshold=0.7):
        """获取相似情绪记录"""
        return EmotionLog.objects.filter(
            user=self.user,
            emotion_label=self.emotion_label,
            confidence__gte=threshold
        ).exclude(id=self.id)[:10]


class EmotionPattern(models.Model):
    """
    情绪模式模型 - 用于分析用户的情绪规律
    """
    class PatternType(models.TextChoices):
        DAILY = 'daily', '每日模式'
        WEEKLY = 'weekly', '每周模式'
        SITUATIONAL = 'situational', '情境模式'
        TRIGGER = 'trigger', '触发模式'
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='emotion_patterns')
    
    pattern_type = models.CharField(
        max_length=20,
        choices=PatternType.choices,
        verbose_name='模式类型'
    )
    pattern_data = models.JSONField(verbose_name='模式数据')
    confidence = models.FloatField(verbose_name='模式置信度')
    
    # 模式描述
    description = models.TextField(verbose_name='模式描述')
    triggers = models.JSONField(verbose_name='触发因素', default=list)
    recommendations = models.JSONField(verbose_name='建议', default=list)
    
    # 统计信息
    occurrence_count = models.PositiveIntegerField(default=1, verbose_name='出现次数')
    accuracy_rate = models.FloatField(default=0.0, verbose_name='准确率')
    
    is_active = models.BooleanField(default=True, verbose_name='是否活跃')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    last_occurrence = models.DateTimeField(verbose_name='最后出现时间')
    
    class Meta:
        verbose_name = '情绪模式'
        verbose_name_plural = '情绪模式'
        db_table = 'emotion_patterns'
        unique_together = ['user', 'pattern_type', 'pattern_data']
    
    def __str__(self):
        return f"{self.user.username} - {self.get_pattern_type_display()}"
    
    def update_occurrence(self):
        """更新出现次数"""
        self.occurrence_count += 1
        self.last_occurrence = timezone.now()
        self.save(update_fields=['occurrence_count', 'last_occurrence'])
    
    def calculate_accuracy(self):
        """计算模式准确率"""
        # 这里可以实现具体的准确率计算逻辑
        pass


class EmotionAnalysisModel(models.Model):
    """
    情绪分析模型配置
    """
    class ModelType(models.TextChoices):
        TEXT_CNN = 'text_cnn', '文本CNN'
        BERT = 'bert', 'BERT模型'
        LSTM = 'lstm', 'LSTM模型'
        TRANSFORMER = 'transformer', 'Transformer'
        RULE_BASED = 'rule_based', '规则基础'
        HYBRID = 'hybrid', '混合模型'
    
    name = models.CharField(max_length=100, verbose_name='模型名称')
    model_type = models.CharField(
        max_length=20,
        choices=ModelType.choices,
        verbose_name='模型类型'
    )
    version = models.CharField(max_length=20, verbose_name='版本号')
    
    # 模型配置
    config = models.JSONField(verbose_name='模型配置', default=dict)
    weights_path = models.CharField(max_length=500, verbose_name='权重路径', blank=True)
    
    # 性能指标
    accuracy = models.FloatField(verbose_name='准确率', default=0.0)
    precision = models.FloatField(verbose_name='精确率', default=0.0)
    recall = models.FloatField(verbose_name='召回率', default=0.0)
    f1_score = models.FloatField(verbose_name='F1分数', default=0.0)
    
    # 使用统计
    usage_count = models.PositiveIntegerField(default=0, verbose_name='使用次数')
    avg_processing_time = models.FloatField(default=0.0, verbose_name='平均处理时间')
    
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    is_default = models.BooleanField(default=False, verbose_name='是否默认')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '情绪分析模型'
        verbose_name_plural = '情绪分析模型'
        db_table = 'emotion_analysis_models'
    
    def __str__(self):
        return f"{self.name} v{self.version}"
    
    def save(self, *args, **kwargs):
        # 如果设置为默认模型，取消其他默认模型
        if self.is_default:
            EmotionAnalysisModel.objects.filter(
                model_type=self.model_type,
                is_default=True
            ).exclude(id=self.id).update(is_default=False)
        
        super().save(*args, **kwargs)


class CrisisAlert(models.Model):
    """
    危机预警模型
    """
    class AlertLevel(models.TextChoices):
        LOW = 'low', '低风险'
        MEDIUM = 'medium', '中风险'
        HIGH = 'high', '高风险'
        CRITICAL = 'critical', '紧急'
    
    class AlertStatus(models.TextChoices):
        PENDING = 'pending', '待处理'
        ACKNOWLEDGED = 'acknowledged', '已确认'
        RESOLVED = 'resolved', '已解决'
        FALSE_POSITIVE = 'false_positive', '误报'
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='crisis_alerts')
    emotion_log = models.ForeignKey(
        EmotionLog, 
        on_delete=models.CASCADE, 
        related_name='crisis_alerts',
        null=True,
        blank=True
    )
    chat_message = models.ForeignKey(
        'chat.ChatMessage',
        on_delete=models.CASCADE,
        related_name='crisis_alerts',
        null=True,
        blank=True
    )
    
    # 预警信息
    alert_level = models.CharField(
        max_length=20,
        choices=AlertLevel.choices,
        verbose_name='预警级别'
    )
    alert_status = models.CharField(
        max_length=20,
        choices=AlertStatus.choices,
        default=AlertStatus.PENDING,
        verbose_name='预警状态'
    )
    
    # 检测信息
    trigger_keywords = models.JSONField(verbose_name='触发关键词', default=list)
    risk_indicators = models.JSONField(verbose_name='风险指标', default=list)
    confidence_score = models.FloatField(verbose_name='置信分数')
    
    # 处理信息
    auto_response_sent = models.BooleanField(default=False, verbose_name='自动回复已发送')
    emergency_contacts_notified = models.BooleanField(default=False, verbose_name='紧急联系人已通知')
    professional_referral = models.BooleanField(default=False, verbose_name='专业转介')
    
    # 备注
    notes = models.TextField(verbose_name='备注', blank=True)
    handled_by = models.CharField(max_length=100, verbose_name='处理人', blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    resolved_at = models.DateTimeField(null=True, blank=True, verbose_name='解决时间')
    
    class Meta:
        verbose_name = '危机预警'
        verbose_name_plural = '危机预警'
        db_table = 'crisis_alerts'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'alert_level']),
            models.Index(fields=['alert_status']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.get_alert_level_display()}"
    
    def acknowledge(self, handler=None):
        """确认预警"""
        self.alert_status = self.AlertStatus.ACKNOWLEDGED
        if handler:
            self.handled_by = handler
        self.save(update_fields=['alert_status', 'handled_by'])
    
    def resolve(self, notes=None):
        """解决预警"""
        self.alert_status = self.AlertStatus.RESOLVED
        self.resolved_at = timezone.now()
        if notes:
            self.notes = notes
        self.save(update_fields=['alert_status', 'resolved_at', 'notes'])
    
    def mark_false_positive(self):
        """标记为误报"""
        self.alert_status = self.AlertStatus.FALSE_POSITIVE
        self.resolved_at = timezone.now()
        self.save(update_fields=['alert_status', 'resolved_at'])
