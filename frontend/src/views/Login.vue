<template>
  <div class="min-h-screen flex items-center justify-center px-4 sm:px-6 lg:px-8 page-container">
    <div class="w-full space-y-8" :class="activeTab === 'register' ? 'max-w-4xl' : 'max-w-md'">
      <!-- Logo 和标题 -->
      <div class="text-center relative">
        <!-- 语言切换组件 -->
        <div class="absolute top-0 right-0">
          <LanguageSwitcher />
        </div>
        
        <div class="mx-auto h-20 w-20 bg-primary-500 rounded-full flex items-center justify-center mb-6">
          <HeartIcon class="h-10 w-10 text-white" />
        </div>
        <div class="flex justify-center mb-2">
          <img 
            src="/images/Omnisolace_logo_wor.png" 
            alt="Omnisolace" 
            class="h-12 sm:h-16 md:h-20 w-auto max-w-xs object-contain"
          />
        </div>
        <p class="text-gray-600">
          {{ t('subtitle') }}
        </p>
      </div>

      <!-- 登录/注册表单 -->
      <div class="rounded-lg shadow-xl p-8 card-bg">
        <!-- 标签切换 -->
        <div v-if="activeTab !== 'forgot-password'" class="flex mb-6 rounded-lg p-1" style="background-color: var(--color-primary-50);">
          <button
            @click="activeTab = 'login'"
            :class="[
              'flex-1 py-2 px-4 rounded-md text-sm font-medium transition-colors duration-200',
              activeTab === 'login' 
                ? 'text-white shadow-sm' 
                : 'text-gray-600 hover:text-gray-900'
            ]"
            :style="activeTab === 'login' ? { backgroundColor: 'var(--color-primary)' } : {}"
          >
            {{ t('login') }}
          </button>
          <button
            @click="activeTab = 'register'"
            :class="[
              'flex-1 py-2 px-4 rounded-md text-sm font-medium transition-colors duration-200',
              activeTab === 'register' 
                ? 'text-white shadow-sm' 
                : 'text-gray-600 hover:text-gray-900'
            ]"
            :style="activeTab === 'register' ? { backgroundColor: 'var(--color-primary)' } : {}"
          >
            {{ t('register') }}
          </button>
        </div>

        <!-- 登录表单 -->
        <form v-if="activeTab === 'login'" @submit.prevent="handleLogin" class="space-y-6">
          <div>
            <label for="phone" class="block text-sm font-medium text-gray-700 mb-2">
              {{ t('phoneNumber') }}
            </label>
            <input
              id="phone"
              v-model="loginForm.phone"
              type="tel"
              required
              class="input-base"
              placeholder="请输入手机号"
              :disabled="loading"
            />
          </div>

          <div>
            <label for="password" class="block text-sm font-medium text-gray-700 mb-2">
              {{ t('password') }}
            </label>
            <div class="relative">
              <input
                id="password"
                v-model="loginForm.password"
                :type="showPassword ? 'text' : 'password'"
                required
                class="input-base pr-10"
                placeholder="请输入密码"
                :disabled="loading"
              />
              <button
                type="button"
                @click="showPassword = !showPassword"
                class="absolute inset-y-0 right-0 pr-3 flex items-center"
              >
                <EyeIcon v-if="!showPassword" class="h-5 w-5 text-gray-400" />
                <EyeSlashIcon v-else class="h-5 w-5 text-gray-400" />
              </button>
            </div>
          </div>

          <button
            type="submit"
            :disabled="loading"
            class="w-full btn-primary"
            :class="{ 'opacity-50 cursor-not-allowed': loading }"
          >
            <div v-if="loading" class="loading-dots">
              <span style="--delay: 0"></span>
              <span style="--delay: 1"></span>
              <span style="--delay: 2"></span>
            </div>
            <span v-else>{{ t('login') }}</span>
          </button>

          <!-- 忘记密码链接 -->
          <div class="text-center mt-4">
            <button
              type="button"
              @click="activeTab = 'forgot-password'"
              class="text-sm text-gray-500 hover:text-primary-600 transition-colors duration-200"
            >
              忘记密码？
            </button>
          </div>
        </form>

        <!-- 忘记密码表单 -->
        <div v-if="activeTab === 'forgot-password'" class="space-y-6">
          <!-- 步骤1: 输入手机号 -->
          <div v-if="forgotPasswordStep === 1">
            <div class="text-center mb-6">
              <h3 class="text-lg font-medium text-gray-900 mb-2">找回密码</h3>
              <p class="text-sm text-gray-600">请输入您的手机号，我们将发送验证码</p>
            </div>
            
            <form @submit.prevent="handleSendVerificationCode" class="space-y-6">
              <div>
                <label for="forgot-phone" class="block text-sm font-medium text-gray-700 mb-2">
                  手机号
                </label>
                <input
                  id="forgot-phone"
                  v-model="forgotPasswordForm.phone"
                  type="tel"
                  required
                  class="input-base"
                  placeholder="请输入手机号"
                  :disabled="loading"
                />
              </div>

              <button
                type="submit"
                :disabled="loading || !forgotPasswordForm.phone"
                class="w-full btn-primary"
                :class="{ 'opacity-50 cursor-not-allowed': loading || !forgotPasswordForm.phone }"
              >
                <div v-if="loading" class="loading-dots">
                  <span style="--delay: 0"></span>
                  <span style="--delay: 1"></span>
                  <span style="--delay: 2"></span>
                </div>
                <span v-else>发送验证码</span>
              </button>

              <!-- 返回登录按钮 -->
              <div class="text-center mt-4">
                <button
                  type="button"
                  @click="activeTab = 'login'; resetForgotPasswordForm()"
                  class="text-sm text-gray-500 hover:text-primary-600 transition-colors duration-200"
                >
                  ← 返回登录
                </button>
              </div>
            </form>
          </div>

          <!-- 步骤2: 输入验证码 -->
          <div v-if="forgotPasswordStep === 2">
            <div class="text-center mb-6">
              <h3 class="text-lg font-medium text-gray-900 mb-2">验证手机号</h3>
              <p class="text-sm text-gray-600">
                验证码已发送至 {{ forgotPasswordForm.phone }}
                <br>
                <span class="text-primary-600">验证码: {{ verificationCode }}</span>
                <br>
                <span class="text-gray-500">{{ countdown }}秒内有效</span>
              </p>
            </div>
            
            <form @submit.prevent="handleVerifyCode" class="space-y-6">
              <div>
                <label for="verification-code" class="block text-sm font-medium text-gray-700 mb-2">
                  验证码
                </label>
                <input
                  id="verification-code"
                  v-model="forgotPasswordForm.verificationCode"
                  type="text"
                  maxlength="6"
                  required
                  class="input-base text-center text-lg tracking-widest"
                  placeholder="请输入6位验证码"
                  :disabled="loading"
                />
              </div>

              <div class="flex space-x-3">
                <button
                  type="button"
                  @click="forgotPasswordStep = 1"
                  class="flex-1 btn-secondary"
                  :disabled="loading"
                >
                  返回
                </button>
                <button
                  type="submit"
                  :disabled="loading || !forgotPasswordForm.verificationCode"
                  class="flex-1 btn-primary"
                  :class="{ 'opacity-50 cursor-not-allowed': loading || !forgotPasswordForm.verificationCode }"
                >
                  <div v-if="loading" class="loading-dots">
                    <span style="--delay: 0"></span>
                    <span style="--delay: 1"></span>
                    <span style="--delay: 2"></span>
                  </div>
                  <span v-else>验证</span>
                </button>
              </div>
            </form>
          </div>

          <!-- 步骤3: 重置密码 -->
          <div v-if="forgotPasswordStep === 3">
            <div class="text-center mb-6">
              <h3 class="text-lg font-medium text-gray-900 mb-2">设置新密码</h3>
              <p class="text-sm text-gray-600">请设置您的新密码</p>
            </div>
            
            <form @submit.prevent="handleResetPassword" class="space-y-6">
              <div>
                <label for="new-password" class="block text-sm font-medium text-gray-700 mb-2">
                  新密码
                </label>
                <div class="relative">
                  <input
                    id="new-password"
                    v-model="forgotPasswordForm.newPassword"
                    :type="showNewPassword ? 'text' : 'password'"
                    required
                    class="input-base pr-10"
                    placeholder="请输入新密码（至少6位）"
                    :disabled="loading"
                  />
                  <button
                    type="button"
                    @click="showNewPassword = !showNewPassword"
                    class="absolute inset-y-0 right-0 pr-3 flex items-center"
                  >
                    <EyeIcon v-if="!showNewPassword" class="h-5 w-5 text-gray-400" />
                    <EyeSlashIcon v-else class="h-5 w-5 text-gray-400" />
                  </button>
                </div>
              </div>

              <div>
                <label for="confirm-new-password" class="block text-sm font-medium text-gray-700 mb-2">
                  确认新密码
                </label>
                <div class="relative">
                  <input
                    id="confirm-new-password"
                    v-model="forgotPasswordForm.confirmNewPassword"
                    :type="showConfirmPassword ? 'text' : 'password'"
                    required
                    class="input-base pr-10"
                    placeholder="请再次输入新密码"
                    :disabled="loading"
                  />
                  <button
                    type="button"
                    @click="showConfirmPassword = !showConfirmPassword"
                    class="absolute inset-y-0 right-0 pr-3 flex items-center"
                  >
                    <EyeIcon v-if="!showConfirmPassword" class="h-5 w-5 text-gray-400" />
                    <EyeSlashIcon v-else class="h-5 w-5 text-gray-400" />
                  </button>
                </div>
              </div>

              <div class="flex space-x-3">
                <button
                  type="button"
                  @click="forgotPasswordStep = 2"
                  class="flex-1 btn-secondary"
                  :disabled="loading"
                >
                  返回
                </button>
                <button
                  type="submit"
                  :disabled="loading || !isResetPasswordValid"
                  class="flex-1 btn-primary"
                  :class="{ 'opacity-50 cursor-not-allowed': loading || !isResetPasswordValid }"
                >
                  <div v-if="loading" class="loading-dots">
                    <span style="--delay: 0"></span>
                    <span style="--delay: 1"></span>
                    <span style="--delay: 2"></span>
                  </div>
                  <span v-else>重置密码</span>
                </button>
              </div>
            </form>
          </div>
        </div>

        <!-- 注册表单 -->
        <form v-else-if="activeTab === 'register'" @submit.prevent="handleRegister" class="space-y-6">
          <!-- 年龄段选择 -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-3">
              {{ t('selectAgeGroup') }}
            </label>
            <div class="grid grid-cols-2 lg:grid-cols-4 gap-3">
              <button
                v-for="group in ageGroups"
                :key="group.value"
                type="button"
                @click="registerForm.ageGroup = group.value; validateField('ageGroup', group.value)"
                :class="[
                  'p-3 border-2 rounded-lg text-left transition-all duration-200',
                  registerForm.ageGroup === group.value
                    ? 'text-white'
                    : 'border-gray-200 hover:border-gray-300'
                ]"
                :style="registerForm.ageGroup === group.value ? { 
                  borderColor: 'var(--color-primary)', 
                  backgroundColor: 'var(--color-primary)' 
                } : {}"
              >
                <div class="font-medium text-sm">{{ group.name }}</div>
                <div class="text-xs text-gray-500 mt-1">{{ group.range }}</div>
              </button>
            </div>
            <div v-if="fieldErrors.ageGroup" class="mt-2 text-sm text-red-600">
              {{ fieldErrors.ageGroup }}
            </div>
          </div>

          <!-- 基本信息 - 两列布局 -->
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
            <div>
              <label for="reg-phone" class="block text-sm font-medium text-gray-700 mb-2">
                {{ t('phoneNumber') }}
              </label>
              <input
                id="reg-phone"
                v-model="registerForm.phone"
                @input="validateField('phone', registerForm.phone)"
                @blur="validateField('phone', registerForm.phone)"
                type="tel"
                required
                :class="[
                  'input-base',
                  fieldErrors.phone ? 'border-red-500 focus:border-red-500' : ''
                ]"
                :placeholder="t('enterPhoneNumber')"
                :disabled="loading"
              />
              <div v-if="fieldErrors.phone" class="mt-1 text-sm text-red-600">
                {{ fieldErrors.phone }}
              </div>
            </div>

            <div>
              <label for="reg-password" class="block text-sm font-medium text-gray-700 mb-2">
                {{ t('password') }}
              </label>
              <input
                id="reg-password"
                v-model="registerForm.password"
                @input="validateField('password', registerForm.password)"
                @blur="validateField('password', registerForm.password)"
                type="password"
                required
                :class="[
                  'input-base',
                  fieldErrors.password ? 'border-red-500 focus:border-red-500' : ''
                ]"
                :placeholder="t('passwordMin6')"
                :disabled="loading"
              />
              <div v-if="fieldErrors.password" class="mt-1 text-sm text-red-600">
                {{ fieldErrors.password }}
              </div>
            </div>

            <div class="lg:col-span-2">
              <label for="confirm-password" class="block text-sm font-medium text-gray-700 mb-2">
                {{ t('confirmPassword') }}
              </label>
              <input
                id="confirm-password"
                v-model="registerForm.confirmPassword"
                @input="validateField('confirmPassword', registerForm.confirmPassword)"
                @blur="validateField('confirmPassword', registerForm.confirmPassword)"
                type="password"
                required
                :class="[
                  'input-base',
                  fieldErrors.confirmPassword ? 'border-red-500 focus:border-red-500' : ''
                ]"
                :placeholder="t('reEnterPassword')"
                :disabled="loading"
              />
              <div v-if="fieldErrors.confirmPassword" class="mt-1 text-sm text-red-600">
                {{ fieldErrors.confirmPassword }}
              </div>
            </div>
          </div>

          <!-- 年龄段特殊设置 -->
          <div v-if="registerForm.ageGroup === 'teen' || registerForm.ageGroup === 'elder'" 
               class="grid grid-cols-1 lg:grid-cols-2 gap-4 p-4 rounded-lg border"
               :class="registerForm.ageGroup === 'teen' ? 'bg-yellow-50 border-yellow-200' : 'bg-green-50 border-green-200'">
            
            <!-- 标题跨两列 -->
            <div class="lg:col-span-2">
              <h4 class="font-medium" 
                  :class="registerForm.ageGroup === 'teen' ? 'text-yellow-800' : 'text-green-800'">
                {{ registerForm.ageGroup === 'teen' ? t('teenSpecialSettings') : t('elderlyUserSettings') }}
              </h4>
            </div>
            
            <!-- 青少年特殊字段 -->
            <template v-if="registerForm.ageGroup === 'teen'">
              <div>
                <label for="parent-phone" class="block text-sm font-medium text-gray-700 mb-2">
                  家长手机号（必填）
                </label>
                <input
                  id="parent-phone"
                  v-model="registerForm.parentPhone"
                  @input="validateField('parentPhone', registerForm.parentPhone)"
                  @blur="validateField('parentPhone', registerForm.parentPhone)"
                  type="tel"
                  required
                  :class="[
                    'input-base',
                    fieldErrors.parentPhone ? 'border-red-500 focus:border-red-500' : ''
                  ]"
                  placeholder="请输入家长手机号"
                  :disabled="loading"
                />
                <div v-if="fieldErrors.parentPhone" class="mt-1 text-sm text-red-600">
                  {{ fieldErrors.parentPhone }}
                </div>
              </div>

              <div class="flex items-start pt-7">
                <input
                  id="parental-consent"
                  v-model="registerForm.parentalConsent"
                  type="checkbox"
                  required
                  class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded mt-1 flex-shrink-0"
                />
                <label for="parental-consent" class="ml-2 text-sm text-gray-700">
                  我已获得家长同意使用此服务，并理解家长有权查看我的使用情况摘要
                </label>
              </div>
            </template>

            <!-- 老年用户特殊字段 -->
            <template v-if="registerForm.ageGroup === 'elder'">
              <div>
                <label for="helper-phone" class="block text-sm font-medium text-gray-700 mb-2">
                  子女联系方式（选填）
                </label>
                <input
                  id="helper-phone"
                  v-model="registerForm.helperPhone"
                  @input="validateField('helperPhone', registerForm.helperPhone)"
                  @blur="validateField('helperPhone', registerForm.helperPhone)"
                  type="tel"
                  :class="[
                    'input-base',
                    fieldErrors.helperPhone ? 'border-red-500 focus:border-red-500' : ''
                  ]"
                  placeholder="子女可协助管理账户"
                  :disabled="loading"
                />
                <div v-if="fieldErrors.helperPhone" class="mt-1 text-sm text-red-600">
                  {{ fieldErrors.helperPhone }}
                </div>
              </div>

              <div class="flex items-start pt-7">
                <input
                  id="voice-priority"
                  v-model="registerForm.voicePriority"
                  type="checkbox"
                  class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded mt-1 flex-shrink-0"
                />
                <label for="voice-priority" class="ml-2 text-sm text-gray-700">
                  优先使用语音交互（推荐）
                </label>
              </div>
            </template>
          </div>

          <!-- 用户协议和注册按钮 -->
          <div class="grid grid-cols-1 lg:grid-cols-3 gap-4 items-center">
            <div class="lg:col-span-2 flex items-start">
              <input
                id="terms"
                v-model="registerForm.agreeTerms"
                type="checkbox"
                required
                class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded mt-1 flex-shrink-0"
              />
              <label for="terms" class="ml-2 text-sm text-gray-700">
                我已阅读并同意 
                <a href="#" class="text-primary-600 hover:text-primary-500">用户协议</a> 
                和 
                <a href="#" class="text-primary-600 hover:text-primary-500">隐私政策</a>
              </label>
            </div>

            <button
              type="submit"
              :disabled="loading || !isRegisterFormValid"
              class="btn-primary"
              :class="{ 'opacity-50 cursor-not-allowed': loading || !isRegisterFormValid }"
              @click="!isRegisterFormValid && showFormErrors()"
            >
              <div v-if="loading" class="loading-dots">
                <span style="--delay: 0"></span>
                <span style="--delay: 1"></span>
                <span style="--delay: 2"></span>
              </div>
              <span v-else>注册</span>
            </button>
          </div>
        </form>

        <!-- 其他登录方式 -->
        <div v-if="activeTab !== 'forgot-password'" class="mt-6">
          <div class="relative">
            <div class="absolute inset-0 flex items-center">
              <div class="w-full border-t border-gray-300"></div>
            </div>
            <div class="relative flex justify-center text-sm">
              <span class="px-2 text-gray-500" style="background-color: var(--color-background);">或</span>
            </div>
          </div>

          <div class="mt-6" :class="activeTab === 'register' ? 'max-w-md mx-auto' : ''">
            <button
              @click="handleGuestLogin"
              :disabled="loading"
              class="w-full btn-secondary"
            >
              <UserIcon class="h-5 w-5 mr-2" />
              {{ t('guestExperience') }}
            </button>
          </div>
        </div>
      </div>

      <!-- 底部信息 -->
      <div class="text-center text-sm text-gray-500" :class="activeTab === 'register' ? 'max-w-2xl mx-auto' : ''">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-2" :class="activeTab === 'register' ? 'md:grid-cols-2' : 'md:grid-cols-1'">
          <p>{{ t('troubleContactCustomerService') }}400-161-9995</p>
          <p>
            {{ t('serviceStandard') }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'
import {
  HeartIcon,
  EyeIcon,
  EyeSlashIcon,
  UserIcon
} from '@heroicons/vue/24/outline'
import LanguageSwitcher from '@/components/LanguageSwitcher.vue'
import { t } from '@/stores/language'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

// 响应式状态
const activeTab = ref('login')
const loading = ref(false)
const showPassword = ref(false)
const showNewPassword = ref(false)
const showConfirmPassword = ref(false)

// 忘记密码相关状态
const forgotPasswordStep = ref(1)
const verificationCode = ref('')
const countdown = ref(0)
const countdownTimer = ref(null)

// 登录表单
const loginForm = ref({
  phone: '',
  password: ''
})

// 注册表单
const registerForm = ref({
  phone: '',
  password: '',
  confirmPassword: '',
  ageGroup: '',
  parentPhone: '', // 青少年家长手机号
  parentalConsent: false, // 家长同意
  helperPhone: '', // 老年用户子女手机号
  voicePriority: false, // 语音优先
  agreeTerms: false
})

// 忘记密码表单
const forgotPasswordForm = ref({
  phone: '',
  verificationCode: '',
  newPassword: '',
  confirmNewPassword: ''
})

// 字段错误状态
const fieldErrors = ref({
  phone: '',
  password: '',
  confirmPassword: '',
  ageGroup: '',
  parentPhone: '',
  helperPhone: ''
})

// 年龄段选项
const ageGroups = computed(() => [
  { value: 'teen', name: t('teenMode'), range: '12-18岁' },
  { value: 'young', name: t('youngMode'), range: '19-35岁' },
  { value: 'middle', name: t('middleMode'), range: '36-59岁' },
  { value: 'elder', name: t('elderMode'), range: '60岁+' }
])

// 显示表单错误提示
const showFormErrors = () => {
  // 触发所有字段的验证
  validateField('phone', registerForm.value.phone)
  validateField('password', registerForm.value.password)
  validateField('confirmPassword', registerForm.value.confirmPassword)
  validateField('ageGroup', registerForm.value.ageGroup)
  validateField('parentPhone', registerForm.value.parentPhone)
  validateField('helperPhone', registerForm.value.helperPhone)
  
  // 收集所有错误
  const errors = []
  if (fieldErrors.value.phone) errors.push(fieldErrors.value.phone)
  if (fieldErrors.value.password) errors.push(fieldErrors.value.password)
  if (fieldErrors.value.confirmPassword) errors.push(fieldErrors.value.confirmPassword)
  if (fieldErrors.value.ageGroup) errors.push(fieldErrors.value.ageGroup)
  if (fieldErrors.value.parentPhone) errors.push(fieldErrors.value.parentPhone)
  if (fieldErrors.value.helperPhone) errors.push(fieldErrors.value.helperPhone)
  
  // 检查必填字段
  if (!registerForm.value.phone) errors.push('请输入手机号')
  if (!registerForm.value.password) errors.push('请输入密码')
  if (!registerForm.value.confirmPassword) errors.push('请确认密码')
  if (!registerForm.value.ageGroup) errors.push('请选择年龄段')
  if (!registerForm.value.agreeTerms) errors.push('请同意用户协议')
  
  // 青少年特殊验证
  if (registerForm.value.ageGroup === 'teen') {
    if (!registerForm.value.parentPhone) errors.push('青少年用户需要填写家长手机号')
    if (!registerForm.value.parentalConsent) errors.push('青少年用户需要家长同意')
  }
  
  // 老年用户特殊验证
  if (registerForm.value.ageGroup === 'elder') {
    if (!registerForm.value.helperPhone) errors.push('老年用户需要填写子女联系方式')
  }
  
  // 显示第一个错误
  if (errors.length > 0) {
    if (window.$notification) {
      window.$notification.error(errors[0])
    }
  }
}

// 实时验证函数
const validateField = (field, value) => {
  switch (field) {
    case 'phone':
      if (!value) {
        fieldErrors.value.phone = '请输入手机号'
      } else if (!/^1[3-9]\d{9}$|^1\d{10}$/.test(value)) {
        fieldErrors.value.phone = '请输入正确的手机号格式'
      } else {
        fieldErrors.value.phone = ''
      }
      break
    case 'password':
      if (!value) {
        fieldErrors.value.password = '请输入密码'
      } else if (value.length < 6) {
        fieldErrors.value.password = '密码长度至少6位'
      } else {
        fieldErrors.value.password = ''
      }
      break
    case 'confirmPassword':
      if (!value) {
        fieldErrors.value.confirmPassword = '请确认密码'
      } else if (value !== registerForm.value.password) {
        fieldErrors.value.confirmPassword = '两次输入的密码不一致'
      } else {
        fieldErrors.value.confirmPassword = ''
      }
      break
    case 'ageGroup':
      if (!value) {
        fieldErrors.value.ageGroup = '请选择年龄段'
      } else {
        fieldErrors.value.ageGroup = ''
      }
      break
    case 'parentPhone':
      if (registerForm.value.ageGroup === 'teen') {
        if (!value) {
          fieldErrors.value.parentPhone = '青少年用户需要填写家长手机号'
        } else if (!/^1[3-9]\d{9}$|^1\d{10}$/.test(value)) {
          fieldErrors.value.parentPhone = '家长手机号格式不正确'
        } else {
          fieldErrors.value.parentPhone = ''
        }
      } else {
        fieldErrors.value.parentPhone = ''
      }
      break
    case 'helperPhone':
      if (registerForm.value.ageGroup === 'elder') {
        if (!value) {
          fieldErrors.value.helperPhone = '老年用户需要填写子女联系方式'
        } else if (!/^1[3-9]\d{9}$|^1\d{10}$/.test(value)) {
          fieldErrors.value.helperPhone = '子女联系方式格式不正确'
        } else {
          fieldErrors.value.helperPhone = ''
        }
      } else {
        fieldErrors.value.helperPhone = ''
      }
      break
  }
}

// 计算属性
const isRegisterFormValid = computed(() => {
  const basic = registerForm.value.phone && 
                registerForm.value.password && 
                registerForm.value.confirmPassword &&
                registerForm.value.ageGroup &&
                registerForm.value.agreeTerms &&
                registerForm.value.password === registerForm.value.confirmPassword

  // 青少年额外验证
  if (registerForm.value.ageGroup === 'teen') {
    return basic && registerForm.value.parentPhone && registerForm.value.parentalConsent
  }

  return basic
})

// 忘记密码表单验证
const isResetPasswordValid = computed(() => {
  return forgotPasswordForm.value.newPassword && 
         forgotPasswordForm.value.confirmNewPassword &&
         forgotPasswordForm.value.newPassword === forgotPasswordForm.value.confirmNewPassword &&
         forgotPasswordForm.value.newPassword.length >= 6
})

// 方法
const handleLogin = async () => {
  loading.value = true
  
  try {
    // 调用真实API
    const result = await userStore.apiLogin({
      phone: loginForm.value.phone,
      password: loginForm.value.password
    })
    
    if (result.success) {
      // 设置年龄段（从后端返回的用户数据中获取）
      if (result.data.user.age_group) {
        userStore.setAgeGroup(result.data.user.age_group)
      }
      
      // 显示成功通知
      if (window.$notification) {
        window.$notification.success(t('loginSuccess'), t('welcomeBack'))
      }
      
      // 跳转到目标页面或首页
      const redirect = route.query.redirect || '/'
      router.push(redirect)
    } else {
      // 显示具体错误信息
      let errorMessage = t('loginFailed')
      console.log('登录错误详情:', result.error) // 调试信息
      
      if (result.error) {
        // 根据后端返回的具体错误信息显示
        // 优先检查具体的业务错误
        if (result.error.includes('用户不存在')) {
          errorMessage = '用户不存在，请检查手机号是否正确'
        } else if (result.error.includes('登录凭证无效')) {
          errorMessage = '登录凭证无效，请检查手机号和密码'
        } else if (result.error.includes('用户账户已被禁用')) {
          errorMessage = '账户已被禁用，请联系客服'
        } else if (result.error.includes('必须提供手机号和密码')) {
          errorMessage = '请输入手机号和密码'
        } else if (result.error.includes('请输入有效的手机号码')) {
          errorMessage = '手机号格式不正确，请输入11位手机号'
        } else if (result.error.includes('登录信息验证失败')) {
          errorMessage = '登录信息格式不正确，请检查输入'
        } else if (result.error.includes('网络错误') || result.error.includes('Network Error')) {
          errorMessage = '网络连接失败，请检查网络后重试'
        } else if (result.error.includes('服务器错误') || result.error.includes('Server Error')) {
          errorMessage = '服务器暂时不可用，请稍后重试'
        } else if (result.error.includes('请求超时') || result.error.includes('timeout')) {
          errorMessage = '请求超时，请检查网络连接'
        } else if (result.error.includes('登录已过期')) {
          errorMessage = '登录已过期，请重新登录'
        } else {
          errorMessage = result.error
        }
      }
      
      if (window.$notification) {
        window.$notification.error(errorMessage)
      }
    }
    
  } catch (error) {
    console.error('登录失败:', error)
    if (window.$notification) {
      window.$notification.error(t('loginFailed'))
    }
  } finally {
    loading.value = false
  }
}

const handleRegister = async () => {
  // 前端表单验证
  const validationErrors = []
  
  // 手机号验证
  if (!registerForm.value.phone) {
    validationErrors.push('请输入手机号')
  } else if (!/^1[3-9]\d{9}$|^1\d{10}$/.test(registerForm.value.phone)) {
    validationErrors.push('请输入正确的手机号格式')
  }
  
  // 密码验证
  if (!registerForm.value.password) {
    validationErrors.push('请输入密码')
  } else if (registerForm.value.password.length < 6) {
    validationErrors.push('密码长度至少6位')
  }
  
  // 确认密码验证
  if (!registerForm.value.confirmPassword) {
    validationErrors.push('请确认密码')
  } else if (registerForm.value.password !== registerForm.value.confirmPassword) {
    validationErrors.push('两次输入的密码不一致')
  }
  
  // 年龄段验证
  if (!registerForm.value.ageGroup) {
    validationErrors.push('请选择年龄段')
  }
  
  // 青少年用户特殊验证
  if (registerForm.value.ageGroup === 'teen') {
    if (!registerForm.value.parentPhone) {
      validationErrors.push('青少年用户需要填写家长手机号')
    } else if (!/^1[3-9]\d{9}$|^1\d{10}$/.test(registerForm.value.parentPhone)) {
      validationErrors.push('家长手机号格式不正确')
    }
    if (!registerForm.value.parentalConsent) {
      validationErrors.push('青少年用户需要家长同意')
    }
  }
  
  // 老年用户特殊验证
  if (registerForm.value.ageGroup === 'elder') {
    if (!registerForm.value.helperPhone) {
      validationErrors.push('老年用户需要填写子女联系方式')
    } else if (!/^1[3-9]\d{9}$|^1\d{10}$/.test(registerForm.value.helperPhone)) {
      validationErrors.push('子女联系方式格式不正确')
    }
  }
  
  // 显示验证错误
  if (validationErrors.length > 0) {
    if (window.$notification) {
      window.$notification.error(validationErrors[0]) // 显示第一个错误
    }
    return
  }

  loading.value = true
  
  try {
    // 准备注册数据
    const registerData = {
      phone: registerForm.value.phone,
      password: registerForm.value.password,
      confirm_password: registerForm.value.confirmPassword, // 后端需要的确认密码字段
      username: registerForm.value.phone, // 使用手机号作为用户名
      age_group: registerForm.value.ageGroup,
      gender: 'prefer_not_say', // 默认性别
      nickname: '', // 默认昵称
      // 青少年特殊字段
      ...(registerForm.value.ageGroup === 'teen' && {
        parent_phone: registerForm.value.parentPhone,
        parental_consent: registerForm.value.parentalConsent
      }),
      // 老年用户特殊字段
      ...(registerForm.value.ageGroup === 'elder' && {
        helper_phone: registerForm.value.helperPhone,
        voice_priority: registerForm.value.voicePriority
      })
    }
    
    // 调用真实API
    const result = await userStore.apiRegister(registerData)
    
    if (result.success) {
      // 设置年龄段
      userStore.setAgeGroup(registerForm.value.ageGroup)
      
      // 青少年用户发送家长通知
      if (registerForm.value.ageGroup === 'teen' && registerForm.value.parentPhone) {
        // 这里应该调用API发送短信通知家长
        console.log('发送家长通知到:', registerForm.value.parentPhone)
      }
      
      // 显示成功通知
      if (window.$notification) {
        window.$notification.success(t('registerSuccess'), t('welcomeToOmnisolace'))
      }
      
      // 跳转到首页
      router.push('/')
    } else {
      // 显示具体错误信息
      let errorMessage = t('registerFailed')
      if (result.error) {
        // 根据后端返回的具体错误信息显示
        if (result.error.includes('该手机号已被注册')) {
          errorMessage = '该手机号已被注册，请使用其他手机号或直接登录'
        } else if (result.error.includes('密码不匹配')) {
          errorMessage = '两次输入的密码不一致'
        } else if (result.error.includes('青少年用户必须提供家长手机号')) {
          errorMessage = '青少年用户必须填写家长手机号'
        } else if (result.error.includes('青少年用户必须获得家长同意')) {
          errorMessage = '青少年用户需要家长同意才能注册'
        } else if (result.error.includes('请输入有效的手机号码')) {
          errorMessage = '手机号格式不正确，请输入11位手机号'
        } else if (result.error.includes('该字段是必填项')) {
          errorMessage = '请填写所有必填信息'
        } else if (result.error.includes('注册信息验证失败')) {
          errorMessage = '注册信息格式不正确，请检查输入'
        } else if (result.error.includes('用户名已存在')) {
          errorMessage = '用户名已存在，请使用其他用户名'
        } else if (result.error.includes('密码长度至少6位')) {
          errorMessage = '密码长度至少6位'
        } else if (result.error.includes('年龄段选择无效')) {
          errorMessage = '请选择有效的年龄段'
        } else if (result.error.includes('家长手机号格式不正确')) {
          errorMessage = '家长手机号格式不正确'
        } else if (result.error.includes('子女联系方式格式不正确')) {
          errorMessage = '子女联系方式格式不正确'
        } else if (result.error.includes('网络错误') || result.error.includes('Network Error')) {
          errorMessage = '网络连接失败，请检查网络后重试'
        } else if (result.error.includes('服务器错误') || result.error.includes('Server Error')) {
          errorMessage = '服务器暂时不可用，请稍后重试'
        } else if (result.error.includes('请求超时') || result.error.includes('timeout')) {
          errorMessage = '请求超时，请检查网络连接'
        } else if (result.error.includes('注册失败，请稍后重试')) {
          errorMessage = '注册失败，请稍后重试'
        } else {
          errorMessage = result.error
        }
      }
      
      if (window.$notification) {
        window.$notification.error(errorMessage)
      }
    }
    
  } catch (error) {
    console.error('注册失败:', error)
    if (window.$notification) {
      window.$notification.error(t('registerFailed'))
    }
  } finally {
    loading.value = false
  }
}

const handleGuestLogin = async () => {
  loading.value = true
  
  try {
    // 调用真实API游客登录
    const result = await userStore.apiGuestLogin({
      age_group: 'young' // 默认青年用户
    })
    
    if (result.success) {
      // 设置年龄段
      userStore.setAgeGroup('young')
      
      if (window.$notification) {
        window.$notification.info('已进入游客模式', '功能受限，建议注册获得完整体验')
      }
      
      router.push('/')
    } else {
      // 显示错误信息
      if (window.$notification) {
        window.$notification.error(result.error || '游客登录失败')
      }
    }
    
  } catch (error) {
    console.error('游客登录失败:', error)
    if (window.$notification) {
      window.$notification.error('游客登录失败')
    }
  } finally {
    loading.value = false
  }
}

// 忘记密码相关方法
const handleSendVerificationCode = async () => {
  loading.value = true
  
  try {
    const response = await fetch('http://localhost:8000/api/v1/auth/forgot-password/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        phone: forgotPasswordForm.value.phone
      })
    })
    
    const result = await response.json()
    
    if (result.success) {
      // 保存验证码（开发环境）
      verificationCode.value = result.data.verification_code
      
      // 开始倒计时
      startCountdown()
      
      // 进入下一步
      forgotPasswordStep.value = 2
      
      if (window.$notification) {
        window.$notification.success('验证码已发送', '请查收短信验证码')
      }
    } else {
      if (window.$notification) {
        window.$notification.error(result.message || '发送验证码失败')
      }
    }
    
  } catch (error) {
    console.error('发送验证码失败:', error)
    if (window.$notification) {
      window.$notification.error('网络错误，请稍后重试')
    }
  } finally {
    loading.value = false
  }
}

