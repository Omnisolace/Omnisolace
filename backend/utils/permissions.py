"""
自定义权限类
"""
from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    只有对象的所有者才能编辑，其他人只能读取
    """
    
    def has_object_permission(self, request, view, obj):
        # 读取权限对所有请求都允许
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # 写权限只给对象的所有者
        return obj.user == request.user


class IsOwner(permissions.BasePermission):
    """
    只有对象的所有者才能访问
    """
    
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsTeenUser(permissions.BasePermission):
    """
    只有青少年用户才能访问
    """
    
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.age_group == 'teen'
        )


class IsElderUser(permissions.BasePermission):
    """
    只有老年用户才能访问
    """
    
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.age_group == 'elder'
        )


class HasParentalConsent(permissions.BasePermission):
    """
    青少年用户需要家长同意
    """
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        if request.user.age_group == 'teen':
            return request.user.parental_consent
        
        return True


class IsNotGuest(permissions.BasePermission):
    """
    非游客用户才能访问
    """
    
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            not getattr(request.user, 'is_guest', False)
        )
