<template>
  <div class="fixed inset-0 z-50 overflow-y-auto">
    <!-- 遮罩层 -->
    <div class="fixed inset-0 bg-black bg-opacity-50 transition-opacity" @click="closeModal"></div>
    
    <!-- 模态框内容 -->
    <div class="flex min-h-full items-center justify-center p-4">
      <div class="relative bg-white rounded-2xl shadow-xl w-full max-w-md mx-auto transform transition-all"
           :class="{ 'scale-95 opacity-0': !isVisible, 'scale-100 opacity-100': isVisible }">
        
        <!-- 头部 -->
        <div class="flex items-center justify-between p-6 border-b border-gray-200">
          <div class="flex items-center space-x-3">
            <div class="w-10 h-10 bg-red-100 rounded-full flex items-center justify-center">
              <ExclamationTriangleIcon class="h-6 w-6 text-red-600" />
            </div>
            <div>
              <h3 class="text-lg font-semibold text-gray-900"
                  :class="{ 'text-elder-lg': userStore.isElderMode }">
                {{ t('clearChatRecords') }}
              </h3>
              <p class="text-sm text-red-600 mt-1"
                 :class="{ 'text-elder-sm': userStore.isElderMode }">
                {{ t('clearChatWarning') }}
              </p>
            </div>
          </div>
          <button
            @click="closeModal"
            class="text-gray-400 hover:text-gray-600 transition-colors"
            :class="{ 'p-2': userStore.isElderMode }"
          >
            <XMarkIcon class="h-5 w-5" :class="{ 'h-6 w-6': userStore.isElderMode }" />
          </button>
        </div>
        
        <!-- 内容 -->
        <div class="p-6 space-y-6">
          <!-- 警告信息 -->
          <div class="bg-red-50 border border-red-200 rounded-lg p-4">
            <div class="flex">
              <ExclamationTriangleIcon class="h-5 w-5 text-red-400 mt-0.5" />
              <div class="ml-3">
                <h4 class="text-sm font-medium text-red-800"
                    :class="{ 'text-elder-base': userStore.isElderMode }">
                  {{ t('clearChatNotice') }}
                </h4>
                <p class="text-sm text-red-700 mt-1"
                   :class="{ 'text-elder-sm': userStore.isElderMode }">
                  {{ t('clearChatNoticeDesc') }}
                </p>
              </div>
            </div>
          </div>
          
          <!-- 密码输入 -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2"
                   :class="{ 'text-elder-base': userStore.isElderMode }">
              {{ t('enterPassword') }}
            </label>
            <div class="relative">
              <input
                v-model="password"
                :type="showPassword ? 'text' : 'password'"
                :placeholder="t('enterPasswordPlaceholder')"
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent transition-colors"
                :class="{ 
                  'text-elder-base py-4': userStore.isElderMode,
                  'border-red-300 focus:ring-red-500': passwordError
                }"
                :disabled="isLoading"
              />
              <button
                @click="showPassword = !showPassword"
                class="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
                :class="{ 'p-2': userStore.isElderMode }"
              >
                <EyeIcon v-if="!showPassword" class="h-5 w-5" :class="{ 'h-6 w-6': userStore.isElderMode }" />
                <EyeSlashIcon v-else class="h-5 w-5" :class="{ 'h-6 w-6': userStore.isElderMode }" />
              </button>
            </div>
            <p v-if="passwordError" class="text-sm text-red-600 mt-1"
               :class="{ 'text-elder-sm': userStore.isElderMode }">
              {{ passwordError }}
            </p>
          </div>
          
          <!-- 确认语句输入 -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2"
                   :class="{ 'text-elder-base': userStore.isElderMode }">
              {{ t('confirmStatement') }}
            </label>
            <div class="bg-gray-50 border border-gray-200 rounded-lg p-3 mb-3">
              <p class="text-sm text-gray-600 font-mono"
                 :class="{ 'text-elder-sm': userStore.isElderMode }">
                {{ getConfirmStatementTemplate() }}
              </p>
            </div>
            <textarea
              v-model="confirmStatement"
              :placeholder="t('confirmStatementPlaceholder')"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent transition-colors resize-none"
              :class="{ 
                'text-elder-base py-4': userStore.isElderMode,
                'border-red-300 focus:ring-red-500': statementError
              }"
              rows="3"
              :disabled="isLoading"
            ></textarea>
            <p v-if="statementError" class="text-sm text-red-600 mt-1"
               :class="{ 'text-elder-sm': userStore.isElderMode }">
              {{ statementError }}
            </p>
          </div>
        </div>
        
        <!-- 底部按钮 -->
        <div class="flex items-center justify-end space-x-3 p-6 border-t border-gray-200 bg-gray-50 rounded-b-2xl">
          <button
            @click="closeModal"
            :disabled="isLoading"
            class="px-6 py-3 text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors disabled:opacity-50"
            :class="{ 'px-8 py-4 text-elder-base': userStore.isElderMode }"
          >
            {{ t('cancel') }}
          </button>
          <button
            @click="handleConfirm"
            :disabled="!canConfirm || isLoading"
            class="px-6 py-3 text-white bg-red-600 rounded-lg hover:bg-red-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
            :class="{ 'px-8 py-4 text-elder-base': userStore.isElderMode }"
          >
            <div v-if="isLoading" class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
            <span>{{ t('confirm') }}</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, nextTick, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { useChatStore } from '@/stores/chat'
