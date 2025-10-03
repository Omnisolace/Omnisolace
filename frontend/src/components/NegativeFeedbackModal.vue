<template>
  <Teleport to="body">
    <div v-if="isVisible" class="fixed inset-0 z-50 overflow-hidden">
      <!-- 遮罩层 -->
      <div 
        class="absolute inset-0 bg-black bg-opacity-50 transition-opacity duration-300"
        @click="closeModal"
      ></div>
      
      <!-- 模态框内容 -->
      <div class="absolute inset-0 flex items-center justify-center p-4">
        <div 
          class="bg-white rounded-2xl shadow-2xl max-w-md w-full max-h-[90vh] overflow-y-auto transform transition-all duration-300"
          :class="isVisible ? 'scale-100 opacity-100' : 'scale-95 opacity-0'"
          @click.stop
        >
          <!-- 头部 -->
          <div class="flex items-center justify-between p-6 border-b border-gray-100">
            <h3 class="text-lg font-semibold text-gray-900" :class="{ 'text-elder-lg': userStore.isElderMode }">
              {{ t('negativeFeedbackTitle') }}
            </h3>
            <button
              @click="closeModal"
              class="p-2 text-gray-400 hover:text-gray-600 rounded-lg hover:bg-gray-100 transition-colors duration-200"
              :class="{ 'p-3': userStore.isElderMode }"
            >
              <XMarkIcon class="h-5 w-5" :class="{ 'h-6 w-6': userStore.isElderMode }" />
            </button>
          </div>
          
          <!-- 内容区域 -->
          <div class="p-6">
            <!-- 反馈类别 -->
            <div class="space-y-4">
              <!-- 针对回答 -->
              <div>
                <h4 class="text-sm font-medium text-gray-700 mb-3" :class="{ 'text-elder-sm': userStore.isElderMode }">
                  {{ t('regardingAnswer') }}
                </h4>
                <div class="grid grid-cols-2 gap-2">
                  <button
                    v-for="option in answerOptions"
                    :key="option.id"
                    @click="selectOption('answer', option.id)"
                    class="p-3 text-left rounded-lg border-2 transition-all duration-200"
                    :class="[
                      selectedOptions.answer === option.id
                        ? 'border-red-500 bg-red-50 text-red-700'
                        : 'border-gray-200 bg-gray-50 text-gray-700 hover:border-gray-300 hover:bg-gray-100',
                      { 'p-4 text-elder-base': userStore.isElderMode }
                    ]"
                  >
                    {{ option.text }}
                  </button>
                </div>
              </div>
              
              <!-- 针对格式 -->
              <div>
                <h4 class="text-sm font-medium text-gray-700 mb-3" :class="{ 'text-elder-sm': userStore.isElderMode }">
                  {{ t('regardingFormat') }}
                </h4>
                <div class="grid grid-cols-2 gap-2">
                  <button
                    v-for="option in formatOptions"
                    :key="option.id"
                    @click="selectOption('format', option.id)"
                    class="p-3 text-left rounded-lg border-2 transition-all duration-200"
                    :class="[
                      selectedOptions.format === option.id
                        ? 'border-red-500 bg-red-50 text-red-700'
                        : 'border-gray-200 bg-gray-50 text-gray-700 hover:border-gray-300 hover:bg-gray-100',
                      { 'p-4 text-elder-base': userStore.isElderMode }
                    ]"
                  >
                    {{ option.text }}
                  </button>
                </div>
              </div>
              
              <!-- 针对问题 -->
              <div>
                <h4 class="text-sm font-medium text-gray-700 mb-3" :class="{ 'text-elder-sm': userStore.isElderMode }">
                  {{ t('regardingQuestion') }}
                </h4>
                <div class="grid grid-cols-2 gap-2">
                  <button
                    v-for="option in questionOptions"
                    :key="option.id"
                    @click="selectOption('question', option.id)"
                    class="p-3 text-left rounded-lg border-2 transition-all duration-200"
                    :class="[
                      selectedOptions.question === option.id
                        ? 'border-red-500 bg-red-50 text-red-700'
                        : 'border-gray-200 bg-gray-50 text-gray-700 hover:border-gray-300 hover:bg-gray-100',
                      { 'p-4 text-elder-base': userStore.isElderMode }
                    ]"
                  >
                    {{ option.text }}
                  </button>
                </div>
              </div>
            </div>
            
            <!-- 额外反馈 -->
            <div class="mt-6">
              <label class="block text-sm font-medium text-gray-700 mb-2" :class="{ 'text-elder-sm': userStore.isElderMode }">
                {{ t('additionalFeedback') }}
              </label>
              <textarea
                v-model="additionalFeedback"
                :placeholder="t('additionalFeedbackPlaceholder')"
                class="w-full p-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent resize-none"
                :class="[
                  { 'text-elder-base p-4 min-h-[80px]': userStore.isElderMode },
                  { 'min-h-[60px]': !userStore.isElderMode }
                ]"
                rows="3"
                maxlength="500"
              ></textarea>
              <div class="mt-1 text-right">
                <span class="text-xs text-gray-400" :class="{ 'text-elder-sm': userStore.isElderMode }">
                  {{ additionalFeedback.length }}/500
                </span>
              </div>
            </div>
          </div>
          
          <!-- 底部按钮 -->
          <div class="flex items-center justify-end space-x-3 p-6 border-t border-gray-100">
            <button
              @click="closeModal"
              class="px-4 py-2 text-sm text-gray-600 hover:text-gray-800 bg-gray-100 hover:bg-gray-200 rounded-lg transition-all duration-200"
              :class="{ 'px-5 py-2.5 text-base': userStore.isElderMode }"
            >
              {{ t('cancel') }}
            </button>
            <button
              @click="submitFeedback"
              :disabled="!hasSelectedOptions || isSubmitting"
              class="px-4 py-2 text-sm text-white bg-red-500 hover:bg-red-600 disabled:opacity-50 disabled:cursor-not-allowed rounded-lg transition-all duration-200"
              :class="{ 'px-5 py-2.5 text-base': userStore.isElderMode }"
            >
              <span v-if="isSubmitting">{{ t('submitting') }}...</span>
              <span v-else>{{ t('submit') }}</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { XMarkIcon } from '@heroicons/vue/24/outline'
