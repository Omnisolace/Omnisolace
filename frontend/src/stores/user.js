import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { userApi } from '@/utils/api'
import { t } from './language'

export const useUserStore = defineStore('user', () => {
  // 状态
  const user = ref(null)
  const token = ref(localStorage.getItem('token') || null)
  const ageGroup = ref(localStorage.getItem('ageGroup') || null) // 年龄段: teen/young/middle/elder
  const theme = ref(localStorage.getItem('theme') || 'default') // 主题模式
  const colorTheme = ref(localStorage.getItem('colorTheme') || 'warmOrange') // 色彩主题
  const isParentalMode = ref(JSON.parse(localStorage.getItem('isParentalMode') || 'false')) // 家长监督模式
  
  // 计算属性
  const isAuthenticated = computed(() => !!token.value && !!user.value)
  
  const userAgeConfig = computed(() => {
    const configs = {
      teen: {
        name: '青少年',
        ageRange: '12-18岁',
        theme: 'teen-mode',
        fontSize: 'text-base',
        buttonSize: 'px-4 py-2',
        features: ['parentalControl', 'contentFilter', 'studySupport']
      },
      young: {
        name: '青年',
        ageRange: '19-35岁',
        theme: 'young-mode',
        fontSize: 'text-base',
        buttonSize: 'px-4 py-2',
        features: ['careerSupport', 'relationshipAdvice', 'stressManagement']
      },
      middle: {
        name: '中年',
        ageRange: '36-59岁',
        theme: 'middle-mode',
        fontSize: 'text-base',
        buttonSize: 'px-4 py-2',
        features: ['familyBalance', 'careerGuidance', 'healthCare']
      },
      elder: {
        name: '老年',
        ageRange: '60岁+',
        theme: 'elder-mode',
        fontSize: 'text-elder-base',
        buttonSize: 'px-6 py-4 min-h-[60px]',
        features: ['voicePriority', 'largeText', 'familySupport']
      }
    }
    return configs[ageGroup.value] || configs.young
  })
  
  const isElderMode = computed(() => ageGroup.value === 'elder')
  const isTeenMode = computed(() => ageGroup.value === 'teen')
  
  // 主题色配置
  const colorThemes = computed(() => ({
    warmOrange: {
      name: t('warmOrange'),
      description: t('warmOrangeDesc'),
      primary: '#FFA84A',
      secondary: '#FFD29D',
      accent: '#E67E22',
      background: '#FFF8F0',
      text: '#664E33',
      cssVars: {
        '--color-primary': '#FFA84A',
        '--color-primary-50': '#FFF8F0',
        '--color-primary-100': '#FFE8CC',
        '--color-primary-500': '#FFA84A',
        '--color-primary-600': '#E67E22',
        '--color-secondary': '#FFD29D',
        '--color-accent': '#E67E22',
        '--color-background': '#FFF8F0',
        '--color-text': '#664E33'
      }
    },
    softPinkBrown: {
      name: t('softPinkBrown'),
      description: t('softPinkBrownDesc'),
      primary: '#D4B499',
      secondary: '#F3D9C6',
      accent: '#A67C52',
      background: '#FCF7F4',
      text: '#5D4A36',
      cssVars: {
        '--color-primary': '#D4B499',
        '--color-primary-50': '#FCF7F4',
        '--color-primary-100': '#F3D9C6',
        '--color-primary-500': '#D4B499',
        '--color-primary-600': '#A67C52',
        '--color-secondary': '#F3D9C6',
        '--color-accent': '#A67C52',
        '--color-background': '#FCF7F4',
        '--color-text': '#5D4A36'
      }
    },
    amberYellow: {
      name: t('amberYellow'),
      description: t('amberYellowDesc'),
      primary: '#F5C745',
      secondary: '#FFE8A3',
      accent: '#DBA82C',
      background: '#FFFDF5',
      text: '#705A2E',
      cssVars: {
        '--color-primary': '#F5C745',
        '--color-primary-50': '#FFFDF5',
        '--color-primary-100': '#FFE8A3',
        '--color-primary-500': '#F5C745',
        '--color-primary-600': '#DBA82C',
        '--color-secondary': '#FFE8A3',
        '--color-accent': '#DBA82C',
        '--color-background': '#FFFDF5',
        '--color-text': '#705A2E'
      }
    },
    caramelBrown: {
      name: t('caramelBrown'),
      description: t('caramelBrownDesc'),
      primary: '#C18A50',
      secondary: '#E8C39E',
      accent: '#8B5A2B',
      background: '#F7F1E7',
      text: '#5A4027',
      cssVars: {
        '--color-primary': '#C18A50',
        '--color-primary-50': '#F7F1E7',
        '--color-primary-100': '#E8C39E',
        '--color-primary-500': '#C18A50',
        '--color-primary-600': '#8B5A2B',
        '--color-secondary': '#E8C39E',
        '--color-accent': '#8B5A2B',
        '--color-background': '#F7F1E7',
        '--color-text': '#5A4027'
      }
    },
    cherryPink: {
      name: t('cherryPink'),
      description: t('cherryPinkDesc'),
      primary: '#FFB7C5',
      secondary: '#FFE0E9',
      accent: '#E68598',
      background: '#FFFBFC',
      text: '#6D5A5A',
      cssVars: {
        '--color-primary': '#FFB7C5',
        '--color-primary-50': '#FFFBFC',
        '--color-primary-100': '#FFE0E9',
        '--color-primary-500': '#FFB7C5',
        '--color-primary-600': '#E68598',
        '--color-secondary': '#FFE0E9',
        '--color-accent': '#E68598',
        '--color-background': '#FFFBFC',
        '--color-text': '#6D5A5A'
      }
    }
  }))
  
  // 当前主题色配置
  const currentColorTheme = computed(() => colorThemes.value[colorTheme.value] || colorThemes.value.warmOrange)
  
  // 方法
  const login = (userData, authToken) => {
    user.value = userData
    token.value = authToken
    localStorage.setItem('token', authToken)
    localStorage.setItem('user', JSON.stringify(userData))
  }
  
  const logout = async () => {
    console.log('🚪 开始登出流程...')
    
    // 直接清除本地数据
    // 不调用后端API，因为token可能已过期
    console.log('🧹 清除本地认证数据...')
    
    // 先清除状态，确保 isAuthenticated 立即变为 false
    user.value = null
    token.value = null
    ageGroup.value = null
    theme.value = 'light'
    isParentalMode.value = false
    
    // 清除所有本地存储
    localStorage.removeItem('token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user')
    localStorage.removeItem('ageGroup')
    localStorage.removeItem('theme')
    localStorage.removeItem('isParentalMode')
    
    // 清除会话存储
    sessionStorage.clear()
    
    console.log('✅ 登出完成 - 本地数据已清除')
    
    // 不在这里处理导航，让调用方处理
    // 这样可以避免路由冲突和硬跳转问题
  }
  
  // 真实API登录方法
  const apiLogin = async (credentials) => {
    try {
      const response = await userApi.login(credentials)
      const { user: userData, tokens } = response.data.data
      const { access, refresh } = tokens
      
      // 存储token和用户信息
      token.value = access
      user.value = userData
      localStorage.setItem('token', access)
      localStorage.setItem('refresh_token', refresh)
      localStorage.setItem('user', JSON.stringify(userData))
      
      return { 
        success: true, 
        data: {
          user: userData,
          access,
          refresh
        }
      }
    } catch (error) {
      console.error('登录失败:', error)
      return { 
        success: false, 
        error: error.response?.data?.message || '登录失败，请检查手机号和密码' 
      }
    }
  }
  
  // 真实API注册方法
  const apiRegister = async (userData) => {
    try {
      const response = await userApi.register(userData)
      const { user: newUser, tokens } = response.data.data
      const { access, refresh } = tokens
      
      // 存储token和用户信息
      token.value = access
      user.value = newUser
      localStorage.setItem('token', access)
      localStorage.setItem('refresh_token', refresh)
      localStorage.setItem('user', JSON.stringify(newUser))
      
      return { 
        success: true, 
        data: {
          user: newUser,
          access,
          refresh
        }
      }
    } catch (error) {
      console.error('注册失败:', error)
      return { 
        success: false, 
        error: error.response?.data?.message || '注册失败，请检查输入信息' 
      }
    }
  }
  
  // 游客登录方法
  const apiGuestLogin = async (guestData) => {
    try {
      const response = await userApi.guestLogin(guestData)
      const { user: guestUser, tokens } = response.data.data
      const { access, refresh } = tokens
      
      // 存储token和用户信息
      token.value = access
      user.value = guestUser
      localStorage.setItem('token', access)
      localStorage.setItem('refresh_token', refresh)
      localStorage.setItem('user', JSON.stringify(guestUser))
      
      return { 
        success: true, 
        data: {
          user: guestUser,
          access,
          refresh
        }
      }
    } catch (error) {
      console.error('游客登录失败:', error)
      return { 
        success: false, 
        error: error.response?.data?.message || '游客登录失败' 
      }
    }
  }
  
  // 刷新token方法
  const refreshAuthToken = async () => {
    try {
      const refreshToken = localStorage.getItem('refresh_token')
      if (!refreshToken) {
        console.warn('没有刷新token，无法自动刷新')
        return { success: false, error: '没有刷新token' }
      }
      
      console.log('🔄 尝试刷新token...')
      const response = await userApi.refreshToken(refreshToken)
      const { access } = response.data
      
      token.value = access
      localStorage.setItem('token', access)
      
      console.log('✅ Token刷新成功')
      return { success: true, token: access }
    } catch (error) {
      console.error('❌ 刷新token失败:', error)
      // 刷新失败，清除所有认证信息
      await logout()
      return { success: false, error: '认证已过期，请重新登录' }
    }
  }
  
  const setAgeGroup = (group) => {
    ageGroup.value = group
    localStorage.setItem('ageGroup', group)
  }
  
  const setTheme = (newTheme) => {
    theme.value = newTheme
    localStorage.setItem('theme', newTheme)
  }
  
  const setColorTheme = (newColorTheme) => {
    colorTheme.value = newColorTheme
    localStorage.setItem('colorTheme', newColorTheme)
    // 应用CSS变量到根元素
    applyThemeColors()
  }
  
  const applyThemeColors = () => {
    const root = document.documentElement
    const theme = currentColorTheme.value
    Object.entries(theme.cssVars).forEach(([key, value]) => {
      root.style.setProperty(key, value)
    })
  }
  
  const toggleParentalMode = () => {
    isParentalMode.value = !isParentalMode.value
    localStorage.setItem('isParentalMode', JSON.stringify(isParentalMode.value))
  }
  
  const updateUserProfile = async (profileData) => {
    try {
      // 调用后端API更新用户信息
      const response = await userApi.updateProfile(profileData)
      
      if (response.data.success) {
        // 更新本地用户数据
        user.value = { ...user.value, ...response.data.data }
        localStorage.setItem('user', JSON.stringify(user.value))
        return { success: true, data: response.data.data }
      } else {
        throw new Error(response.data.message || '更新失败')
      }
    } catch (error) {
      console.error('更新用户信息失败:', error)
      throw error
    }
  }

  const updateAvatar = async (avatarUrl) => {
    try {
      // 创建新的用户对象以确保响应式更新
      user.value = { ...user.value, avatar: avatarUrl }
      localStorage.setItem('user', JSON.stringify(user.value))
      return { success: true }
    } catch (error) {
      console.error('更新头像失败:', error)
      throw error
    }
  }

  const fetchUserProfile = async () => {
    try {
      // 从后端获取最新的用户信息
      const response = await userApi.getProfile()
      
      if (response.data) {
        // 更新本地用户数据
        user.value = { ...user.value, ...response.data }
        localStorage.setItem('user', JSON.stringify(user.value))
        return { success: true, data: response.data }
      } else {
        throw new Error('获取用户信息失败')
      }
    } catch (error) {
      console.error('获取用户信息失败:', error)
      throw error
    }
  }
  
  // 初始化用户数据（从localStorage恢复）
  const initializeUser = () => {
    const savedUser = localStorage.getItem('user')
    if (savedUser && token.value) {
      try {
        user.value = JSON.parse(savedUser)
      } catch (error) {
        console.error('解析用户数据失败:', error)
        logout()
      }
    } else {
      // 如果没有有效的用户数据，确保用户状态为未认证
      user.value = null
      token.value = null
    }
  }
  
  return {
    // 状态
    user,
    token,
    ageGroup,
    theme,
    colorTheme,
    isParentalMode,
    
    // 计算属性
    isAuthenticated,
    userAgeConfig,
    isElderMode,
    isTeenMode,
    colorThemes,
    currentColorTheme,
    
    // 方法
    login,
    logout,
    apiLogin,
    apiRegister,
    apiGuestLogin,
    refreshAuthToken,
    setAgeGroup,
    setTheme,
    setColorTheme,
    applyThemeColors,
    toggleParentalMode,
    updateUserProfile,
    updateAvatar,
    fetchUserProfile,
    initializeUser
  }
})
