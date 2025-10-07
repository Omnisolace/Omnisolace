"""
聊天相关视图
"""
from rest_framework import status, generics, permissions, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.http import StreamingHttpResponse
from django.utils import timezone
from django.db import transaction
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
import json
import asyncio
import logging
import time
import queue
import threading
from asgiref.sync import sync_to_async

from .models import ChatSession, ChatMessage, ChatFeedback, ChatTemplate
from .serializers import (
    ChatSessionSerializer,
    ChatSessionCreateSerializer,
    ChatMessageSerializer,
    ChatMessageCreateSerializer,
    SendMessageSerializer,
    ChatFeedbackSerializer,
    ChatFeedbackCreateSerializer
)
# from apps.emotion.services import EmotionAnalysisService
# from apps.emergency.services import CrisisDetectionService
from services.ai_service import ai_service
from utils.responses import success_response, error_response
from utils.permissions import IsOwnerOrReadOnly
from utils.renderers import ServerSentEventRenderer

logger = logging.getLogger(__name__)


class ChatSessionListCreateView(generics.ListCreateAPIView):
    """
    聊天会话列表和创建视图
    """
    serializer_class = ChatSessionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return ChatSession.objects.filter(
            user=self.request.user,
            is_archived=False
        ).order_by('-updated_at')
    
    def perform_create(self, serializer):
        """创建新的聊天会话"""
        serializer.save(user=self.request.user)


class ChatSessionDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    聊天会话详情视图
    """
    serializer_class = ChatSessionSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    
    def get_queryset(self):
        return ChatSession.objects.filter(user=self.request.user)


class ChatMessageListView(generics.ListAPIView):
    """
    聊天消息列表视图
    """
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        session_id = self.kwargs.get('session_id')
        if not session_id:
            return ChatMessage.objects.none()
        
        try:
            return ChatMessage.objects.filter(
                session__id=session_id,
                session__user=self.request.user
            ).order_by('created_at')
        except Exception as e:
            logger.error(f"获取聊天消息失败: {str(e)}")
            return ChatMessage.objects.none()
    
    def list(self, request, *args, **kwargs):
        """重写list方法确保返回正确的响应格式"""
        try:
            session_id = self.kwargs.get('session_id')
            
            # 验证会话是否存在且属于当前用户
            try:
                session = ChatSession.objects.get(
                    id=session_id,
                    user=request.user
                )
            except ChatSession.DoesNotExist:
                return error_response(
                    message="聊天会话不存在",
                    status_code=status.HTTP_404_NOT_FOUND
                )
            
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            
            return success_response(
                message="聊天历史获取成功",
                data={
                    'session_id': str(session_id),
                    'session_title': session.title,
                    'messages': serializer.data,
                    'total_count': queryset.count()
                }
            )
            
        except Exception as e:
            logger.error(f"获取聊天历史失败: {str(e)}")
            return error_response(
                message="获取聊天历史失败",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class SendMessageView(APIView):
    """
    发送消息视图（支持流式响应）
    """
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [JSONRenderer, ServerSentEventRenderer]
    parser_classes = [JSONParser]
    
    def post(self, request):
        serializer = SendMessageSerializer(data=request.data)
        
        if not serializer.is_valid():
            return error_response(
                message="消息验证失败",
                data=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            with transaction.atomic():
                # 获取或创建会话
                session_id = serializer.validated_data.get('session_id')
                content = serializer.validated_data.get('content')
                message_type = serializer.validated_data.get('message_type', 'text')
                
                if session_id:
                    try:
                        session = ChatSession.objects.get(
                            id=session_id,
                            user=request.user
                        )
                    except ChatSession.DoesNotExist:
                        return error_response(
                            message="聊天会话不存在",
                            status_code=status.HTTP_404_NOT_FOUND
                        )
                else:
                    # 创建新会话
                    session = ChatSession.objects.create(
                        user=request.user,
                        title="新的对话"
                    )
                
                # 创建用户消息
                user_message = ChatMessage.objects.create(
                    session=session,
                    content=content,
                    message_type=message_type,
                    sender_type=ChatMessage.SenderType.USER
                )
                
                # 情绪分析
                # emotion_result = ai_service.analyze_emotion(content) # 此行已弃用
                
                # if emotion_result:
                #     user_message.emotion_data = emotion_result
                #     user_message.save()
                    
                    # 记录情绪日志
                    # emotion_service.create_emotion_log(
                    #     user=request.user,
                    #     message=user_message,
                    #     emotion_data=emotion_result
                    # )
                
                # 危机检测
                # crisis_service = CrisisDetectionService()
                # 暂时使用模拟数据
                crisis_detected = False
                # crisis_result = crisis_service.detect_crisis(content, request.user)
                crisis_result = {'is_crisis': crisis_detected, 'keywords': []}
                
                if crisis_result['is_crisis']:
                    user_message.crisis_detected = True
                    user_message.crisis_keywords = crisis_result['keywords']
                    user_message.save()
                    
                    # 触发危机预警
                    # crisis_service.trigger_alert(
                    #     user=request.user,
                    #     message=user_message,
                    #     crisis_data=crisis_result
                    # )
                    
                    # 返回危机预警响应
                    return success_response(
                        message="消息已发送，检测到需要关注的内容",
                        data={
                            'message': ChatMessageSerializer(user_message).data,
                            'session_id': str(session.id),
                            'crisis_detected': True,
                            'crisis_response': crisis_result['auto_response']
                        }
                    )
                
                # 检查是否支持流式响应
                accept_stream = request.headers.get('Accept') == 'text/event-stream'
                
                if accept_stream:
                    return self._stream_ai_response(session, user_message, request)
                else:
                    return self._generate_ai_response(session, user_message, request)
                
        except Exception as e:
            logger.error(f"发送消息失败: {str(e)}")
            return error_response(
                message="发送消息失败，请稍后重试",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def _generate_ai_response(self, session, user_message, request):
        """生成AI回复（非流式）"""
        try:
            # 获取用户年龄段配置
            age_group = getattr(request.user, 'age_group', 'young')
            
            # 获取聊天历史
            chat_history = self._get_chat_history(session)
            
            # 获取深度思考和联网搜索参数
            deep_thinking = request.data.get('deep_thinking', False)
            web_search = request.data.get('web_search', False)
            
            # 生成AI回复 - 使用线程池避免事件循环冲突
            import concurrent.futures
            import threading
            
            def run_async_response():
                # 在新线程中创建新的事件循环
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    return loop.run_until_complete(ai_service.generate_response(
                        message=user_message.content,
                        age_group=age_group,
                        chat_history=chat_history,
                        user_profile=getattr(request.user, 'psychological_profile', None),
                        deep_thinking=deep_thinking,
                        web_search=web_search
                    ))
                finally:
                    loop.close()
            
            start_time = time.time()
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(run_async_response)
                ai_response_content = future.result(timeout=60)  # 60秒超时
            processing_time = time.time() - start_time
            
            # 创建AI消息
            ai_message = ChatMessage.objects.create(
                session=session,
                content=ai_response_content,
                message_type=ChatMessage.MessageType.TEXT,
                sender_type=ChatMessage.SenderType.AI,
                ai_model='deepseek-chat',
                ai_confidence=0.8,
                processing_time=processing_time
            )
            
            # 如果是深度思考模式，尝试从AI响应中提取思考内容
            if deep_thinking:
                # 这里可以添加从AI响应中提取思考内容的逻辑
                # 由于非流式响应可能不包含思考内容，这里暂时跳过
                pass
            
            return success_response(
                message="消息发送成功",
                data={
                    'user_message': ChatMessageSerializer(user_message).data,
                    'ai_message': ChatMessageSerializer(ai_message).data,
                    'session_id': str(session.id)
                }
            )
            
        except Exception as e:
            logger.error(f"生成AI回复失败: {str(e)}")
            
            # 创建错误回复
            error_message = ChatMessage.objects.create(
                session=session,
                content="抱歉，我现在遇到了一些技术问题，请稍后再试。如果您需要紧急帮助，请点击紧急求助按钮。",
                message_type=ChatMessage.MessageType.SYSTEM_NOTICE,
                sender_type=ChatMessage.SenderType.SYSTEM
            )
            
            return success_response(
                message="消息发送成功",
                data={
                    'user_message': ChatMessageSerializer(user_message).data,
                    'ai_message': ChatMessageSerializer(error_message).data,
                    'session_id': str(session.id)
                }
            )
    
    def _stream_ai_response(self, session, user_message, request):
        """流式AI回复"""
        q = queue.Queue()

        # 在后台线程中运行流式生成
        thread = threading.Thread(
            target=self._run_streaming_in_thread,
            args=(q, session, user_message, request)
        )
        thread.start()

        def event_stream():
            try:
                while True:
                    # 从队列中获取数据块
                    chunk = q.get()
                    if chunk is None:  # None作为结束信号
                        break
                    yield chunk
            except Exception as e:
                logger.error(f"Event stream generator error: {str(e)}")
                # 确保即使出错，也能通知客户端
                yield f"data: {json.dumps({'type': 'error', 'message': 'Stream connection closed due to an error.'})}\n\n"

        response = StreamingHttpResponse(
            event_stream(),
            content_type='text/event-stream'
        )
        response['Cache-Control'] = 'no-cache'
        # 注意：不要设置 Connection 头，它是 hop-by-hop 头，在 WSGI 中不允许
        response['X-Accel-Buffering'] = 'no'  # For Nginx
        
        return response

    def _run_streaming_in_thread(self, q, session, user_message, request):
        """
        在后台线程中运行流式生成，并将结果放入队列。
        """
        # 在传递到异步上下文之前，先提取所需的数据
        user_message_id = str(user_message.id)
        user_message_content = user_message.content
        session_id = str(session.id)
        age_group = getattr(request.user, 'age_group', 'young')
        user_profile = getattr(request.user, 'psychological_profile', None)
        
        # 从请求数据中获取深度思考和联网搜索参数
        deep_thinking = request.data.get('deep_thinking', False)
        web_search = request.data.get('web_search', False)
        
        # 为这个线程创建一个新的事件循环
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(
                self._async_stream_logic(q, session, user_message_id, user_message_content, 
                                       session_id, age_group, user_profile, deep_thinking, web_search)
            )
        except Exception as e:
            logger.error(f"Streaming AI response thread error: {str(e)}")
            q.put(f"data: {json.dumps({'type': 'error', 'message': 'Failed to generate AI response.'})}\n\n")
        finally:
            # 发送结束信号
            q.put(None)
            loop.close()

    async def _async_stream_logic(self, q, session, user_message_id, user_message_content, 
                                  session_id, age_group, user_profile, deep_thinking, web_search):
        """
        包含所有异步逻辑的核心函数，包括数据库访问。
        """
        chat_history = await self._get_chat_history_async(session)

        # 1. 发送开始事件
        q.put(f"data: {json.dumps({'type': 'start', 'user_message_id': user_message_id})}\n\n")
        
        response_content = ""
        thinking_content = ""  # 收集思考内容
        thinking_start_time = time.time()  # 记录思考开始时间

        # 2. 运行异步流式任务
        try:
            async for chunk in ai_service.stream_response(
                message=user_message_content,
                age_group=age_group,
                chat_history=chat_history,
                user_profile=user_profile,
                deep_thinking=deep_thinking,
                web_search=web_search
            ):
                if chunk is not None and isinstance(chunk, str):
                    # 检查是否是思考过程
                    if chunk.startswith('<thinking>') and chunk.endswith('</thinking>'):
                        # 提取思考内容
                        thinking_chunk = chunk[10:-11]  # 移除<thinking>标签
                        thinking_content += thinking_chunk
                        q.put(f"data: {json.dumps({'type': 'thinking', 'content': thinking_chunk})}\n\n")
                    else:
                        # 普通内容
                        response_content += chunk
                        q.put(f"data: {json.dumps({'type': 'chunk', 'content': chunk})}\n\n")
        except Exception as stream_error:
            logger.error(f"流式响应处理错误: {stream_error}")
            q.put(f"data: {json.dumps({'type': 'error', 'message': '流式响应处理失败'})}\n\n")
            return

        # 3. 异步保存完整的AI回复到数据库（包含思考内容）
        # 计算思考时间
        thinking_time = 0
        if thinking_content:
            thinking_time = int((time.time() - thinking_start_time))
        
        ai_message = await self._create_ai_message_async(session, response_content, thinking_content, thinking_time)
        
        # 4. 发送完成事件
        q.put(f"data: {json.dumps({'type': 'complete', 'ai_message_id': str(ai_message.id), 'session_id': session_id})}\n\n")

    @sync_to_async
    def _get_chat_history_async(self, session, limit=10):
        """获取聊天历史的异步版本"""
        return self._get_chat_history(session, limit)

    @sync_to_async
    def _create_ai_message_async(self, session, response_content, thinking_content="", thinking_time=0):
        """创建AI消息的异步版本"""
        with transaction.atomic():
            # 解析情绪数据（如果存在）
            final_content = response_content
            emotion_data = None
            crisis_level = 0
            
            if '|||' in response_content:
                parts = response_content.split('|||')
                final_content = parts[0].strip()
                emotion_json_string = parts[1]
                
                try:
                    # 提取纯JSON（移除markdown标记）
                    first_brace = emotion_json_string.find('{')
                    last_brace = emotion_json_string.rfind('}')
                    
                    if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
                        json_string = emotion_json_string[first_brace:last_brace + 1]
                        emotion_data = json.loads(json_string)
                        logger.info(f"成功解析情绪数据: {emotion_data}")
                        
                        # 提取危机等级
                        crisis_level = int(emotion_data.get('crisis_level', 0))
                        
                        # 如果检测到高危机等级，记录危机标记
                        if crisis_level >= 2:
                            logger.warning(f"🚨 检测到危机事件 - 等级{crisis_level}: {session.user.username}")
                except Exception as e:
                    logger.error(f"解析情绪数据失败: {e}")
            
            # 创建消息对象
            message = ChatMessage.objects.create(
                session=session,
                content=final_content,  # 保存纯净的内容（不含情绪JSON）
                message_type=ChatMessage.MessageType.TEXT,
                sender_type=ChatMessage.SenderType.AI,
                ai_model='deepseek-chat',
                emotion_data=emotion_data,  # 保存情绪数据
                crisis_detected=(crisis_level >= 2)  # 标记危机消息
            )
            
            # 如果检测到高度危机，标记会话为紧急状态
            if crisis_level >= 3:
                session.is_emergency = True
                session.save(update_fields=['is_emergency'])
            
            # 构建metadata
            metadata = {}
            
            # 如果有思考内容，添加到metadata
            if thinking_content:
                metadata['thinking_content'] = thinking_content
                metadata['thinking_time'] = thinking_time
                metadata['has_thinking'] = True
            
            # 如果有情绪数据，也添加到metadata（方便前端访问）
            if emotion_data:
                metadata['emotion_analysis'] = emotion_data
                metadata['crisis_level'] = crisis_level
            
            if metadata:
                message.metadata = metadata
                message.save()
            
            return message

    def _get_chat_history(self, session, limit=10):
        """获取聊天历史"""
        messages = ChatMessage.objects.filter(
            session=session
        ).order_by('-created_at')[:limit]
        
        history = []
        for msg in reversed(messages):
            history.append({
                'role': 'user' if msg.sender_type == ChatMessage.SenderType.USER else 'assistant',
                'content': msg.content,
                'timestamp': msg.created_at.isoformat()
            })
        
        return history


class VoiceMessageView(APIView):
    """
    语音消息处理视图
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        if 'audio' not in request.FILES:
            return error_response(
                message="请上传语音文件",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        audio_file = request.FILES['audio']
        session_id = request.data.get('session_id')
        
        # 验证文件大小
        if audio_file.size > 10 * 1024 * 1024:  # 10MB限制
            return error_response(
                message="语音文件过大",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # 获取或创建会话
            if session_id:
                session = ChatSession.objects.get(
                    id=session_id,
                    user=request.user
                )
            else:
                session = ChatSession.objects.create(
                    user=request.user,
                    title="语音对话"
                )
            
            # 语音转文字（暂时使用模拟实现）
            # TODO: 实现真实的语音识别服务
            transcription_result = {
                'success': True,
                'text': '模拟语音识别结果',
                'confidence': 0.8,
                'duration': 5.0
            }
            
            if not transcription_result['success']:
                return error_response(
                    message="语音识别失败",
                    status_code=status.HTTP_400_BAD_REQUEST
                )
            
            text_content = transcription_result['text']
            
            # 创建语音消息
            voice_message = ChatMessage.objects.create(
                session=session,
                content=text_content,
                message_type=ChatMessage.MessageType.AUDIO,
                sender_type=ChatMessage.SenderType.USER,
                audio_file=audio_file,
                metadata={
                    'transcription_confidence': transcription_result.get('confidence', 0),
                    'audio_duration': transcription_result.get('duration', 0)
                }
            )
            
            # 情绪分析（语音）
            # emotion_service = EmotionAnalysisService()
            
            # 文本情绪分析
            # text_emotion = emotion_service.analyze_text(text_content)
            # 使用模拟数据
            text_emotion = {'emotion': 'neutral', 'confidence': 0.5}
            
            # 语音情绪分析
            # voice_emotion = emotion_service.analyze_voice(audio_file)
            voice_emotion = {'emotion': 'neutral', 'confidence': 0.5}
            
            # 合并情绪结果
            # combined_emotion = emotion_service.combine_emotion_results(
            #     text_emotion, voice_emotion
            # )
            combined_emotion = text_emotion
            
            if combined_emotion:
                voice_message.emotion_data = combined_emotion
                voice_message.save()
                
                # 记录情绪日志
                # emotion_service.create_emotion_log(
                #     user=request.user,
                #     message=voice_message,
                #     emotion_data=combined_emotion,
                #     analysis_source='voice'
                # )
            
            return success_response(
                message="语音消息处理成功",
                data={
                    'message': ChatMessageSerializer(voice_message).data,
                    'transcription': text_content,
                    'session_id': str(session.id)
                }
            )
            
        except Exception as e:
            logger.error(f"语音消息处理失败: {str(e)}")
            return error_response(
                message="语音消息处理失败",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ChatFeedbackView(APIView):
    """
    聊天反馈视图
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = ChatFeedbackCreateSerializer(data=request.data, context={'request': request})
        
        if not serializer.is_valid():
            return error_response(
                message="反馈验证失败",
                data=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            feedback = serializer.save()
            
            return success_response(
                message="反馈提交成功",
                data=ChatFeedbackSerializer(feedback).data
            )
            
        except Exception as e:
            logger.error(f"提交反馈失败: {str(e)}")
            return error_response(
                message="反馈提交失败",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def get(self, request):
        """获取用户的反馈列表"""
        try:
            message_id = request.GET.get('message_id')
            
            if message_id:
                # 获取特定消息的反馈
                try:
                    feedback = ChatFeedback.objects.get(
                        user=request.user,
                        message__id=message_id
                    )
                    return success_response(
                        message="反馈获取成功",
                        data=ChatFeedbackSerializer(feedback).data
                    )
                except ChatFeedback.DoesNotExist:
                    return success_response(
                        message="暂无反馈",
                        data=None
                    )
            else:
                # 获取用户的所有反馈
                feedbacks = ChatFeedback.objects.filter(
                    user=request.user
                ).order_by('-created_at')[:50]  # 限制返回数量
                
                serializer = ChatFeedbackSerializer(feedbacks, many=True)
                return success_response(
                    message="反馈列表获取成功",
                    data=serializer.data
                )
                
        except Exception as e:
            logger.error(f"获取反馈失败: {str(e)}")
            return error_response(
                message="获取反馈失败",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def report_crisis(request):
    """
    报告危机事件
    """
    try:
        content = request.data.get('content', '')
        keywords = request.data.get('keywords', [])
        session_id = request.data.get('session_id')
        
        # 记录危机事件
        logger.critical(f"🚨🚨🚨 危机事件报告 - 用户: {request.user.username}, 内容: {content}, 关键词: {keywords}")
        
        # 如果有会话ID，标记会话为紧急状态
        if session_id:
            try:
                session = ChatSession.objects.get(id=session_id, user=request.user)
                session.is_emergency = True
                session.save(update_fields=['is_emergency'])
            except ChatSession.DoesNotExist:
                pass
        
        # TODO: 这里可以添加更多处理逻辑
        # 1. 发送邮件通知管理员
        # 2. 发送短信通知紧急联系人
        # 3. 记录到专门的危机事件表
        # 4. 触发自动工单系统
        
        return success_response(
            message="危机事件已记录，请立即寻求专业帮助",
            data={
                'crisis_reported': True,
                'helpline': '400-161-9995'
            }
        )
        
    except Exception as e:
        logger.error(f"记录危机事件失败: {str(e)}")
        return error_response(
            message="记录失败，但请务必立即寻求专业帮助",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def clear_chat_history(request):
    """
    清空聊天记录（需要密码验证和确认语句）
    """
    try:
        # 获取请求数据
        password = request.data.get('password')
        confirm_statement = request.data.get('confirm_statement')
        
        # 验证密码
        if not password:
            return error_response(
                message="密码不能为空",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        # 验证用户密码
        from django.contrib.auth import authenticate
        user = authenticate(username=request.user.username, password=password)
        if not user:
            return error_response(
                message="密码错误",
                status_code=status.HTTP_401_UNAUTHORIZED
            )
        
        # 验证确认语句
        expected_statement = f"我，{request.user.nickname or request.user.username}，确认清空本账户的聊天记录"
        if not confirm_statement or confirm_statement.strip() != expected_statement:
            return error_response(
                message="确认语句不正确",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        # 软删除：归档所有会话
        sessions_updated = ChatSession.objects.filter(
            user=request.user,
            is_archived=False
        ).update(is_archived=True)
        
        logger.info(f"用户 {request.user.username} 清空了 {sessions_updated} 个聊天会话")
        
        return success_response(
            message="聊天记录已清空",
            data={"cleared_sessions": sessions_updated}
        )
        
    except Exception as e:
        logger.error(f"清空聊天记录失败: {str(e)}")
        return error_response(
            message="清空聊天记录失败",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def export_chat_history(request):
    """
    导出聊天记录
    """
    try:
        format_type = request.GET.get('format', 'json')
        
        # 获取用户的所有会话
        sessions = ChatSession.objects.filter(
            user=request.user
        ).prefetch_related('messages')
        
        if format_type == 'json':
            data = []
            for session in sessions:
                session_data = {
                    'id': str(session.id),
                    'title': session.title,
                    'created_at': session.created_at.isoformat(),
                    'messages': []
                }
                
                for message in session.messages.all():
                    message_data = {
                        'content': message.content,
                        'sender': message.get_sender_type_display(),
                        'timestamp': message.created_at.isoformat(),
                        'emotion': message.emotion_data
                    }
                    session_data['messages'].append(message_data)
                
                data.append(session_data)
            
            response = Response(
                data,
                content_type='application/json'
            )
            response['Content-Disposition'] = 'attachment; filename="chat_history.json"'
            
        else:
            return error_response(
                message="不支持的导出格式",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        return response
        
    except Exception as e:
        logger.error(f"导出聊天记录失败: {str(e)}")
        return error_response(
            message="导出聊天记录失败",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# ViewSet classes for URL routing
class ChatSessionViewSet(viewsets.ModelViewSet):
    """聊天会话管理"""
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return ChatSession.objects.filter(user=self.request.user, is_archived=False).order_by('-updated_at')
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ChatSessionCreateSerializer
        return ChatSessionSerializer
    
    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)
        except Exception as e:
            logger.error(f"创建聊天会话失败: {str(e)}")
            raise
    
    def list(self, request, *args, **kwargs):
        """重写list方法确保返回正确的响应格式"""
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            
            return success_response(
                message="聊天会话列表获取成功",
                data=serializer.data,
                status_code=status.HTTP_200_OK
            )
        except Exception as e:
            logger.error(f"获取聊天会话列表失败: {str(e)}")
            return error_response(
                message="获取聊天会话列表失败",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def create(self, request, *args, **kwargs):
        """重写create方法确保返回正确的响应格式"""
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            
            # 返回完整的会话信息
            session = serializer.instance
            response_serializer = ChatSessionSerializer(session)
            
            return success_response(
                message="聊天会话创建成功",
                data=response_serializer.data,
                status_code=status.HTTP_201_CREATED
            )
        except Exception as e:
            logger.error(f"创建聊天会话失败: {str(e)}")
            return error_response(
                message="创建聊天会话失败",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ChatMessageViewSet(viewsets.ModelViewSet):
    """聊天消息管理"""
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return ChatMessage.objects.filter(session__user=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ChatMessageCreateSerializer
        return ChatMessageSerializer
    
    def perform_create(self, serializer):
        # 验证session是否属于当前用户
        session_id = serializer.validated_data.get('session_id')
        session = get_object_or_404(ChatSession, id=session_id, user=self.request.user)
        serializer.save(session=session)
