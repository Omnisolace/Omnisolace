"""
URL configuration for omnisolace project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from utils.views import health_check
from apps.users.views import (
    UserProfileView,
    UserDetailProfileView,
    PasswordChangeView,
    UserAvatarUploadView,
)

# API v1 router
api_v1_router = DefaultRouter()

# Main URL patterns
urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Health check
    path('health/', health_check, name='health-check'),
    
    # API v1
    path('api/v1/', include([
        # Authentication
        path('auth/', include('apps.users.urls')),
        
        # User profile management
        path('user/', include([
            path('profile/', UserProfileView.as_view(), name='user-profile'),
            path('profile/detail/', UserDetailProfileView.as_view(), name='user-profile-detail'),
            path('change-password/', PasswordChangeView.as_view(), name='user-change-password'),
            path('avatar/', UserAvatarUploadView.as_view(), name='user-avatar-upload'),
        ])),
        
        # Chat system
        path('chat/', include('apps.chat.urls')),
        
        # Emotion analysis
        path('emotion/', include('apps.emotion.urls')),
        
        # Psychological profile
        path('profile/', include('apps.profile.urls')),
        
        # Emergency system
        path('emergency/', include('apps.emergency.urls')),
        
        # System utilities
        path('system/', include('apps.common.urls')),
    ])),
    
    # API router
    path('api/v1/', include(api_v1_router.urls)),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Admin site customization
admin.site.site_header = 'Omnisolace 管理后台'
admin.site.site_title = 'Omnisolace'
admin.site.index_title = '欢迎使用 Omnisolace 管理系统'
