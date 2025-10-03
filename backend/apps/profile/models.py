"""
心理档案相关模型
"""
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
import uuid

User = get_user_model()


class PsychologicalProfile(models.Model):
    """
    心理档案模型
    """
    class PersonalityType(models.TextChoices):
        INTROVERT = 'introvert', '内向型'
        EXTROVERT = 'extrovert', '外向型'
        AMBIVERT = 'ambivert', '中间型'
        UNKNOWN = 'unknown', '未知'
    
    class CommunicationStyle(models.TextChoices):
        DIRECT = 'direct', '直接型'
        INDIRECT = 'indirect', '间接型'
        ANALYTICAL = 'analytical', '分析型'
        EXPRESSIVE = 'expressive', '表达型'
        SUPPORTIVE = 'supportive', '支持型'
        CONTROLLED = 'controlled', '控制型'
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='psychological_profile')
    
    # 基础信息
    assessment_date = models.DateTimeField(default=timezone.now, verbose_name='评估日期')
    last_updated = models.DateTimeField(auto_now=True, verbose_name='最后更新')
    
    # 人格特征
    personality_type = models.CharField(
        max_length=20,
        choices=PersonalityType.choices,
        default=PersonalityType.UNKNOWN,
        verbose_name='人格类型'
    )
    communication_style = models.CharField(
        max_length=20,
        choices=CommunicationStyle.choices,
        default=CommunicationStyle.SUPPORTIVE,
        verbose_name='沟通风格'
    )
    
    # 情绪特征
    emotional_stability = models.PositiveSmallIntegerField(
        default=50,
        verbose_name='情绪稳定性',
        help_text='0-100, 数值越高越稳定'
    )
    stress_tolerance = models.PositiveSmallIntegerField(
        default=50,
        verbose_name='压力耐受性',
        help_text='0-100, 数值越高耐受性越强'
    )
    social_anxiety_level = models.PositiveSmallIntegerField(
        default=30,
        verbose_name='社交焦虑水平',
        help_text='0-100, 数值越高焦虑越严重'
    )
    
    # 认知模式
    thinking_patterns = models.JSONField(
        default=list,
        verbose_name='思维模式',
        help_text='如：灾难化思维、全或无思维等'
    )
    core_beliefs = models.JSONField(
        default=list,
        verbose_name='核心信念'
    )
    cognitive_biases = models.JSONField(
        default=list,
        verbose_name='认知偏误'
    )
    
    # 应对机制
    coping_strategies = models.JSONField(
        default=list,
        verbose_name='应对策略'
    )
    defense_mechanisms = models.JSONField(
        default=list,
        verbose_name='防御机制'
    )
    
    # 社会支持
    support_system_strength = models.PositiveSmallIntegerField(
        default=50,
        verbose_name='支持系统强度',
        help_text='0-100, 数值越高支持系统越强'
    )
    family_relationship_quality = models.PositiveSmallIntegerField(
        default=50,
        verbose_name='家庭关系质量',
        help_text='0-100, 数值越高关系质量越好'
    )
    
    # 风险评估
    depression_risk = models.PositiveSmallIntegerField(
        default=10,
        verbose_name='抑郁风险',
        help_text='0-100, 数值越高风险越大'
    )
    anxiety_risk = models.PositiveSmallIntegerField(
        default=10,
        verbose_name='焦虑风险',
        help_text='0-100, 数值越高风险越大'
    )
    suicide_risk = models.PositiveSmallIntegerField(
        default=0,
        verbose_name='自杀风险',
        help_text='0-100, 数值越高风险越大'
    )
    
    # 治疗建议
    recommended_approaches = models.JSONField(
        default=list,
        verbose_name='推荐治疗方法'
    )
    contraindicated_approaches = models.JSONField(
        default=list,
        verbose_name='禁忌治疗方法'
    )
    
    # 个性化设置
    preferred_conversation_topics = models.JSONField(
        default=list,
        verbose_name='偏好话题'
    )
    sensitive_topics = models.JSONField(
        default=list,
        verbose_name='敏感话题'
    )
    communication_preferences = models.JSONField(
        default=dict,
        verbose_name='沟通偏好'
    )
    
    # 进展追踪
    improvement_areas = models.JSONField(
        default=list,
        verbose_name='改进领域'
    )
    progress_indicators = models.JSONField(
        default=dict,
        verbose_name='进展指标'
    )
    
    # 数据来源
    data_sources = models.JSONField(
        default=list,
        verbose_name='数据来源',
        help_text='聊天记录、测评结果、专业评估等'
    )
    confidence_score = models.FloatField(
        default=0.0,
        verbose_name='档案置信度',
        help_text='0.0-1.0, 表示档案信息的可信度'
    )
    
    class Meta:
        verbose_name = '心理档案'
        verbose_name_plural = '心理档案'
        db_table = 'psychological_profiles'
    
    def __str__(self):
        return f"{self.user.username} 的心理档案"
    
    def calculate_overall_risk(self):
        """计算总体风险等级"""
        risk_factors = [
            self.depression_risk,
            self.anxiety_risk,
            self.suicide_risk * 2,  # 自杀风险权重更高
        ]
        
        overall_risk = sum(risk_factors) / len(risk_factors)
        
        if overall_risk >= 70:
            return 'critical'
        elif overall_risk >= 50:
            return 'high'
        elif overall_risk >= 30:
            return 'medium'
        else:
            return 'low'
    
    def get_personalized_recommendations(self):
        """获取个性化建议"""
        recommendations = []
        
        # 基于人格类型的建议
        if self.personality_type == self.PersonalityType.INTROVERT:
            recommendations.extend([
                '提供独处时间进行自我反思',
                '使用书面表达方式',
                '避免过多的群体活动'
            ])
        elif self.personality_type == self.PersonalityType.EXTROVERT:
            recommendations.extend([
                '鼓励社交活动和群体讨论',
                '使用口头表达方式',
                '提供团体支持机会'
            ])
        
        # 基于压力耐受性的建议
        if self.stress_tolerance < 30:
            recommendations.extend([
                '学习压力管理技巧',
                '建立规律的生活作息',
                '实践放松技术'
            ])
        
        return recommendations
    
    def update_from_chat_analysis(self, emotion_logs):
        """根据聊天分析更新档案"""
        # 分析最近的情绪日志
        if not emotion_logs:
            return
        
        # 更新情绪稳定性
        emotion_variance = self._calculate_emotion_variance(emotion_logs)
        if emotion_variance > 50:
            self.emotional_stability = max(0, self.emotional_stability - 5)
        elif emotion_variance < 20:
            self.emotional_stability = min(100, self.emotional_stability + 2)
        
        # 更新风险评估
        negative_emotions = [log for log in emotion_logs if log.is_negative_emotion]
        if len(negative_emotions) / len(emotion_logs) > 0.7:
            self.depression_risk = min(100, self.depression_risk + 10)
            self.anxiety_risk = min(100, self.anxiety_risk + 10)
        
        self.save()
    
    def _calculate_emotion_variance(self, emotion_logs):
        """计算情绪方差"""
        if not emotion_logs:
            return 0
        
        intensities = [log.intensity for log in emotion_logs]
        mean = sum(intensities) / len(intensities)
        variance = sum((x - mean) ** 2 for x in intensities) / len(intensities)
        return variance ** 0.5


