/**
 * 常量定义文件
 * 存放应用中使用的各种常量
 */

// 年龄段配置
export const AGE_GROUPS = {
  TEEN: 'teen',
  YOUNG: 'young', 
  MIDDLE: 'middle',
  ELDER: 'elder'
}

// 年龄段信息
export const AGE_GROUP_INFO = {
  [AGE_GROUPS.TEEN]: {
    name: '青少年',
    ageRange: '12-18岁',
    color: '#10b981',
    features: ['parentalControl', 'contentFilter', 'studySupport']
  },
  [AGE_GROUPS.YOUNG]: {
    name: '青年',
    ageRange: '19-35岁',
    color: '#3b82f6',
    features: ['careerSupport', 'relationshipAdvice', 'stressManagement']
  },
  [AGE_GROUPS.MIDDLE]: {
    name: '中年',
    ageRange: '36-59岁',
    color: '#8b5cf6',
    features: ['familyBalance', 'careerGuidance', 'healthCare']
  },
  [AGE_GROUPS.ELDER]: {
    name: '老年',
    ageRange: '60岁+',
    color: '#059669',
    features: ['voicePriority', 'largeText', 'familySupport']
  }
}

// 情绪类型
export const EMOTION_TYPES = {
  HAPPY: 'happy',
  NEUTRAL: 'neutral',
  SAD: 'sad',
  ANXIOUS: 'anxious',
  ANGRY: 'angry',
  EXCITED: 'excited',
  DEPRESSED: 'depressed',
  CONFUSED: 'confused'
}

// 情绪信息
export const EMOTION_INFO = {
  [EMOTION_TYPES.HAPPY]: {
    name: '开心',
    color: '#10b981',
    bgColor: 'bg-green-500',
    textColor: 'text-green-500',
    icon: '😊'
  },
  [EMOTION_TYPES.NEUTRAL]: {
    name: '平静',
    color: '#6b7280',
    bgColor: 'bg-gray-500',
    textColor: 'text-gray-500',
    icon: '😐'
  },
  [EMOTION_TYPES.SAD]: {
    name: '难过',
    color: '#3b82f6',
    bgColor: 'bg-blue-500',
    textColor: 'text-blue-500',
    icon: '😢'
  },
  [EMOTION_TYPES.ANXIOUS]: {
    name: '焦虑',
    color: '#f59e0b',
    bgColor: 'bg-yellow-500',
    textColor: 'text-yellow-500',
    icon: '😰'
  },
  [EMOTION_TYPES.ANGRY]: {
    name: '愤怒',
    color: '#ef4444',
    bgColor: 'bg-red-500',
    textColor: 'text-red-500',
    icon: '😠'
  },
  [EMOTION_TYPES.EXCITED]: {
    name: '兴奋',
    color: '#f97316',
    bgColor: 'bg-orange-500',
    textColor: 'text-orange-500',
    icon: '🤩'
  },
  [EMOTION_TYPES.DEPRESSED]: {
    name: '抑郁',
    color: '#6366f1',
    bgColor: 'bg-indigo-500',
    textColor: 'text-indigo-500',
    icon: '😔'
  },
  [EMOTION_TYPES.CONFUSED]: {
    name: '困惑',
    color: '#8b5cf6',
    bgColor: 'bg-purple-500',
    textColor: 'text-purple-500',
    icon: '😕'
  }
}

// 消息类型
export const MESSAGE_TYPES = {
  USER: 'user',
  AI: 'ai',
  SYSTEM: 'system',
  NOTIFICATION: 'notification'
}

// 危机关键词
export const CRISIS_KEYWORDS = [
  '想死', '自杀', '结束生命', '不想活', '活着没意思',
  '自伤', '自残', '伤害自己', '想消失', '解脱',
  '没有希望', '绝望', '痛苦', '受不了', '崩溃',
  '割腕', '跳楼', '上吊', '服毒', '轻生'
]

