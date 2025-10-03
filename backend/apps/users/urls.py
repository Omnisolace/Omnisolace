"""
用户认证相关URL配置
"""
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    UserRegistrationView,
    UserLoginView,
    UserLogoutView,
    UserProfileView,
    UserDetailProfileView,
    PasswordChangeView,
    UserAvatarUploadView,
    UserDeleteView,
    GuestLoginView,
    ForgotPasswordView,
    VerifyResetCodeView,
    ResetPasswordView,
    user_stats
)

app_name = 'users'

urlpatterns = [
    # 认证相关
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('guest-login/', GuestLoginView.as_view(), name='guest-login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    
    # 忘记密码相关
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('verify-reset-code/', VerifyResetCodeView.as_view(), name='verify-reset-code'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    
    # 用户管理
    path('delete/', UserDeleteView.as_view(), name='delete-account'),
    path('stats/', user_stats, name='user-stats'),
]