const handleVerifyCode = async () => {
  loading.value = true
  
  try {
    const response = await fetch('http://localhost:8000/api/v1/auth/verify-reset-code/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        phone: forgotPasswordForm.value.phone,
        verification_code: forgotPasswordForm.value.verificationCode
      })
    })
    
    const result = await response.json()
    
    if (result.success) {
      // 进入重置密码步骤
      forgotPasswordStep.value = 3
      
      if (window.$notification) {
        window.$notification.success('验证成功', '请设置新密码')
      }
    } else {
      if (window.$notification) {
        window.$notification.error(result.message || '验证码错误')
      }
    }
    
  } catch (error) {
    console.error('验证码验证失败:', error)
    if (window.$notification) {
      window.$notification.error('网络错误，请稍后重试')
    }
  } finally {
    loading.value = false
  }
}

const handleResetPassword = async () => {
  // 前端验证
  if (!isResetPasswordValid.value) {
    if (window.$notification) {
      window.$notification.error('请填写完整的新密码信息')
    }
    return
  }
  
  loading.value = true
  
  try {
    const response = await fetch('http://localhost:8000/api/v1/auth/reset-password/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        phone: forgotPasswordForm.value.phone,
        verification_code: forgotPasswordForm.value.verificationCode,
        new_password: forgotPasswordForm.value.newPassword,
        confirm_password: forgotPasswordForm.value.confirmNewPassword
      })
    })
    
    const result = await response.json()
    
    if (result.success) {
      if (window.$notification) {
        window.$notification.success('密码重置成功', '请使用新密码登录')
      }
      
      // 重置表单状态
      resetForgotPasswordForm()
      
      // 跳转到登录页面
      activeTab.value = 'login'
      
    } else {
      if (window.$notification) {
        window.$notification.error(result.message || '密码重置失败')
      }
    }
    
  } catch (error) {
    console.error('密码重置失败:', error)
    if (window.$notification) {
      window.$notification.error('网络错误，请稍后重试')
    }
  } finally {
    loading.value = false
  }
}

