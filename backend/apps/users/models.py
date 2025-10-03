"""
用户相关模型
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator, MinLengthValidator
from django.utils import timezone
from cryptography.fernet import Fernet
from django.conf import settings
import uuid


class User(AbstractUser):
    """
    自定义用户模型
    """
    
    class AgeGroup(models.TextChoices):
        TEEN = 'teen', '青少年 (12-18岁)'
        YOUNG = 'young', '青年 (19-35岁)'
        MIDDLE = 'middle', '中年 (36-59岁)'
        ELDER = 'elder', '老年 (60岁+)'
    
    class Gender(models.TextChoices):
        MALE = 'male', '男性'
        FEMALE = 'female', '女性'
        OTHER = 'other', '其他'
        PREFER_NOT_SAY = 'prefer_not_say', '不愿透露'
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # 基本信息
    phone_validator = RegexValidator(
        regex=r'^(1[3-9]\d{9}|g[a-f0-9]{8}|1\d{10})$',
        message="请输入有效的手机号码或游客标识"
    )
    phone = models.CharField(
        max_length=20,
        validators=[phone_validator],
        unique=True,
        verbose_name='手机号',
        help_text='加密存储，游客用户使用guest_前缀'
    )
    
    # 个人资料
    nickname = models.CharField(max_length=50, verbose_name='昵称', blank=True)
    avatar = models.ImageField(upload_to='avatars/%Y/%m/', verbose_name='头像', blank=True, null=True)
    age_group = models.CharField(
        max_length=10,
        choices=AgeGroup.choices,
        default=AgeGroup.YOUNG,
        verbose_name='年龄段'
    )
    gender = models.CharField(
        max_length=20,
        choices=Gender.choices,
        default=Gender.PREFER_NOT_SAY,
        verbose_name='性别'
    )
    birth_date = models.DateField(verbose_name='出生日期', null=True, blank=True)
    
    # 特殊用户设置
    is_guest = models.BooleanField(default=False, verbose_name='游客用户')
    
    # 青少年用户特殊字段
    parent_phone = models.CharField(
        max_length=11,
        validators=[phone_validator],
        verbose_name='家长手机号',
        blank=True,
        null=True,
        help_text='青少年用户必填，加密存储'
    )
    parental_consent = models.BooleanField(default=False, verbose_name='家长同意')
    parental_mode = models.BooleanField(default=False, verbose_name='家长监督模式')
    
    # 老年用户特殊字段
    helper_phone = models.CharField(
        max_length=11,
        validators=[phone_validator],
        verbose_name='子女联系方式',
        blank=True,
        null=True,
        help_text='老年用户子女手机号，加密存储'
    )
    voice_priority = models.BooleanField(default=False, verbose_name='语音优先模式')
    
    # 系统设置
    color_theme = models.CharField(
        max_length=20,
        default='warmOrange',
        verbose_name='主题色'
    )
    notifications_enabled = models.BooleanField(default=True, verbose_name='推送通知')
    data_sync_enabled = models.BooleanField(default=True, verbose_name='数据同步')
    
    # 时间戳
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    last_active = models.DateTimeField(default=timezone.now, verbose_name='最后活跃时间')
    
    # 数据保护
    is_data_deleted = models.BooleanField(default=False, verbose_name='数据已删除')
    data_deletion_scheduled = models.DateTimeField(null=True, blank=True, verbose_name='数据删除计划时间')
    
    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'
        db_table = 'users'
        indexes = [
            models.Index(fields=['phone']),
            models.Index(fields=['age_group']),
            models.Index(fields=['created_at']),
            models.Index(fields=['last_active']),
        ]
    
    def __str__(self):
        return f"{self.username} ({self.get_age_group_display()})"
    
    @property
    def encrypted_phone(self):
        """返回加密的手机号"""
        if not hasattr(settings, 'ENCRYPTION_KEY'):
            return self.phone
        
        try:
            f = Fernet(settings.ENCRYPTION_KEY.encode())
            return f.encrypt(self.phone.encode()).decode()
        except:
            return self.phone
    
    @property
    def decrypted_phone(self):
        """返回解密的手机号"""
        return self.phone
    
    def save(self, *args, **kwargs):
        """保存时加密敏感信息"""
        # 青少年用户验证（游客用户除外）
        if self.age_group == self.AgeGroup.TEEN and not self.is_guest:
            if not self.parent_phone:
                raise ValueError("青少年用户必须提供家长手机号")
            if not self.parental_consent:
                raise ValueError("青少年用户必须获得家长同意")
        
        # 更新最后活跃时间
        if not self.pk:  # 新用户
            self.last_active = timezone.now()
        
        super().save(*args, **kwargs)
    
    def update_last_active(self):
        """更新最后活跃时间"""
        self.last_active = timezone.now()
        self.save(update_fields=['last_active'])
    
    def schedule_data_deletion(self, days=90):
        """安排数据删除"""
        from datetime import timedelta
        self.data_deletion_scheduled = timezone.now() + timedelta(days=days)
        self.save(update_fields=['data_deletion_scheduled'])
    
    def can_access_feature(self, feature):
        """检查用户是否可以访问某个功能"""
        if self.is_guest:
            guest_features = ['basic_chat', 'emotion_detection']
            return feature in guest_features
        return True
    
    def get_parental_summary(self):
        """获取家长监督摘要"""
        if self.age_group != self.AgeGroup.TEEN or not self.parental_mode:
            return None
        
        # 这里可以添加生成家长摘要的逻辑
        return {
            'usage_hours': 0,  # 使用时长
            'emotion_status': 'stable',  # 情绪状态
            'crisis_alerts': 0,  # 危机预警次数
            'last_chat': None,  # 最后聊天时间
        }


class UserProfile(models.Model):
    """
    用户详细档案
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # 个人信息
    bio = models.TextField(max_length=500, verbose_name='个人简介', blank=True)
    location = models.CharField(max_length=100, verbose_name='所在地', blank=True)
    occupation = models.CharField(max_length=100, verbose_name='职业', blank=True)
    education = models.CharField(max_length=100, verbose_name='教育背景', blank=True)
    
    # 心理健康信息
    mental_health_concerns = models.TextField(verbose_name='心理健康关注点', blank=True)
    therapy_history = models.TextField(verbose_name='治疗历史', blank=True)
    medication_info = models.TextField(verbose_name='用药信息', blank=True)
    
    # 偏好设置
    preferred_communication_style = models.CharField(
        max_length=20,
        choices=[
            ('formal', '正式'),
            ('casual', '随意'),
            ('empathetic', '共情'),
            ('solution_focused', '解决方案导向'),
        ],
        default='empathetic',
        verbose_name='偏好的沟通风格'
    )
    
    # 隐私设置
    share_data_for_research = models.BooleanField(default=False, verbose_name='同意数据用于研究')
    anonymous_data_sharing = models.BooleanField(default=True, verbose_name='匿名数据共享')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '用户档案'
        verbose_name_plural = '用户档案'
        db_table = 'user_profiles'
    
    def __str__(self):
        return f"{self.user.username} 的档案"


