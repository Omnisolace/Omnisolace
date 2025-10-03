<template>
  <div class="fixed inset-0 z-50 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
    <!-- 背景遮罩 -->
    <div class="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
      <div 
        class="fixed inset-0 bg-black bg-opacity-50 transition-opacity"
        @click="$emit('close')"
      ></div>

      <!-- 模态框内容 -->
      <div class="inline-block align-bottom bg-white rounded-lg px-4 pt-5 pb-4 text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-2xl sm:w-full sm:p-6"
           :class="{ 'sm:max-w-3xl': userStore.isElderMode }">
        
        <!-- 标题 -->
        <div class="flex items-center justify-between mb-6">
          <div class="flex items-center">
            <div class="h-12 w-12 bg-primary-500 rounded-full flex items-center justify-center mr-4"
                 :class="{ 'h-16 w-16': userStore.isElderMode }">
              <HeartIcon class="h-6 w-6 text-white" :class="{ 'h-8 w-8': userStore.isElderMode }" />
            </div>
            <div>
              <h3 class="text-lg leading-6 font-medium text-gray-900" 
                  :class="{ 'text-elder-xl': userStore.isElderMode }"
                  id="modal-title">
                {{ t('aboutOmnisolace') }}
              </h3>
              <p class="text-sm text-gray-500"
                 :class="{ 'text-elder-base': userStore.isElderMode }">
                {{ t('version') }} 1.0.0
              </p>
            </div>
          </div>
          <button
            @click="$emit('close')"
            class="text-gray-400 hover:text-gray-600"
          >
            <XMarkIcon class="h-6 w-6" :class="{ 'h-8 w-8': userStore.isElderMode }" />
          </button>
        </div>

        <!-- 内容区域 -->
        <div class="max-h-96 overflow-y-auto custom-scrollbar space-y-6">
          <!-- 产品介绍 -->
          <div>
            <h4 class="text-base font-semibold text-gray-900 mb-3"
                :class="{ 'text-elder-lg': userStore.isElderMode }">
              {{ t('productIntroduction') }}
            </h4>
            <p class="text-sm text-gray-700 leading-relaxed"
               :class="{ 'text-elder-base': userStore.isElderMode }">
              {{ t('productDescription') }}
            </p>
          </div>

          <!-- 核心特性 -->
          <div>
            <h4 class="text-base font-semibold text-gray-900 mb-3"
                :class="{ 'text-elder-lg': userStore.isElderMode }">
              {{ t('coreFeatures') }}
            </h4>
            <div class="space-y-3">
              <div v-for="feature in features" :key="feature.id" class="flex items-start">
                <component :is="feature.icon" 
                          class="h-5 w-5 text-primary-500 mr-3 mt-0.5 flex-shrink-0"
                          :class="{ 'h-6 w-6': userStore.isElderMode }" />
                <div>
                  <h5 class="font-medium text-gray-900"
                      :class="{ 'text-elder-base': userStore.isElderMode }">
                    {{ feature.title }}
                  </h5>
                  <p class="text-sm text-gray-600"
                     :class="{ 'text-elder-sm': userStore.isElderMode }">
                    {{ feature.description }}
                  </p>
                </div>
              </div>
            </div>
          </div>

          <!-- 技术架构 -->
          <div>
            <h4 class="text-base font-semibold text-gray-900 mb-3"
                :class="{ 'text-elder-lg': userStore.isElderMode }">
              {{ t('technicalArchitecture') }}
            </h4>
            <div class="bg-gray-50 rounded-lg p-4">
              <div class="grid grid-cols-2 gap-4 text-sm"
                   :class="{ 'text-elder-sm grid-cols-1': userStore.isElderMode }">
                <div>
                  <h6 class="font-medium text-gray-900 mb-2">{{ t('frontendTechnology') }}</h6>
                  <ul class="space-y-1 text-gray-600">
                    <li>• Vue 3 + Vite</li>
                    <li>• Tailwind CSS</li>
                    <li>• PWA 支持</li>
                    <li>• Web Speech API</li>
                  </ul>
                </div>
                <div>
                  <h6 class="font-medium text-gray-900 mb-2">{{ t('aiTechnology') }}</h6>
                  <ul class="space-y-1 text-gray-600">
                    <li>• 多模态情绪识别</li>
                    <li>• 自然语言处理</li>
                    <li>• 认知行为疗法框架</li>
                    <li>• 危机预警系统</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>

          <!-- 安全与隐私 -->
          <div>
            <h4 class="text-base font-semibold text-gray-900 mb-3"
                :class="{ 'text-elder-lg': userStore.isElderMode }">
              {{ t('securityAndPrivacy') }}
            </h4>
            <div class="bg-green-50 border border-green-200 rounded-lg p-4">
              <div class="flex items-start">
                <ShieldCheckIcon class="h-5 w-5 text-green-500 mr-3 mt-0.5 flex-shrink-0"
                                :class="{ 'h-6 w-6': userStore.isElderMode }" />
                <div class="space-y-2">
                  <p class="text-sm text-green-800"
                     :class="{ 'text-elder-sm': userStore.isElderMode }">
                    {{ t('dataEncryption') }}
                  </p>
                  <p class="text-sm text-green-800"
                     :class="{ 'text-elder-sm': userStore.isElderMode }">
                    {{ t('privacyProtection') }}
                  </p>
                  <p class="text-sm text-green-800"
                     :class="{ 'text-elder-sm': userStore.isElderMode }">
                    {{ t('complianceCertification') }}
                  </p>
                </div>
              </div>
            </div>
          </div>

          <!-- 联系我们 -->
          <div>
            <h4 class="text-base font-semibold text-gray-900 mb-3"
                :class="{ 'text-elder-lg': userStore.isElderMode }">
              {{ t('contactUs') }}
            </h4>
            <div class="space-y-3">
              <div class="flex items-center">
                <PhoneIcon class="h-5 w-5 text-gray-400 mr-3"
                          :class="{ 'h-6 w-6': userStore.isElderMode }" />
                <div>
                  <p class="text-sm text-gray-900 font-medium"
                     :class="{ 'text-elder-base': userStore.isElderMode }">
                    {{ t('customerService') }}
                  </p>
                  <p class="text-sm text-gray-600"
                     :class="{ 'text-elder-sm': userStore.isElderMode }">
                    400-161-9995 (24小时服务)
                  </p>
                </div>
              </div>
              <div class="flex items-center">
                <EnvelopeIcon class="h-5 w-5 text-gray-400 mr-3"
                             :class="{ 'h-6 w-6': userStore.isElderMode }" />
                <div>
                  <p class="text-sm text-gray-900 font-medium"
                     :class="{ 'text-elder-base': userStore.isElderMode }">
                    {{ t('emailSupport') }}
                  </p>
                  <p class="text-sm text-gray-600"
                     :class="{ 'text-elder-sm': userStore.isElderMode }">
                    support@omnisolace.com
                  </p>
                </div>
              </div>
              <div class="flex items-center">
                <GlobeAltIcon class="h-5 w-5 text-gray-400 mr-3"
                             :class="{ 'h-6 w-6': userStore.isElderMode }" />
                <div>
                  <p class="text-sm text-gray-900 font-medium"
                     :class="{ 'text-elder-base': userStore.isElderMode }">
                    {{ t('officialWebsite') }}
                  </p>
                  <p class="text-sm text-gray-600"
                     :class="{ 'text-elder-sm': userStore.isElderMode }">
                    www.omnisolace.com
                  </p>
                </div>
              </div>
            </div>
          </div>

          <!-- 免责声明 -->
          <div class="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
            <div class="flex items-start">
              <ExclamationTriangleIcon class="h-5 w-5 text-yellow-500 mr-3 mt-0.5 flex-shrink-0"
                                      :class="{ 'h-6 w-6': userStore.isElderMode }" />
              <div>
                <h5 class="font-medium text-yellow-900 mb-2"
                    :class="{ 'text-elder-base': userStore.isElderMode }">
                  {{ t('importantStatement') }}
                </h5>
                <p class="text-sm text-yellow-800"
                   :class="{ 'text-elder-sm': userStore.isElderMode }">
                  {{ t('disclaimer') }}
                </p>
              </div>
            </div>
          </div>

          <!-- 版权信息 -->
          <div class="text-center pt-4 border-t border-gray-200">
            <p class="text-sm text-gray-500"
               :class="{ 'text-elder-sm': userStore.isElderMode }">
              © 2025 Omnisolace. All rights reserved.
            </p>
            <p class="text-xs text-gray-400 mt-1"
               :class="{ 'text-elder-sm': userStore.isElderMode }">
              {{ t('copyrightProtected') }}
            </p>
          </div>
        </div>

        <!-- 底部按钮 -->
        <div class="mt-6 flex flex-col sm:flex-row sm:justify-end space-y-3 sm:space-y-0 sm:space-x-3">
          <button
            @click="checkUpdate"
            class="btn-secondary"
            :class="{ 'py-3 text-elder-base': userStore.isElderMode }"
          >
            {{ t('checkUpdate') }}
          </button>
          <button
            @click="$emit('close')"
            class="btn-primary"
            :class="{ 'py-3 text-elder-base': userStore.isElderMode }"
          >
            {{ t('gotIt') }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useUserStore } from '@/stores/user'
