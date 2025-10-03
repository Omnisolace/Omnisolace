"""
心理档案相关视图
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import (
    PsychologicalProfile, 
    PsychologicalAssessment, 
    PsychologicalReport
)
from .serializers import (
    PsychologicalProfileSerializer,
    PsychologicalAssessmentSerializer,
    PsychologicalReportSerializer
)
from utils.views import BaseAPIView
from utils.responses import success_response, error_response


class PsychologicalProfileViewSet(viewsets.ModelViewSet):
    """心理档案管理"""
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return PsychologicalProfile.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        return PsychologicalProfileSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PsychologicalAssessmentViewSet(viewsets.ModelViewSet):
    """心理测评管理"""
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return PsychologicalAssessment.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        return PsychologicalAssessmentSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PsychologicalReportViewSet(viewsets.ReadOnlyModelViewSet):
    """心理报告查看"""
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return PsychologicalReport.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        return PsychologicalReportSerializer


class MyProfileAPIView(BaseAPIView):
    """我的心理档案API"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """获取我的心理档案"""
        try:
            profile = PsychologicalProfile.objects.get(user=request.user)
            serializer = PsychologicalProfileSerializer(profile)
            return Response(success_response("获取成功", serializer.data))
        except PsychologicalProfile.DoesNotExist:
            return Response(error_response("心理档案不存在"))
    
    def post(self, request):
        """创建或更新心理档案"""
        try:
            profile = PsychologicalProfile.objects.get(user=request.user)
            serializer = PsychologicalProfileSerializer(profile, data=request.data, partial=True)
        except PsychologicalProfile.DoesNotExist:
            serializer = PsychologicalProfileSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(success_response("心理档案保存成功", serializer.data))
        
        return Response(error_response("数据验证失败", serializer.errors))


class AssessmentAPIView(BaseAPIView):
    """心理测评API"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """提交测评结果"""
        serializer = PsychologicalAssessmentSerializer(data=request.data)
        if serializer.is_valid():
            assessment = serializer.save(user=request.user)
            return Response(success_response("测评提交成功", serializer.data))
        
        return Response(error_response("数据验证失败", serializer.errors))
    
    def get(self, request):
        """获取测评历史"""
        assessments = PsychologicalAssessment.objects.filter(
            user=request.user
        ).order_by('-created_at')
        
        serializer = PsychologicalAssessmentSerializer(assessments, many=True)
        return Response(success_response("获取成功", serializer.data))
