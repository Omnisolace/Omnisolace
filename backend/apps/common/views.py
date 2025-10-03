from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.shortcuts import get_object_or_404

from .models import SystemLog, Notification, AppConfig
from .serializers import (
    SystemLogSerializer,
    NotificationSerializer,
    NotificationCreateSerializer,
    AppConfigSerializer
)
from utils.views import BaseAPIView
from utils.responses import success_response, error_response


class SystemLogViewSet(viewsets.ReadOnlyModelViewSet):
    """系统日志查看"""
    permission_classes = [IsAdminUser]
    serializer_class = SystemLogSerializer
    
    def get_queryset(self):
        return SystemLog.objects.all()


class NotificationViewSet(viewsets.ModelViewSet):
    """通知管理"""
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return NotificationCreateSerializer
        return NotificationSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """标记为已读"""
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        
        return Response(success_response("通知已标记为已读"))
    
    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        """标记所有通知为已读"""
        Notification.objects.filter(
            user=request.user, 
            is_read=False
        ).update(is_read=True)
        
        return Response(success_response("所有通知已标记为已读"))
    
    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        """获取未读通知数量"""
        count = Notification.objects.filter(
            user=request.user, 
            is_read=False
        ).count()
        
        return Response(success_response("获取成功", {'count': count}))


class AppConfigViewSet(viewsets.ModelViewSet):
    """应用配置管理"""
    permission_classes = [IsAdminUser]
    serializer_class = AppConfigSerializer
    
    def get_queryset(self):
        return AppConfig.objects.filter(is_active=True)
    
    @action(detail=False, methods=['get'])
    def by_type(self, request):
        """按类型获取配置"""
        config_type = request.query_params.get('type')
        if config_type:
            configs = AppConfig.objects.filter(
                config_type=config_type, 
                is_active=True
            )
        else:
            configs = AppConfig.objects.filter(is_active=True)
        
        serializer = self.get_serializer(configs, many=True)
        return Response(success_response("获取成功", serializer.data))


class CommonAPIView(BaseAPIView):
    """通用API"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """获取用户统计信息"""
        user = request.user
        
        # 获取未读通知数量
        unread_notifications = Notification.objects.filter(
            user=user, 
            is_read=False
        ).count()
        
        # 获取最近的活动日志
        recent_logs = SystemLog.objects.filter(
            user=user
        ).order_by('-created_at')[:5]
        
        data = {
            'unread_notifications': unread_notifications,
            'recent_logs': SystemLogSerializer(recent_logs, many=True).data
        }
        
        return Response(success_response("获取成功", data))
