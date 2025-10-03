from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()


class EmergencyContact(models.Model):
    """紧急联系人模型"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='emergency_contacts')
    
    name = models.CharField(max_length=100, verbose_name='联系人姓名')
    phone = models.CharField(max_length=11, verbose_name='手机号')
    relationship = models.CharField(max_length=50, verbose_name='关系')
    is_primary = models.BooleanField(default=False, verbose_name='是否主要联系人')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    
    notes = models.TextField(blank=True, null=True, verbose_name='备注')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'emergency_contacts'
        verbose_name = '紧急联系人'
        verbose_name_plural = '紧急联系人'
        indexes = [
            models.Index(fields=['user', 'is_active']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.relationship})"


class EmergencyRequest(models.Model):
    """紧急求助记录模型"""
    REQUEST_TYPES = [
        ('crisis', '危机求助'),
        ('medical', '医疗紧急'),
        ('safety', '安全求助'),
        ('other', '其他'),
    ]
    
    URGENCY_LEVELS = [
        ('low', '低'),
        ('medium', '中'),
        ('high', '高'),
        ('critical', '紧急'),
    ]
    
    RESPONSE_STATUS = [
        ('pending', '待处理'),
        ('in_progress', '处理中'),
        ('resolved', '已解决'),
        ('cancelled', '已取消'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='emergency_requests')
    
    request_type = models.CharField(max_length=20, choices=REQUEST_TYPES, verbose_name='求助类型')
    urgency_level = models.CharField(max_length=20, choices=URGENCY_LEVELS, verbose_name='紧急程度')
    description = models.TextField(blank=True, null=True, verbose_name='求助描述')
    location_info = models.JSONField(blank=True, null=True, verbose_name='位置信息')
    
    # 响应信息
    response_status = models.CharField(max_length=20, choices=RESPONSE_STATUS, default='pending', verbose_name='响应状态')
    response_time = models.DateTimeField(blank=True, null=True, verbose_name='响应时间')
    responder_info = models.JSONField(blank=True, null=True, verbose_name='响应人信息')
    
    # 通知信息
    contacts_notified = models.JSONField(blank=True, null=True, verbose_name='已通知的联系人')
    notification_methods = models.JSONField(blank=True, null=True, verbose_name='通知方式')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    resolved_at = models.DateTimeField(blank=True, null=True, verbose_name='解决时间')
    
    class Meta:
        db_table = 'emergency_requests'
        verbose_name = '紧急求助记录'
        verbose_name_plural = '紧急求助记录'
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['response_status']),
            models.Index(fields=['urgency_level']),
        ]
    
    def __str__(self):
        return f"紧急求助 - {self.get_urgency_level_display()} - {self.user.username}"
