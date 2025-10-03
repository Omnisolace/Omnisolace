"""
用户认证相关视图
"""
from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.utils import timezone
from django.conf import settings
from django.db import transaction
import logging

from .models import User, UserProfile, UserSession, PasswordResetToken
from .serializers import (
    UserRegistrationSerializer, 
    UserLoginSerializer, 
    UserDetailSerializer,
    UserProfileSerializer,
    PasswordChangeSerializer,
    ForgotPasswordSerializer,
    VerifyResetCodeSerializer,
    ResetPasswordSerializer
)
from utils.responses import success_response, error_response
from utils.permissions import IsOwnerOrReadOnly

logger = logging.getLogger(__name__)


class UserRegistrationView(APIView):
    """
    用户注册视图
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        
        if not serializer.is_valid():
            return error_response(
                message="注册信息验证失败",
                data=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            with transaction.atomic():
                user = serializer.save()
                
                # 创建用户档案
                UserProfile.objects.get_or_create(user=user)
                
                # 为青少年用户创建心理档案
                if user.age_group == User.AgeGroup.TEEN:
                    from apps.profile.models import PsychologicalProfile
                    PsychologicalProfile.objects.get_or_create(
                        user=user,
                        defaults={'communication_style': 'supportive'}
                    )
                
                # 生成JWT令牌
                refresh = RefreshToken.for_user(user)
                
                # 记录用户会话
                self._create_user_session(user, request)
                
                # 发送家长通知（青少年用户）
                if user.age_group == User.AgeGroup.TEEN and user.parent_phone:
                    self._send_parent_notification(user)
                
                user_data = UserDetailSerializer(user).data
                
                response_data = {
                    'user': user_data,
                    'tokens': {
                        'access': str(refresh.access_token),
                        'refresh': str(refresh)
                    }
                }
                
                return success_response(
                    message="注册成功",
                    data=response_data,
                    status_code=status.HTTP_201_CREATED
                )
                
        except Exception as e:
            logger.error(f"用户注册失败: {str(e)}")
            # 检查是否是重复键错误
            error_msg = str(e)
            if "Duplicate entry" in error_msg:
                if "phone" in error_msg:
                    return error_response(
                        message="该手机号已被注册，请使用其他手机号或直接登录",
                        status_code=status.HTTP_400_BAD_REQUEST
                    )
                elif "username" in error_msg:
                    return error_response(
                        message="用户名已存在，请使用其他用户名",
                        status_code=status.HTTP_400_BAD_REQUEST
                    )
                elif "user_id" in error_msg:
                    return error_response(
                        message="用户档案已存在",
                        status_code=status.HTTP_400_BAD_REQUEST
                    )
            elif "IntegrityError" in error_msg:
                return error_response(
                    message="数据完整性错误，请检查输入信息",
                    status_code=status.HTTP_400_BAD_REQUEST
                )
            elif "ValidationError" in error_msg:
                return error_response(
                    message="数据验证失败，请检查输入格式",
                    status_code=status.HTTP_400_BAD_REQUEST
                )
            elif "DatabaseError" in error_msg:
                return error_response(
                    message="数据库操作失败，请稍后重试",
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            else:
                return error_response(
                    message="注册失败，请稍后重试",
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
    
    def _create_user_session(self, user, request):
        """创建用户会话"""
        import uuid
        session_key = request.session.session_key or f'web_session_{uuid.uuid4().hex[:8]}'
        
        UserSession.objects.create(
            user=user,
            session_key=session_key,
            ip_address=self._get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            device_info=self._get_device_info(request)
        )
    
    def _get_client_ip(self, request):
        """获取客户端IP"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def _get_device_info(self, request):
        """获取设备信息"""
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        return {
            'user_agent': user_agent,
            'platform': 'web',
            'timestamp': timezone.now().isoformat()
        }
    
    def _send_parent_notification(self, user):
        """发送家长通知"""
        # 这里可以集成短信服务
        logger.info(f"应该向家长 {user.parent_phone} 发送通知：子女 {user.username} 已注册心理疏导服务")


