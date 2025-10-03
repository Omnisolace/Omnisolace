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
           :class="{ 'sm:max-w-2xl': userStore.isElderMode }">
        
        <!-- 标题 -->
        <div class="flex items-center justify-between mb-6">
          <h3 class="text-lg leading-6 font-medium text-gray-900" 
              :class="{ 'text-elder-xl': userStore.isElderMode }"
              id="modal-title">
            {{ t('editPersonalInfo') }}
          </h3>
          <button
            @click="$emit('close')"
            class="text-gray-400 hover:text-gray-600"
          >
            <XMarkIcon class="h-6 w-6" :class="{ 'h-8 w-8': userStore.isElderMode }" />
          </button>
        </div>

        <!-- 表单 -->
        <form @submit.prevent="handleSubmit" class="space-y-6">
          <!-- 头像上传 -->
          <div class="text-center">
            <div class="mx-auto h-24 w-24 rounded-full flex items-center justify-center text-white text-2xl font-bold mb-4 overflow-hidden"
                 :class="{ 'h-32 w-32 text-3xl': userStore.isElderMode }"
                 :style="userStore.user?.avatar ? `background-image: url(${userStore.user.avatar}); background-size: cover; background-position: center;` : 'background-color: var(--color-primary-500);'">
              <img v-if="userStore.user?.avatar" 
                   :src="userStore.user.avatar" 
                   :alt="userStore.user?.nickname || '头像'"
                   class="w-full h-full object-cover rounded-full" />
              <span v-else>{{ getInitials() }}</span>
            </div>
            <button
              type="button"
              @click="uploadAvatar"
              class="text-primary-600 hover:text-primary-500 text-sm font-medium"
              :class="{ 'text-elder-base': userStore.isElderMode }"
            >
              {{ t('changeAvatar') }}
            </button>
          </div>

          <!-- 基本信息 -->
          <div class="grid grid-cols-1 gap-6">
            <div>
              <label for="name" class="block text-sm font-medium text-gray-700 mb-2"
                     :class="{ 'text-elder-base': userStore.isElderMode }">
                {{ t('nickname') }}
              </label>
              <input
                id="name"
                v-model="formData.name"
                type="text"
                required
                class="input-base"
                :class="{ 'text-elder-base py-4': userStore.isElderMode }"
                placeholder="请输入昵称"
              />
            </div>


            <div>
              <label class="block text-sm font-medium text-gray-700 mb-3"
                     :class="{ 'text-elder-base': userStore.isElderMode }">
                年龄段
              </label>
              <div class="space-y-3">
                <div
                  v-for="ageOption in ageOptions"
                  :key="ageOption.value"
                  @click="formData.ageGroup = ageOption.value"
                  class="flex items-center p-4 border border-gray-200 rounded-lg cursor-pointer hover:border-primary-500 transition-colors"
                  :class="{ 
                    'border-primary-500 bg-primary-50': formData.ageGroup === ageOption.value,
                    'p-5': userStore.isElderMode
                  }"
                >
                  <component :is="ageOption.icon" 
                            class="h-6 w-6 text-gray-600 mr-3 flex-shrink-0"
                            :class="{ 'h-8 w-8': userStore.isElderMode }" />
                  <div class="flex-1">
                    <h4 class="font-medium text-gray-900"
                        :class="{ 'text-elder-base': userStore.isElderMode }">
                      {{ ageOption.name }}
                    </h4>
                    <p class="text-sm text-gray-500"
                       :class="{ 'text-elder-sm': userStore.isElderMode }">
                      {{ ageOption.description }}
                    </p>
                  </div>
                  <div v-if="formData.ageGroup === ageOption.value"
                       class="w-5 h-5 bg-primary-500 rounded-full flex items-center justify-center flex-shrink-0">
                    <CheckIcon class="h-3 w-3 text-white" />
                  </div>
                </div>
              </div>
            </div>

            <!-- 青少年特殊字段 -->
            <div v-if="formData.ageGroup === 'teen'" class="space-y-4 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
              <h4 class="font-medium text-yellow-800"
                  :class="{ 'text-elder-base': userStore.isElderMode }">
                青少年用户设置
              </h4>
              
              <div>
                <label for="parent-phone" class="block text-sm font-medium text-gray-700 mb-2"
                       :class="{ 'text-elder-base': userStore.isElderMode }">
                  家长手机号
                </label>
                <input
                  id="parent-phone"
                  v-model="formData.parentPhone"
                  type="tel"
                  class="input-base"
                  :class="{ 'text-elder-base py-4': userStore.isElderMode }"
                  placeholder="请输入家长手机号"
                />
              </div>
            </div>

            <!-- 老年特殊字段 -->
            <div v-if="formData.ageGroup === 'elder'" class="space-y-4 p-4 bg-green-50 border border-green-200 rounded-lg">
              <h4 class="font-medium text-green-800"
                  :class="{ 'text-elder-base': userStore.isElderMode }">
                老年用户设置
              </h4>
              
              <div>
                <label for="helper-phone" class="block text-sm font-medium text-gray-700 mb-2"
                       :class="{ 'text-elder-base': userStore.isElderMode }">
                  子女联系方式
                </label>
                <input
                  id="helper-phone"
                  v-model="formData.helperPhone"
                  type="tel"
                  class="input-base"
                  :class="{ 'text-elder-base py-4': userStore.isElderMode }"
                  placeholder="子女可协助管理账户"
                />
              </div>

              <div class="flex items-start">
                <input
                  id="voice-priority"
                  v-model="formData.voicePriority"
                  type="checkbox"
                  class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded mt-1"
                  :class="{ 'h-6 w-6': userStore.isElderMode }"
                />
                <label for="voice-priority" class="ml-2 text-sm text-gray-700"
                       :class="{ 'text-elder-base': userStore.isElderMode }">
                  优先使用语音交互
                </label>
              </div>
            </div>

            <!-- 个人简介 -->
            <div>
                <label for="bio" class="block text-sm font-medium text-gray-700 mb-2"
                       :class="{ 'text-elder-base': userStore.isElderMode }">
                  个人简介
                  <span class="text-xs text-gray-500 ml-1">(最多15字)</span>
                </label>
                <div class="relative">
                  <textarea
                    id="bio"
                    v-model="formData.bio"
                    rows="3"
                    maxlength="15"
                    class="input-base resize-none pr-16"
                    :class="{ 'text-elder-base py-4': userStore.isElderMode }"
                    placeholder="简单介绍一下自己..."
                    @input="validateBio"
                  ></textarea>
                  <div class="absolute bottom-2 right-2 text-xs text-gray-400"
                       :class="{ 'text-elder-xs': userStore.isElderMode }">
                    {{ formData.bio.length }}/15
                  </div>
                </div>
                <div v-if="bioError" class="mt-1 text-xs text-red-500"
                     :class="{ 'text-elder-xs': userStore.isElderMode }">
                  {{ bioError }}
                </div>
            </div>
          </div>

          <!-- 按钮组 -->
          <div class="flex flex-col-reverse sm:flex-row sm:justify-end sm:space-x-3 space-y-3 space-y-reverse sm:space-y-0">
            <button
              type="button"
              @click="$emit('close')"
              class="w-full sm:w-auto btn-secondary"
              :class="{ 'py-3 text-elder-base': userStore.isElderMode }"
            >
              取消
            </button>
            <button
              type="submit"
              :disabled="loading"
              class="w-full sm:w-auto btn-primary"
              :class="{ 'py-3 text-elder-base': userStore.isElderMode }"
            >
              <div v-if="loading" class="loading-dots">
                <span style="--delay: 0"></span>
                <span style="--delay: 1"></span>
                <span style="--delay: 2"></span>
              </div>
              <span v-else>保存</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { t } from '@/stores/language'
