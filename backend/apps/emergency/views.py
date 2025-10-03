from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import EmergencyContact, EmergencyRequest
from .serializers import (
    EmergencyContactSerializer, 
    EmergencyContactCreateSerializer,
    EmergencyRequestSerializer,
    EmergencyRequestCreateSerializer
)
from utils.views import BaseAPIView
from utils.responses import success_response, error_response


class EmergencyContactViewSet(viewsets.ModelViewSet):
    """紧急联系人管理"""
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return EmergencyContact.objects.filter(user=self.request.user, is_active=True)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return EmergencyContactCreateSerializer
        return EmergencyContactSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def set_primary(self, request, pk=None):
        """设置为主要联系人"""
        contact = self.get_object()
        
        # 取消其他主要联系人
        EmergencyContact.objects.filter(
            user=request.user, 
            is_primary=True
        ).update(is_primary=False)
        
        # 设置当前为主要联系人
        contact.is_primary = True
        contact.save()
        
        return Response(success_response("已设置为主要联系人"))
    
    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """停用联系人"""
        contact = self.get_object()
        contact.is_active = False
        contact.save()
        
        return Response(success_response("联系人已停用"))


class EmergencyRequestViewSet(viewsets.ModelViewSet):
    """紧急求助管理"""
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return EmergencyRequest.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return EmergencyRequestCreateSerializer
        return EmergencyRequestSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def resolve(self, request, pk=None):
        """标记为已解决"""
        emergency_request = self.get_object()
        emergency_request.response_status = 'resolved'
        emergency_request.save()
        
        return Response(success_response("求助已标记为解决"))
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """取消求助"""
        emergency_request = self.get_object()
        emergency_request.response_status = 'cancelled'
        emergency_request.save()
        
        return Response(success_response("求助已取消"))


class EmergencyAPIView(BaseAPIView):
    """紧急求助API"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """创建紧急求助"""
        serializer = EmergencyRequestCreateSerializer(data=request.data)
        if serializer.is_valid():
            emergency_request = serializer.save(user=request.user)
            
            # 这里可以添加自动通知逻辑
            # 例如：发送短信、邮件给紧急联系人
            
            return Response(success_response(
                "紧急求助已提交", 
                data=EmergencyRequestSerializer(emergency_request).data
            ))
        
        return Response(error_response("数据验证失败", serializer.errors))
    
    def get(self, request):
        """获取紧急求助历史"""
        requests = EmergencyRequest.objects.filter(user=request.user).order_by('-created_at')
        serializer = EmergencyRequestSerializer(requests, many=True)
        
        return Response(success_response("获取成功", serializer.data))
