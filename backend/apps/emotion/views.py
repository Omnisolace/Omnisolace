"""
情绪分析相关视图
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import EmotionLog, EmotionPattern, EmotionAnalysisModel
from .serializers import (
    EmotionLogSerializer,
    EmotionPatternSerializer,
    EmotionAnalysisModelSerializer
)
from utils.views import BaseAPIView
from utils.responses import success_response, error_response


class EmotionLogViewSet(viewsets.ModelViewSet):
    """情绪日志管理"""
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return EmotionLog.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        return EmotionLogSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class EmotionPatternViewSet(viewsets.ModelViewSet):
    """情绪模式管理"""
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return EmotionPattern.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        return EmotionPatternSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class EmotionAnalysisModelViewSet(viewsets.ReadOnlyModelViewSet):
    """情绪分析模型查看"""
    permission_classes = [IsAuthenticated]
    serializer_class = EmotionAnalysisModelSerializer
    
    def get_queryset(self):
        return EmotionAnalysisModel.objects.filter(is_active=True)


class EmotionAnalysisAPIView(BaseAPIView):
    """情绪分析API"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """分析情绪"""
        text = request.data.get('text')
        if not text:
            return error_response("缺少文本内容", status_code=status.HTTP_400_BAD_REQUEST)
        
        try:
            # 这里应该调用AI服务进行情绪分析
            # 暂时返回模拟数据
            emotion_data = {
                'emotion_label': 'neutral',
                'confidence': 0.8,
                'intensity': 50,
                'keywords': ['测试', '情绪']
            }
            
            # 保存情绪日志
            emotion_log = EmotionLog.objects.create(
                user=request.user,
                emotion_label=emotion_data['emotion_label'],
                confidence=emotion_data['confidence'],
                intensity=emotion_data['intensity'],
                analysis_source='text',
                keywords=emotion_data['keywords']
            )
            
            return success_response("情绪分析完成", emotion_data)
        except Exception as e:
            return error_response(f"情绪分析失败: {str(e)}", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EmotionHistoryAPIView(BaseAPIView):
    """情绪历史API"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """获取情绪历史"""
        try:
            emotion_logs = EmotionLog.objects.filter(
                user=request.user
            ).order_by('-created_at')[:30]
            
            serializer = EmotionLogSerializer(emotion_logs, many=True)
            return success_response("获取成功", serializer.data)
        except Exception as e:
            return error_response(f"获取情绪历史失败: {str(e)}", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
