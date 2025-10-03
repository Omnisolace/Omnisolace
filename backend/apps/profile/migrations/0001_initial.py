# Generated migration for profile app

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PsychologicalProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assessment_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='评估日期')),
                ('last_updated', models.DateTimeField(auto_now=True, verbose_name='最后更新')),
                ('personality_type', models.CharField(choices=[('introvert', '内向型'), ('extrovert', '外向型'), ('ambivert', '中间型'), ('unknown', '未知')], default='unknown', max_length=20, verbose_name='人格类型')),
                ('communication_style', models.CharField(choices=[('direct', '直接型'), ('indirect', '间接型'), ('analytical', '分析型'), ('expressive', '表达型'), ('supportive', '支持型'), ('controlled', '控制型')], default='supportive', max_length=20, verbose_name='沟通风格')),
                ('emotional_stability', models.PositiveSmallIntegerField(default=50, help_text='0-100, 数值越高越稳定', verbose_name='情绪稳定性')),
                ('stress_tolerance', models.PositiveSmallIntegerField(default=50, help_text='0-100, 数值越高耐受性越强', verbose_name='压力耐受性')),
                ('social_anxiety_level', models.PositiveSmallIntegerField(default=30, help_text='0-100, 数值越高焦虑越严重', verbose_name='社交焦虑水平')),
                ('thinking_patterns', models.JSONField(default=list, help_text='如：灾难化思维、全或无思维等', verbose_name='思维模式')),
                ('core_beliefs', models.JSONField(default=list, verbose_name='核心信念')),
                ('cognitive_biases', models.JSONField(default=list, verbose_name='认知偏误')),
                ('coping_strategies', models.JSONField(default=list, verbose_name='应对策略')),
                ('defense_mechanisms', models.JSONField(default=list, verbose_name='防御机制')),
                ('support_system_strength', models.PositiveSmallIntegerField(default=50, help_text='0-100, 数值越高支持系统越强', verbose_name='支持系统强度')),
                ('family_relationship_quality', models.PositiveSmallIntegerField(default=50, help_text='0-100, 数值越高关系质量越好', verbose_name='家庭关系质量')),
                ('depression_risk', models.PositiveSmallIntegerField(default=10, help_text='0-100, 数值越高风险越大', verbose_name='抑郁风险')),
                ('anxiety_risk', models.PositiveSmallIntegerField(default=10, help_text='0-100, 数值越高风险越大', verbose_name='焦虑风险')),
                ('suicide_risk', models.PositiveSmallIntegerField(default=0, help_text='0-100, 数值越高风险越大', verbose_name='自杀风险')),
                ('recommended_approaches', models.JSONField(default=list, verbose_name='推荐治疗方法')),
                ('contraindicated_approaches', models.JSONField(default=list, verbose_name='禁忌治疗方法')),
                ('preferred_conversation_topics', models.JSONField(default=list, verbose_name='偏好话题')),
                ('sensitive_topics', models.JSONField(default=list, verbose_name='敏感话题')),
                ('communication_preferences', models.JSONField(default=dict, verbose_name='沟通偏好')),
                ('improvement_areas', models.JSONField(default=list, verbose_name='改进领域')),
                ('progress_indicators', models.JSONField(default=dict, verbose_name='进展指标')),
                ('data_sources', models.JSONField(default=list, help_text='聊天记录、测评结果、专业评估等', verbose_name='数据来源')),
                ('confidence_score', models.FloatField(default=0.0, help_text='0.0-1.0, 表示档案信息的可信度', verbose_name='档案置信度')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='psychological_profile', to='users.user')),
            ],
            options={
                'verbose_name': '心理档案',
                'verbose_name_plural': '心理档案',
                'db_table': 'psychological_profiles',
            },
        ),
        migrations.CreateModel(
            name='PsychologicalAssessment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('assessment_type', models.CharField(choices=[('phq9', 'PHQ-9抑郁症筛查'), ('gad7', 'GAD-7焦虑症筛查'), ('pss', '感知压力量表'), ('big5', '大五人格测试'), ('mbti', 'MBTI人格测试'), ('custom', '自定义测评')], max_length=20, verbose_name='测评类型')),
                ('title', models.CharField(max_length=200, verbose_name='测评标题')),
                ('description', models.TextField(blank=True, verbose_name='测评描述')),
                ('status', models.CharField(choices=[('draft', '草稿'), ('in_progress', '进行中'), ('completed', '已完成'), ('expired', '已过期')], default='draft', max_length=20, verbose_name='测评状态')),
                ('raw_scores', models.JSONField(default=dict, verbose_name='原始分数')),
                ('normalized_scores', models.JSONField(default=dict, verbose_name='标准化分数')),
                ('interpretation', models.TextField(blank=True, verbose_name='结果解释')),
                ('recommendations', models.JSONField(default=list, verbose_name='建议')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('started_at', models.DateTimeField(blank=True, null=True, verbose_name='开始时间')),
                ('completed_at', models.DateTimeField(blank=True, null=True, verbose_name='完成时间')),
                ('expires_at', models.DateTimeField(blank=True, null=True, verbose_name='过期时间')),
                ('questions_count', models.PositiveIntegerField(default=0, verbose_name='题目数量')),
                ('completion_time', models.PositiveIntegerField(default=0, verbose_name='完成时间(秒)')),
                ('profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assessments', to='profile.psychologicalprofile')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assessments', to='users.user')),
            ],
            options={
                'verbose_name': '心理测评',
                'verbose_name_plural': '心理测评',
                'db_table': 'psychological_assessments',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='PsychologicalReport',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('report_type', models.CharField(choices=[('weekly', '周报'), ('monthly', '月报'), ('comprehensive', '综合报告'), ('crisis', '危机报告'), ('progress', '进展报告')], max_length=20, verbose_name='报告类型')),
                ('title', models.CharField(max_length=200, verbose_name='报告标题')),
                ('executive_summary', models.TextField(blank=True, verbose_name='执行摘要')),
                ('detailed_analysis', models.JSONField(default=dict, verbose_name='详细分析')),
                ('recommendations', models.JSONField(default=list, verbose_name='建议')),
                ('risk_assessment', models.JSONField(default=dict, verbose_name='风险评估')),
                ('data_start_date', models.DateTimeField(verbose_name='数据开始日期')),
                ('data_end_date', models.DateTimeField(verbose_name='数据结束日期')),
                ('status', models.CharField(choices=[('generating', '生成中'), ('completed', '已完成'), ('failed', '生成失败')], default='generating', max_length=20, verbose_name='报告状态')),
                ('generated_by', models.CharField(default='AI系统', max_length=100, verbose_name='生成者')),
                ('generation_time', models.PositiveIntegerField(default=0, verbose_name='生成时间(秒)')),
                ('pdf_file', models.FileField(blank=True, null=True, upload_to='reports/pdf/%Y/%m/', verbose_name='PDF文件')),
                ('json_data', models.JSONField(default=dict, verbose_name='JSON数据')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('completed_at', models.DateTimeField(blank=True, null=True, verbose_name='完成时间')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reports', to='profile.psychologicalprofile')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reports', to='users.user')),
            ],
            options={
                'verbose_name': '心理报告',
                'verbose_name_plural': '心理报告',
                'db_table': 'psychological_reports',
                'ordering': ['-created_at'],
            },
        ),
    ]
