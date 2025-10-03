"""
工具视图函数
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.conf import settings
from django.db import connection
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)


class BaseAPIView(APIView):
    """基础API视图类"""
    pass


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """
    健康检查接口
    """
    health_data = {
        'status': 'healthy',
        'timestamp': request.META.get('HTTP_HOST', 'localhost'),
        'services': {}
    }
    
    # 检查数据库连接
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            health_data['services']['database'] = 'healthy'
    except Exception as e:
        health_data['services']['database'] = f'error: {str(e)}'
        health_data['status'] = 'degraded'
    
    # 检查缓存连接
    try:
        cache.set('health_check', 'test', 60)
        cache.get('health_check')
        health_data['services']['cache'] = 'healthy'
    except Exception as e:
        health_data['services']['cache'] = f'error: {str(e)}'
        health_data['status'] = 'degraded'
    
    # 检查AI服务（如果配置了）
    if hasattr(settings, 'OPENAI_API_KEY') and settings.OPENAI_API_KEY:
        health_data['services']['ai_service'] = 'configured'
    else:
        health_data['services']['ai_service'] = 'not_configured'
    
    status_code = status.HTTP_200_OK if health_data['status'] == 'healthy' else status.HTTP_503_SERVICE_UNAVAILABLE
    
    return Response(health_data, status=status_code)