class UserLoginView(TokenObtainPairView):
    """
    用户登录视图
    """
    serializer_class = UserLoginSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        if not serializer.is_valid():
            # 获取具体的验证错误信息
            error_messages = []
            for field, errors in serializer.errors.items():
                if isinstance(errors, list):
                    error_messages.extend(errors)
                else:
                    error_messages.append(str(errors))
            
            # 如果有具体的错误信息，使用第一个；否则使用通用错误
            if error_messages:
                main_error = error_messages[0]
            else:
                main_error = "登录信息验证失败"
            
            return error_response(
                message=main_error,
                data=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            phone = serializer.validated_data.get('phone')
            password = serializer.validated_data.get('password')
            
            # 查找用户
            try:
                user = User.objects.get(phone=phone)
            except User.DoesNotExist:
                return error_response(
                    message="用户不存在",
                    status_code=status.HTTP_404_NOT_FOUND
                )
            
            # 验证密码
            if not user.check_password(password):
                return error_response(
                    message="密码错误",
                    status_code=status.HTTP_401_UNAUTHORIZED
                )
            
            # 检查用户状态
            if not user.is_active:
                return error_response(
                    message="账户已被禁用",
                    status_code=status.HTTP_401_UNAUTHORIZED
                )
            
            # 生成令牌
            refresh = RefreshToken.for_user(user)
            
            # 更新最后活跃时间
            user.update_last_active()
            
            # 创建会话记录
            self._create_login_session(user, request)
            
            user_data = UserDetailSerializer(user).data
            
            response_data = {
                'user': user_data,
                'tokens': {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh)
                }
            }
            
            return success_response(
                message="登录成功",
                data=response_data
            )
            
        except Exception as e:
            logger.error(f"用户登录失败: {str(e)}")
            error_msg = str(e)
            if "DatabaseError" in error_msg:
                return error_response(
                    message="数据库连接失败，请稍后重试",
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            elif "AuthenticationError" in error_msg:
                return error_response(
                    message="认证服务暂时不可用，请稍后重试",
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            elif "PermissionError" in error_msg:
                return error_response(
                    message="权限验证失败，请联系管理员",
                    status_code=status.HTTP_403_FORBIDDEN
                )
            else:
                return error_response(
                    message="登录失败，请稍后重试",
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
    
    def _create_login_session(self, user, request):
        """创建登录会话"""
        # 使现有会话失效
        UserSession.objects.filter(
            user=user,
            is_active=True
        ).update(is_active=False)
        
        # 创建新会话
        UserSession.objects.create(
            user=user,
            session_key=request.session.session_key or f'login_{timezone.now().timestamp()}',
            ip_address=self._get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            device_info=self._get_device_info(request)
        )
    
    def _get_client_ip(self, request):
        """获取客户端IP"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def _get_device_info(self, request):
        """获取设备信息"""
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        return {
            'user_agent': user_agent,
            'platform': 'web',
            'login_time': timezone.now().isoformat()
        }


class UserLogoutView(APIView):
    """
    用户登出视图
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        try:
            # 将刷新令牌加入黑名单
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            
            # 使会话失效
            UserSession.objects.filter(
                user=request.user,
                is_active=True
            ).update(is_active=False)
            
            return success_response(message="登出成功")
            
        except Exception as e:
            logger.error(f"用户登出失败: {str(e)}")
            return error_response(
                message="登出失败",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    用户资料视图
    """
    serializer_class = UserDetailSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    
    def get_object(self):
        return self.request.user
    
    def patch(self, request, *args, **kwargs):
        """部分更新用户信息"""
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        
        if not serializer.is_valid():
            return error_response(
                message="用户信息验证失败",
                data=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            updated_user = serializer.save()
            return success_response(
                message="用户信息更新成功",
                data=UserDetailSerializer(updated_user).data
            )
        except Exception as e:
            logger.error(f"更新用户信息失败: {str(e)}")
            return error_response(
                message="更新失败，请稍后重试",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UserDetailProfileView(generics.RetrieveUpdateAPIView):
    """
    用户详细档案视图
    """
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    
    def get_object(self):
        profile, created = UserProfile.objects.get_or_create(
            user=self.request.user
        )
        return profile


class PasswordChangeView(APIView):
    """
    修改密码视图
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = PasswordChangeSerializer(
            data=request.data,
            context={'request': request}
        )
        
        if not serializer.is_valid():
            return error_response(
                message="密码验证失败",
                data=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = request.user
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']
            
            # 验证旧密码
            if not user.check_password(old_password):
                return error_response(
                    message="原密码错误",
                    status_code=status.HTTP_400_BAD_REQUEST
                )
            
            # 设置新密码
            user.set_password(new_password)
            user.save()
            
            # 使所有会话失效（强制重新登录）
            UserSession.objects.filter(
                user=user,
                is_active=True
            ).update(is_active=False)
            
            return success_response(message="密码修改成功，请重新登录")
            
        except Exception as e:
            logger.error(f"修改密码失败: {str(e)}")
            return error_response(
                message="修改密码失败，请稍后重试",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UserAvatarUploadView(APIView):
    """
    用户头像上传视图
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        if 'avatar' not in request.FILES:
            return error_response(
                message="请选择头像文件",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        avatar_file = request.FILES['avatar']
        
        # 验证文件大小
        if avatar_file.size > settings.FILE_UPLOAD_MAX_MEMORY_SIZE:
            return error_response(
                message="头像文件过大",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        # 验证文件类型
        allowed_types = ['image/jpeg', 'image/png', 'image/gif']
        if avatar_file.content_type not in allowed_types:
            return error_response(
                message="不支持的文件类型，请上传JPG、PNG或GIF格式的图片",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = request.user
            
            # 删除旧头像
            if user.avatar:
                user.avatar.delete()
            
            # 保存新头像
            user.avatar = avatar_file
            user.save()
            
            return success_response(
                message="头像上传成功",
                data={'avatar_url': user.avatar.url if user.avatar else None}
            )
            
        except Exception as e:
            logger.error(f"头像上传失败: {str(e)}")
            return error_response(
                message="头像上传失败，请稍后重试",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UserDeleteView(APIView):
    """
    用户注销账户视图
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def delete(self, request):
        try:
            user = request.user
            
            # 软删除：标记数据为已删除，安排数据删除
            user.is_active = False
            user.is_data_deleted = True
            user.schedule_data_deletion()
            user.save()
            
            # 使所有会话失效
            UserSession.objects.filter(
                user=user,
                is_active=True
            ).update(is_active=False)
            
            # 这里可以添加清理用户数据的异步任务
            
            return success_response(
                message="账户注销成功，您的数据将在90天后永久删除"
            )
            
        except Exception as e:
            logger.error(f"用户注销账户失败: {str(e)}")
            return error_response(
                message="注销失败，请稍后重试",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class GuestLoginView(APIView):
    """
    游客登录视图
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        try:
            # 创建游客用户
            import uuid
            guest_username = f"guest_{uuid.uuid4().hex[:8]}"
            
            # 为游客用户生成一个唯一的手机号占位符
            guest_phone = f"g{uuid.uuid4().hex[:8]}"
            
            guest_user = User.objects.create_user(
                username=guest_username,
                phone=guest_phone,  # 游客用户使用唯一占位符
                is_guest=True,
                age_group=User.AgeGroup.YOUNG  # 默认年龄段
            )
            
            # 生成令牌
            refresh = RefreshToken.for_user(guest_user)
            
            # 创建会话
            UserSession.objects.create(
                user=guest_user,
                session_key=f'guest_{timezone.now().timestamp()}',
                ip_address=self._get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                device_info={'platform': 'web', 'type': 'guest'}
            )
            
            user_data = UserDetailSerializer(guest_user).data
            
            response_data = {
                'user': user_data,
                'tokens': {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh)
                }
            }
            
            return success_response(
                message="游客登录成功",
                data=response_data
            )
            
        except Exception as e:
            logger.error(f"游客登录失败: {str(e)}")
            # 检查是否是重复键错误
            error_msg = str(e)
            if "Duplicate entry" in error_msg:
                if "phone" in error_msg:
                    # 如果手机号重复，尝试使用不同的手机号
                    try:
                        guest_phone = f"g{uuid.uuid4().hex[:8]}"
                        guest_user = User.objects.create_user(
                            username=f"guest_{uuid.uuid4().hex[:8]}",
                            phone=guest_phone,
                            is_guest=True,
                            age_group=User.AgeGroup.YOUNG
                        )
                        
                        refresh = RefreshToken.for_user(guest_user)
                        user_data = UserDetailSerializer(guest_user).data
                        
                        response_data = {
                            'user': user_data,
                            'tokens': {
                                'access': str(refresh.access_token),
                                'refresh': str(refresh)
                            }
                        }
                        
                        return success_response(
                            message="游客登录成功",
                            data=response_data
                        )
                    except Exception as retry_e:
                        logger.error(f"重试游客登录失败: {str(retry_e)}")
            
            return error_response(
                message="游客登录失败，请稍后重试",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def _get_client_ip(self, request):
        """获取客户端IP"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class ForgotPasswordView(APIView):
    """
    忘记密码 - 发送验证码视图
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        
        if not serializer.is_valid():
            return error_response(
                message="手机号验证失败",
                data=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            phone = serializer.validated_data['phone']
            
            # 生成6位验证码
            import random
            verification_code = str(random.randint(100000, 999999))
            
            # 生成重置令牌
            import uuid
            reset_token = str(uuid.uuid4())
            
            # 设置过期时间（10分钟）
            expires_at = timezone.now() + timezone.timedelta(minutes=10)
            
            # 删除该手机号的旧验证码
            PasswordResetToken.objects.filter(
                phone=phone,
                is_used=False
            ).update(is_used=True)
            
            # 创建新的验证码记录
            PasswordResetToken.objects.create(
                phone=phone,
                verification_code=verification_code,
                token=reset_token,
                expires_at=expires_at
            )
            
            # 这里应该调用短信服务发送验证码
            # 为了演示，我们只在日志中记录验证码
            logger.info(f"发送验证码到 {phone}: {verification_code}")
            
            return success_response(
                message="验证码已发送",
                data={
                    'phone': phone,
                    'expires_in': 600,  # 10分钟
                    'verification_code': verification_code  # 开发环境返回验证码，生产环境应移除
                }
            )
            
        except Exception as e:
            logger.error(f"发送验证码失败: {str(e)}")
            return error_response(
                message="发送验证码失败，请稍后重试",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class VerifyResetCodeView(APIView):
    """
    验证重置验证码视图
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = VerifyResetCodeSerializer(data=request.data)
        
        if not serializer.is_valid():
            return error_response(
                message="验证码验证失败",
                data=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            reset_token = serializer.save()
            
            return success_response(
                message="验证码验证成功",
                data={
                    'phone': reset_token.phone,
                    'token': reset_token.token
                }
            )
            
        except Exception as e:
            logger.error(f"验证码验证失败: {str(e)}")
            return error_response(
                message="验证码验证失败，请稍后重试",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ResetPasswordView(APIView):
    """
    重置密码视图
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        
        if not serializer.is_valid():
            return error_response(
                message="密码重置失败",
                data=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = serializer.save()
            
            return success_response(
                message="密码重置成功，请使用新密码登录",
                data={
                    'user_id': str(user.id),
                    'username': user.username
                }
            )
            
        except Exception as e:
            logger.error(f"密码重置失败: {str(e)}")
            return error_response(
                message="密码重置失败，请稍后重试",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_stats(request):
    """
    用户统计信息
    """
    try:
        user = request.user
        
        # 获取聊天统计
        from apps.chat.models import ChatSession
        chat_count = ChatSession.objects.filter(user=user).count()
        
        # 获取情绪统计
        from apps.emotion.models import EmotionLog
        emotion_count = EmotionLog.objects.filter(user=user).count()
        
        # 计算连续使用天数
        from datetime import timedelta
        from django.db.models import Count
        
        sessions_by_day = ChatSession.objects.filter(
            user=user,
            created_at__gte=timezone.now() - timedelta(days=30)
        ).extra(
            select={'day': 'date(created_at)'}
        ).values('day').annotate(count=Count('id')).order_by('day')
        
        continuous_days = len(sessions_by_day)
        
        stats = {
            'chat_sessions': chat_count,
            'emotion_records': emotion_count,
            'continuous_days': continuous_days,
            'user_since': user.created_at.isoformat(),
            'last_active': user.last_active.isoformat() if user.last_active else None,
        }
        
        return success_response(
            message="统计信息获取成功",
            data=stats
        )
        
    except Exception as e:
        logger.error(f"获取用户统计失败: {str(e)}")
        return error_response(
            message="获取统计信息失败",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
