/**
 * API 工具类
 * 封装所有与后端 API 的交互
 */

import axios from 'axios'
import { useUserStore } from '@/stores/user'

// 创建 axios 实例
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    const userStore = useUserStore()
    
    // 添加认证 token
    if (userStore.token) {
      config.headers.Authorization = `Bearer ${userStore.token}`
    }
    
    // 添加请求 ID 用于追踪
    config.headers['X-Request-ID'] = generateRequestId()
    
    // 添加年龄段信息
    if (userStore.ageGroup) {
      config.headers['X-Age-Group'] = userStore.ageGroup
    }
    
    console.log('API 请求:', config.method?.toUpperCase(), config.url, config.data)
    return config
  },
  (error) => {
    console.error('请求拦截器错误:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    console.log('API 响应:', response.status, response.config.url, response.data)
    return response
  },
  async (error) => {
    const userStore = useUserStore()
    
    console.error('API 错误:', error.response?.status, error.config?.url, error.response?.data)
    
    // 处理认证错误
    if (error.response?.status === 401) {
      // 如果是logout接口，直接跳转登录页，不尝试刷新token
      if (error.config?.url?.includes('/logout/')) {
        userStore.logout()
        window.location.href = '/login'
        return Promise.reject(new Error('登录已过期，请重新登录'))
      }
      
      // 尝试刷新token
      const refreshResult = await userStore.refreshAuthToken()
      if (refreshResult.success) {
        // 刷新成功，重试原请求
        const originalRequest = error.config
        originalRequest.headers.Authorization = `Bearer ${userStore.token}`
        return api(originalRequest)
      } else {
        // 刷新失败，跳转到登录页
        userStore.logout()
        window.location.href = '/login'
        return Promise.reject(new Error('登录已过期，请重新登录'))
      }
    }
    
    // 处理服务器错误
    if (error.response?.status >= 500) {
      if (window.$notification) {
        window.$notification.error('服务器暂时不可用，请稍后重试')
      }
    }
    
    // 处理网络错误
    if (error.code === 'NETWORK_ERROR' || error.message.includes('Network Error')) {
      if (window.$notification) {
        window.$notification.error('网络连接失败，请检查网络设置')
      }
    }
    
    return Promise.reject(error)
  }
)

// 生成请求 ID
function generateRequestId() {
  return Date.now().toString(36) + Math.random().toString(36).substr(2)
}

