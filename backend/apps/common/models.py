from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()


class SystemLog(models.Model):
    """系统操作日志模型"""
    ACTION_TYPES = [
        ('login', '登录'),
        ('logout', '登出'),
        ('register', '注册'),
        ('update_profile', '更新资料'),
        ('create_chat', '创建对话'),
        ('send_message', '发送消息'),
        ('emotion_analysis', '情绪分析'),
        ('crisis_alert', '危机预警'),
        ('emergency_request', '紧急求助'),
        ('other', '其他'),
    ]
    
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='system_logs')
    
    action = models.CharField(max_length=100, verbose_name='操作动作')
    model = models.CharField(max_length=50, blank=True, null=True, verbose_name='模型名称')
    object_id = models.CharField(max_length=36, blank=True, null=True, verbose_name='对象ID')
    changes = models.JSONField(blank=True, null=True, verbose_name='变更内容')
    
    # 请求信息
    ip_address = models.GenericIPAddressField(blank=True, null=True, verbose_name='IP地址')
    user_agent = models.TextField(blank=True, null=True, verbose_name='用户代理')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        db_table = 'system_logs'
        verbose_name = '系统操作日志'
        verbose_name_plural = '系统操作日志'
        indexes = [
            models.Index(fields=['user', 'action']),
            models.Index(fields=['created_at']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.action} - {self.user.username if self.user else 'Anonymous'}"


class Notification(models.Model):
    """通知模型"""
    NOTIFICATION_TYPES = [
        ('system', '系统通知'),
        ('chat', '聊天通知'),
        ('emotion', '情绪提醒'),
        ('crisis', '危机预警'),
        ('emergency', '紧急通知'),
        ('reminder', '提醒'),
    ]
    
    PRIORITY_LEVELS = [
        ('low', '低'),
        ('medium', '中'),
        ('high', '高'),
        ('urgent', '紧急'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    
    title = models.CharField(max_length=200, verbose_name='通知标题')
    content = models.TextField(verbose_name='通知内容')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, verbose_name='通知类型')
    priority = models.CharField(max_length=10, choices=PRIORITY_LEVELS, default='medium', verbose_name='优先级')
    
    # 关联信息
    related_model = models.CharField(max_length=50, blank=True, null=True, verbose_name='关联模型')
    related_id = models.CharField(max_length=36, blank=True, null=True, verbose_name='关联ID')
    
    # 状态信息
    is_read = models.BooleanField(default=False, verbose_name='是否已读')
    is_sent = models.BooleanField(default=False, verbose_name='是否已发送')
    
    # 时间信息
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    read_at = models.DateTimeField(blank=True, null=True, verbose_name='阅读时间')
    sent_at = models.DateTimeField(blank=True, null=True, verbose_name='发送时间')
    
    class Meta:
        db_table = 'notifications'
        verbose_name = '通知'
        verbose_name_plural = '通知'
        indexes = [
            models.Index(fields=['user', 'is_read']),
            models.Index(fields=['notification_type']),
            models.Index(fields=['priority']),
            models.Index(fields=['created_at']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"


class AppConfig(models.Model):
    """应用配置模型"""
    CONFIG_TYPES = [
        ('system', '系统配置'),
        ('ai', 'AI配置'),
        ('security', '安全配置'),
        ('notification', '通知配置'),
        ('other', '其他'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    key = models.CharField(max_length=100, unique=True, verbose_name='配置键')
    value = models.JSONField(verbose_name='配置值')
    config_type = models.CharField(max_length=20, choices=CONFIG_TYPES, verbose_name='配置类型')
    description = models.TextField(blank=True, null=True, verbose_name='描述')
    
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'app_configs'
        verbose_name = '应用配置'
        verbose_name_plural = '应用配置'
        indexes = [
            models.Index(fields=['key']),
            models.Index(fields=['config_type']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"{self.key} ({self.get_config_type_display()})"
