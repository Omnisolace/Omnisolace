from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'contacts', views.EmergencyContactViewSet, basename='emergency-contact')
router.register(r'requests', views.EmergencyRequestViewSet, basename='emergency-request')

urlpatterns = [
    path('', include(router.urls)),
    path('emergency/', views.EmergencyAPIView.as_view(), name='emergency-api'),
]
