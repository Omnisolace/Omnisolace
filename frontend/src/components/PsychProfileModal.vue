<template>
  <div class="fixed inset-0 z-50 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
    <!-- 背景遮罩 -->
    <div class="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
      <div 
        class="fixed inset-0 bg-black bg-opacity-50 transition-opacity"
        @click="$emit('close')"
      ></div>

      <!-- 模态框内容 -->
      <div class="inline-block align-bottom bg-white rounded-lg px-4 pt-5 pb-4 text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-4xl sm:w-full sm:p-6"
           :class="{ 'sm:max-w-5xl': userStore.isElderMode }">
        
        <!-- 标题 -->
        <div class="flex items-center justify-between mb-6">
          <h3 class="text-lg leading-6 font-medium text-gray-900" 
              :class="{ 'text-elder-xl': userStore.isElderMode }"
              id="modal-title">
            {{ t('psychProfileDetails') }}
          </h3>
          <div class="flex items-center space-x-3">
            <button
              @click="exportReport"
              class="btn-secondary"
              :class="{ 'px-4 py-3 text-elder-base': userStore.isElderMode }"
            >
              {{ t('exportReport') }}
            </button>
            <button
              @click="$emit('close')"
              class="text-gray-400 hover:text-gray-600"
            >
              <XMarkIcon class="h-6 w-6" :class="{ 'h-8 w-8': userStore.isElderMode }" />
            </button>
          </div>
        </div>

        <!-- 内容区域 -->
        <div class="max-h-96 overflow-y-auto custom-scrollbar">
          <!-- 基础统计 -->
          <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            <div class="text-center p-4 bg-blue-50 rounded-lg">
              <div class="text-2xl font-bold text-blue-600 mb-1"
                   :class="{ 'text-elder-xl': userStore.isElderMode }">
                {{ profileData.totalSessions }}
              </div>
              <div class="text-sm text-gray-600"
                   :class="{ 'text-elder-sm': userStore.isElderMode }">
                {{ t('totalConversations') }}
              </div>
            </div>
            <div class="text-center p-4 bg-green-50 rounded-lg">
              <div class="text-2xl font-bold text-green-600 mb-1"
                   :class="{ 'text-elder-xl': userStore.isElderMode }">
                {{ profileData.averageScore }}
              </div>
              <div class="text-sm text-gray-600"
                   :class="{ 'text-elder-sm': userStore.isElderMode }">
                {{ t('avgEmotionScore') }}
              </div>
            </div>
            <div class="text-center p-4 bg-yellow-50 rounded-lg">
              <div class="text-2xl font-bold text-yellow-600 mb-1"
                   :class="{ 'text-elder-xl': userStore.isElderMode }">
                {{ profileData.improvementRate }}%
              </div>
              <div class="text-sm text-gray-600"
                   :class="{ 'text-elder-sm': userStore.isElderMode }">
                {{ t('emotionImprovementRate') }}
              </div>
            </div>
            <div class="text-center p-4 bg-purple-50 rounded-lg">
              <div class="text-2xl font-bold text-purple-600 mb-1"
                   :class="{ 'text-elder-xl': userStore.isElderMode }">
                {{ profileData.continuousDays }}
              </div>
              <div class="text-sm text-gray-600"
                   :class="{ 'text-elder-sm': userStore.isElderMode }">
                连续使用天数
              </div>
            </div>
          </div>

          <!-- 情绪分析 -->
          <div class="mb-8">
            <h4 class="text-lg font-semibold text-gray-900 mb-4"
                :class="{ 'text-elder-lg': userStore.isElderMode }">
              情绪分析报告
            </h4>
            
            <!-- 情绪分布 -->
            <div class="bg-gray-50 rounded-lg p-6 mb-6">
              <h5 class="font-medium text-gray-900 mb-4"
                  :class="{ 'text-elder-base': userStore.isElderMode }">
                情绪分布 (近30天)
              </h5>
              <div class="space-y-3">
                <div v-for="emotion in emotionDistribution" :key="emotion.label"
                     class="flex items-center">
                  <div class="w-20 text-sm text-gray-600"
                       :class="{ 'text-elder-sm': userStore.isElderMode }">
                    {{ emotion.name }}
                  </div>
                  <div class="flex-1 mx-4">
                    <div class="w-full bg-gray-200 rounded-full h-3"
                         :class="{ 'h-4': userStore.isElderMode }">
                      <div 
                        :class="emotion.bgColor"
                        class="h-full rounded-full transition-all duration-500"
                        :style="{ width: `${emotion.percentage}%` }"
                      ></div>
                    </div>
                  </div>
                  <div class="w-12 text-sm font-medium text-gray-900 text-right"
                       :class="{ 'text-elder-sm': userStore.isElderMode }">
                    {{ emotion.percentage }}%
                  </div>
                </div>
              </div>
            </div>

            <!-- 情绪趋势图 -->
            <div class="bg-gray-50 rounded-lg p-6 mb-6">
              <h5 class="font-medium text-gray-900 mb-4"
                  :class="{ 'text-elder-base': userStore.isElderMode }">
                情绪趋势 (近7天)
              </h5>
              <div class="flex items-end space-x-2 h-32">
                <div
                  v-for="(day, index) in emotionTrendData"
                  :key="index"
                  class="flex-1 bg-primary-200 rounded-t flex flex-col justify-end"
                  :style="{ height: `${day.score}%` }"
                >
                  <div class="text-xs text-center text-gray-600 p-1"
                       :class="{ 'text-elder-sm': userStore.isElderMode }">
                    {{ day.day }}
                  </div>
                </div>
              </div>
              <div class="flex justify-between mt-2 text-xs text-gray-500"
                   :class="{ 'text-elder-sm': userStore.isElderMode }">
                <span>7天前</span>
                <span>今天</span>
              </div>
            </div>
          </div>

          <!-- 问题类型分析 -->
          <div class="mb-8">
            <h4 class="text-lg font-semibold text-gray-900 mb-4"
                :class="{ 'text-elder-lg': userStore.isElderMode }">
              问题类型分析
            </h4>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div class="bg-gray-50 rounded-lg p-6">
                <h5 class="font-medium text-gray-900 mb-4"
                    :class="{ 'text-elder-base': userStore.isElderMode }">
                  高频问题
                </h5>
                <div class="space-y-3">
                  <div v-for="issue in topIssues" :key="issue.category"
                       class="flex items-center justify-between">
                    <span class="text-sm text-gray-700"
                          :class="{ 'text-elder-sm': userStore.isElderMode }">
                      {{ issue.category }}
                    </span>
                    <div class="flex items-center">
                      <div class="w-16 bg-gray-200 rounded-full h-2 mr-2"
                           :class="{ 'h-3': userStore.isElderMode }">
                        <div 
                          class="bg-primary-500 h-full rounded-full"
                          :style="{ width: `${issue.percentage}%` }"
                        ></div>
                      </div>
                      <span class="text-sm font-medium text-gray-900 w-8 text-right"
                            :class="{ 'text-elder-sm': userStore.isElderMode }">
                        {{ issue.count }}
                      </span>
                    </div>
                  </div>
                </div>
              </div>

              <div class="bg-gray-50 rounded-lg p-6">
                <h5 class="font-medium text-gray-900 mb-4"
                    :class="{ 'text-elder-base': userStore.isElderMode }">
                  改善建议
                </h5>
                <div class="space-y-3">
                  <div v-for="suggestion in suggestions" :key="suggestion.id"
                       class="flex items-start">
                    <div class="w-2 h-2 bg-primary-500 rounded-full mt-2 mr-3 flex-shrink-0"></div>
                    <p class="text-sm text-gray-700"
                       :class="{ 'text-elder-sm': userStore.isElderMode }">
                      {{ suggestion.text }}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 专业评估 -->
          <div class="mb-6">
            <h4 class="text-lg font-semibold text-gray-900 mb-4"
                :class="{ 'text-elder-lg': userStore.isElderMode }">
              专业评估
            </h4>
            <div class="bg-blue-50 border border-blue-200 rounded-lg p-6">
              <div class="flex items-start">
                <InformationCircleIcon class="h-6 w-6 text-blue-500 mr-3 mt-0.5 flex-shrink-0"
                                      :class="{ 'h-8 w-8': userStore.isElderMode }" />
                <div>
                  <h5 class="font-medium text-blue-900 mb-2"
                      :class="{ 'text-elder-base': userStore.isElderMode }">
                    综合评估结果
                  </h5>
                  <p class="text-blue-800 text-sm leading-relaxed"
                     :class="{ 'text-elder-sm': userStore.isElderMode }">
                    {{ assessmentResult }}
                  </p>
                </div>
              </div>
            </div>
          </div>

          <!-- 注意事项 -->
          <div class="bg-yellow-50 border border-yellow-200 rounded-lg p-6">
            <div class="flex items-start">
              <ExclamationTriangleIcon class="h-6 w-6 text-yellow-500 mr-3 mt-0.5 flex-shrink-0"
                                      :class="{ 'h-8 w-8': userStore.isElderMode }" />
              <div>
                <h5 class="font-medium text-yellow-900 mb-2"
                    :class="{ 'text-elder-base': userStore.isElderMode }">
                  重要提醒
                </h5>
                <p class="text-yellow-800 text-sm"
                   :class="{ 'text-elder-sm': userStore.isElderMode }">
                  此报告仅供参考，不能替代专业心理咨询。如有严重心理问题，请及时寻求专业帮助。
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useUserStore } from '@/stores/user'
import { useChatStore } from '@/stores/chat'
import { t } from '@/stores/language'
import {
  XMarkIcon,
  InformationCircleIcon,
  ExclamationTriangleIcon
} from '@heroicons/vue/24/outline'

