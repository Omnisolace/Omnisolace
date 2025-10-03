/**
 * 语音功能工具类
 * 封装 Web Speech API 的语音识别和语音合成功能
 */

// 语音识别类
export class SpeechRecognition {
  constructor(options = {}) {
    this.isSupported = 'webkitSpeechRecognition' in window || 'SpeechRecognition' in window
    this.recognition = null
    this.isListening = false
    this.callbacks = {}
    
    // 默认配置
    this.config = {
      continuous: false,
      interimResults: true,
      lang: 'zh-CN',
      maxAlternatives: 1,
      ...options
    }
    
    if (this.isSupported) {
      this.initRecognition()
    }
  }
  
  // 初始化语音识别
  initRecognition() {
    const SpeechRecognitionAPI = window.SpeechRecognition || window.webkitSpeechRecognition
    this.recognition = new SpeechRecognitionAPI()
    
    // 配置识别器
    Object.keys(this.config).forEach(key => {
      if (key in this.recognition) {
        this.recognition[key] = this.config[key]
      }
    })
    
    // 绑定事件
    this.recognition.onstart = () => {
      this.isListening = true
      this.emit('start')
    }
    
    this.recognition.onend = () => {
      this.isListening = false
      this.emit('end')
    }
    
    this.recognition.onresult = (event) => {
      let finalTranscript = ''
      let interimTranscript = ''
      
      for (let i = event.resultIndex; i < event.results.length; i++) {
        const result = event.results[i]
        const transcript = result[0].transcript
        
        if (result.isFinal) {
          finalTranscript += transcript
        } else {
          interimTranscript += transcript
        }
      }
      
      this.emit('result', {
        final: finalTranscript,
        interim: interimTranscript,
        confidence: event.results[event.results.length - 1][0].confidence
      })
    }
    
    this.recognition.onerror = (event) => {
      this.emit('error', this.getErrorMessage(event.error))
    }
    
    this.recognition.onnomatch = () => {
      this.emit('nomatch', '未识别到有效语音')
    }
  }
  
  // 开始识别
  start() {
    if (!this.isSupported) {
      throw new Error('浏览器不支持语音识别')
    }
    
    if (this.isListening) {
      return false
    }
    
    try {
      this.recognition.start()
      return true
    } catch (error) {
      this.emit('error', '启动语音识别失败: ' + error.message)
      return false
    }
  }
  
  // 停止识别
  stop() {
    if (this.recognition && this.isListening) {
      this.recognition.stop()
    }
  }
  
  // 中止识别
  abort() {
    if (this.recognition && this.isListening) {
      this.recognition.abort()
    }
  }
  
  // 事件监听
  on(event, callback) {
    if (!this.callbacks[event]) {
      this.callbacks[event] = []
    }
    this.callbacks[event].push(callback)
  }
  
  // 移除事件监听
  off(event, callback) {
    if (this.callbacks[event]) {
      const index = this.callbacks[event].indexOf(callback)
      if (index > -1) {
        this.callbacks[event].splice(index, 1)
      }
    }
  }
  
  // 触发事件
  emit(event, data) {
    if (this.callbacks[event]) {
      this.callbacks[event].forEach(callback => callback(data))
    }
  }
  
  // 获取错误信息
  getErrorMessage(error) {
    const errorMessages = {
      'no-speech': '未检测到语音，请重试',
      'audio-capture': '无法访问麦克风',
      'not-allowed': '麦克风权限被拒绝',
      'network': '网络错误，请检查网络连接',
      'service-not-allowed': '语音识别服务不可用',
      'bad-grammar': '语法错误',
      'language-not-supported': '不支持的语言'
    }
    
    return errorMessages[error] || '语音识别失败，请重试'
  }
}

// 语音合成类
export class SpeechSynthesis {
  constructor(options = {}) {
    this.isSupported = 'speechSynthesis' in window
    this.synthesis = window.speechSynthesis
    this.voices = []
    this.currentUtterance = null
    
    // 默认配置
    this.config = {
      lang: 'zh-CN',
      rate: 0.9,
      pitch: 1,
      volume: 1,
      ...options
    }
    
    if (this.isSupported) {
      this.loadVoices()
    }
  }
  
  // 加载可用语音
  loadVoices() {
    const loadVoicesImpl = () => {
      this.voices = this.synthesis.getVoices()
      
      // 优先选择中文语音
      const chineseVoice = this.voices.find(voice => 
        voice.lang.includes('zh') || voice.lang.includes('CN')
      )
      
      if (chineseVoice) {
        this.config.voice = chineseVoice
      }
    }
    
    // 某些浏览器需要异步加载语音列表
    if (this.voices.length === 0) {
      this.synthesis.onvoiceschanged = loadVoicesImpl
    }
    
    loadVoicesImpl()
  }
  
  // 语音播放
  speak(text, options = {}) {
    if (!this.isSupported) {
      throw new Error('浏览器不支持语音合成')
    }
    
    // 停止当前播放
    this.stop()
    
    const utterance = new SpeechSynthesisUtterance(text)
    
    // 应用配置
    const config = { ...this.config, ...options }
    Object.keys(config).forEach(key => {
      if (key in utterance) {
        utterance[key] = config[key]
      }
    })
    
    // 事件处理
    utterance.onstart = () => {
      console.log('语音播放开始')
    }
    
    utterance.onend = () => {
      console.log('语音播放结束')
      this.currentUtterance = null
    }
    
    utterance.onerror = (event) => {
      console.error('语音播放错误:', event.error)
      this.currentUtterance = null
    }
    
    this.currentUtterance = utterance
    this.synthesis.speak(utterance)
    
    return utterance
  }
  
