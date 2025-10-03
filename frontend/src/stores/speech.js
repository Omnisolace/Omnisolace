import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useSpeechStore = defineStore('speech', () => {
  // 状态
  const isSupported = ref('webkitSpeechRecognition' in window || 'SpeechRecognition' in window)
  const isListening = ref(false)
  const transcript = ref('')
  const confidence = ref(0)
  const error = ref(null)
  
  // 语音识别实例
  let recognition = null
  let speechSynthesis = null
  
  // 初始化语音识别
  const initializeSpeechRecognition = () => {
    if (!isSupported.value) {
      console.warn('浏览器不支持语音识别')
      return false
    }
    
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
    recognition = new SpeechRecognition()
    
    // 配置语音识别
    recognition.continuous = false // 单次识别
    recognition.interimResults = true // 显示中间结果
    recognition.lang = 'zh-CN' // 中文识别
    recognition.maxAlternatives = 1
    
    // 事件监听
    recognition.onstart = () => {
      isListening.value = true
      error.value = null
      transcript.value = ''
    }
    
    recognition.onresult = (event) => {
      let finalTranscript = ''
      let interimTranscript = ''
      
      for (let i = event.resultIndex; i < event.results.length; i++) {
        const result = event.results[i]
        if (result.isFinal) {
          finalTranscript += result[0].transcript
          confidence.value = result[0].confidence
        } else {
          interimTranscript += result[0].transcript
        }
      }
      
      transcript.value = finalTranscript || interimTranscript
    }
    
    recognition.onend = () => {
      isListening.value = false
    }
    
    recognition.onerror = (event) => {
      error.value = event.error
      isListening.value = false
      
      // 错误处理
      switch (event.error) {
        case 'no-speech':
          error.value = '未检测到语音，请重试'
          break
        case 'audio-capture':
          error.value = '无法访问麦克风'
          break
        case 'not-allowed':
          error.value = '麦克风权限被拒绝'
          break
        case 'network':
          error.value = '网络错误，请检查网络连接'
          break
        default:
          error.value = '语音识别失败，请重试'
      }
    }
    
    return true
  }
  
  // 开始语音识别
  const startListening = () => {
    if (!recognition) {
      if (!initializeSpeechRecognition()) {
        return false
      }
    }
    
    if (isListening.value) {
      return false
    }
    
    try {
      recognition.start()
      return true
    } catch (err) {
      error.value = '启动语音识别失败'
      return false
    }
  }
  
  // 停止语音识别
  const stopListening = () => {
    if (recognition && isListening.value) {
      recognition.stop()
    }
  }
  
  // 语音合成（文本转语音）
  const speak = (text, options = {}) => {
    if (!('speechSynthesis' in window)) {
      console.warn('浏览器不支持语音合成')
      return false
    }
    
    // 停止当前播放
    window.speechSynthesis.cancel()
    
    const utterance = new SpeechSynthesisUtterance(text)
    
    // 配置语音合成
    utterance.lang = options.lang || 'zh-CN'
    utterance.rate = options.rate || 0.9 // 语速稍慢，适合老年用户
    utterance.pitch = options.pitch || 1
    utterance.volume = options.volume || 1
    
    // 选择合适的语音
    const voices = window.speechSynthesis.getVoices()
    const chineseVoice = voices.find(voice => 
      voice.lang.includes('zh') || voice.lang.includes('CN')
    )
    if (chineseVoice) {
      utterance.voice = chineseVoice
    }
    
    window.speechSynthesis.speak(utterance)
    return true
  }
  
  // 停止语音播放
  const stopSpeaking = () => {
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel()
    }
  }
  
  // 请求麦克风权限
  const requestMicrophonePermission = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      stream.getTracks().forEach(track => track.stop()) // 立即停止，只是为了获取权限
      return true
    } catch (err) {
      error.value = '无法访问麦克风，请检查权限设置'
      return false
    }
  }
  
  // 检查麦克风权限
  const checkMicrophonePermission = async () => {
    if (!navigator.permissions) {
      return 'unknown'
    }
    
    try {
      const permission = await navigator.permissions.query({ name: 'microphone' })
      return permission.state // 'granted', 'denied', 'prompt'
    } catch (err) {
      return 'unknown'
    }
  }
  
  // 清除错误
  const clearError = () => {
    error.value = null
  }
  
  // 重置状态
  const reset = () => {
    transcript.value = ''
    confidence.value = 0
    error.value = null
    isListening.value = false
  }
  
  return {
    // 状态
    isSupported,
    isListening,
    transcript,
    confidence,
    error,
    
    // 方法
    startListening,
    stopListening,
    speak,
    stopSpeaking,
    requestMicrophonePermission,
    checkMicrophonePermission,
    clearError,
    reset
  }
})
