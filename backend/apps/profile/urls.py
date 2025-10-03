from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'profiles', views.PsychologicalProfileViewSet, basename='psychological-profile')
router.register(r'assessments', views.PsychologicalAssessmentViewSet, basename='psychological-assessment')
router.register(r'reports', views.PsychologicalReportViewSet, basename='psychological-report')

urlpatterns = [
    path('', include(router.urls)),
    path('my-profile/', views.MyProfileAPIView.as_view(), name='my-profile'),
    path('assessment/', views.AssessmentAPIView.as_view(), name='assessment'),
]