import { t } from '@/stores/language'
import {
  XMarkIcon,
  HeartIcon,
  ShieldCheckIcon,
  PhoneIcon,
  EnvelopeIcon,
  GlobeAltIcon,
  ExclamationTriangleIcon,
  UserGroupIcon,
  CpuChipIcon,
  EyeIcon,
  BellIcon
} from '@heroicons/vue/24/outline'

const emit = defineEmits(['close'])
const userStore = useUserStore()

// 核心特性列表
const features = computed(() => [
  {
    id: 1,
    title: t('allAgeAdaptation'),
    description: t('allAgeAdaptationDesc'),
    icon: UserGroupIcon
  },
  {
    id: 2,
    title: t('multimodalEmotionRecognition'),
    description: t('multimodalEmotionRecognitionDesc'),
    icon: CpuChipIcon
  },
  {
    id: 3,
    title: t('professionalPsychologicalFramework'),
    description: t('professionalPsychologicalFrameworkDesc'),
    icon: HeartIcon
  },
  {
    id: 4,
    title: t('crisisWarningSystem'),
    description: t('crisisWarningSystemDesc'),
    icon: BellIcon
  },
  {
    id: 5,
    title: t('privacySecurityProtection'),
    description: t('privacySecurityProtectionDesc'),
    icon: EyeIcon
  },
  {
    id: 6,
    title: t('pwaOfflineSupport'),
    description: t('pwaOfflineSupportDesc'),
    icon: CpuChipIcon
  }
])

// 方法
const checkUpdate = () => {
  // 检查应用更新
  if (window.$notification) {
    window.$notification.info(t('currentVersionIsLatest'))
  }
}
</script>

<style scoped>
/* 响应式设计 */
@media (max-width: 640px) {
  .grid-cols-2 {
    grid-template-columns: repeat(1, minmax(0, 1fr));
  }
}

/* 高对比度支持 */
@media (prefers-contrast: high) {
  .bg-gray-50,
  .bg-green-50,
  .bg-yellow-50 {
    border-width: 2px;
  }
}

/* 老年模式特殊样式 */
.elder-mode .max-h-96 {
  max-height: 32rem;
}
</style>
