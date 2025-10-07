from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'sessions', views.ChatSessionViewSet, basename='chat-session')
router.register(r'messages', views.ChatMessageViewSet, basename='chat-message')

urlpatterns = [
    path('', include(router.urls)),
    path('send/', views.SendMessageView.as_view(), name='send-message'),
    path('stream/', views.SendMessageView.as_view(), name='stream-chat'),
    # 添加专门用于获取会话消息的URL
    path('sessions/<uuid:session_id>/messages/', views.ChatMessageListView.as_view(), name='session-messages'),
    # 反馈相关API
    path('feedback/', views.ChatFeedbackView.as_view(), name='chat-feedback'),
    # 清空聊天记录
    path('clear/', views.clear_chat_history, name='clear-chat-history'),
    # 危机报告
    path('crisis-report/', views.report_crisis, name='crisis-report'),
]
