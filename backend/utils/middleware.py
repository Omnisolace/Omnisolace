"""
安全中间件
"""
from django.http import JsonResponse
from django.core.cache import cache
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model
import logging
import re
import json
from datetime import timedelta

User = get_user_model()
logger = logging.getLogger(__name__)


class RateLimitMiddleware:
    """
    限流中间件
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
        # 限流配置
        self.rate_limits = getattr(settings, 'RATE_LIMIT_SETTINGS', {
            'USER_CHAT_LIMIT': '100/h',
            'USER_GLOBAL_LIMIT': '200/h',
            'IP_LIMIT': '1000/h',
        })
    
    def __call__(self, request):
        # 检查限流
        if self._should_apply_rate_limit(request):
            rate_limit_result = self._check_rate_limit(request)
            if not rate_limit_result['allowed']:
                return JsonResponse({
                    'code': 429,
                    'message': '请求过于频繁，请稍后再试',
                    'data': {
                        'retry_after': rate_limit_result['retry_after']
                    }
                }, status=429)
        
        response = self.get_response(request)
        
        # 记录成功的请求
        if self._should_apply_rate_limit(request) and response.status_code < 400:
            self._record_request(request)
        
        return response
    
    def _should_apply_rate_limit(self, request):
        """判断是否需要应用限流"""
        # 跳过静态文件和管理员接口
        skip_paths = ['/admin/', '/static/', '/media/', '/health/']
        for path in skip_paths:
            if request.path.startswith(path):
                return False
        
        # 只对API接口应用限流
        return request.path.startswith('/api/')
    
    def _check_rate_limit(self, request):
        """检查限流"""
        user_id = getattr(request.user, 'id', None) if request.user.is_authenticated else None
        ip_address = self._get_client_ip(request)
        
        # 检查用户限流
        if user_id:
            # 检查聊天API专门限流
            if '/api/v1/chat/' in request.path:
                user_chat_key = f"rate_limit_user_chat_{user_id}"
                if not self._check_limit(user_chat_key, self.rate_limits['USER_CHAT_LIMIT']):
                    return {'allowed': False, 'retry_after': 3600}
            
            # 检查用户全局限流
            user_global_key = f"rate_limit_user_global_{user_id}"
            if not self._check_limit(user_global_key, self.rate_limits['USER_GLOBAL_LIMIT']):
                return {'allowed': False, 'retry_after': 3600}
        
        # 检查IP限流
        ip_key = f"rate_limit_ip_{ip_address}"
        if not self._check_limit(ip_key, self.rate_limits['IP_LIMIT']):
            return {'allowed': False, 'retry_after': 3600}
        
        return {'allowed': True, 'retry_after': 0}
    
    def _check_limit(self, key, limit_str):
        """检查特定键的限流"""
        try:
            # 解析限流配置 (如 "100/h")
            count, period = limit_str.split('/')
            count = int(count)
            
            period_seconds = {
                's': 1,
                'm': 60,
                'h': 3600,
                'd': 86400
            }.get(period, 3600)
            
            current_count = cache.get(key, 0)
            return current_count < count
        except Exception as e:
            # Redis不可用时，允许请求通过
            logger.warning(f"限流检查失败，允许请求通过: {str(e)}")
            return True
    
    def _record_request(self, request):
        """记录请求"""
        user_id = getattr(request.user, 'id', None) if request.user.is_authenticated else None
        ip_address = self._get_client_ip(request)
        
        # 记录用户请求
        if user_id:
            if '/api/v1/chat/' in request.path:
                user_chat_key = f"rate_limit_user_chat_{user_id}"
                self._increment_counter(user_chat_key, 3600)
            
            user_global_key = f"rate_limit_user_global_{user_id}"
            self._increment_counter(user_global_key, 3600)
        
        # 记录IP请求
        ip_key = f"rate_limit_ip_{ip_address}"
        self._increment_counter(ip_key, 3600)
    
    def _increment_counter(self, key, timeout):
        """增加计数器"""
        try:
            current = cache.get(key, 0)
            cache.set(key, current + 1, timeout)
        except Exception as e:
            # Redis不可用时，忽略计数更新
            logger.warning(f"限流计数器更新失败，忽略计数: {str(e)}")
    
    def _get_client_ip(self, request):
        """获取客户端IP"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR', '0.0.0.0')
        return ip