class PsychologicalAssessment(models.Model):
    """
    心理测评模型
    """
    class AssessmentType(models.TextChoices):
        PHQ9 = 'phq9', 'PHQ-9抑郁症筛查'
        GAD7 = 'gad7', 'GAD-7焦虑症筛查'
        PSS = 'pss', '感知压力量表'
        BIG5 = 'big5', '大五人格测试'
        MBTI = 'mbti', 'MBTI人格测试'
        CUSTOM = 'custom', '自定义测评'
    
    class AssessmentStatus(models.TextChoices):
        DRAFT = 'draft', '草稿'
        IN_PROGRESS = 'in_progress', '进行中'
        COMPLETED = 'completed', '已完成'
        EXPIRED = 'expired', '已过期'
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assessments')
    profile = models.ForeignKey(
        PsychologicalProfile,
        on_delete=models.CASCADE,
        related_name='assessments',
        null=True,
        blank=True
    )
    
    # 测评信息
    assessment_type = models.CharField(
        max_length=20,
        choices=AssessmentType.choices,
        verbose_name='测评类型'
    )
    title = models.CharField(max_length=200, verbose_name='测评标题')
    description = models.TextField(verbose_name='测评描述', blank=True)
    
    # 状态信息
    status = models.CharField(
        max_length=20,
        choices=AssessmentStatus.choices,
        default=AssessmentStatus.DRAFT,
        verbose_name='测评状态'
    )
    
    # 结果信息
    raw_scores = models.JSONField(verbose_name='原始分数', default=dict)
    normalized_scores = models.JSONField(verbose_name='标准化分数', default=dict)
    interpretation = models.TextField(verbose_name='结果解释', blank=True)
    recommendations = models.JSONField(verbose_name='建议', default=list)
    
    # 时间信息
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    started_at = models.DateTimeField(null=True, blank=True, verbose_name='开始时间')
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name='完成时间')
    expires_at = models.DateTimeField(null=True, blank=True, verbose_name='过期时间')
    
    # 元数据
    questions_count = models.PositiveIntegerField(default=0, verbose_name='题目数量')
    completion_time = models.PositiveIntegerField(default=0, verbose_name='完成时间(秒)')
    
    class Meta:
        verbose_name = '心理测评'
        verbose_name_plural = '心理测评'
        db_table = 'psychological_assessments'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"
    
    def start_assessment(self):
        """开始测评"""
        self.status = self.AssessmentStatus.IN_PROGRESS
        self.started_at = timezone.now()
        self.save(update_fields=['status', 'started_at'])
    
    def complete_assessment(self, scores, interpretation=None):
        """完成测评"""
        self.status = self.AssessmentStatus.COMPLETED
        self.completed_at = timezone.now()
        self.raw_scores = scores
        
        if interpretation:
            self.interpretation = interpretation
        
        if self.started_at:
            self.completion_time = int(
                (self.completed_at - self.started_at).total_seconds()
            )
        
        self.save()
        
        # 更新心理档案
        if self.profile:
            self._update_profile_from_assessment()
    
    def _update_profile_from_assessment(self):
        """根据测评结果更新心理档案"""
        if self.assessment_type == self.AssessmentType.PHQ9:
            score = self.raw_scores.get('total_score', 0)
            if score >= 15:
                self.profile.depression_risk = min(100, self.profile.depression_risk + 20)
            elif score >= 10:
                self.profile.depression_risk = min(100, self.profile.depression_risk + 10)
        
        elif self.assessment_type == self.AssessmentType.GAD7:
            score = self.raw_scores.get('total_score', 0)
            if score >= 15:
                self.profile.anxiety_risk = min(100, self.profile.anxiety_risk + 20)
            elif score >= 10:
                self.profile.anxiety_risk = min(100, self.profile.anxiety_risk + 10)
        
        self.profile.save()


