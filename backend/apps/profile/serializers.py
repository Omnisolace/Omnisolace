from rest_framework import serializers
from .models import (
    PsychologicalProfile, 
    PsychologicalAssessment, 
    PsychologicalReport
)


class PsychologicalProfileSerializer(serializers.ModelSerializer):
    """心理档案序列化器"""
    
    class Meta:
        model = PsychologicalProfile
        fields = [
            'id', 'assessment_date', 'last_updated',
            'personality_type', 'communication_style',
            'emotional_stability', 'stress_tolerance', 'social_anxiety_level',
            'thinking_patterns', 'core_beliefs', 'cognitive_biases',
            'coping_strategies', 'defense_mechanisms',
            'support_system_strength', 'family_relationship_quality',
            'depression_risk', 'anxiety_risk', 'suicide_risk',
            'recommended_approaches', 'contraindicated_approaches',
            'preferred_conversation_topics', 'sensitive_topics',
            'communication_preferences', 'improvement_areas',
            'progress_indicators', 'data_sources', 'confidence_score'
        ]
        read_only_fields = ['id', 'assessment_date', 'last_updated']


class PsychologicalAssessmentSerializer(serializers.ModelSerializer):
    """心理测评序列化器"""
    
    class Meta:
        model = PsychologicalAssessment
        fields = [
            'id', 'assessment_type', 'title', 'description',
            'status', 'raw_scores', 'normalized_scores',
            'interpretation', 'recommendations',
            'created_at', 'started_at', 'completed_at', 'expires_at',
            'questions_count', 'completion_time'
        ]
        read_only_fields = ['id', 'created_at']


class PsychologicalReportSerializer(serializers.ModelSerializer):
    """心理报告序列化器"""
    
    class Meta:
        model = PsychologicalReport
        fields = [
            'id', 'report_type', 'title', 'executive_summary',
            'detailed_analysis', 'recommendations', 'risk_assessment',
            'data_start_date', 'data_end_date', 'status',
            'generated_by', 'generation_time', 'pdf_file',
            'json_data', 'created_at', 'completed_at'
        ]
        read_only_fields = ['id', 'created_at', 'completed_at']