class CrisisDetectionMiddleware:
    """
    危机检测中间件
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
        # 危机关键词
        self.crisis_keywords = getattr(settings, 'CRISIS_KEYWORDS', [
            '想死', '自杀', '结束生命', '不想活', '活着没意思',
            '自伤', '自残', '伤害自己', '想消失', '解脱',
            '死了算了', '生无可恋', '轻生', '寻死', '自尽'
        ])
        
        # 编译正则表达式
        self.crisis_patterns = [re.compile(keyword) for keyword in self.crisis_keywords]
    
    def __call__(self, request):
        # 预处理请求
        if self._should_check_crisis(request):
            crisis_result = self._detect_crisis_in_request(request)
            if crisis_result['detected']:
                # 记录危机检测日志
                self._log_crisis_detection(request, crisis_result)
                
                # 如果是高风险，可以考虑阻断请求
                if crisis_result['risk_level'] >= 4:
                    logger.critical(f"检测到高风险危机内容: {crisis_result}")
        
        response = self.get_response(request)
        return response
    
    def _should_check_crisis(self, request):
        """判断是否需要检查危机"""
        # 只检查聊天相关的API
        crisis_check_paths = ['/api/v1/chat/']
        return any(request.path.startswith(path) for path in crisis_check_paths)
    
    def _detect_crisis_in_request(self, request):
        """检测请求中的危机内容"""
        crisis_result = {
            'detected': False,
            'keywords': [],
            'risk_level': 0,
            'content': ''
        }
        
        # 检查POST请求的内容
        if request.method == 'POST':
            try:
                if hasattr(request, 'body') and request.body:
                    if request.content_type == 'application/json':
                        data = json.loads(request.body.decode('utf-8'))
                        content = data.get('content', '')
                    else:
                        content = request.POST.get('content', '')
                    
                    if content:
                        crisis_result = self._analyze_content_for_crisis(content)
                        
            except Exception as e:
                logger.error(f"危机检测解析请求失败: {str(e)}")
        
        return crisis_result
    
    def _analyze_content_for_crisis(self, content):
        """分析内容中的危机信号"""
        detected_keywords = []
        risk_level = 0
        
        for keyword in self.crisis_keywords:
            if keyword in content:
                detected_keywords.append(keyword)
                
                # 根据关键词严重程度计算风险等级
                if keyword in ['自杀', '想死', '轻生', '寻死', '自尽']:
                    risk_level = max(risk_level, 5)  # 最高风险
                elif keyword in ['结束生命', '不想活', '死了算了', '生无可恋']:
                    risk_level = max(risk_level, 4)  # 高风险
                elif keyword in ['自伤', '自残', '伤害自己']:
                    risk_level = max(risk_level, 3)  # 中等风险
                else:
                    risk_level = max(risk_level, 2)  # 低风险
        
        return {
            'detected': len(detected_keywords) > 0,
            'keywords': detected_keywords,
            'risk_level': risk_level,
            'content': content
        }
    
    def _log_crisis_detection(self, request, crisis_result):
        """记录危机检测日志"""
        user_info = "anonymous"
        if request.user.is_authenticated:
            user_info = f"user_{request.user.id}"
        
        logger.warning(
            f"危机检测报警 - 用户: {user_info}, "
            f"风险等级: {crisis_result['risk_level']}, "
            f"关键词: {crisis_result['keywords']}, "
            f"IP: {self._get_client_ip(request)}"
        )
        
        # 可以在这里添加发送报警通知的逻辑
        if crisis_result['risk_level'] >= 4:
            self._send_crisis_alert(request, crisis_result)
    
    def _send_crisis_alert(self, request, crisis_result):
        """发送危机报警"""
        # 这里可以集成短信、邮件或其他报警系统
        logger.critical(f"发送危机报警: {crisis_result}")
    
    def _get_client_ip(self, request):
        """获取客户端IP"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR', '0.0.0.0')
        return ip


