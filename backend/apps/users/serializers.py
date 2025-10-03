"""
用户相关序列化器
"""
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.core.validators import RegexValidator
from .models import User, UserProfile, UserSession, PasswordResetToken


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    用户注册序列化器
    """
    password = serializers.CharField(
        write_only=True,
        min_length=6,
        style={'input_type': 'password'}
    )
    confirm_password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )
    parent_phone = serializers.CharField(
        required=False,
        allow_blank=True,
        validators=[RegexValidator(r'^(1[3-9]\d{9}|1\d{10})$', '请输入有效的手机号码')]
    )
    helper_phone = serializers.CharField(
        required=False,
        allow_blank=True,
        validators=[RegexValidator(r'^(1[3-9]\d{9}|1\d{10})$', '请输入有效的手机号码')]
    )
    
    class Meta:
        model = User
        fields = [
            'username', 'phone', 'password', 'confirm_password',
            'age_group', 'gender', 'nickname', 'parent_phone',
            'parental_consent', 'helper_phone', 'voice_priority'
        ]
        extra_kwargs = {
            'phone': {'write_only': True},
            'parent_phone': {'write_only': True},
            'helper_phone': {'write_only': True},
        }
    
    def validate(self, attrs):
        # 密码确认验证
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("密码不匹配")
        
        # 青少年用户验证
        if attrs.get('age_group') == User.AgeGroup.TEEN:
            if not attrs.get('parent_phone'):
                raise serializers.ValidationError("青少年用户必须提供家长手机号")
            if not attrs.get('parental_consent'):
                raise serializers.ValidationError("青少年用户必须获得家长同意")
        
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        password = validated_data.pop('password')
        
        user = User.objects.create_user(
            password=password,
            **validated_data
        )
        
        # 创建用户档案
        UserProfile.objects.create(user=user)
        
        return user


class UserLoginSerializer(serializers.Serializer):
    """
    用户登录序列化器
    """
    phone = serializers.CharField(
        validators=[RegexValidator(r'^(1[3-9]\d{9}|1\d{10})$', '请输入有效的手机号码')]
    )
    password = serializers.CharField(style={'input_type': 'password'})
    
    def validate(self, attrs):
        phone = attrs.get('phone')
        password = attrs.get('password')
        
        if phone and password:
            # 尝试通过手机号查找用户
            try:
                user = User.objects.get(phone=phone)
                username = user.username
            except User.DoesNotExist:
                raise serializers.ValidationError("用户不存在")
            
            user = authenticate(
                request=self.context.get('request'),
                username=username,
                password=password
            )
            
            if not user:
                raise serializers.ValidationError("登录凭证无效")
            
            if not user.is_active:
                raise serializers.ValidationError("用户账户已被禁用")
            
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError("必须提供手机号和密码")


class UserProfileSerializer(serializers.ModelSerializer):
    """
    用户档案序列化器
    """
    class Meta:
        model = UserProfile
        fields = [
            'bio', 'location', 'occupation', 'education',
            'mental_health_concerns', 'therapy_history', 'medication_info',
            'preferred_communication_style', 'share_data_for_research',
            'anonymous_data_sharing', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户详细信息序列化器（包含档案信息）
    """
    profile = serializers.SerializerMethodField()
    session_count = serializers.SerializerMethodField()
    last_session = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'nickname', 'avatar', 'age_group',
            'gender', 'birth_date', 'is_guest', 'color_theme',
            'notifications_enabled', 'data_sync_enabled',
            'voice_priority', 'parental_mode', 'parent_phone',
            'helper_phone', 'created_at', 'last_active', 
            'profile', 'session_count', 'last_session'
        ]
        read_only_fields = ['id', 'created_at', 'last_active']
    
    def get_profile(self, obj):
        if hasattr(obj, 'profile'):
            return UserProfileDetailSerializer(obj.profile).data
        return None
    
    def get_session_count(self, obj):
        return obj.chat_sessions.count()
    
    def get_last_session(self, obj):
        last_session = obj.chat_sessions.filter(is_active=True).first()
        if last_session:
            return {
                'id': str(last_session.id),
                'title': last_session.title,
                'last_message_at': last_session.last_message_at,
                'message_count': last_session.message_count
            }
        return None


