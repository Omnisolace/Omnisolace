from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'logs', views.SystemLogViewSet, basename='system-log')
router.register(r'notifications', views.NotificationViewSet, basename='notification')
router.register(r'configs', views.AppConfigViewSet, basename='app-config')

urlpatterns = [
    path('', include(router.urls)),
    path('common/', views.CommonAPIView.as_view(), name='common-api'),
]