import { userApi } from '@/utils/api'
import { 
  XMarkIcon, 
  CheckIcon,
  SparklesIcon,
  UserIcon,
  HeartIcon,
  AcademicCapIcon
} from '@heroicons/vue/24/outline'

const emit = defineEmits(['close'])
const userStore = useUserStore()

// 响应式状态
const loading = ref(false)
const bioError = ref('')

// 年龄段选项
const ageOptions = [
  {
    value: 'teen',
    name: '青少年 (12-18岁)',
    description: '青春活力，学习成长',
    icon: SparklesIcon
  },
  {
    value: 'young',
    name: '青年 (19-35岁)',
    description: '职场拼搏，追求梦想',
    icon: UserIcon
  },
  {
    value: 'middle',
    name: '中年 (36-59岁)',
    description: '稳重实用，家庭事业',
    icon: HeartIcon
  },
  {
    value: 'elder',
    name: '老年 (60岁+)',
    description: '智慧人生，享受晚年',
    icon: AcademicCapIcon
  }
]

// 表单数据
const formData = reactive({
  name: '',
  ageGroup: '',
  parentPhone: '',
  helperPhone: '',
  voicePriority: false,
  bio: ''
})

// 初始化表单数据
const initializeFormData = () => {
  formData.name = userStore.user?.nickname || ''
  formData.ageGroup = userStore.user?.age_group || ''
  formData.parentPhone = userStore.user?.parent_phone || ''
  formData.helperPhone = userStore.user?.helper_phone || ''
  formData.voicePriority = userStore.user?.voice_priority || false
  formData.bio = userStore.user?.profile?.bio || ''
}

