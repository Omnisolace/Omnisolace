"""
自定义异常处理器
"""
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from django.http import Http404
import logging

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    自定义异常处理器
    """
    # 调用REST framework默认的异常处理器
    response = exception_handler(exc, context)
    
    # 如果响应为None，表示异常没有被处理
    if response is not None:
        custom_response_data = {
            'code': response.status_code,
            'message': get_error_message(exc, response),
            'data': response.data if isinstance(response.data, dict) else {'detail': response.data},
            'success': False
        }
        
        response.data = custom_response_data
    else:
        # 处理未被捕获的异常
        if isinstance(exc, Http404):
            custom_response_data = {
                'code': status.HTTP_404_NOT_FOUND,
                'message': '请求的资源未找到',
                'data': None,
                'success': False
            }
            response = Response(custom_response_data, status=status.HTTP_404_NOT_FOUND)
        
        elif isinstance(exc, ValidationError):
            custom_response_data = {
                'code': status.HTTP_400_BAD_REQUEST,
                'message': '数据验证失败',
                'data': {'validation_errors': exc.messages},
                'success': False
            }
            response = Response(custom_response_data, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            # 记录未处理的异常
            logger.error(f"未处理的异常: {type(exc).__name__}: {str(exc)}")
            
            custom_response_data = {
                'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': '服务器内部错误',
                'data': None,
                'success': False
            }
            response = Response(custom_response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return response


def get_error_message(exc, response):
    """
    获取错误消息
    """
    error_messages = {
        400: '请求参数错误',
        401: '未授权访问',
        403: '权限不足',
        404: '请求的资源未找到',
        405: '不支持的请求方法',
        429: '请求过于频繁',
        500: '服务器内部错误',
    }
    
    status_code = response.status_code
    
    # 尝试从响应数据中获取详细错误信息
    if isinstance(response.data, dict):
        if 'detail' in response.data:
            return str(response.data['detail'])
        elif 'message' in response.data:
            return str(response.data['message'])
        elif 'non_field_errors' in response.data:
            return str(response.data['non_field_errors'][0])
    
    # 使用默认错误消息
    return error_messages.get(status_code, '未知错误')
