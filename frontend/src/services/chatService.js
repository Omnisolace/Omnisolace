/**
 * 聊天服务
 * 集成真实的后端API调用
 */

import { chatApi, emotionApi } from '@/utils/api'

export class ChatService {
  constructor() {
    this.currentSessionId = null
  }

  /**
   * 创建新的聊天会话
   */
  async createSession(title = '新的对话', summary = '') {
    try {
      const response = await chatApi.createSession({
        title,
        summary
      })
      
      if (response.data && response.data.data) {
        this.currentSessionId = response.data.data.id
        return response.data.data
      }
      
      throw new Error('创建会话失败：响应数据格式错误')
    } catch (error) {
      console.error('创建聊天会话失败:', error)
      throw error
    }
  }

  /**
   * 获取会话列表
   */
  async getSessions() {
    try {
      const response = await chatApi.getSessions()
      
      if (response.data && response.data.data) {
        return response.data.data
      }
      
      return []
    } catch (error) {
      console.error('获取会话列表失败:', error)
      throw error
    }
  }

  /**
   * 发送消息
   */
  async sendMessage(content, messageType = 'text', sessionId = null) {
    try {
      const messageData = {
        content,
        message_type: messageType,
        session_id: sessionId || this.currentSessionId
      }

      const response = await chatApi.sendMessage(messageData)
      
      if (response.data && response.data.data) {
        const data = response.data.data
        
        // 更新当前会话ID（如果创建了新会话）
        if (data.session_id && !this.currentSessionId) {
          this.currentSessionId = data.session_id
        }
        
        return {
          userMessage: data.user_message,
          aiMessage: data.ai_message,
          sessionId: data.session_id,
          crisisDetected: data.crisis_detected || false
        }
      }
      
      throw new Error('发送消息失败：响应数据格式错误')
    } catch (error) {
      console.error('发送消息失败:', error)
      throw error
    }
  }

  /**
   * 发送消息（流式响应）
   */
  async sendMessageStream(content, messageType = 'text', sessionId = null, onChunk = null, onComplete = null, onError = null, options = {}) {
    try {
      const messageData = {
        content,
        message_type: messageType,
        session_id: sessionId || this.currentSessionId,
        deep_thinking: options.deep_thinking || false,
        web_search: options.web_search || false
      }

      // 在开发环境中，VITE_API_BASE_URL 通常未设置，我们依赖 vite.config.js 中的代理配置。
      // 代理配置监听 '/api' 路径。因此，我们需要确保这里的 baseURL 默认为 '/api'，
      // 与项目中 axios 实例的配置保持一致。
      const baseUrl = import.meta.env.VITE_API_BASE_URL || '/api';
      const url = `${baseUrl}/v1/chat/send/`;

      // 使用fetch API支持流式响应
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
          'Accept': 'text/event-stream'
        },
        body: JSON.stringify(messageData)
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const reader = response.body.getReader()
      const decoder = new TextDecoder()
      let buffer = ''
      let userMessage = null
      let aiMessageContent = ''
      let responseSessionId = null // 重命名变量以避免作用域冲突

      try {
        while (true) {
          const { done, value } = await reader.read()
          if (done) break

          buffer += decoder.decode(value, { stream: true })
          const lines = buffer.split('\n')
          buffer = lines.pop() || ''

          for (const line of lines) {
            if (line.startsWith('data: ')) {
              try {
                const data = JSON.parse(line.slice(6))
                
                switch (data.type) {
                  case 'start':
                    if (onChunk) onChunk({ 
                      type: 'start', 
                      messageId: data.message_id,
                      userMessageId: data.user_message_id 
                    })
                    break
                  case 'chunk':
                    aiMessageContent += data.content
                    if (onChunk) onChunk({ type: 'chunk', content: data.content })
                    break
                  case 'thinking':
                    // 处理思考过程
                    if (onChunk) onChunk({ type: 'thinking', content: data.content })
                    break
                  case 'complete':
                    responseSessionId = data.session_id // 使用重命名后的变量
                    if (onComplete) onComplete({ 
                      type: 'complete', 
                      messageId: data.ai_message_id || data.message_id, // 兼容两种字段名
                      sessionId: responseSessionId, // 使用重命名后的变量
                      fullContent: aiMessageContent
                    })
                    break
                  case 'error':
                    if (onError) onError({ type: 'error', message: data.message })
                    break
                }
              } catch (e) {
                console.error('解析SSE数据失败:', e)
              }
            }
          }
        }
      } finally {
        reader.releaseLock()
      }

      // 更新当前会话ID
      if (responseSessionId && !this.currentSessionId) {
        this.currentSessionId = responseSessionId
      }

      return {
        sessionId: responseSessionId,
        fullContent: aiMessageContent
      }
    } catch (error) {
      console.error('发送流式消息失败:', error)
      if (onError) onError({ type: 'error', message: error.message })
      throw error
    }
  }

  /**
   * 获取会话消息历史
   */
  async getSessionMessages(sessionId) {
    try {
      const response = await chatApi.getSessionMessages(sessionId)
      
      if (response.data && response.data.data) {
        return response.data.data.messages || []
      }
      
      return []
    } catch (error) {
      console.error('获取消息历史失败:', error)
      throw error
    }
  }

  /**
   * 分析情绪
   */
  async analyzeEmotion(text, context = '') {
    try {
      const response = await emotionApi.analyzeText({
        text,
        context
      })
      
      if (response.data && response.data.data) {
        return response.data.data
      }
      
      return null
    } catch (error) {
      console.error('情绪分析失败:', error)
      return null
    }
  }

  /**
   * 获取情绪历史
   */
  async getEmotionHistory(params = {}) {
    try {
      const response = await emotionApi.getEmotionHistory(params)
      
      if (response.data && response.data.data) {
        return response.data.data
      }
      
      return []
    } catch (error) {
      console.error('获取情绪历史失败:', error)
      return []
    }
  }

  /**
   * 删除会话
   */
  async deleteSession(sessionId) {
    try {
      await chatApi.deleteSession(sessionId)
      
      // 如果删除的是当前会话，清空当前会话ID
      if (this.currentSessionId === sessionId) {
        this.currentSessionId = null
      }
      
      return true
    } catch (error) {
      console.error('删除会话失败:', error)
      throw error
    }
  }

  /**
   * 设置当前会话ID
   */
  setCurrentSessionId(sessionId) {
    this.currentSessionId = sessionId
  }

  /**
   * 获取当前会话ID
   */
  getCurrentSessionId() {
    return this.currentSessionId
  }

  /**
   * 清空当前会话
   */
  clearCurrentSession() {
    this.currentSessionId = null
  }
}

// 创建单例实例
export const chatService = new ChatService()
export default chatService
