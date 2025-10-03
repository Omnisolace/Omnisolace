import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { chatService } from '@/services/chatService'

export const useChatStore = defineStore('chat', () => {
  // 状态
  const messages = ref([])
  const currentEmotion = ref({
    label: 'neutral',
    score: 50,
    confidence: 0.8,
    timestamp: Date.now()
  })
  const emotionHistory = ref([])
  const isLoading = ref(false)
  const isRecording = ref(false)
  const chatHistory = ref([]) // 历史对话列表
  const currentChatId = ref(null)
  
  // 情绪标签映射
  const emotionLabels = {
    happy: { name: '开心', color: 'text-emotion-happy', bgColor: 'bg-emotion-happy' },
    neutral: { name: '平静', color: 'text-emotion-neutral', bgColor: 'bg-emotion-neutral' },
    sad: { name: '难过', color: 'text-emotion-sad', bgColor: 'bg-emotion-sad' },
    anxious: { name: '焦虑', color: 'text-emotion-anxious', bgColor: 'bg-emotion-anxious' },
    angry: { name: '愤怒', color: 'text-emotion-angry', bgColor: 'bg-emotion-angry' }
  }
  
  // 计算属性
  const currentEmotionLabel = computed(() => {
    return emotionLabels[currentEmotion.value.label] || emotionLabels.neutral
  })
  
  const emotionTrend = computed(() => {
    if (emotionHistory.value.length < 2) return 'stable'
    
    const recent = emotionHistory.value.slice(-5)
    const trend = recent[recent.length - 1].score - recent[0].score
    
    if (trend > 10) return 'improving'
    if (trend < -10) return 'declining'
    return 'stable'
  })
  
  const hasMessages = computed(() => messages.value.length > 0)
  
  // 危机预警关键词
  const crisisKeywords = [
    '想死', '自杀', '结束生命', '不想活', '活着没意思',
    '自伤', '自残', '伤害自己', '想消失', '解脱'
  ]
  
  // 方法
  const addMessage = (message) => {
    const newMessage = {
      id: Date.now() + Math.random(),
      content: message.content,
      type: message.type, // 'user' | 'ai' | 'system'
      timestamp: Date.now(),
      emotion: message.emotion || null,
      audioUrl: message.audioUrl || null
    }
    
    messages.value.push(newMessage)
    
    // 检查危机关键词
    if (message.type === 'user') {
      checkCrisisKeywords(message.content)
    }
    
    return newMessage
  }
  
  const updateEmotion = (emotionData) => {
    const newEmotion = {
      ...emotionData,
      timestamp: Date.now()
    }
    
    currentEmotion.value = newEmotion
    emotionHistory.value.push(newEmotion)
    
    // 保持历史记录在合理范围内（最近100条）
    if (emotionHistory.value.length > 100) {
      emotionHistory.value = emotionHistory.value.slice(-100)
    }
  }
  
  const checkCrisisKeywords = (content) => {
    const hasCrisisKeyword = crisisKeywords.some(keyword => 
      content.includes(keyword)
    )
    
    if (hasCrisisKeyword) {
      // 触发危机预警
      addMessage({
        content: '我注意到您可能遇到了困难。如果您正在经历危机，请立即寻求专业帮助。您可以拨打心理援助热线：400-161-9995，或点击下方的紧急求助按钮。',
        type: 'system'
      })
      
      // 发送危机预警通知
      triggerCrisisAlert(content)
    }
  }
  
  const triggerCrisisAlert = (content) => {
    // 这里应该调用后端API发送紧急通知
    console.warn('危机预警触发:', content)
    
    // 可以在这里添加通知紧急联系人的逻辑
    if ('Notification' in window && Notification.permission === 'granted') {
      new Notification('紧急提醒', {
        body: '检测到用户可能需要紧急帮助',
        icon: '/pwa-192x192.png'
      })
    }
  }
  
  const clearMessages = () => {
    messages.value = []
  }
  
  const startRecording = () => {
    isRecording.value = true
  }
  
  const stopRecording = () => {
    isRecording.value = false
  }
  
  const setLoading = (loading) => {
    isLoading.value = loading
  }
  
  const createNewChat = async () => {
    try {
      const session = await chatService.createSession('新的对话')
      const newChat = {
        id: session.id,
        title: session.title,
        messages: [],
        createdAt: new Date(session.created_at).getTime(),
        updatedAt: new Date(session.updated_at).getTime()
      }
      
      chatHistory.value.unshift(newChat)
      currentChatId.value = session.id
      messages.value = []
      
      return session.id
    } catch (error) {
      console.error('创建新对话失败:', error)
      // 降级到本地创建
      const chatId = Date.now().toString()
      const newChat = {
        id: chatId,
        title: '新的对话',
        messages: [],
        createdAt: Date.now(),
        updatedAt: Date.now()
      }
      
      chatHistory.value.unshift(newChat)
      currentChatId.value = chatId
      messages.value = []
      
      return chatId
    }
  }
  
  const loadChat = async (chatId) => {
    try {
      // 首先从后端加载消息历史
      const sessionMessages = await chatService.getSessionMessages(chatId)
      
      // 转换消息格式
      const formattedMessages = sessionMessages.map(msg => ({
        id: msg.id,
        content: msg.content,
        type: msg.sender_type === 'user' ? 'user' : (msg.sender_type === 'ai' ? 'ai' : 'system'),
        timestamp: new Date(msg.created_at).getTime(),
        emotion: msg.emotion_data || null,
        audioUrl: msg.audio_file || null,
        // 加载思考内容
        thinking: msg.metadata?.thinking_content || '',
        thinkingTime: msg.metadata?.thinking_time || 0,
        thinkingExpanded: true // 默认展开
      }))
      
      // 更新消息列表
      messages.value = formattedMessages
      currentChatId.value = chatId
      chatService.setCurrentSessionId(chatId)
      
      // 更新本地聊天历史
      const chat = chatHistory.value.find(c => c.id === chatId)
      if (chat) {
        chat.messages = formattedMessages
        chat.updatedAt = Date.now()
      }
    } catch (error) {
      console.error('加载聊天失败:', error)
      // 降级到本地加载
      const chat = chatHistory.value.find(c => c.id === chatId)
      if (chat) {
        currentChatId.value = chatId
        messages.value = [...chat.messages]
      }
    }
  }

  /**
   * 发送消息到后端（流式响应）
   */
  const sendMessageToBackend = async (content, messageType = 'text', options = {}) => {
    setLoading(true);
    let aiMessageId = null; // 将 aiMessageId 声明移到 try 块外部
    let userMessageTempId = null; // 用户消息的临时ID

    try {
      // 首先添加用户消息
      userMessageTempId = Date.now()
      const userMessage = {
        id: userMessageTempId,
        content: content,
        type: 'user',
        timestamp: Date.now(),
        emotion: null
      }
      messages.value.push(userMessage)
      
      // 创建AI消息占位符
      aiMessageId = Date.now() + 1 // 在这里赋值
      const aiMessage = {
        id: aiMessageId,
        content: '',
        type: 'ai',
        timestamp: Date.now(),
        isStreaming: true,
        thinking: '',
        thinkingTime: 0,
        thinkingExpanded: true // 默认展开
      }
      messages.value.push(aiMessage)
      
      // 使用流式响应
      await chatService.sendMessageStream(
        content,
        messageType,
        currentChatId.value,
        // onChunk回调
        (chunk) => {
          if (chunk.type === 'start' && chunk.userMessageId) {
            // 更新用户消息的ID为后端返回的真实UUID
            const userMsgIndex = messages.value.findIndex(m => m.id === userMessageTempId)
            if (userMsgIndex !== -1) {
              messages.value[userMsgIndex].id = chunk.userMessageId
              messages.value[userMsgIndex].backendId = chunk.userMessageId
            }
          } else if (chunk.type === 'chunk') {
            // 更新AI消息内容
            const messageIndex = messages.value.findIndex(m => m.id === aiMessageId)
            if (messageIndex !== -1) {
              messages.value[messageIndex].content += chunk.content
            }
          } else if (chunk.type === 'thinking') {
            // 处理思考过程
            const messageIndex = messages.value.findIndex(m => m.id === aiMessageId)
            if (messageIndex !== -1) {
              // 添加思考过程到消息中
              if (!messages.value[messageIndex].thinking) {
                messages.value[messageIndex].thinking = ''
                messages.value[messageIndex].thinkingStartTime = Date.now()
              }
              messages.value[messageIndex].thinking += chunk.content
              
              // 实时更新思考时间
              if (messages.value[messageIndex].thinkingStartTime) {
                const currentThinkingTime = Math.round((Date.now() - messages.value[messageIndex].thinkingStartTime) / 1000)
                messages.value[messageIndex].thinkingTime = currentThinkingTime
              }
            }
          }
        },
        // onComplete回调
        (complete) => {
          const messageIndex = messages.value.findIndex(m => m.id === aiMessageId)
          if (messageIndex !== -1) {
            messages.value[messageIndex].content = complete.fullContent
            messages.value[messageIndex].isStreaming = false
            // 更新为后端返回的真实UUID
            messages.value[messageIndex].id = complete.messageId
            messages.value[messageIndex].backendId = complete.messageId // 保存后端ID
            
            // 计算思考时间
            if (messages.value[messageIndex].thinkingStartTime) {
              const thinkingDuration = Math.round((Date.now() - messages.value[messageIndex].thinkingStartTime) / 1000)
              messages.value[messageIndex].thinkingTime = thinkingDuration
            }
          }
          
          // 更新当前会话ID
          if (complete.sessionId) {
            currentChatId.value = complete.sessionId
            chatService.setCurrentSessionId(complete.sessionId)
          }
        },
        // onError回调
        (error) => {
          console.error('流式响应错误:', error)
          const messageIndex = messages.value.findIndex(m => m.id === aiMessageId)
          if (messageIndex !== -1) {
            messages.value[messageIndex].content = '抱歉，AI服务暂时不可用，请稍后再试。'
            messages.value[messageIndex].isStreaming = false
          }
        },
        // 传递选项参数
        options
      )
      
    } catch (error) {
      console.error('发送消息失败:', error)
      // 移除可能添加的消息
      if (aiMessageId) { // 确保 aiMessageId 已被赋值
        messages.value = messages.value.filter(m => m.id !== aiMessageId)
      }
      throw error
    } finally {
      setLoading(false)
    }
  }
  
  const saveCurrentChat = () => {
    if (!currentChatId.value) return
    
    const chatIndex = chatHistory.value.findIndex(c => c.id === currentChatId.value)
    if (chatIndex !== -1) {
      chatHistory.value[chatIndex] = {
        ...chatHistory.value[chatIndex],
        messages: [...messages.value],
        updatedAt: Date.now(),
        title: generateChatTitle()
      }
    }
  }
  
  const generateChatTitle = () => {
    if (messages.value.length === 0) return '新的对话'
    
    const firstUserMessage = messages.value.find(m => m.type === 'user')
    if (firstUserMessage) {
      return firstUserMessage.content.slice(0, 20) + (firstUserMessage.content.length > 20 ? '...' : '')
    }
    
    return '新的对话'
  }
  
  const deleteChat = async (chatId) => {
    try {
      await chatService.deleteSession(chatId)
      chatHistory.value = chatHistory.value.filter(c => c.id !== chatId)
      if (currentChatId.value === chatId) {
        currentChatId.value = null
        messages.value = []
      }
    } catch (error) {
      console.error('删除对话失败:', error)
      // 降级到本地删除
      chatHistory.value = chatHistory.value.filter(c => c.id !== chatId)
      if (currentChatId.value === chatId) {
        currentChatId.value = null
        messages.value = []
      }
    }
  }

  /**
   * 加载会话历史列表
   */
  const loadChatHistory = async () => {
    try {
      const sessions = await chatService.getSessions()
      
      // 转换会话格式
      const formattedSessions = sessions.map(session => ({
        id: session.id,
        title: session.title,
        messages: [], // 消息将在加载具体会话时获取
        createdAt: new Date(session.created_at).getTime(),
        updatedAt: new Date(session.updated_at).getTime()
      }))
      
      chatHistory.value = formattedSessions
      return formattedSessions
    } catch (error) {
      console.error('加载会话历史失败:', error)
      return []
    }
  }
  
  return {
    // 状态
    messages,
    currentEmotion,
    emotionHistory,
    isLoading,
    isRecording,
    chatHistory,
    currentChatId,
    
    // 计算属性
    currentEmotionLabel,
    emotionTrend,
    hasMessages,
    
    // 方法
    addMessage,
    updateEmotion,
    clearMessages,
    startRecording,
    stopRecording,
    setLoading,
    createNewChat,
    loadChat,
    saveCurrentChat,
    deleteChat,
    checkCrisisKeywords,
    
    // 新的API集成方法
    sendMessageToBackend,
    loadChatHistory
  }
})