class PsychologicalReport(models.Model):
    """
    心理报告模型
    """
    class ReportType(models.TextChoices):
        WEEKLY = 'weekly', '周报'
        MONTHLY = 'monthly', '月报'
        COMPREHENSIVE = 'comprehensive', '综合报告'
        CRISIS = 'crisis', '危机报告'
        PROGRESS = 'progress', '进展报告'
    
    class ReportStatus(models.TextChoices):
        GENERATING = 'generating', '生成中'
        COMPLETED = 'completed', '已完成'
        FAILED = 'failed', '生成失败'
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports')
    profile = models.ForeignKey(
        PsychologicalProfile,
        on_delete=models.CASCADE,
        related_name='reports'
    )
    
    # 报告信息
    report_type = models.CharField(
        max_length=20,
        choices=ReportType.choices,
        verbose_name='报告类型'
    )
    title = models.CharField(max_length=200, verbose_name='报告标题')
    
    # 报告内容
    executive_summary = models.TextField(verbose_name='执行摘要', blank=True)
    detailed_analysis = models.JSONField(verbose_name='详细分析', default=dict)
    recommendations = models.JSONField(verbose_name='建议', default=list)
    risk_assessment = models.JSONField(verbose_name='风险评估', default=dict)
    
    # 数据范围
    data_start_date = models.DateTimeField(verbose_name='数据开始日期')
    data_end_date = models.DateTimeField(verbose_name='数据结束日期')
    
    # 生成信息
    status = models.CharField(
        max_length=20,
        choices=ReportStatus.choices,
        default=ReportStatus.GENERATING,
        verbose_name='报告状态'
    )
    generated_by = models.CharField(max_length=100, verbose_name='生成者', default='AI系统')
    generation_time = models.PositiveIntegerField(default=0, verbose_name='生成时间(秒)')
    
    # 文件信息
    pdf_file = models.FileField(
        upload_to='reports/pdf/%Y/%m/',
        verbose_name='PDF文件',
        null=True,
        blank=True
    )
    json_data = models.JSONField(verbose_name='JSON数据', default=dict)
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name='完成时间')
    
    class Meta:
        verbose_name = '心理报告'
        verbose_name_plural = '心理报告'
        db_table = 'psychological_reports'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"
    
    def mark_completed(self):
        """标记为已完成"""
        self.status = self.ReportStatus.COMPLETED
        self.completed_at = timezone.now()
        
        if self.created_at:
            self.generation_time = int(
                (self.completed_at - self.created_at).total_seconds()
            )
        
        self.save(update_fields=['status', 'completed_at', 'generation_time'])
    
    def mark_failed(self):
        """标记为生成失败"""
        self.status = self.ReportStatus.FAILED
        self.save(update_fields=['status'])