// 紧急联系方式
export const EMERGENCY_CONTACTS = {
  CRISIS_HOTLINE: '400-161-9995',
  SUICIDE_PREVENTION: '400-161-9995',
  MENTAL_HEALTH: '12320',
  POLICE: '110',
  AMBULANCE: '120'
}

// 应用配置
export const APP_CONFIG = {
  NAME: 'Omnisolace',
  VERSION: '1.0.0',
  DESCRIPTION: '全年龄段AI心理疏导机器人',
  AUTHOR: 'Omnisolace Team',
  SUPPORT_EMAIL: 'support@omnisolace.com',
  WEBSITE: 'https://www.omnisolace.com'
}

// 存储键名
export const STORAGE_KEYS = {
  USER_TOKEN: 'omnisolace_token',
  USER_INFO: 'omnisolace_user',
  AGE_GROUP: 'omnisolace_age_group',
  THEME: 'omnisolace_theme',
  SETTINGS: 'omnisolace_settings',
  CHAT_HISTORY: 'omnisolace_chat_history',
  EMOTION_HISTORY: 'omnisolace_emotion_history',
  PARENTAL_MODE: 'omnisolace_parental_mode'
}

// API 端点
export const API_ENDPOINTS = {
  AUTH: {
    LOGIN: '/v1/auth/login/',
    REGISTER: '/v1/auth/register/',
    LOGOUT: '/v1/auth/logout/',
    REFRESH: '/v1/auth/refresh/'
  },
  USER: {
    PROFILE: '/v1/user/profile/',
    AVATAR: '/v1/user/avatar/',
    SETTINGS: '/v1/user/settings/',
    DELETE: '/v1/user/delete/'
  },
  CHAT: {
    SEND: '/v1/chat/send/',
    HISTORY: '/v1/chat/history/',
    DELETE: '/v1/chat/delete/',
    CLEAR: '/v1/chat/clear/',
    EXPORT: '/v1/chat/export/',
    FEEDBACK: '/v1/chat/feedback/'
  },
  EMOTION: {
    ANALYZE: '/v1/emotion/analyze/',
    HISTORY: '/v1/emotion/history/',
    STATS: '/v1/emotion/stats/'
  },
  EMERGENCY: {
    TRIGGER: '/v1/emergency/trigger/',
    CONTACTS: '/v1/emergency/contacts/'
  }
}

// 文件配置
export const FILE_CONFIG = {
  MAX_SIZE: 10 * 1024 * 1024, // 10MB
  ALLOWED_TYPES: {
    IMAGE: ['image/jpeg', 'image/png', 'image/gif', 'image/webp'],
    AUDIO: ['audio/wav', 'audio/mp3', 'audio/ogg', 'audio/webm'],
    DOCUMENT: ['application/pdf', 'text/plain']
  }
}

// 主题配置
export const THEME_CONFIG = {
  DEFAULT: 'light',
  AVAILABLE: ['light', 'dark', 'elder', 'teen'],
  COLORS: {
    light: {
      primary: '#3b82f6',
      secondary: '#6b7280',
      background: '#ffffff',
      surface: '#f9fafb'
    },
    dark: {
      primary: '#60a5fa',
      secondary: '#9ca3af',
      background: '#111827',
      surface: '#1f2937'
    },
    elder: {
      primary: '#059669',
      secondary: '#6b7280',
      background: '#ffffff',
      surface: '#f3f4f6'
    },
    teen: {
      primary: '#10b981',
      secondary: '#f59e0b',
      background: '#ffffff',
      surface: '#ecfdf5'
    }
  }
}

// 语音配置
export const SPEECH_CONFIG = {
  RECOGNITION: {
    LANG: 'zh-CN',
    CONTINUOUS: false,
    INTERIM_RESULTS: true,
    MAX_ALTERNATIVES: 1
  },
  SYNTHESIS: {
    LANG: 'zh-CN',
    RATE: 0.9,
    PITCH: 1,
    VOLUME: 1
  },
  ELDER_MODE: {
    RATE: 0.8,
    PITCH: 1.1,
    VOLUME: 1
  }
}

