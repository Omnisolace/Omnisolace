from rest_framework import serializers
from .models import ChatSession, ChatMessage, ChatFeedback


class ChatSessionSerializer(serializers.ModelSerializer):
    """聊天会话序列化器"""
    
    class Meta:
        model = ChatSession
        fields = [
            'id', 'title', 'summary', 'is_active', 'is_archived',
            'is_emergency', 'message_count', 'duration_minutes',
            'created_at', 'updated_at', 'last_message_at',
            'is_desensitized', 'desensitized_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ChatSessionCreateSerializer(serializers.ModelSerializer):
    """创建聊天会话序列化器"""
    
    class Meta:
        model = ChatSession
        fields = ['title', 'summary']


class ChatMessageSerializer(serializers.ModelSerializer):
    """聊天消息序列化器"""
    
    class Meta:
        model = ChatMessage
        fields = [
            'id', 'content', 'message_type', 'sender_type',
            'audio_file', 'image_file', 'metadata', 'emotion_data',
            'crisis_detected', 'crisis_keywords', 'ai_model',
            'ai_confidence', 'processing_time', 'created_at',
            'original_content', 'is_desensitized'
        ]
        read_only_fields = ['id', 'created_at']


class ChatMessageCreateSerializer(serializers.ModelSerializer):
    """创建聊天消息序列化器"""
    
    class Meta:
        model = ChatMessage
        fields = ['content', 'message_type', 'audio_file', 'image_file', 'metadata']
    
    def validate_message_type(self, value):
        """验证消息类型"""
        valid_types = ['text', 'audio', 'image', 'system_notice']
        if value not in valid_types:
            raise serializers.ValidationError("无效的消息类型")
        return value


class SendMessageSerializer(serializers.Serializer):
    """发送消息序列化器"""
    content = serializers.CharField(max_length=5000, help_text='消息内容')
    message_type = serializers.ChoiceField(
        choices=['text', 'audio', 'image'],
        default='text',
        help_text='消息类型'
    )
    session_id = serializers.CharField(required=False, help_text='会话ID')
    session = serializers.CharField(required=False, help_text='会话ID（兼容字段）')
    audio_file = serializers.FileField(required=False, help_text='语音文件')
    image_file = serializers.ImageField(required=False, help_text='图片文件')
    metadata = serializers.JSONField(required=False, help_text='元数据')
    deep_thinking = serializers.BooleanField(default=False, help_text='启用深度思考模式')
    web_search = serializers.BooleanField(default=False, help_text='启用联网搜索')
    
    def validate(self, data):
        """验证数据"""
        # 兼容处理session和session_id字段
        session_id = data.get('session_id') or data.get('session')
        if not session_id:
            raise serializers.ValidationError("session_id或session字段是必填项。")
        
        # 统一使用session_id字段
        data['session_id'] = session_id
        return data
    
    def validate_content(self, value):
        """验证消息内容"""
        if not value or not value.strip():
            raise serializers.ValidationError("消息内容不能为空")
        return value.strip()


class ChatFeedbackSerializer(serializers.ModelSerializer):
    """聊天反馈序列化器"""
    
    class Meta:
        model = ChatFeedback
        fields = [
            'id', 'feedback_type', 'positive_category', 'negative_category',
            'additional_feedback', 'rating', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def validate_rating(self, value):
        """验证评分"""
        if value is not None and (value < 1 or value > 5):
            raise serializers.ValidationError("评分必须在1-5之间")
        return value
    
    def validate(self, data):
        """验证反馈数据"""
        feedback_type = data.get('feedback_type')
        positive_category = data.get('positive_category')
        negative_category = data.get('negative_category')
        
        # 根据反馈类型验证分类字段
        if feedback_type == 'positive':
            if not positive_category:
                raise serializers.ValidationError("正反馈必须选择分类")
            if negative_category:
                raise serializers.ValidationError("正反馈不能包含负反馈分类")
        elif feedback_type == 'negative':
            if not negative_category:
                raise serializers.ValidationError("负反馈必须选择分类")
            if positive_category:
                raise serializers.ValidationError("负反馈不能包含正反馈分类")
        
        return data


class ChatFeedbackCreateSerializer(serializers.ModelSerializer):
    """创建聊天反馈序列化器"""
    
    message_id = serializers.CharField(write_only=True, help_text='消息ID')
    
    class Meta:
        model = ChatFeedback
        fields = [
            'message_id', 'feedback_type', 'positive_category', 'negative_category',
            'additional_feedback', 'rating'
        ]
    
    def validate_message_id(self, value):
        """验证消息ID"""
        try:
            from .models import ChatMessage
            message = ChatMessage.objects.get(id=value)
            return value
        except ChatMessage.DoesNotExist:
            raise serializers.ValidationError("消息不存在")
    
    def validate(self, data):
        """验证反馈数据"""
        feedback_type = data.get('feedback_type')
        positive_category = data.get('positive_category')
        negative_category = data.get('negative_category')
        
        # 根据反馈类型验证分类字段
        if feedback_type == 'positive':
            if not positive_category:
                raise serializers.ValidationError("正反馈必须选择分类")
            if negative_category:
                raise serializers.ValidationError("正反馈不能包含负反馈分类")
        elif feedback_type == 'negative':
            if not negative_category:
                raise serializers.ValidationError("负反馈必须选择分类")
            if positive_category:
                raise serializers.ValidationError("负反馈不能包含正反馈分类")
        
        return data
    
    def create(self, validated_data):
        """创建反馈"""
        message_id = validated_data.pop('message_id')
        from .models import ChatMessage
        message = ChatMessage.objects.get(id=message_id)
        
        # 检查是否已存在反馈
        existing_feedback = ChatFeedback.objects.filter(
            user=self.context['request'].user,
            message=message
        ).first()
        
        if existing_feedback:
            # 更新现有反馈
            for key, value in validated_data.items():
                setattr(existing_feedback, key, value)
            existing_feedback.save()
            return existing_feedback
        else:
            # 创建新反馈
            return ChatFeedback.objects.create(
                user=self.context['request'].user,
                message=message,
                **validated_data
            )
