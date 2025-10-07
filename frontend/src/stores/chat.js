import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { chatService } from '@/services/chatService'
import { t } from './language'

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
  const streamingControllers = ref(new Map()) // 存储流式响应的控制器
  const emotionSuggestions = ref([]) // 新增：存储个性化建议
  const lastCrisisAlertTime = ref(0) // 上次危机预警时间（防止重复触发）
  
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
  
  // 当前情绪显示名称（优先显示AI原始情绪词）
  const currentEmotionDisplayName = computed(() => {
    const emotion = currentEmotion.value
    console.log('🔍 currentEmotionDisplayName - emotion:', emotion)
    if (!emotion) {
      console.log('🔍 currentEmotionDisplayName - emotion is null/undefined, returning "平静"')
      return '平静'
    }
    
    // 如果有原始情绪词，直接显示第一个
    if (emotion.rawEmotionWords && emotion.rawEmotionWords.length > 0) {
      console.log('🔍 currentEmotionDisplayName - rawEmotionWords found:', emotion.rawEmotionWords[0])
      return emotion.rawEmotionWords[0]
    }
    
    // 降级到映射的情绪词
    const fallbackName = currentEmotionLabel.value.name
    console.log('🔍 currentEmotionDisplayName - No rawEmotionWords, falling back to:', fallbackName)
    return fallbackName
  })
  
  const emotionTrend = computed(() => {
    if (emotionHistory.value.length < 2) return 'stable'
    
    // 使用最近5次情绪得分的平均值来判断趋势
    const recentScores = emotionHistory.value.slice(-5).map(e => e.score)
    if (recentScores.length < 2) return 'stable'

    const average = arr => arr.reduce((a, b) => a + b, 0) / arr.length
    
    const trend = average(recentScores.slice(-3)) - average(recentScores.slice(0, 3))
    
    if (trend > 2) return 'improving' // 趋势改善阈值
    if (trend < -2) return 'declining' // 趋势下降阈值
    return 'stable'
  })
  
  const hasMessages = computed(() => messages.value.length > 0)
  
  // 危机预警关键词（扩展版）
  const crisisKeywords = [
    // 自杀相关
    '想死', '自杀', '结束生命', '不想活', '活着没意思', '不想活了',
    '去死', '寻死', '轻生', '了结', '一了百了', '自我了断',
    
    // 自伤相关
    '自伤', '自残', '伤害自己', '割腕', '跳楼', '上吊', '服药',
    '自我伤害', '弄伤自己', '伤害身体',
    
    // 绝望相关
    '想消失', '解脱', '活不下去', '没有希望', '彻底绝望',
    '生无可恋', '行尸走肉', '没有意义', '毫无价值',
    
    // 极端行为
    '遗书', '告别', '最后一次', '永别', '再见了',
    '安排后事', '交代遗言',
    
    // 崩溃状态
    '崩溃了', '撑不下去', '无法承受', '精神崩溃', '崩溃边缘'
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
    
    console.log('🔍 updateEmotion - 更新情绪数据:', newEmotion)
    currentEmotion.value = newEmotion
    console.log('🔍 updateEmotion - currentEmotion.value 更新后:', currentEmotion.value)
    emotionHistory.value.push(newEmotion)
    
    // 保持历史记录在合理范围内（最近100条）
    if (emotionHistory.value.length > 100) {
      emotionHistory.value = emotionHistory.value.slice(-100)
    }
  }

  // 生成危机消息（支持动态翻译）
  const generateCrisisMessage = (crisisLevel) => {
    if (crisisLevel === 3) {
      return `${t('crisisEmergencyHigh')}

${t('crisisActionImmediate')}
• ${t('crisisHotline1')}
• ${t('crisisHotline2')}
• ${t('crisisEmergencyButton')}
• ${t('crisisContactEmergency')}

${t('crisisLifePrecious')}`
    } else {
      return `${t('crisisMediumWarning')}

${t('crisisSuggestions')}
• ${t('crisisFeelOverwhelmed')}
• ${t('crisisGetProfessional')}
• ${t('crisisSeekCounselor')}

${t('crisisSeekingHelpBrave')}`
    }
  }

  // 新增：解析并更新情绪数据的方法
  const parseAndSetEmotionData = (emotionData) => {
    console.log('🔍 parseAndSetEmotionData 接收到的数据:', emotionData)
    if (!emotionData || typeof emotionData !== 'object') return

    // 检查危机等级并触发预警
    if (emotionData.crisis_level !== undefined) {
      const crisisLevel = parseInt(emotionData.crisis_level)
      console.log('🚨 AI检测到的危机等级:', crisisLevel)
      
      if (crisisLevel >= 2) {
        // 中度或高度危机，触发预警
        // 存储翻译键而不是翻译后的文本，以支持动态语言切换
        const crisisMessageData = crisisLevel === 3 
          ? {
              type: 'crisis-high',
              keys: [
                'crisisEmergencyHigh',
                'crisisActionImmediate',
                'crisisHotline1',
                'crisisHotline2',
                'crisisEmergencyButton',
                'crisisContactEmergency',
                'crisisLifePrecious'
              ]
            }
          : {
              type: 'crisis-medium',
              keys: [
                'crisisMediumWarning',
                'crisisSuggestions',
                'crisisFeelOverwhelmed',
                'crisisGetProfessional',
                'crisisSeekCounselor',
                'crisisSeekingHelpBrave'
              ]
            }

        addMessage({
          content: generateCrisisMessage(crisisLevel),
          type: 'system',
          crisisData: crisisMessageData  // 存储翻译键数据以支持动态翻译
        })
        
        // 如果是高度危机，触发完整的危机预警流程
        if (crisisLevel === 3) {
          const crisisDetectedMsg = t('crisisDetectedByAI').replace('{level}', crisisLevel)
          triggerCrisisAlert(crisisDetectedMsg, [`crisis_level_${crisisLevel}`])
        }
      }
    }

    // 更新情绪建议
    if (Array.isArray(emotionData.suggestions)) {
      emotionSuggestions.value = emotionData.suggestions.map((text, i) => ({ id: i + 1, text }))
    }

    // 更新当前情绪
    if (Array.isArray(emotionData.emotion_words) && emotionData.emotion_words.length > 0) {
      console.log('🔍 情绪词汇:', emotionData.emotion_words)
      // 完整的情绪词映射表（中英双语）
      const emotionMap = {
        // 开心 - happy
        '开心': 'happy',
        '喜悦': 'happy',
        '快乐': 'happy',
        '愉快': 'happy',
        '高兴': 'happy',
        '兴奋': 'happy',
        '满意': 'happy',
        '欣慰': 'happy',
        '幸福': 'happy',
        'happy': 'happy',
        'joy': 'happy',
        'joyful': 'happy',
        'pleased': 'happy',
        'delighted': 'happy',
        'excited': 'happy',
        'cheerful': 'happy',
        'content': 'happy',
        'satisfied': 'happy',
        
        // 平静 - neutral
        '平静': 'neutral',
        '平和': 'neutral',
        '冷静': 'neutral',
        '淡定': 'neutral',
        '放松': 'neutral',
        '安静': 'neutral',
        '稳定': 'neutral',
        'neutral': 'neutral',
        'calm': 'neutral',
        'peaceful': 'neutral',
        'relaxed': 'neutral',
        'composed': 'neutral',
        'serene': 'neutral',
        'tranquil': 'neutral',
        
        // 难过 - sad
        '难过': 'sad',
        '悲伤': 'sad',
        '伤心': 'sad',
        '沮丧': 'sad',
        '失落': 'sad',
        '低落': 'sad',
        '痛苦': 'sad',
        '忧伤': 'sad',
        '郁闷': 'sad',
        '消沉': 'sad',
        '失望': 'sad',
        '绝望': 'sad',
        '心碎': 'sad',
        '泪流满面': 'sad',
        '痛哭': 'sad',
        '心酸': 'sad',
        'sad': 'sad',
        'sorrow': 'sad',
        'unhappy': 'sad',
        'depressed': 'sad',
        'down': 'sad',
        'blue': 'sad',
        'melancholy': 'sad',
        'disappointed': 'sad',
        'dejected': 'sad',
        'heartbroken': 'sad',
        'devastated': 'sad',
        'miserable': 'sad',
        'grief': 'sad',
        'despair': 'sad',
        
        // 焦虑 - anxious
        '焦虑': 'anxious',
        '紧张': 'anxious',
        '担心': 'anxious',
        '担忧': 'anxious',
        '不安': 'anxious',
        '害怕': 'anxious',
        '恐惧': 'anxious',
        '慌张': 'anxious',
        '忐忑': 'anxious',
        '烦躁': 'anxious',
        '压力': 'anxious',
        '恐慌': 'anxious',
        '惊恐': 'anxious',
        '坐立不安': 'anxious',
        '心神不宁': 'anxious',
        '焦虑不安': 'anxious',
        'anxious': 'anxious',
        'anxiety': 'anxious',
        'nervous': 'anxious',
        'worried': 'anxious',
        'tense': 'anxious',
        'stressed': 'anxious',
        'uneasy': 'anxious',
        'afraid': 'anxious',
        'fearful': 'anxious',
        'restless': 'anxious',
        'panicked': 'anxious',
        'terrified': 'anxious',
        'overwhelmed': 'anxious',
        
        // 愤怒 - angry
        '愤怒': 'angry',
        '生气': 'angry',
        '恼火': 'angry',
        '气愤': 'angry',
        '愤慨': 'angry',
        '烦恼': 'angry',
        '恼怒': 'angry',
        '暴躁': 'angry',
        '不满': 'angry',
        '暴怒': 'angry',
        '狂怒': 'angry',
        '暴跳如雷': 'angry',
        '怒不可遏': 'angry',
        '怒火中烧': 'angry',
        '气急败坏': 'angry',
        '暴走': 'angry',
        '爆炸': 'angry',
        '崩溃': 'angry',
        '失控': 'angry',
        '抓狂': 'angry',
        '发疯': 'angry',
        '暴怒': 'angry',
        'angry': 'angry',
        'anger': 'angry',
        'mad': 'angry',
        'furious': 'angry',
        'irritated': 'angry',
        'annoyed': 'angry',
        'frustrated': 'angry',
        'outraged': 'angry',
        'rage': 'angry',
        'explosive': 'angry',
        'exploding': 'angry',
        'livid': 'angry',
        'enraged': 'angry',
        'infuriated': 'angry',
        'seething': 'angry',
        'boiling': 'angry',
        'raging': 'angry'
      }
      
      const primaryEmotionWord = emotionData.emotion_words[0].toLowerCase()
      console.log('🔍 主要情绪词:', primaryEmotionWord)
      
      // 修复：先尝试精确匹配，再尝试模糊匹配
      let labelKey = 'neutral'
      if (emotionMap[primaryEmotionWord]) {
        labelKey = emotionMap[primaryEmotionWord]
        console.log('🔍 精确匹配成功:', primaryEmotionWord, '->', labelKey)
      } else {
        // 模糊匹配（不区分大小写）
        for (const [key, value] of Object.entries(emotionMap)) {
          if (primaryEmotionWord.includes(key.toLowerCase()) || key.toLowerCase().includes(primaryEmotionWord)) {
            labelKey = value
            console.log('🔍 模糊匹配成功:', primaryEmotionWord, '匹配', key, '->', labelKey)
            break
          }
        }
        if (labelKey === 'neutral') {
          console.log('🔍 未找到匹配的情绪词，使用默认值 neutral')
        }
      }
      
      const newEmotion = {
        label: labelKey,
        score: emotionData.emotion_score, // 直接使用模型返回的-10到10的分数
        words: emotionData.emotion_words,
        rawEmotionWords: emotionData.emotion_words, // 保存原始情绪词
        timestamp: Date.now()
      }
      console.log('🔍 最终情绪对象:', newEmotion)
      console.log('🔍 rawEmotionWords 字段:', newEmotion.rawEmotionWords)
      updateEmotion(newEmotion)
    }
  }
  
  const checkCrisisKeywords = (content) => {
    const hasCrisisKeyword = crisisKeywords.some(keyword => 
      content.includes(keyword)
    )
    
    if (hasCrisisKeyword) {
      // 记录触发的关键词
      const triggeredKeywords = crisisKeywords.filter(keyword => content.includes(keyword))
      
      const crisisActionList = t('crisisActionList')
      const crisisHotline1 = t('crisisHotline1')
      const crisisHotline2 = t('crisisHotline2')
      const crisisEmergencyButton = t('crisisEmergencyButton')
      const crisisNotAlone = t('crisisNotAlone')
      
      // 触发危机预警
      addMessage({
        content: `${t('crisisWarningKeyword')}

${crisisActionList}
• ${crisisHotline1}
• ${crisisHotline2}
• ${crisisEmergencyButton}

${crisisNotAlone}`,
        type: 'system'
      })
      
      // 发送危机预警通知到后端
      triggerCrisisAlert(content, triggeredKeywords)
      
      return true // 返回是否检测到危机
    }
    
    return false
  }
  
  const triggerCrisisAlert = async (content, keywords = []) => {
    console.warn('🚨 危机预警触发:', content, '关键词:', keywords)
    
    // 防止5秒内重复触发
    const now = Date.now()
    if (now - lastCrisisAlertTime.value < 5000) {
      console.log('🚨 危机预警已在5秒内触发过，跳过重复触发')
      return
    }
    lastCrisisAlertTime.value = now
    
    try {
      // 调用后端API记录危机事件
      const { chatApi } = await import('@/utils/api')
      await chatApi.reportCrisis({
        content: content,
        keywords: keywords,
        session_id: currentChatId.value,
        timestamp: Date.now()
      }).catch(err => {
        console.error('发送危机预警到后端失败:', err)
      })
      
      // 获取翻译文本
      const notificationTitle = t('notificationEmergencyTitle')
      const notificationBody = t('notificationEmergencyBody')
      
      // 浏览器通知
      if ('Notification' in window) {
        if (Notification.permission === 'granted') {
          new Notification(notificationTitle, {
            body: notificationBody,
            icon: '/pwa-192x192.png',
            requireInteraction: true
          })
        } else if (Notification.permission !== 'denied') {
          // 请求通知权限
          Notification.requestPermission().then(permission => {
            if (permission === 'granted') {
              new Notification(notificationTitle, {
                body: notificationBody,
                icon: '/pwa-192x192.png',
                requireInteraction: true
              })
            }
          })
        }
      }
      
      // 触发全局事件，让 Chat.vue 自动弹出紧急求助弹窗
      window.dispatchEvent(new CustomEvent('crisis-detected', { 
        detail: { content, keywords } 
      }))
      
    } catch (error) {
      console.error('危机预警处理失败:', error)
    }
  }
  
  const clearMessages = () => {
    messages.value = []
    // 清空情绪历史和建议
    emotionHistory.value = []
    emotionSuggestions.value = []
    currentEmotion.value = {
      label: 'neutral',
      score: 50,
      confidence: 0.8,
      timestamp: Date.now()
    }
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
      
      // 清空情绪历史和建议
      emotionHistory.value = []
      emotionSuggestions.value = []
      currentEmotion.value = {
        label: 'neutral',
        score: 50,
        confidence: 0.8,
        timestamp: Date.now()
      }
      
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
      
      // 清空情绪历史和建议
      emotionHistory.value = []
      emotionSuggestions.value = []
      currentEmotion.value = {
        label: 'neutral',
        score: 50,
        confidence: 0.8,
        timestamp: Date.now()
      }
      
      return chatId
    }
  }
  
  const loadChat = async (chatId) => {
    try {
      // 首先从后端加载消息历史
      const sessionMessages = await chatService.getSessionMessages(chatId)
      
      // 清空当前的情绪历史和建议
      emotionHistory.value = []
      emotionSuggestions.value = []
      
      // 找到最后一条AI消息的建议（用于最后设置）
      let lastAiEmotionData = null
      
      // 转换消息格式并重建情绪历史
      const formattedMessages = sessionMessages.map(msg => {
        // 如果是AI消息且包含情绪数据，恢复到emotionHistory
        if (msg.sender_type === 'ai' && msg.metadata?.emotion_analysis) {
          const emotionData = msg.metadata.emotion_analysis
          
          // 记录最后一条AI消息的情绪数据
          lastAiEmotionData = emotionData
          
          // 构建情绪对象并添加到历史
          if (Array.isArray(emotionData.emotion_words) && emotionData.emotion_words.length > 0) {
            const emotionMap = {
              '开心': 'happy', '喜悦': 'happy', '快乐': 'happy', '愉快': 'happy',
              '平静': 'neutral', '平和': 'neutral', '冷静': 'neutral',
              '难过': 'sad', '悲伤': 'sad', '伤心': 'sad', '沮丧': 'sad',
              '焦虑': 'anxious', '紧张': 'anxious', '担心': 'anxious',
              '愤怒': 'angry', '生气': 'angry', '恼火': 'angry'
            }
            
            const primaryEmotionWord = emotionData.emotion_words[0].toLowerCase()
            let labelKey = 'neutral'
            
            if (emotionMap[primaryEmotionWord]) {
              labelKey = emotionMap[primaryEmotionWord]
            } else {
              for (const [key, value] of Object.entries(emotionMap)) {
                if (primaryEmotionWord.includes(key.toLowerCase())) {
                  labelKey = value
                  break
                }
              }
            }
            
            emotionHistory.value.push({
              label: labelKey,
              score: emotionData.emotion_score || 0,
              words: emotionData.emotion_words,
              timestamp: new Date(msg.created_at).getTime()
            })
          }
        }
        
        return {
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
        }
      })
      
      // 只使用最后一条AI消息的建议
      if (lastAiEmotionData && Array.isArray(lastAiEmotionData.suggestions)) {
        emotionSuggestions.value = lastAiEmotionData.suggestions.map((text, i) => ({ id: i + 1, text }))
      }
      
      // 更新当前情绪（使用最新的情绪数据）
      if (emotionHistory.value.length > 0) {
        currentEmotion.value = emotionHistory.value[emotionHistory.value.length - 1]
      }
      
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
      
      // 创建AbortController用于停止流式响应
      const controller = new AbortController()
      streamingControllers.value.set(aiMessageId, controller)
      
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
              const currentContent = messages.value[messageIndex].content
              
              // 如果已经开始情绪数据部分，不再追加任何内容，并更新状态提示
              if (messages.value[messageIndex]._emotionDataStarted) {
                messages.value[messageIndex].isGeneratingEmotion = true
                return
              }
              
              // 将新chunk与当前内容合并
              const newContent = currentContent + chunk.content
              
              // 检查合并后的内容是否包含分隔符
              if (newContent.includes('|||')) {
                // 只保留分隔符之前的部分（不包含|||）
                const beforeSeparator = newContent.split('|||')[0]
                messages.value[messageIndex].content = beforeSeparator.trimEnd()
                messages.value[messageIndex]._emotionDataStarted = true
                messages.value[messageIndex].isGeneratingEmotion = true
              } else {
                // 正常追加
                messages.value[messageIndex].content = newContent
              }
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
            let finalContent = complete.fullContent
            
            // 增强：解析情绪数据
            if (finalContent.includes('|||')) {
              const parts = finalContent.split('|||')
              finalContent = parts[0].trim()
              const emotionJsonString = parts[1]
              console.log('🔍 情绪分析原始数据:', emotionJsonString)
              try {
                // 修复：直接找到第一个 { 和最后一个 } 之间的内容
                const firstBrace = emotionJsonString.indexOf('{')
                const lastBrace = emotionJsonString.lastIndexOf('}')
                
                if (firstBrace !== -1 && lastBrace !== -1 && lastBrace > firstBrace) {
                  const jsonString = emotionJsonString.substring(firstBrace, lastBrace + 1)
                  console.log('🔍 提取的JSON字符串:', jsonString)
                  const emotionData = JSON.parse(jsonString)
                  console.log('🔍 解析后的情绪数据:', emotionData)
                  parseAndSetEmotionData(emotionData)
                } else {
                   console.warn('在情绪分析块中未找到有效的JSON对象:', emotionJsonString)
                }
              } catch (e) {
                console.error('解析情绪JSON失败:', e, '原始字符串:', emotionJsonString)
              }
            }

            messages.value[messageIndex].content = finalContent
            messages.value[messageIndex].isStreaming = false
            messages.value[messageIndex].isGeneratingEmotion = false // 清除情绪生成标志
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
          
          // 清理控制器
          streamingControllers.value.delete(aiMessageId)
        },
        // onError回调
        (error) => {
          console.error('流式响应错误:', error)
          
          // 检查是否是用户主动停止（使用isAbort标志）
          const isAbortError = error.isAbort === true
          
          const messageIndex = messages.value.findIndex(m => m.id === aiMessageId)
          if (messageIndex !== -1) {
            if (!isAbortError) {
              // 只有在非中止错误时才显示错误消息
              messages.value[messageIndex].content = '抱歉，AI服务暂时不可用，请稍后再试。'
            }
            messages.value[messageIndex].isStreaming = false
          }
          
          // 清理控制器
          streamingControllers.value.delete(aiMessageId)
        },
        // 传递选项参数
        options,
        // 传递AbortController
        controller
      )
      
    } catch (error) {
      console.error('发送消息失败:', error)
      
      // 检查是否是用户主动停止（AbortError）
      const isAbortError = error.name === 'AbortError' || error.message.includes('aborted')
      
      if (!isAbortError) {
        // 只有在非中止错误时才移除消息
        if (aiMessageId) {
          messages.value = messages.value.filter(m => m.id !== aiMessageId)
        }
        throw error
      } else {
        // 如果是中止错误，只更新消息状态，不删除消息
        const messageIndex = messages.value.findIndex(m => m.id === aiMessageId)
        if (messageIndex !== -1) {
          messages.value[messageIndex].isStreaming = false
        }
      }
    } finally {
      setLoading(false)
      // 清理控制器
      if (aiMessageId) {
        streamingControllers.value.delete(aiMessageId)
      }
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
   * 停止流式响应
   */
  const stopStreamingResponse = async (messageId) => {
    try {
      // 获取对应的控制器
      const controller = streamingControllers.value.get(messageId)
      if (controller) {
        // 中止流式响应
        controller.abort()
        streamingControllers.value.delete(messageId)
        
        console.log('流式响应已停止:', messageId)
      }
    } catch (error) {
      console.error('停止流式响应失败:', error)
      // 不抛出错误，避免影响UI状态
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
  
  // 更新危机消息的翻译（当语言切换时调用）
  const updateCrisisMessagesTranslation = () => {
    messages.value = messages.value.map(msg => {
      if (msg.type === 'system' && msg.crisisData) {
        // 从危机数据中获取危机等级
        const crisisLevel = msg.crisisData.type === 'crisis-high' ? 3 : 2
        return {
          ...msg,
          content: generateCrisisMessage(crisisLevel)
        }
      }
      return msg
    })
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
    emotionSuggestions, // 导出
    
    // 计算属性
    currentEmotionLabel,
    currentEmotionDisplayName,
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
    parseAndSetEmotionData, // 导出
    
    // 新的API集成方法
    sendMessageToBackend,
    loadChatHistory,
    stopStreamingResponse,
    updateCrisisMessagesTranslation
  }
})
