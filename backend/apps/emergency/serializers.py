from rest_framework import serializers
from .models import EmergencyContact, EmergencyRequest


class EmergencyContactSerializer(serializers.ModelSerializer):
    """紧急联系人序列化器"""
    
    class Meta:
        model = EmergencyContact
        fields = [
            'id', 'name', 'phone', 'relationship', 
            'is_primary', 'is_active', 'notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_phone(self, value):
        """验证手机号格式"""
        if not value.isdigit() or len(value) != 11:
            raise serializers.ValidationError("手机号格式不正确")
        return value


class EmergencyContactCreateSerializer(serializers.ModelSerializer):
    """创建紧急联系人序列化器"""
    
    class Meta:
        model = EmergencyContact
        fields = ['name', 'phone', 'relationship', 'is_primary', 'notes']
    
    def validate_phone(self, value):
        """验证手机号格式"""
        if not value.isdigit() or len(value) != 11:
            raise serializers.ValidationError("手机号格式不正确")
        return value


class EmergencyRequestSerializer(serializers.ModelSerializer):
    """紧急求助记录序列化器"""
    
    class Meta:
        model = EmergencyRequest
        fields = [
            'id', 'request_type', 'urgency_level', 'description',
            'location_info', 'response_status', 'response_time',
            'responder_info', 'contacts_notified', 'notification_methods',
            'created_at', 'resolved_at'
        ]
        read_only_fields = ['id', 'created_at', 'response_time', 'resolved_at']


class EmergencyRequestCreateSerializer(serializers.ModelSerializer):
    """创建紧急求助序列化器"""
    
    class Meta:
        model = EmergencyRequest
        fields = ['request_type', 'urgency_level', 'description', 'location_info']
    
    def validate_urgency_level(self, value):
        """验证紧急程度"""
        if value not in ['low', 'medium', 'high', 'critical']:
            raise serializers.ValidationError("无效的紧急程度")
        return value
