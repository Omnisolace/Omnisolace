<template>
  <div class="fixed inset-0 z-50 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
    <!-- 背景遮罩 -->
    <div class="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
      <div 
        class="fixed inset-0 bg-black bg-opacity-50 transition-opacity"
        @click="$emit('close')"
      ></div>

      <!-- 模态框内容 -->
      <div class="inline-block align-bottom bg-white rounded-lg px-4 pt-5 pb-4 text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full sm:p-6"
           :class="{ 'elder-modal': userStore.isElderMode }">
        
        <!-- 标题 -->
        <div class="sm:flex sm:items-start">
          <div class="mx-auto flex-shrink-0 flex items-center justify-center h-12 w-12 rounded-full bg-red-100 sm:mx-0 sm:h-10 sm:w-10"
               :class="{ 'h-16 w-16 sm:h-16 sm:w-16': userStore.isElderMode }">
            <ExclamationTriangleIcon class="h-6 w-6 text-red-600" 
                                   :class="{ 'h-8 w-8': userStore.isElderMode }" />
          </div>
          <div class="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left">
            <h3 class="text-lg leading-6 font-medium text-gray-900" 
                :class="{ 'text-elder-xl': userStore.isElderMode }"
                id="modal-title">
              {{ t('emergency') }}
            </h3>
            <div class="mt-2">
              <p class="text-sm text-gray-500"
                 :class="{ 'text-elder-base': userStore.isElderMode }">
                {{ t('emergencyDescription') }}
              </p>
            </div>
          </div>
        </div>

        <!-- 紧急联系方式列表 -->
        <div class="mt-6 space-y-4">
          <div v-for="contact in emergencyContacts" :key="contact.id" 
               class="emergency-contact-item">
            <div class="flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:border-red-300 transition-colors">
              <div class="flex items-center">
                <component :is="contact.icon" 
                          class="h-6 w-6 text-red-500 mr-3"
                          :class="{ 'h-8 w-8': userStore.isElderMode }" />
                <div>
                  <h4 class="font-medium text-gray-900"
                      :class="{ 'text-elder-base': userStore.isElderMode }">
                    {{ contact.name }}
                  </h4>
                  <p class="text-sm text-gray-500"
                     :class="{ 'text-elder-sm': userStore.isElderMode }">
                    {{ contact.description }}
                  </p>
                </div>
              </div>
              <button 
                @click="handleContactClick(contact)"
                class="emergency-contact-btn"
                :class="emergencyBtnClass"
                :aria-label="`拨打${contact.name}`">
                {{ contact.action }}
              </button>
            </div>
          </div>
        </div>

        <!-- 个人紧急联系人 -->
        <div v-if="personalContacts.length > 0" class="mt-6">
          <h4 class="font-medium text-gray-900 mb-3"
              :class="{ 'text-elder-base': userStore.isElderMode }">
            {{ t('personalEmergencyContacts') }}
          </h4>
          <div class="space-y-2">
            <div v-for="contact in personalContacts" :key="contact.id"
                 class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <div>
                <span class="font-medium text-gray-900"
                      :class="{ 'text-elder-base': userStore.isElderMode }">
                  {{ contact.name }}
                </span>
                <span class="text-sm text-gray-500 ml-2"
                      :class="{ 'text-elder-sm': userStore.isElderMode }">
                  {{ contact.relationship }}
                </span>
              </div>
              <button 
                @click="callPersonalContact(contact)"
                class="emergency-contact-btn"
                :class="emergencyBtnClass">
                {{ t('call') }}
              </button>
            </div>
          </div>
        </div>

        <!-- 底部按钮 -->
        <div class="mt-6 sm:flex sm:flex-row-reverse gap-3">
          <button 
            @click="$emit('close')"
            type="button" 
            class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-gray-600 text-base font-medium text-white hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500 sm:w-auto sm:text-sm"
            :class="{ 'px-6 py-4 text-elder-base': userStore.isElderMode }">
            {{ t('close') }}
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
  ExclamationTriangleIcon,
  PhoneIcon,
  ChatBubbleLeftRightIcon,
  GlobeAltIcon
} from '@heroicons/vue/24/outline'

const emit = defineEmits(['close'])
const userStore = useUserStore()

