from rest_framework import serializers
from .models import SystemLog, Notification, AppConfig


class SystemLogSerializer(serializers.ModelSerializer):
    """系统日志序列化器"""
    
    class Meta:
        model = SystemLog
        fields = [
            'id', 'action', 'model', 'object_id', 'changes',
            'ip_address', 'user_agent', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class NotificationSerializer(serializers.ModelSerializer):
    """通知序列化器"""
    
    class Meta:
        model = Notification
        fields = [
            'id', 'title', 'content', 'notification_type', 'priority',
            'related_model', 'related_id', 'is_read', 'is_sent',
            'created_at', 'read_at', 'sent_at'
        ]
        read_only_fields = ['id', 'created_at', 'read_at', 'sent_at']


class NotificationCreateSerializer(serializers.ModelSerializer):
    """创建通知序列化器"""
    
    class Meta:
        model = Notification
        fields = [
            'title', 'content', 'notification_type', 'priority',
            'related_model', 'related_id'
        ]
    
    def validate_notification_type(self, value):
        """验证通知类型"""
        valid_types = ['system', 'chat', 'emotion', 'crisis', 'emergency', 'reminder']
        if value not in valid_types:
            raise serializers.ValidationError("无效的通知类型")
        return value


class AppConfigSerializer(serializers.ModelSerializer):
    """应用配置序列化器"""
    
    class Meta:
        model = AppConfig
        fields = [
            'id', 'key', 'value', 'config_type', 'description',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_key(self, value):
        """验证配置键格式"""
        if not value.replace('_', '').replace('-', '').isalnum():
            raise serializers.ValidationError("配置键只能包含字母、数字、下划线和连字符")
        return value