import { useUserStore } from '@/stores/user'
import { t } from '@/stores/language'
import { chatApi } from '@/utils/api'

const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  },
  messageId: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['close', 'submit'])

const userStore = useUserStore()

// 响应式状态
const isVisible = ref(false)
const isSubmitting = ref(false)
const additionalFeedback = ref('')
const selectedOptions = ref({
  answer: null,
  format: null,
  question: null
})

// 反馈选项 - 使用计算属性确保语言切换时更新
const answerOptions = computed(() => [
  { id: 'factualError', text: t('factualError') },
  { id: 'incompleteContent', text: t('incompleteContent') },
  { id: 'calculationError', text: t('calculationError') },
  { id: 'reasoningError', text: t('reasoningError') },
  { id: 'unprofessionalContent', text: t('unprofessionalContent') },
  { id: 'illegalHarmful', text: t('illegalHarmful') }
])

const formatOptions = computed(() => [
  { id: 'formatError', text: t('formatError') },
  { id: 'repetitiveContent', text: t('repetitiveContent') },
  { id: 'garbledText', text: t('garbledText') },
  { id: 'needsDiagram', text: t('needsDiagram') }
])

const questionOptions = computed(() => [
  { id: 'understandingError', text: t('understandingError') },
  { id: 'contextError', text: t('contextError') },
  { id: 'unrecognizedError', text: t('unrecognizedError') }
])

// 计算属性
const hasSelectedOptions = computed(() => {
  return selectedOptions.value.answer || selectedOptions.value.format || selectedOptions.value.question
})

// 监听visible变化
watch(() => props.visible, (newVal) => {
  isVisible.value = newVal
  if (newVal) {
    // 重置表单
    resetForm()
  }
}, { immediate: true })

// 方法
const selectOption = (category, optionId) => {
  if (selectedOptions.value[category] === optionId) {
    // 如果已选中，则取消选择
    selectedOptions.value[category] = null
  } else {
    selectedOptions.value[category] = optionId
  }
}

const resetForm = () => {
  selectedOptions.value = {
    answer: null,
    format: null,
    question: null
  }
  additionalFeedback.value = ''
  isSubmitting.value = false
}

const closeModal = () => {
  isVisible.value = false
  emit('close')
}

const submitFeedback = async () => {
  if (!hasSelectedOptions.value || isSubmitting.value) return
  
  isSubmitting.value = true
  
  try {
    // 获取用户选中的第一个分类作为主要分类
    let primaryCategory = selectedOptions.value.answer || selectedOptions.value.format || selectedOptions.value.question
    
    const feedbackData = {
      message_id: props.messageId,
      feedback_type: 'negative',
      negative_category: primaryCategory,
      additional_feedback: additionalFeedback.value.trim()
    }
    
    // 发送反馈到后端
    await submitFeedbackToBackend(feedbackData)
    
    // 显示成功提示
    if (window.$notification) {
      window.$notification.success(t('feedbackSubmittedSuccessfully'))
    }
    
    // 关闭模态框
    closeModal()
    
    // 触发父组件事件
    emit('submit', feedbackData)
    
  } catch (error) {
    console.error('提交反馈失败:', error)
    if (window.$notification) {
      window.$notification.error(t('feedbackSubmissionFailed'))
    }
  } finally {
    isSubmitting.value = false
  }
}

// 提交反馈到后端
const submitFeedbackToBackend = async (feedbackData) => {
  try {
    // 使用封装的API方法
    const response = await chatApi.sendFeedback(feedbackData)
    return response.data
  } catch (error) {
    console.error('提交反馈到后端失败:', error)
    throw error
  }
}
</script>

<style scoped>
/* 确保模态框在移动端正确显示 */
@media (max-width: 768px) {
  .max-w-md {
    max-width: calc(100vw - 2rem);
  }
}

/* 按钮悬停效果 */
button:not(:disabled):hover {
  transform: translateY(-1px);
}

/* 选中状态动画 */
.border-red-500 {
  animation: selectPulse 0.3s ease-out;
}

@keyframes selectPulse {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.02);
  }
  100% {
    transform: scale(1);
  }
}
</style>