import { t } from '@/stores/language'
import { chatApi } from '@/utils/api'
import {
  XMarkIcon,
  ExclamationTriangleIcon,
  EyeIcon,
  EyeSlashIcon
} from '@heroicons/vue/24/outline'

const emit = defineEmits(['close', 'success'])

const userStore = useUserStore()
const chatStore = useChatStore()

// 响应式状态
const isVisible = ref(false)
const password = ref('')
const confirmStatement = ref('')
const showPassword = ref(false)
const isLoading = ref(false)
const passwordError = ref('')
const statementError = ref('')

// 计算属性
const canConfirm = computed(() => {
  return password.value.trim() && 
         confirmStatement.value.trim() && 
         !passwordError.value && 
         !statementError.value
})

// 监听器
watch(password, () => {
  passwordError.value = ''
})

watch(confirmStatement, () => {
  statementError.value = ''
})

// 方法
const closeModal = () => {
  if (isLoading.value) return
  emit('close')
}

const validatePassword = () => {
  if (!password.value.trim()) {
    passwordError.value = t('passwordRequired')
    return false
  }
  return true
}

const getConfirmStatementTemplate = () => {
  const username = userStore.user?.nickname || userStore.user?.username || t('user')
  const template = t('confirmStatementTemplate')
  return template.replace('{0}', username)
}

const validateStatement = () => {
  const expectedStatement = getConfirmStatementTemplate()
  
  if (!confirmStatement.value.trim()) {
    statementError.value = t('statementRequired')
    return false
  }
  
  if (confirmStatement.value.trim() !== expectedStatement) {
    statementError.value = t('statementIncorrect')
    return false
  }
  
  return true
}

const handleConfirm = async () => {
  if (!canConfirm.value || isLoading.value) return
  
  // 验证密码
  const isPasswordValid = validatePassword()
  if (!isPasswordValid) return
  
  // 验证确认语句
  const isStatementValid = validateStatement()
  if (!isStatementValid) return
  
  isLoading.value = true
  
  try {
    // 调用后端API清空聊天记录
    await chatApi.clearAllChatHistory({
      password: password.value,
      confirm_statement: confirmStatement.value
    })
    
    // 清空前端store数据
    chatStore.chatHistory = []
    chatStore.messages = []
    chatStore.currentChatId = null
    
    // 显示成功提示
    if (window.$notification) {
      window.$notification.success(t('chatRecordsCleared'))
    }
    
    // 触发成功事件
    emit('success')
    emit('close')
    
  } catch (error) {
    console.error('清空聊天记录失败:', error)
    
    if (error.response?.status === 401) {
      passwordError.value = t('passwordIncorrect')
    } else if (error.response?.status === 400) {
      if (error.response.data?.message?.includes('密码')) {
        passwordError.value = t('passwordIncorrect')
      } else if (error.response.data?.message?.includes('确认语句')) {
        statementError.value = t('statementIncorrect')
      } else {
        statementError.value = t('statementIncorrect')
      }
    } else {
      if (window.$notification) {
        window.$notification.error(t('clearChatFailed'))
      }
    }
  } finally {
    isLoading.value = false
  }
}

// 组件挂载时显示模态框
onMounted(() => {
  isVisible.value = true
  // 重置表单
  password.value = ''
  confirmStatement.value = ''
  passwordError.value = ''
  statementError.value = ''
  showPassword.value = false
  isLoading.value = false
})
</script>

<style scoped>
/* 动画效果 */
.transform {
  transition: all 0.3s ease-out;
}

/* 加载动画 */
@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.animate-spin {
  animation: spin 1s linear infinite;
}
</style>