const emit = defineEmits(['close'])
const userStore = useUserStore()
const chatStore = useChatStore()

// 模拟心理档案数据
const profileData = ref({
  totalSessions: 23,
  averageScore: 68,
  improvementRate: 15,
  continuousDays: 7
})

// 情绪分布数据
const emotionDistribution = ref([
  { label: 'happy', name: '开心', percentage: 35, bgColor: 'bg-emotion-happy' },
  { label: 'neutral', name: '平静', percentage: 40, bgColor: 'bg-emotion-neutral' },
  { label: 'anxious', name: '焦虑', percentage: 20, bgColor: 'bg-emotion-anxious' },
  { label: 'sad', name: '难过', percentage: 5, bgColor: 'bg-emotion-sad' }
])

// 情绪趋势数据
const emotionTrendData = ref([
  { day: '周一', score: 60 },
  { day: '周二', score: 55 },
  { day: '周三', score: 70 },
  { day: '周四', score: 65 },
  { day: '周五', score: 75 },
  { day: '周六', score: 80 },
  { day: '周日', score: 72 }
])

// 高频问题
const topIssues = ref([
  { category: '学习压力', count: 8, percentage: 80 },
  { category: '人际关系', count: 6, percentage: 60 },
  { category: '情绪管理', count: 4, percentage: 40 },
  { category: '睡眠问题', count: 3, percentage: 30 },
  { category: '家庭关系', count: 2, percentage: 20 }
])