const startCountdown = () => {
  countdown.value = 60
  countdownTimer.value = setInterval(() => {
    countdown.value--
    if (countdown.value <= 0) {
      clearInterval(countdownTimer.value)
      countdownTimer.value = null
    }
  }, 1000)
}

const resetForgotPasswordForm = () => {
  forgotPasswordStep.value = 1
  forgotPasswordForm.value = {
    phone: '',
    verificationCode: '',
    newPassword: '',
    confirmNewPassword: ''
  }
  verificationCode.value = ''
  if (countdownTimer.value) {
    clearInterval(countdownTimer.value)
    countdownTimer.value = null
  }
  countdown.value = 0
}

// 生命周期
onMounted(() => {
  // 如果已登录，重定向到首页
  if (userStore.isAuthenticated) {
    router.push('/')
  }
})

// 组件卸载时清理定时器
onUnmounted(() => {
  if (countdownTimer.value) {
    clearInterval(countdownTimer.value)
  }
})
</script>

<style scoped>
/* 响应式设计 */
@media (max-width: 640px) {
  .max-w-md {
    max-width: 24rem;
  }
  
  .p-8 {
    padding: 1.5rem;
  }
}

/* 年龄段选择按钮动画 */
.grid button {
  transition: all 0.2s ease;
}

.grid button:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

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

/* 加载动画优化 */
.loading-dots span:nth-child(1) { animation-delay: 0s; }
.loading-dots span:nth-child(2) { animation-delay: 0.2s; }
.loading-dots span:nth-child(3) { animation-delay: 0.4s; }

/* 高对比度支持 */
@media (prefers-contrast: high) {
  .bg-gradient-to-br {
    background-color: white;
  }
  
  .border-2 {
    border-width: 4px;
  }
}
</style>
