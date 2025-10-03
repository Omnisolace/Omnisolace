from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'logs', views.EmotionLogViewSet, basename='emotion-log')
router.register(r'patterns', views.EmotionPatternViewSet, basename='emotion-pattern')

urlpatterns = [
    path('', include(router.urls)),
    path('analyze/', views.EmotionAnalysisAPIView.as_view(), name='emotion-analysis'),
    path('history/', views.EmotionHistoryAPIView.as_view(), name='emotion-history'),
]