// 用户相关 API
export const userApi = {
  // 登录
  login: (credentials) => api.post('/v1/auth/login/', credentials),
  
  // 注册
  register: (userData) => api.post('/v1/auth/register/', userData),
  
  // 游客登录
  guestLogin: (guestData) => api.post('/v1/auth/guest-login/', guestData),
  
  // 刷新令牌
  refreshToken: (refreshToken) => api.post('/v1/auth/refresh/', { refresh: refreshToken }),
  
  // 登出
  logout: () => api.post('/v1/auth/logout/'),
  
  // 获取用户信息
  getProfile: () => api.get('/v1/user/profile/'),
  
  // 更新用户信息
  updateProfile: (profileData) => api.patch('/v1/user/profile/', profileData),
  
  // 获取用户统计
  getUserStats: () => api.get('/v1/user/stats/'),
  
  // 上传头像
  uploadAvatar: (formData) => api.post('/v1/user/avatar/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
  
  // 更新用户详细档案
  updateProfileDetail: (profileData) => api.patch('/v1/user/profile/detail/', profileData),
  
  // 修改密码
  changePassword: (passwordData) => api.post('/v1/user/change-password/', passwordData),
  
  // 注销账户
  deleteAccount: () => api.delete('/v1/user/account/')
}

// 对话相关 API
export const chatApi = {
  // 创建聊天会话
  createSession: (sessionData) => api.post('/v1/chat/sessions/', sessionData),
  
  // 获取会话列表
  getSessions: () => api.get('/v1/chat/sessions/'),
  
  // 获取会话详情
  getSession: (sessionId) => api.get(`/v1/chat/sessions/${sessionId}/`),
  
  // 删除会话
  deleteSession: (sessionId) => api.delete(`/v1/chat/sessions/${sessionId}/`),
  
  // 发送消息
  sendMessage: (messageData) => api.post('/v1/chat/send/', messageData),
  
  // 获取会话消息历史
  getSessionMessages: (sessionId) => api.get(`/v1/chat/sessions/${sessionId}/messages/`),
  
  // 清空所有聊天记录
  clearAllChatHistory: (data) => api.post('/v1/chat/clear/', data),
  
  // 获取消息列表
  getMessages: (params) => api.get('/v1/chat/messages/', { params }),
  
  // 删除消息
  deleteMessage: (messageId) => api.delete(`/v1/chat/messages/${messageId}/`),
  
  // 清空所有对话
  clearAllChats: () => api.delete('/v1/chat/sessions/'),
  
  // 导出对话记录
  exportChats: (format = 'json') => api.get(`/v1/chat/export?format=${format}`, {
    responseType: 'blob'
  }),

  // 发送反馈
  sendFeedback: (feedbackData) => api.post('/v1/chat/feedback/', feedbackData)
}

// 情绪分析相关 API
export const emotionApi = {
  // 分析文本情绪
  analyzeText: (text) => api.post('/v1/emotion/analyze/', { text }),
  
  // 分析语音情绪
  analyzeVoice: (audioData) => api.post('/v1/emotion/analyze/', audioData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
  
  // 获取情绪历史
  getEmotionHistory: (params) => api.get('/v1/emotion/history/', { params }),
  
  // 获取情绪统计
  getEmotionStats: (timeRange) => api.get(`/v1/emotion/stats/?range=${timeRange}`)
}

// 心理档案相关 API
export const profileApi = {
  // 获取心理档案
  getPsychProfile: () => api.get('/profile/psychological'),
  
  // 生成心理报告
  generateReport: (reportType) => api.post('/profile/generate-report', { reportType }),
  
  // 获取报告列表
  getReports: () => api.get('/profile/reports'),
  
  // 下载报告
  downloadReport: (reportId) => api.get(`/profile/reports/${reportId}/download`, {
    responseType: 'blob'
  })
}

// 紧急求助相关 API
export const emergencyApi = {
  // 触发紧急求助
  triggerEmergency: (emergencyData) => api.post('/v1/emergency/trigger/', emergencyData),
  
  // 获取紧急联系人
  getEmergencyContacts: () => api.get('/v1/emergency/contacts/'),
  
  // 添加紧急联系人
  addEmergencyContact: (contactData) => api.post('/v1/emergency/contacts/', contactData),
  
  // 更新紧急联系人
  updateEmergencyContact: (contactId, contactData) => 
    api.put(`/v1/emergency/contacts/${contactId}/`, contactData),
  
  // 删除紧急联系人
  deleteEmergencyContact: (contactId) => api.delete(`/v1/emergency/contacts/${contactId}/`)
}

// 系统相关 API
export const systemApi = {
  // 检查系统状态
  getStatus: () => api.get('/system/status'),
  
  // 获取应用配置
  getConfig: () => api.get('/system/config'),
  
  // 上报错误
  reportError: (errorData) => api.post('/system/error-report', errorData),
  
  // 发送反馈
  sendFeedback: (feedbackData) => api.post('/system/feedback', feedbackData),
  
  // 检查更新
  checkUpdate: () => api.get('/system/check-update')
}

// 工具函数
export const apiUtils = {
  // 处理文件上传
  uploadFile: async (file, endpoint, onProgress) => {
    const formData = new FormData()
    formData.append('file', file)
    
    return api.post(endpoint, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      onUploadProgress: (progressEvent) => {
        if (onProgress) {
          const percentCompleted = Math.round(
            (progressEvent.loaded * 100) / progressEvent.total
          )
          onProgress(percentCompleted)
        }
      }
    })
  },
  
  // 批量请求
  batchRequest: async (requests) => {
    try {
      const responses = await Promise.allSettled(requests)
      return responses.map((response, index) => ({
        index,
        status: response.status,
        data: response.status === 'fulfilled' ? response.value.data : null,
        error: response.status === 'rejected' ? response.reason : null
      }))
    } catch (error) {
      console.error('批量请求失败:', error)
      throw error
    }
  },
  
  // 重试请求
  retryRequest: async (requestFn, maxRetries = 3, delay = 1000) => {
    let lastError
    
    for (let i = 0; i < maxRetries; i++) {
      try {
        return await requestFn()
      } catch (error) {
        lastError = error
        
        if (i < maxRetries - 1) {
          console.log(`请求失败，${delay}ms 后重试... (${i + 1}/${maxRetries})`)
          await new Promise(resolve => setTimeout(resolve, delay))
          delay *= 2 // 指数退避
        }
      }
    }
    
    throw lastError
  }
}

// 离线支持
export const offlineApi = {
  // 缓存请求
  cacheRequest: (key, data, ttl = 3600000) => { // 默认1小时过期
    const cacheData = {
      data,
      timestamp: Date.now(),
      ttl
    }
    localStorage.setItem(`api_cache_${key}`, JSON.stringify(cacheData))
  },
  
  // 获取缓存
  getCachedData: (key) => {
    const cached = localStorage.getItem(`api_cache_${key}`)
    if (!cached) return null
    
    const cacheData = JSON.parse(cached)
    const now = Date.now()
    
    if (now - cacheData.timestamp > cacheData.ttl) {
      localStorage.removeItem(`api_cache_${key}`)
      return null
    }
    
    return cacheData.data
  },
  
  // 清除过期缓存
  clearExpiredCache: () => {
    const keys = Object.keys(localStorage).filter(key => key.startsWith('api_cache_'))
    const now = Date.now()
    
    keys.forEach(key => {
      const cached = localStorage.getItem(key)
      if (cached) {
        const cacheData = JSON.parse(cached)
        if (now - cacheData.timestamp > cacheData.ttl) {
          localStorage.removeItem(key)
        }
      }
    })
  }
}

export default api