class UserProfileDetailSerializer(serializers.ModelSerializer):
    """
    用户详细档案序列化器
    """
    class Meta:
        model = UserProfile
        fields = [
            'bio', 'location', 'occupation', 'education',
            'mental_health_concerns', 'preferred_communication_style',
            'share_data_for_research', 'anonymous_data_sharing',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class UserSessionSerializer(serializers.ModelSerializer):
    """
    用户会话序列化器
    """
    class Meta:
        model = UserSession
        fields = [
            'id', 'session_key', 'ip_address', 'device_info',
            'created_at', 'last_activity', 'is_active'
        ]
        read_only_fields = ['id', 'created_at', 'last_activity']


class GuestUserSerializer(serializers.Serializer):
    """
    游客用户序列化器
    """
    device_id = serializers.CharField(required=False)
    age_group = serializers.ChoiceField(
        choices=User.AgeGroup.choices,
        default=User.AgeGroup.YOUNG
    )
    
    def create(self, validated_data):
        device_id = validated_data.get('device_id', '')
        age_group = validated_data.get('age_group', User.AgeGroup.YOUNG)
        
        # 创建游客用户
        import uuid
        username = f'guest_{uuid.uuid4().hex[:8]}'
        
        user = User.objects.create_user(
            username=username,
            phone=f'guest_{username}',  # 临时手机号
            is_guest=True,
            age_group=age_group
        )
        
        # 创建用户档案
        UserProfile.objects.create(user=user)
        
        return user


class PasswordChangeSerializer(serializers.Serializer):
    """
    密码修改序列化器
    """
    old_password = serializers.CharField(style={'input_type': 'password'})
    new_password = serializers.CharField(
        min_length=6,
        style={'input_type': 'password'}
    )
    confirm_password = serializers.CharField(style={'input_type': 'password'})
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError("新密码不匹配")
        return attrs
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("原密码不正确")
        return value
    
    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


class ForgotPasswordSerializer(serializers.Serializer):
    """
    忘记密码 - 发送验证码序列化器
    """
    phone = serializers.CharField(
        validators=[RegexValidator(r'^(1[3-9]\d{9}|1\d{10})$', '请输入有效的手机号码')]
    )
    
    def validate_phone(self, value):
        # 检查用户是否存在
        try:
            User.objects.get(phone=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("该手机号未注册")
        return value


class VerifyResetCodeSerializer(serializers.Serializer):
    """
    验证重置验证码序列化器
    """
    phone = serializers.CharField(
        validators=[RegexValidator(r'^(1[3-9]\d{9}|1\d{10})$', '请输入有效的手机号码')]
    )
    verification_code = serializers.CharField(max_length=6, min_length=6)
    
    def validate(self, attrs):
        phone = attrs.get('phone')
        verification_code = attrs.get('verification_code')
        
        try:
            reset_token = PasswordResetToken.objects.get(
                phone=phone,
                verification_code=verification_code,
                is_used=False
            )
            
            if reset_token.is_expired():
                raise serializers.ValidationError("验证码已过期，请重新获取")
            
            attrs['reset_token'] = reset_token
            return attrs
            
        except PasswordResetToken.DoesNotExist:
            raise serializers.ValidationError("验证码错误")
    
    def save(self):
        """验证验证码但不标记为已使用（重置密码时再标记）"""
        reset_token = self.validated_data['reset_token']
        # 不标记为已使用，重置密码成功后再标记
        return reset_token


class ResetPasswordSerializer(serializers.Serializer):
    """
    重置密码序列化器
    """
    phone = serializers.CharField(
        validators=[RegexValidator(r'^(1[3-9]\d{9}|1\d{10})$', '请输入有效的手机号码')]
    )
    verification_code = serializers.CharField(max_length=6, min_length=6)
    new_password = serializers.CharField(
        min_length=6,
        style={'input_type': 'password'}
    )
    confirm_password = serializers.CharField(style={'input_type': 'password'})
    
    def validate(self, attrs):
        # 密码确认验证
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError("两次输入的密码不一致")
        
        phone = attrs.get('phone')
        verification_code = attrs.get('verification_code')
        
        # 验证验证码
        try:
            reset_token = PasswordResetToken.objects.get(
                phone=phone,
                verification_code=verification_code,
                is_used=False
            )
            
            if reset_token.is_expired():
                raise serializers.ValidationError("验证码已过期，请重新获取")
            
            attrs['reset_token'] = reset_token
            return attrs
            
        except PasswordResetToken.DoesNotExist:
            raise serializers.ValidationError("验证码错误")
    
    def save(self):
        """重置密码"""
        phone = self.validated_data['phone']
        new_password = self.validated_data['new_password']
        reset_token = self.validated_data['reset_token']
        
        # 获取用户
        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            raise serializers.ValidationError("用户不存在")
        
        # 设置新密码
        user.set_password(new_password)
        user.save()
        
        # 标记验证码为已使用
        reset_token.mark_as_used()
        
        # 使所有会话失效（强制重新登录）
        UserSession.objects.filter(
            user=user,
            is_active=True
        ).update(is_active=False)
        
        return user
