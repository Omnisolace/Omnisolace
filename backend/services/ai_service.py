"""
AI服务类 - 集成DeepSeek API
"""
import os
import json
import logging
import asyncio
import aiohttp
from typing import List, Dict, Any, AsyncGenerator, Optional
from django.conf import settings

logger = logging.getLogger(__name__)


class DeepSeekAIService:
    """DeepSeek AI服务类"""
    
    def __init__(self):
        self.api_key = os.getenv('DEEPSEEK_API_KEY', '')
        self.base_url = "https://api.deepseek.com/v1"
        self.model = "deepseek-chat"  # 默认模型
        self.r1_model = "deepseek-reasoner"  # R1深度思考模型
        
        if not self.api_key:
            logger.warning("DeepSeek API密钥未配置")
    
    def _get_headers(self) -> Dict[str, str]:
        """获取请求头"""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def _build_messages(self, user_message: str, chat_history: List[Dict], age_group: str) -> List[Dict]:
        """构建消息列表"""
        messages = []
        
        # 添加系统提示词（根据年龄段定制）
        system_prompt = self._get_system_prompt(age_group)
        messages.append({
            "role": "system",
            "content": system_prompt
        })
        
        # 添加聊天历史
        for msg in chat_history[-10:]:  # 只保留最近10条消息
            messages.append({
                "role": msg.get("role", "user"),
                "content": msg.get("content", "")
            })
        
        # 添加当前用户消息
        messages.append({
            "role": "user",
            "content": user_message
        })
        
        # 添加用于情绪分析的附加指令
        emotion_analysis_prompt = """

---
你的任务：
1. 像心理伙伴一样，正常地、共情地回答用户的上述问题。
2. 在你的回答内容结束后，请另起一行，并附加一个特殊的分隔符 `|||`。
3. 在分隔符后面，提供一个 JSON 对象，包含对用户问题的分析。JSON 结构必须如下：
```json
{
  "emotion_words": ["焦虑", "疲惫"],
  "emotion_score": -7,
  "suggestions": [
    "尝试正念冥想，每天安排10分钟的独处时间。",
    "将大的工作任务分解成小的、可执行的步骤。",
    "下班后进行半小时的散步或慢跑，帮助释放压力。"
  ]
}
```
**请注意：** `emotion_score` 是一个在 -10 (极度负面) 到 +10 (极度正面) 之间的整数。`emotion_words` 必须是1到2个描述性词语。`suggestions` 必须是3条简短实用的建议。确保JSON格式正确无误。
"""
        # 将附加指令附加到用户消息内容的末尾
        if len(messages) > 0 and messages[-1]["role"] == "user":
            messages[-1]["content"] += emotion_analysis_prompt
        
        return messages
    
    def _get_system_prompt(self, age_group: str) -> str:
        """根据年龄段获取系统提示词"""
        prompts = {
            "teen": """你是一位专业的心理咨询师，专门为青少年提供心理支持。请用温和、理解的语言与用户交流，帮助他们处理学习压力、人际关系、情绪困扰等问题。保持积极正面的态度，提供实用的建议和情感支持。""",
            
            "young": """你是一位专业的心理咨询师，专门为年轻人提供心理支持。请用专业而亲切的语言与用户交流，帮助他们处理工作压力、情感问题、职业规划、焦虑抑郁等心理困扰。提供实用的建议和情感支持。""",
            
            "middle": """你是一位专业的心理咨询师，专门为中年人提供心理支持。请用成熟、理解的语言与用户交流，帮助他们处理家庭关系、工作压力、健康担忧、中年危机等问题。提供实用的建议和情感支持。""",
            
            "elder": """你是一位专业的心理咨询师，专门为老年人提供心理支持。请用耐心、温暖的语言与用户交流，帮助他们处理孤独感、健康担忧、家庭关系、适应退休生活等问题。提供实用的建议和情感支持。"""
        }
        
        return prompts.get(age_group, prompts["young"])
    
    
    async def generate_response(
        self, 
        message: str, 
        age_group: str = "young",
        chat_history: List[Dict] = None,
        user_profile: Dict = None,
        deep_thinking: bool = False,
        web_search: bool = False
    ) -> str:
        """生成AI回复"""
        if not self.api_key:
            return "抱歉，AI服务暂时不可用，请稍后再试。"
        
        try:
            messages = self._build_messages(message, chat_history or [], age_group)
            
            # 根据深度思考模式选择模型
            model_to_use = self.r1_model if deep_thinking else self.model
            
            # 构建基础payload
            payload = {
                "model": model_to_use,
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 2000,
                "stream": False
            }
            
            # 如果是R1模型，添加特殊参数
            if deep_thinking:
                payload["reasoning"] = True
                payload["max_tokens"] = 4000  # R1模型需要更多token
            
            # 如果启用联网搜索，在系统提示词中添加搜索指令
            if web_search:
                search_instruction = "\n\n请根据用户的问题，如果需要最新信息或具体数据，请明确说明需要搜索相关信息。"
                if messages and messages[0]["role"] == "system":
                    messages[0]["content"] += search_instruction
                else:
                    messages.insert(0, {
                        "role": "system", 
                        "content": "你是一位专业的心理咨询师。" + search_instruction
                    })
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/chat/completions",
                    headers=self._get_headers(),
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data["choices"][0]["message"]["content"]
                    else:
                        error_text = await response.text()
                        logger.error(f"DeepSeek API错误: {response.status} - {error_text}")
                        return "抱歉，AI服务暂时遇到问题，请稍后再试。"
                        
        except asyncio.TimeoutError:
            logger.error("DeepSeek API请求超时")
            return "抱歉，AI服务响应超时，请稍后再试。"
        except Exception as e:
            logger.error(f"DeepSeek API调用失败: {str(e)}")
            return "抱歉，AI服务暂时不可用，请稍后再试。"
    
    async def stream_response(
        self, 
        message: str, 
        age_group: str = "young",
        chat_history: List[Dict] = None,
        user_profile: Dict = None,
        deep_thinking: bool = False,
        web_search: bool = False
    ) -> AsyncGenerator[str, None]:
        """流式生成AI回复"""
        if not self.api_key:
            yield "抱歉，AI服务暂时不可用，请稍后再试。"
            return
        
        try:
            messages = self._build_messages(message, chat_history or [], age_group)
            
            # 根据深度思考模式选择模型
            model_to_use = self.r1_model if deep_thinking else self.model
            logger.info(f"流式响应使用模型: {model_to_use}, 深度思考: {deep_thinking}, 联网搜索: {web_search}")
            if deep_thinking:
                logger.info("启用R1模型深度思考模式，将解析reasoning_content字段")
            
            # 构建基础payload
            payload = {
                "model": model_to_use,
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 2000,
                "stream": True
            }
            
            # 如果是R1模型，添加特殊参数
            if deep_thinking:
                payload["reasoning"] = True
                payload["max_tokens"] = 4000  # R1模型需要更多token
            
            # 如果启用联网搜索，在系统提示词中添加搜索指令
            if web_search:
                search_instruction = "\n\n请根据用户的问题，如果需要最新信息或具体数据，请明确说明需要搜索相关信息。"
                if messages and messages[0]["role"] == "system":
                    messages[0]["content"] += search_instruction
                else:
                    messages.insert(0, {
                        "role": "system", 
                        "content": "你是一位专业的心理咨询师。" + search_instruction
                    })
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/chat/completions",
                    headers=self._get_headers(),
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=60)
                ) as response:
                    if response.status == 200:
                        async for line in response.content:
                            if line:
                                try:
                                    line_str = line.decode('utf-8').strip()
                                    if line_str.startswith('data: '):
                                        data_str = line_str[6:]
                                        if data_str == '[DONE]':
                                            break
                                        try:
                                            data = json.loads(data_str)
                                            if 'choices' in data and len(data['choices']) > 0:
                                                choice = data['choices'][0]
                                                delta = choice.get('delta', {})
                                                
                                                # 调试日志：查看完整的delta结构
                                                if deep_thinking and delta:
                                                    logger.debug(f"R1模型delta结构: {list(delta.keys())}")
                                                
                                                # 检查是否有reasoning_content字段（R1模型的思考过程）
                                                if 'reasoning_content' in delta and delta['reasoning_content'] is not None:
                                                    reasoning_content = str(delta['reasoning_content'])
                                                    if reasoning_content.strip():
                                                        logger.debug(f"收到思考内容: {reasoning_content[:100]}...")
                                                        yield f"<thinking>{reasoning_content}</thinking>"
                                                
                                                # 处理普通内容
                                                if 'content' in delta and delta['content'] is not None:
                                                    content = str(delta['content'])
                                                    if content.strip():
                                                        yield content
                                        except json.JSONDecodeError:
                                            continue
                                except Exception as decode_error:
                                    logger.warning(f"解码流式响应行失败: {decode_error}")
                                    continue
                    else:
                        error_text = await response.text()
                        logger.error(f"DeepSeek API流式错误: {response.status} - {error_text}")
                        yield "抱歉，AI服务暂时遇到问题，请稍后再试。"
                        
        except asyncio.TimeoutError:
            logger.error("DeepSeek API流式请求超时")
            yield "抱歉，AI服务响应超时，请稍后再试。"
        except Exception as e:
            logger.error(f"DeepSeek API流式调用失败: {str(e)}")
            yield "抱歉，AI服务暂时不可用，请稍后再试。"
        finally:
            # 确保生成器正常结束
            pass
    
    def analyze_emotion(self, text: str) -> Dict[str, Any]:
        """分析文本情绪（此方法已弃用，功能合并到主AI响应中）"""
        logger.warning("analyze_emotion 方法已被弃用，情绪分析功能已集成到 stream_response 和 generate_response 中。")
        return {
            'emotion': 'neutral',
            'confidence': 0.5,
            'scores': {}
        }


# 创建全局实例
ai_service = DeepSeekAIService()