  // 停止播放
  stop() {
    if (this.isSupported && this.synthesis.speaking) {
      this.synthesis.cancel()
      this.currentUtterance = null
    }
  }
  
  // 暂停播放
  pause() {
    if (this.isSupported && this.synthesis.speaking) {
      this.synthesis.pause()
    }
  }
  
  // 恢复播放
  resume() {
    if (this.isSupported && this.synthesis.paused) {
      this.synthesis.resume()
    }
  }
  
  // 获取可用语音列表
  getVoices() {
    return this.voices
  }
  
  // 设置语音
  setVoice(voiceName) {
    const voice = this.voices.find(v => v.name === voiceName)
    if (voice) {
      this.config.voice = voice
      return true
    }
    return false
  }
  
  // 检查是否正在播放
  isSpeaking() {
    return this.isSupported && this.synthesis.speaking
  }
}

// 语音工具函数
export const speechUtils = {
  // 请求麦克风权限
  async requestMicrophonePermission() {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      stream.getTracks().forEach(track => track.stop())
      return true
    } catch (error) {
      console.error('麦克风权限请求失败:', error)
      return false
    }
  },
  
  // 检查麦克风权限状态
  async checkMicrophonePermission() {
    if (!navigator.permissions) {
      return 'unknown'
    }
    
    try {
      const permission = await navigator.permissions.query({ name: 'microphone' })
      return permission.state // 'granted', 'denied', 'prompt'
    } catch (error) {
      return 'unknown'
    }
  },
  
  // 检测语音识别支持
  isSpeechRecognitionSupported() {
    return 'webkitSpeechRecognition' in window || 'SpeechRecognition' in window
  },
  
  // 检测语音合成支持
  isSpeechSynthesisSupported() {
    return 'speechSynthesis' in window
  },
  
  // 音频录制
  async startAudioRecording() {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      const mediaRecorder = new MediaRecorder(stream)
      const audioChunks = []
      
      mediaRecorder.ondataavailable = (event) => {
        audioChunks.push(event.data)
      }
      
      return {
        mediaRecorder,
        audioChunks,
        stream,
        stop: () => {
          return new Promise((resolve) => {
            mediaRecorder.onstop = () => {
              const audioBlob = new Blob(audioChunks, { type: 'audio/wav' })
              stream.getTracks().forEach(track => track.stop())
              resolve(audioBlob)
            }
            mediaRecorder.stop()
          })
        }
      }
    } catch (error) {
      console.error('音频录制失败:', error)
      throw error
    }
  },
  
  // 音频文件转换
  audioToBase64(audioBlob) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader()
      reader.onload = () => resolve(reader.result)
      reader.onerror = reject
      reader.readAsDataURL(audioBlob)
    })
  },
  
  // 分析音频特征
  async analyzeAudioFeatures(audioBlob) {
    try {
      const audioContext = new (window.AudioContext || window.webkitAudioContext)()
      const arrayBuffer = await audioBlob.arrayBuffer()
      const audioBuffer = await audioContext.decodeAudioData(arrayBuffer)
      
      const channelData = audioBuffer.getChannelData(0)
      
      // 计算音频特征
      const features = {
        duration: audioBuffer.duration,
        sampleRate: audioBuffer.sampleRate,
        volume: this.calculateVolume(channelData),
        energy: this.calculateEnergy(channelData),
        zeroCrossingRate: this.calculateZeroCrossingRate(channelData)
      }
      
      audioContext.close()
      return features
    } catch (error) {
      console.error('音频特征分析失败:', error)
      throw error
    }
  },
  
  // 计算音量
  calculateVolume(channelData) {
    let sum = 0
    for (let i = 0; i < channelData.length; i++) {
      sum += Math.abs(channelData[i])
    }
    return sum / channelData.length
  },
  
  // 计算能量
  calculateEnergy(channelData) {
    let sum = 0
    for (let i = 0; i < channelData.length; i++) {
      sum += channelData[i] * channelData[i]
    }
    return sum / channelData.length
  },
  
  // 计算过零率
  calculateZeroCrossingRate(channelData) {
    let crossings = 0
    for (let i = 1; i < channelData.length; i++) {
      if ((channelData[i] >= 0) !== (channelData[i - 1] >= 0)) {
        crossings++
      }
    }
    return crossings / channelData.length
  }
}

// 语音助手类（整合识别和合成）
export class VoiceAssistant {
  constructor(options = {}) {
    this.recognition = new SpeechRecognition(options.recognition)
    this.synthesis = new SpeechSynthesis(options.synthesis)
    this.isActive = false
    this.callbacks = {}
  }
  
  // 开始语音交互
  startConversation() {
    if (!this.recognition.isSupported) {
      throw new Error('语音识别不支持')
    }
    
    this.isActive = true
    
    this.recognition.on('result', (result) => {
      if (result.final) {
        this.emit('userSpoke', result.final)
      }
    })
    
    this.recognition.on('error', (error) => {
      this.emit('error', error)
    })
    
    this.recognition.start()
  }
  
  // 停止语音交互
  stopConversation() {
    this.isActive = false
    this.recognition.stop()
    this.synthesis.stop()
  }
  
  // AI 回复
  respond(text, options = {}) {
    if (this.synthesis.isSupported) {
      this.synthesis.speak(text, options)
    }
    this.emit('aiResponded', text)
  }
  
  // 事件监听
  on(event, callback) {
    if (!this.callbacks[event]) {
      this.callbacks[event] = []
    }
    this.callbacks[event].push(callback)
  }
  
  // 触发事件
  emit(event, data) {
    if (this.callbacks[event]) {
      this.callbacks[event].forEach(callback => callback(data))
    }
  }
}

export default {
  SpeechRecognition,
  SpeechSynthesis,
  VoiceAssistant,
  speechUtils
}