// 紧急联系方式
const emergencyContacts = computed(() => [
  {
    id: 1,
    name: t('psychologicalHelpline'),
    description: t('psychologicalHelplineDesc'),
    phone: '400-161-9995',
    action: t('call'),
    icon: PhoneIcon
  },
  {
    id: 2,
    name: t('lifeline'),
    description: t('lifelineDesc'),
    phone: '400-161-9995',
    action: t('call'),
    icon: PhoneIcon
  },
  {
    id: 3,
    name: t('onlinePsychologicalConsulting'),
    description: t('onlinePsychologicalConsultingDesc'),
    url: 'https://www.xinli001.com',
    action: t('visit'),
    icon: GlobeAltIcon
  },
  {
    id: 4,
    name: t('crisisSMSSupport'),
    description: t('crisisSMSSupportDesc'),
    phone: '741741',
    action: t('send'),
    icon: ChatBubbleLeftRightIcon
  }
])

// 个人紧急联系人（从用户设置中获取）
const personalContacts = ref([
  // 这里应该从用户设置中获取
  // {
  //   id: 1,
  //   name: '张医生',
  //   phone: '138****8888',
  //   relationship: '心理咨询师'
  // }
])

// 计算属性
const emergencyBtnClass = computed(() => {
  if (userStore.isElderMode) {
    return 'px-4 py-3 text-elder-base bg-red-500 text-white rounded-lg hover:bg-red-600'
  }
  return 'px-3 py-2 text-sm bg-red-500 text-white rounded-lg hover:bg-red-600'
})

// 方法
const handleContactClick = (contact) => {
  if (contact.phone) {
    // 拨打电话
    if (contact.phone === '741741') {
      // 短信
      window.open(`sms:${contact.phone}?body=帮助`)
    } else {
      // 电话
      window.open(`tel:${contact.phone}`)
    }
  } else if (contact.url) {
    // 打开网址
    window.open(contact.url, '_blank')
  }
  
  // 记录紧急求助事件
  logEmergencyEvent(contact)
  
  // 显示确认通知
  if (window.$notification) {
    window.$notification.info(
      t('emergencyContactOpened', { name: contact.name }),
      t('emergency'),
      { duration: 3000 }
    )
  }
}

const callPersonalContact = (contact) => {
  window.open(`tel:${contact.phone}`)
  logEmergencyEvent({
    name: `${t('personalContact')}-${contact.name}`,
    phone: contact.phone
  })
}

const logEmergencyEvent = (contact) => {
  // 记录紧急求助事件，用于后续分析和改进
  const eventData = {
    type: 'emergency_contact',
    contact: contact.name,
    timestamp: Date.now(),
    userAgeGroup: userStore.ageGroup
  }
  
  console.log('紧急求助事件:', eventData)
  
  // 这里应该调用API记录事件
  // api.logEmergencyEvent(eventData)
}
</script>

<style scoped>
.emergency-contact-item {
  transition: all 0.2s ease;
}

.emergency-contact-item:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.emergency-contact-btn {
  transition: all 0.2s ease;
  white-space: nowrap;
}

.emergency-contact-btn:hover {
  transform: scale(1.05);
}

.emergency-contact-btn:active {
  transform: scale(0.95);
}

/* 老年模式样式 */
.elder-modal {
  max-width: 42rem;
}

.elder-modal .emergency-contact-item {
  margin-bottom: 1rem;
}

.elder-modal .emergency-contact-btn {
  min-width: 80px;
  min-height: 48px;
}

/* 响应式设计 */
@media (max-width: 640px) {
  .emergency-contact-item .flex {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }
  
  .emergency-contact-btn {
    align-self: stretch;
    text-align: center;
  }
}

/* 高对比度支持 */
@media (prefers-contrast: high) {
  .emergency-contact-item .border {
    border-width: 2px;
    border-color: rgb(156 163 175);
  }
  
  .emergency-contact-btn {
    border-width: 2px;
    border-color: white;
  }
}

/* 动画效果 */
@keyframes pulse-red {
  0%, 100% {
    box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7);
  }
  50% {
    box-shadow: 0 0 0 10px rgba(239, 68, 68, 0);
  }
}

.emergency-contact-btn:focus {
  animation: pulse-red 1.5s infinite;
}
</style>
