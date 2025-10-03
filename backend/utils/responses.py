"""
统一响应格式工具
"""
from rest_framework.response import Response
from rest_framework import status


def success_response(message="操作成功", data=None, status_code=status.HTTP_200_OK):
    """
    成功响应格式
    
    Args:
        message: 响应消息
        data: 响应数据
        status_code: HTTP状态码
    
    Returns:
        Response: DRF响应对象
    """
    response_data = {
        'code': status_code,
        'message': message,
        'data': data,
        'success': True
    }
    
    return Response(response_data, status=status_code)


def error_response(message="操作失败", data=None, status_code=status.HTTP_400_BAD_REQUEST):
    """
    错误响应格式
    
    Args:
        message: 错误消息
        data: 错误详情数据
        status_code: HTTP状态码
    
    Returns:
        Response: DRF响应对象
    """
    response_data = {
        'code': status_code,
        'message': message,
        'data': data,
        'success': False
    }
    
    return Response(response_data, status=status_code)


def paginated_response(message="获取成功", data=None, pagination_info=None, status_code=status.HTTP_200_OK):
    """
    分页响应格式
    
    Args:
        message: 响应消息
        data: 响应数据
        pagination_info: 分页信息
        status_code: HTTP状态码
    
    Returns:
        Response: DRF响应对象
    """
    response_data = {
        'code': status_code,
        'message': message,
        'data': data,
        'pagination': pagination_info,
        'success': True
    }
    
    return Response(response_data, status=status_code)