// 缓存配置
export const CACHE_CONFIG = {
  TTL: {
    SHORT: 5 * 60 * 1000,      // 5分钟
    MEDIUM: 30 * 60 * 1000,    // 30分钟
    LONG: 24 * 60 * 60 * 1000, // 24小时
    WEEK: 7 * 24 * 60 * 60 * 1000 // 7天
  },
  KEYS: {
    USER_PROFILE: 'user_profile',
    EMOTION_STATS: 'emotion_stats',
    CHAT_HISTORY: 'chat_history',
    SYSTEM_CONFIG: 'system_config'
  }
}

// 验证规则
export const VALIDATION_RULES = {
  PASSWORD: {
    MIN_LENGTH: 6,
    MAX_LENGTH: 128,
    REQUIRE_NUMBER: true,
    REQUIRE_LETTER: true
  },
  PHONE: {
    PATTERN: /^1[3-9]\d{9}$/,
    LENGTH: 11
  },
  EMAIL: {
    PATTERN: /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  },
  NAME: {
    MIN_LENGTH: 1,
    MAX_LENGTH: 50
  }
}

// 分页配置
export const PAGINATION_CONFIG = {
  DEFAULT_PAGE_SIZE: 20,
  MAX_PAGE_SIZE: 100,
  PAGE_SIZE_OPTIONS: [10, 20, 50, 100]
}

// 通知配置
export const NOTIFICATION_CONFIG = {
  DURATION: {
    SHORT: 2000,
    MEDIUM: 5000,
    LONG: 10000
  },
  TYPES: {
    SUCCESS: 'success',
    ERROR: 'error',
    WARNING: 'warning',
    INFO: 'info'
  }
}

// 路由配置
export const ROUTE_CONFIG = {
  PUBLIC_ROUTES: ['/login', '/404'],
  PROTECTED_ROUTES: ['/', '/chat', '/profile'],
  REDIRECT_AFTER_LOGIN: '/',
  REDIRECT_AFTER_LOGOUT: '/login'
}

// 错误代码
export const ERROR_CODES = {
  NETWORK_ERROR: 'NETWORK_ERROR',
  AUTH_FAILED: 'AUTH_FAILED',
  PERMISSION_DENIED: 'PERMISSION_DENIED',
  VALIDATION_ERROR: 'VALIDATION_ERROR',
  SERVER_ERROR: 'SERVER_ERROR',
  NOT_FOUND: 'NOT_FOUND',
  RATE_LIMITED: 'RATE_LIMITED'
}

// 功能开关
export const FEATURE_FLAGS = {
  ENABLE_VOICE_RECOGNITION: true,
  ENABLE_EMOTION_ANALYSIS: true,
  ENABLE_CRISIS_DETECTION: true,
  ENABLE_PARENTAL_CONTROL: true,
  ENABLE_OFFLINE_MODE: true,
  ENABLE_PUSH_NOTIFICATIONS: true,
  ENABLE_DATA_EXPORT: true
}

export default {
  AGE_GROUPS,
  AGE_GROUP_INFO,
  EMOTION_TYPES,
  EMOTION_INFO,
  MESSAGE_TYPES,
  CRISIS_KEYWORDS,
  EMERGENCY_CONTACTS,
  APP_CONFIG,
  STORAGE_KEYS,
  API_ENDPOINTS,
  FILE_CONFIG,
  THEME_CONFIG,
  SPEECH_CONFIG,
  CACHE_CONFIG,
  VALIDATION_RULES,
  PAGINATION_CONFIG,
  NOTIFICATION_CONFIG,
  ROUTE_CONFIG,
  ERROR_CODES,
  FEATURE_FLAGS
}