// 改善建议
const suggestions = ref([
  { id: 1, text: '建议每天进行10-15分钟的正念冥想练习' },
  { id: 2, text: '保持规律的作息时间，确保充足的睡眠' },
  { id: 3, text: '增加户外活动和体育锻炼的频率' },
  { id: 4, text: '学习有效的压力管理技巧' },
  { id: 5, text: '考虑寻求专业心理咨询师的帮助' }
])

// 专业评估结果
const assessmentResult = computed(() => {
  const ageGroup = userStore.ageGroup
  const baseAssessment = '根据您近期的对话记录和情绪数据分析，您的整体心理状态处于正常范围内。'
  
  const ageSpecificAssessment = {
    teen: '作为青少年，您在学业压力和人际关系方面表现出一定的焦虑，这是正常的成长过程。建议加强情绪调节技能的学习。',
    young: '作为青年人，您在职业发展和人际关系方面有一些困扰，建议通过专业技能提升和社交能力培养来改善。',
    middle: '作为中年人，您在工作和家庭平衡方面承受一定压力，建议学习时间管理和压力释放技巧。',
    elder: '作为老年人，您在适应生活变化方面表现良好，建议继续保持积极的生活态度和社交活动。'
  }
  
  return baseAssessment + ageSpecificAssessment[ageGroup]
})

// 方法
const exportReport = () => {
  // 生成并下载心理报告
  const reportData = {
    userId: userStore.user?.id,
    userName: userStore.user?.name,
    ageGroup: userStore.ageGroup,
    generatedAt: new Date().toISOString(),
    profileData: profileData.value,
    emotionDistribution: emotionDistribution.value,
    emotionTrend: emotionTrendData.value,
    topIssues: topIssues.value,
    suggestions: suggestions.value,
    assessment: assessmentResult.value
  }
  
  // 创建并下载JSON文件
  const blob = new Blob([JSON.stringify(reportData, null, 2)], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `心理档案报告_${new Date().toLocaleDateString()}.json`
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
  
  if (window.$notification) {
    window.$notification.success('心理报告已导出')
  }
}
</script>

<style scoped>
/* 进度条动画 */
.bg-primary-200,
.bg-primary-500 {
  transition: all 0.5s ease;
}

/* 情绪趋势图 */
.flex.items-end > div {
  transition: height 0.3s ease;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .grid-cols-4 {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
  
  .grid-cols-2 {
    grid-template-columns: repeat(1, minmax(0, 1fr));
  }
}

/* 老年模式特殊样式 */
.elder-mode .max-h-96 {
  max-height: 32rem;
}

/* 高对比度支持 */
@media (prefers-contrast: high) {
  .bg-gray-50 {
    background-color: rgb(243 244 246);
  }
  
  .border {
    border-width: 2px;
  }
}
</style>
