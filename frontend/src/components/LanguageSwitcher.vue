<template>
  <div class="relative">
    <button
      @click="toggleDropdown"
      class="flex items-center space-x-0.5 px-1 py-1 rounded-lg transition-colors duration-200 hover:bg-gray-100 flex-shrink-0"
      :class="{ 
        'bg-gray-100': showDropdown,
        'px-1.5 py-1.5 space-x-1': userStore.isElderMode 
      }"
      :title="currentLanguage === 'zh' ? 'Switch to English' : '切换到中文'"
    >
      <!-- 语言图标 -->
      <div class="w-3 h-3 flex items-center justify-center"
           :class="{ 'w-4 h-4': userStore.isElderMode }">
        <img 
          src="/images/translate.png" 
          alt="Translate" 
          class="w-2.5 h-2.5 object-contain"
          :class="{ 'w-3 h-3': userStore.isElderMode }"
        />
      </div>
      
      <!-- 下拉箭头 -->
      <ChevronDownIcon 
        class="w-2 h-2 text-gray-500 transition-transform duration-200"
        :class="{ 
          'rotate-180': showDropdown,
          'w-2.5 h-2.5': userStore.isElderMode 
        }"
      />
    </button>

    <!-- 下拉菜单 -->
    <div
      v-if="showDropdown"
      class="absolute top-full mt-1 w-36 bg-white rounded-lg shadow-xl border border-gray-200 py-1 z-50 right-0 language-dropdown"
      :style="isMobile ? 'max-width: calc(100vw - 2rem);' : ''"
    >
      <button
        @click="selectLanguage('zh')"
        class="w-full text-left px-3 py-2 text-sm text-gray-700 hover:bg-gray-50 transition-colors duration-150 flex items-center space-x-2"
        :class="{ 
          'bg-gray-50 text-gray-900': currentLanguage === 'zh',
          'text-elder-sm': userStore.isElderMode 
        }"
      >
        <!-- 中国国旗图标 -->
        <img 
          src="/images/cn_circle.svg" 
          alt="中国国旗" 
          class="w-4 h-4 flex-shrink-0 flag-icon"
          :class="{ 'w-5 h-5': userStore.isElderMode }"
        />
        <span>简体中文</span>
      </button>
      <div class="border-t border-gray-100 my-1"></div>
      <button
        @click="selectLanguage('en')"
        class="w-full text-left px-3 py-2 text-sm text-gray-700 hover:bg-gray-50 transition-colors duration-150 flex items-center space-x-2"
        :class="{
          'bg-gray-50 text-gray-900': currentLanguage === 'en',
          'text-elder-sm': userStore.isElderMode 
        }"
      >
        <!-- 英国国旗图标 -->
        <img 
          src="/images/gb_circle.svg" 
          alt="英国国旗" 
          class="w-4 h-4 flex-shrink-0 flag-icon"
          :class="{ 'w-5 h-5': userStore.isElderMode }"
        />
        <span>English</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { ChevronDownIcon } from '@heroicons/vue/24/outline'
import { currentLanguage, setLanguage } from '@/stores/language'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

// 响应式状态
const showDropdown = ref(false)
const isMobile = ref(window.innerWidth < 768)

// 方法
const toggleDropdown = () => {
  showDropdown.value = !showDropdown.value
}

const selectLanguage = (lang) => {
  setLanguage(lang)
  showDropdown.value = false
}

const handleClickOutside = (event) => {
  if (!event.target.closest('.relative')) {
    showDropdown.value = false
  }
}

const handleResize = () => {
  isMobile.value = window.innerWidth < 768
}

// 生命周期
onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
/* 确保下拉菜单在正确的层级 */
.z-50 {
  z-index: 50;
}

/* 移动端适配 - 使用Tailwind类处理 */

/* 国旗图标样式优化 */
.flag-icon {
  border-radius: 50%;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease;
}

.flag-icon:hover {
  transform: scale(1.05);
}

/* 下拉菜单动画 */
.dropdown-enter-active,
.dropdown-leave-active {
  transition: all 0.2s ease;
}

.dropdown-enter-from,
.dropdown-leave-to {
  opacity: 0;
  transform: translateY(-4px);
}

/* 移动端优化 */
@media (max-width: 768px) {
  .language-dropdown {
    max-width: calc(100vw - 2rem);
    right: 0;
    left: auto;
  }
  
  /* 确保下拉菜单不会超出屏幕 */
  .language-dropdown {
    transform: none;
  }
}
</style>
