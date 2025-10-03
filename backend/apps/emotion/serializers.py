from rest_framework import serializers
from .models import EmotionLog, EmotionPattern, EmotionAnalysisModel


class EmotionLogSerializer(serializers.ModelSerializer):
    """情绪日志序列化器"""
    
    class Meta:
        model = EmotionLog
        fields = [
            'id', 'emotion_label', 'confidence', 'intensity',
            'analysis_source', 'raw_data', 'keywords', 'context',
            'session_emotion_trend', 'crisis_indicators', 'risk_level',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class EmotionPatternSerializer(serializers.ModelSerializer):
    """情绪模式序列化器"""
    
    class Meta:
        model = EmotionPattern
        fields = [
            'id', 'pattern_type', 'pattern_data', 'confidence',
            'description', 'triggers', 'recommendations',
            'occurrence_count', 'accuracy_rate', 'is_active',
            'created_at', 'updated_at', 'last_occurrence'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class EmotionAnalysisModelSerializer(serializers.ModelSerializer):
    """情绪分析模型序列化器"""
    
    class Meta:
        model = EmotionAnalysisModel
        fields = [
            'id', 'name', 'model_type', 'version', 'config',
            'accuracy', 'precision', 'recall', 'f1_score',
            'usage_count', 'avg_processing_time', 'is_active',
            'is_default', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