// 验证个人简介
const validateBio = () => {
  if (formData.bio.length > 15) {
    bioError.value = '个人简介不能超过15字'
  } else {
    bioError.value = ''
  }
}

// 方法
const getInitials = () => {
  return formData.name ? formData.name.slice(0, 2).toUpperCase() : 'U'
}

const uploadAvatar = () => {
  // 创建文件输入元素
  const input = document.createElement('input')
  input.type = 'file'
  input.accept = 'image/*'
  input.onchange = async (e) => {
    const file = e.target.files[0]
    if (file) {
      // 验证文件类型
      if (!file.type.startsWith('image/')) {
        if (window.$notification) {
          window.$notification.error('请选择图片文件')
        }
        return
      }
      
      // 验证文件大小 (限制为2MB)
      if (file.size > 2 * 1024 * 1024) {
        if (window.$notification) {
          window.$notification.error('图片大小不能超过2MB')
        }
        return
      }
      
      try {
        loading.value = true
        
        // 创建FormData对象
        const formData = new FormData()
        formData.append('avatar', file)
        
        // 调用上传API
        const response = await userApi.uploadAvatar(formData)
        
        if (response.data) {
          // 更新本地用户头像
          const avatarUrl = response.data.avatar_url || response.data.avatar
          await userStore.updateAvatar(avatarUrl)

          // 重新获取用户信息，确保头像是最新的
          await userStore.fetchUserProfile()
          
          if (window.$notification) {
            window.$notification.success('头像上传成功')
          }
        }
      } catch (error) {
        console.error('头像上传失败:', error)
        if (window.$notification) {
          window.$notification.error('头像上传失败，请稍后重试')
        }
      } finally {
        loading.value = false
      }
    }
  }
  input.click()
}

const handleSubmit = async () => {
  loading.value = true
  
  try {
    // 准备要更新的数据
    const updateData = {
      nickname: formData.name,
      age_group: formData.ageGroup,
      parent_phone: formData.parentPhone,
      helper_phone: formData.helperPhone,
      voice_priority: formData.voicePriority
    }
    
    // 调用后端API更新用户信息
    await userStore.updateUserProfile(updateData)
    
    // 如果有bio信息，需要单独更新profile
    if (formData.bio) {
      try {
        await userApi.updateProfileDetail({ bio: formData.bio })
      } catch (error) {
        console.error('更新个人简介失败:', error)
        // 如果profile更新失败，不影响主要信息更新
      }
    }
    
    // 如果年龄段发生变化，更新全局年龄段设置
    if (formData.ageGroup !== userStore.ageGroup) {
      userStore.setAgeGroup(formData.ageGroup)
    }
    
    // 重新获取最新的用户信息
    try {
      await userStore.fetchUserProfile()
    } catch (error) {
      console.error('获取用户信息失败:', error)
    }
    
    if (window.$notification) {
      window.$notification.success('个人信息更新成功')
    }
    
    emit('close')
    
  } catch (error) {
    console.error('更新失败:', error)
    if (window.$notification) {
      window.$notification.error('更新失败，请稍后重试')
    }
  } finally {
    loading.value = false
  }
}


// 生命周期
onMounted(() => {
  initializeFormData()
})
</script>

<style scoped>
/* 表单验证样式 */
.input-base:invalid {
  border-color: rgb(252 165 165);
}

.input-base:invalid:focus {
  border-color: rgb(239 68 68);
  box-shadow: 0 0 0 3px rgb(239 68 68 / 0.1);
}

.input-base:valid {
  border-color: rgb(134 239 172);
}

/* 响应式设计 */
@media (max-width: 640px) {
  .grid-cols-1 {
    gap: 1rem;
  }
}

/* 老年模式特殊样式 */
.elder-mode input[type="checkbox"] {
  width: 1.5rem;
  height: 1.5rem;
}

/* 高对比度支持 */
@media (prefers-contrast: high) {
  .border {
    border-width: 2px;
  }
}
</style>
