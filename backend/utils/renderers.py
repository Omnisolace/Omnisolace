"""
自定义渲染器
"""
from rest_framework.renderers import BaseRenderer

class ServerSentEventRenderer(BaseRenderer):
    """
    用于服务器发送事件 (SSE) 的渲染器。
    """
    media_type = 'text/event-stream'
    format = 'sse'
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        直接返回数据，因为数据应该已经是格式化好的SSE字符串。
        """
        return data