class ParentalControlMiddleware:
    """
    家长监督中间件
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
        # 家长监督配置
        self.parental_features = getattr(settings, 'PARENTAL_CONTROL_FEATURES', {
            'REQUIRE_CONSENT': True,
            'ACTIVITY_SUMMARY': True,
            'CONTENT_FILTER': True,
            'TIME_LIMITS': True,
        })
    
    def __call__(self, request):
        # 检查青少年用户的家长监督
        if self._should_apply_parental_control(request):
            parental_result = self._check_parental_control(request)
            if not parental_result['allowed']:
                return JsonResponse({
                    'code': 403,
                    'message': parental_result['message'],
                    'data': {
                        'parental_control': True,
                        'reason': parental_result['reason']
                    }
                }, status=403)
        
        response = self.get_response(request)
        
        # 记录青少年用户活动
        if self._should_log_activity(request):
            self._log_teen_activity(request, response)
        
        return response
    
    def _should_apply_parental_control(self, request):
        """判断是否需要应用家长监督"""
        if not request.user.is_authenticated:
            return False
        
        return (
            request.user.age_group == User.AgeGroup.TEEN and
            request.path.startswith('/api/')
        )
    
    def _check_parental_control(self, request):
        """检查家长监督规则"""
        user = request.user
        
        # 检查家长同意
        if self.parental_features.get('REQUIRE_CONSENT') and not user.parental_consent:
            return {
                'allowed': False,
                'message': '需要家长同意才能使用此服务',
                'reason': 'no_consent'
            }
        
        # 检查时间限制（如果启用）
        if self.parental_features.get('TIME_LIMITS'):
            time_limit_result = self._check_time_limits(user)
            if not time_limit_result['allowed']:
                return time_limit_result
        
        return {'allowed': True}
    
    def _check_time_limits(self, user):
        """检查时间限制"""
        # 这里可以实现具体的时间限制逻辑
        # 比如每天使用时长限制、使用时间段限制等
        
        # 示例：检查每日使用时长
        today = timezone.now().date()
        daily_usage_key = f"teen_daily_usage_{user.id}_{today}"
        daily_usage = cache.get(daily_usage_key, 0)  # 分钟
        
        max_daily_usage = 120  # 2小时
        
        if daily_usage >= max_daily_usage:
            return {
                'allowed': False,
                'message': '今日使用时长已达上限，请明天再使用',
                'reason': 'daily_limit_exceeded'
            }
        
        return {'allowed': True}
    
    def _should_log_activity(self, request):
        """判断是否需要记录活动"""
        if not request.user.is_authenticated:
            return False
        
        return (
            request.user.age_group == User.AgeGroup.TEEN and
            request.user.parental_mode and
            request.path.startswith('/api/')
        )
    
    def _log_teen_activity(self, request, response):
        """记录青少年用户活动"""
        try:
            user = request.user
            
            # 记录活动摘要
            activity_data = {
                'timestamp': timezone.now().isoformat(),
                'path': request.path,
                'method': request.method,
                'status_code': response.status_code,
                'ip': self._get_client_ip(request)
            }
            
            # 存储到缓存中，定期汇总发送给家长
            activity_key = f"teen_activity_{user.id}_{timezone.now().date()}"
            activities = cache.get(activity_key, [])
            activities.append(activity_data)
            
            # 只保留最近100条活动记录
            if len(activities) > 100:
                activities = activities[-100:]
            
            cache.set(activity_key, activities, 86400)  # 保存24小时
            
            # 更新使用时长
            if request.path.startswith('/api/v1/chat/'):
                daily_usage_key = f"teen_daily_usage_{user.id}_{timezone.now().date()}"
                daily_usage = cache.get(daily_usage_key, 0)
                cache.set(daily_usage_key, daily_usage + 1, 86400)  # 增加1分钟
            
        except Exception as e:
            logger.error(f"记录青少年活动失败: {str(e)}")
    
    def _get_client_ip(self, request):
        """获取客户端IP"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR', '0.0.0.0')
        return ip


class SecurityHeadersMiddleware:
    """
    安全头中间件
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # 添加安全头
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # 只在HTTPS环境下添加HSTS头
        if request.is_secure():
            response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        
        # 添加内容安全策略（根据需要调整）
        response['Content-Security-Policy'] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self'; "
            "connect-src 'self'; "
            "frame-ancestors 'none';"
        )
        
        return response


class RequestLoggingMiddleware:
    """
    请求日志中间件
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        start_time = timezone.now()
        
        # 记录请求信息
        request_info = {
            'method': request.method,
            'path': request.path,
            'user': str(request.user) if request.user.is_authenticated else 'anonymous',
            'ip': self._get_client_ip(request),
            'user_agent': request.META.get('HTTP_USER_AGENT', '')[:200],
            'timestamp': start_time.isoformat()
        }
        
        response = self.get_response(request)
        
        # 计算处理时间
        end_time = timezone.now()
        processing_time = (end_time - start_time).total_seconds()
        
        # 记录响应信息
        request_info.update({
            'status_code': response.status_code,
            'processing_time': processing_time,
            'response_size': len(getattr(response, 'content', ''))
        })
        
        # 根据状态码选择日志级别
        if response.status_code >= 500:
            logger.error(f"Server Error: {request_info}")
        elif response.status_code >= 400:
            logger.warning(f"Client Error: {request_info}")
        elif processing_time > 5:  # 超过5秒的慢请求
            logger.warning(f"Slow Request: {request_info}")
        else:
            logger.info(f"Request: {request_info}")
        
        return response
    
    def _get_client_ip(self, request):
        """获取客户端IP"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR', '0.0.0.0')
        return ip