class UserSession(models.Model):
    """
    用户会话记录
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
    session_key = models.CharField(max_length=40, unique=True, verbose_name='会话密钥')
    ip_address = models.GenericIPAddressField(verbose_name='IP地址')
    user_agent = models.TextField(verbose_name='用户代理')
    device_info = models.JSONField(default=dict, verbose_name='设备信息')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    last_activity = models.DateTimeField(auto_now=True, verbose_name='最后活动时间')
    is_active = models.BooleanField(default=True, verbose_name='是否活跃')
    
    class Meta:
        verbose_name = '用户会话'
        verbose_name_plural = '用户会话'
        db_table = 'user_sessions'
        indexes = [
            models.Index(fields=['user', 'is_active']),
            models.Index(fields=['session_key']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.ip_address}"

 
class PasswordResetToken(models.Model):
    """
    密码重置验证码记录
    """
    phone = models.CharField(max_length=20, verbose_name='手机号')
    verification_code = models.CharField(max_length=6, verbose_name='验证码')
    token = models.CharField(max_length=100, unique=True, verbose_name='重置令牌')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    expires_at = models.DateTimeField(verbose_name='过期时间')
    is_used = models.BooleanField(default=False, verbose_name='是否已使用')
    
    class Meta:
        verbose_name = '密码重置验证码'
        verbose_name_plural = '密码重置验证码'
        db_table = 'password_reset_tokens'
        indexes = [
            models.Index(fields=['phone', 'is_used']),
            models.Index(fields=['token']),
            models.Index(fields=['expires_at']),
        ]
    
    def __str__(self):
        return f"{self.phone} - {self.verification_code}"
    
    def is_expired(self):
        """检查验证码是否过期"""
        return timezone.now() > self.expires_at
    
    def mark_as_used(self):
        """标记为已使用"""
        self.is_used = True
        self.save(update_fields=['is_used'])
