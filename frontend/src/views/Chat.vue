<template>
  <div class="flex flex-col overflow-hidden page-container" :class="{ 'h-screen': !isMobile }" :style="{ height: isMobile ? 'calc(100vh - 60px)' : '100vh' }">
    <!-- 移动端顶部导航 -->
    <header class="lg:hidden border-b shadow-sm safe-area-inset-top" style="background-color: var(--color-primary-50); border-color: var(--color-primary-100);">
      <div class="px-3 sm:px-4">
        <div class="flex items-center justify-between h-14" :class="{ 'h-16': userStore.isElderMode }">
          <!-- 左侧：侧边栏按钮、返回按钮和简化标题 -->
          <div class="flex items-center min-w-0 flex-1">
            <!-- 移动端侧边栏按钮 -->
            <button
              @click="toggleSidebar"
              class="mr-2 p-1.5 text-gray-400 hover:text-gray-600 rounded-lg flex-shrink-0"
              :class="{ 'p-2 mr-3': userStore.isElderMode }"
            >
              <Bars3Icon class="h-4 w-4" :class="{ 'h-5 w-5': userStore.isElderMode }" />
            </button>
            
            <button
              @click="$router.back()"
              class="mr-2 p-1.5 text-gray-400 hover:text-gray-600 rounded-lg flex-shrink-0"
              :class="{ 'p-2 mr-3': userStore.isElderMode }"
            >
              <ArrowLeftIcon class="h-4 w-4" :class="{ 'h-5 w-5': userStore.isElderMode }" />
            </button>
            <div class="min-w-0 flex-1">
              <h1 class="text-sm font-semibold text-gray-900 truncate"
                  :class="{ 'text-base': userStore.isElderMode }">
                {{ t('psychologicalCounseling') }}
              </h1>
            </div>
          </div>
          
          <!-- 右侧：操作按钮组 -->
          <div class="flex items-center space-x-1 flex-shrink-0" :class="{ 'space-x-2': userStore.isElderMode }">
            <!-- 情绪状态指示器 -->
            <div class="flex items-center space-x-1 bg-white/50 rounded-full px-2 py-1"
                 :class="{ 'px-3 py-1.5': userStore.isElderMode }">
              <div class="emotion-indicator w-2.5 h-2.5"
                   :class="[
                     chatStore.currentEmotionLabel.bgColor,
                     { 'w-3 h-3': userStore.isElderMode }
                   ]">
              </div>
              <span class="text-xs font-medium"
                    :class="[
                      chatStore.currentEmotionLabel.color,
                      { 'text-sm': userStore.isElderMode }
                    ]">
                {{ chatStore.currentEmotionLabel.name }}
              </span>
            </div>
            
            <!-- 语言切换组件 -->
            <LanguageSwitcher />
            
            <!-- 紧急求助按钮 -->
            <button
              @click="showEmergencyModal = true"
              class="w-6 h-6 bg-red-500 text-white rounded-full shadow-md hover:bg-red-600 transition-all duration-200 flex items-center justify-center flex-shrink-0"
              :class="{ 'w-8 h-8': userStore.isElderMode }"
              :aria-label="t('emergency')"
            >
              <ExclamationTriangleIcon class="h-2.5 w-2.5" :class="{ 'h-3 w-3': userStore.isElderMode }" />
            </button>
            
          </div>
        </div>
      </div>
    </header>

    <!-- 桌面端页面标题 -->
    <div class="hidden lg:block border-b" style="background-color: var(--color-primary-50); border-color: var(--color-primary-100);">
      <div class="px-6 lg:px-8 py-4">
        <div class="flex justify-between items-center">
          <div>
            <h1 class="text-xl font-semibold text-gray-900" :class="{ 'text-elder-xl': userStore.isElderMode }">
              {{ t('psychologicalCounseling') }}
            </h1>
            <p class="text-sm text-gray-500 mt-1" :class="{ 'text-elder-sm': userStore.isElderMode }">
              {{ t('aiAssistantServing') }}
            </p>
          </div>
          
          <!-- 桌面端语言切换、情绪状态和菜单 -->
          <div class="flex items-center space-x-4">
            <!-- 语言切换组件 -->
            <LanguageSwitcher />
            
            <!-- 情绪指示器 -->
            <div class="flex items-center space-x-2">
              <div class="emotion-indicator"
                   :class="[
                     chatStore.currentEmotionLabel.bgColor,
                     { 'w-6 h-6': userStore.isElderMode }
                   ]">
              </div>
              <span class="text-sm font-medium"
                    :class="[
                      chatStore.currentEmotionLabel.color,
                      { 'text-elder-sm': userStore.isElderMode }
                    ]">
                {{ chatStore.currentEmotionLabel.name }}
              </span>
            </div>
            
          </div>
        </div>
      </div>
    </div>

    <!-- 主要内容区域 -->
    <div class="flex-1 flex overflow-hidden min-h-0 relative">
      <!-- 左侧侧边栏（桌面端） -->
      <div v-if="!isMobile" class="absolute left-0 top-0 z-10">
        <!-- 收起状态：只显示按钮组 -->
        <div v-if="isSidebarCollapsed" class="flex flex-col space-y-2 p-2">
          <!-- 展开/收起按钮 -->
          <button
            @click="toggleSidebar"
            class="p-2 bg-white rounded-lg shadow-lg hover:bg-gray-50 transition-colors duration-200 flex-shrink-0"
            :class="{ 'p-3': userStore.isElderMode }"
            title="展开侧边栏"
          >
            <ChevronRightIcon 
              class="h-4 w-4 text-gray-600" 
              :class="{ 'h-5 w-5': userStore.isElderMode }" 
            />
          </button>
          
          <!-- 新建对话按钮 -->
          <button
            @click="createNewChat"
            class="p-2 bg-primary-500 text-white rounded-lg shadow-lg hover:bg-primary-600 transition-colors duration-200 flex-shrink-0"
            :class="{ 'p-3': userStore.isElderMode }"
            :title="t('newChat')"
          >
            <PlusIcon class="h-4 w-4" :class="{ 'h-5 w-5': userStore.isElderMode }" />
          </button>
        </div>

        <!-- 展开状态：显示完整侧边栏 -->
        <aside 
          v-else
          class="bg-white/95 backdrop-blur-sm border-r border-gray-200 flex flex-col transition-all duration-300 ease-in-out rounded-r-2xl shadow-xl w-56"
          :style="{
            height: 'calc(100vh - 300px)'
          }"
        >
          <!-- 侧边栏头部 -->
          <div class="p-4 border-b border-gray-200">
            <div class="flex items-center space-x-2">
              <!-- 收起/展开按钮 -->
              <button
                @click="toggleSidebar"
                class="p-2 rounded-lg hover:bg-gray-100 transition-colors duration-200 flex-shrink-0"
                :class="{ 'p-3': userStore.isElderMode }"
                title="收起侧边栏"
              >
                <ChevronLeftIcon 
                  class="h-4 w-4 text-gray-600" 
                  :class="{ 'h-5 w-5': userStore.isElderMode }" 
                />
              </button>
              
              <!-- 新建对话按钮 -->
              <button
                @click="createNewChat"
                class="p-2 bg-primary-500 text-white rounded-lg hover:bg-primary-600 transition-colors duration-200 flex-shrink-0"
                :class="{ 'p-3': userStore.isElderMode }"
                :title="t('newChat')"
              >
                <PlusIcon class="h-4 w-4" :class="{ 'h-5 w-5': userStore.isElderMode }" />
              </button>
            </div>
          </div>
        
          <!-- 搜索框 -->
          <div class="p-4 border-b border-gray-200">
            <div class="relative">
              <input
                v-model="searchQuery"
                type="text"
                :placeholder="t('searchChatHistory')"
                class="w-full pl-10 pr-4 py-2 bg-gray-100 border border-gray-200 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent focus:bg-white transition-colors duration-200"
                :class="{ 'text-elder-base py-3': userStore.isElderMode }"
              />
              <MagnifyingGlassIcon class="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
            </div>
          </div>
          
          <!-- 历史聊天列表 -->
          <div class="flex-1 overflow-y-auto custom-scrollbar">
          <div class="p-4 space-y-2">
            <div
              v-for="chat in filteredChatHistory"
              :key="chat.id"
              @click="loadHistoryChat(chat.id)"
              :class="[
                'p-3 rounded-lg cursor-pointer transition-colors duration-200',
                chat.id === chatStore.currentChatId 
                  ? 'bg-primary-50 border border-primary-100' 
                  : 'hover:bg-gray-50'
              ]"
            >
              <h4 class="font-medium text-gray-900 mb-1 truncate"
                  :class="{ 'text-elder-base': userStore.isElderMode }"
                  :title="chat.title">
                {{ chat.title }}
              </h4>
              <p class="text-sm text-gray-500 truncate"
                 :class="{ 'text-elder-sm': userStore.isElderMode }"
                 :title="getLastMessage(chat)">
                {{ getLastMessage(chat) }}
              </p>
              <span class="text-xs text-gray-400"
                    :class="{ 'text-elder-sm': userStore.isElderMode }">
                {{ formatTime(chat.updatedAt) }}
              </span>
            </div>
            
              <!-- 空状态 -->
              <div v-if="filteredChatHistory.length === 0" class="text-center py-8">
                <p class="text-sm text-gray-500" :class="{ 'text-elder-sm': userStore.isElderMode }">
                  {{ searchQuery ? t('noSearchResults') : t('noChatHistory') }}
                </p>
              </div>
            </div>
          </div>
        </aside>
      </div>

      <!-- 移动端侧边栏弹窗 -->
      <Teleport to="body">
        <div 
          v-if="isMobile && !isSidebarCollapsed"
          class="fixed inset-0 z-50 overflow-hidden"
        >
          <!-- 遮罩层 - 点击关闭侧边栏 -->
          <div 
            class="absolute inset-0 bg-black bg-opacity-50 transition-opacity duration-300"
            @click="toggleSidebar"
          ></div>
          
          <!-- 侧边栏内容 -->
          <div 
            class="absolute left-0 top-0 h-full w-3/4 max-w-sm bg-white shadow-2xl flex flex-col transform transition-transform duration-300 ease-out"
            :class="isSidebarClosing ? 'slide-out-left' : 'slide-in-left'"
            @click.stop
          >
            <!-- 侧边栏头部 -->
            <div class="p-4 border-b border-gray-200">
              <div class="flex items-center space-x-2">
                <!-- 关闭按钮 -->
                <button
                  @click="toggleSidebar"
                  class="p-2 rounded-lg hover:bg-gray-100 transition-colors duration-200 flex-shrink-0"
                  :class="{ 'p-3': userStore.isElderMode }"
                >
                  <XMarkIcon class="h-4 w-4 text-gray-600" :class="{ 'h-5 w-5': userStore.isElderMode }" />
                </button>
                
                <!-- 新建对话按钮 -->
                <button
                  @click="createNewChat"
                  class="p-2 bg-primary-500 text-white rounded-lg hover:bg-primary-600 transition-colors duration-200 flex-shrink-0"
                  :class="{ 'p-3': userStore.isElderMode }"
                  :title="t('newChat')"
                >
                  <PlusIcon class="h-4 w-4" :class="{ 'h-5 w-5': userStore.isElderMode }" />
                </button>
              </div>
            </div>
            
            <!-- 搜索框 -->
            <div class="p-4 border-b border-gray-200">
              <div class="relative">
                <input
                  v-model="searchQuery"
                  type="text"
                  :placeholder="t('searchChatHistory')"
                  class="w-full pl-10 pr-4 py-2 bg-gray-100 border border-gray-200 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent focus:bg-white transition-colors duration-200"
                  :class="{ 'text-elder-base py-3': userStore.isElderMode }"
                />
                <MagnifyingGlassIcon class="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
              </div>
            </div>
            
            <!-- 历史聊天列表 -->
            <div class="flex-1 overflow-y-auto custom-scrollbar">
              <div class="p-4 space-y-2">
                <div
                  v-for="chat in filteredChatHistory"
                  :key="chat.id"
                  @click="loadHistoryChat(chat.id)"
                  :class="[
                    'p-3 rounded-lg cursor-pointer transition-colors duration-200',
                    chat.id === chatStore.currentChatId 
                      ? 'bg-primary-50 border border-primary-100' 
                      : 'hover:bg-gray-50'
                  ]"
                >
                  <h4 class="font-medium text-gray-900 mb-1 truncate"
                      :class="{ 'text-elder-base': userStore.isElderMode }"
                      :title="chat.title">
                    {{ chat.title }}
                  </h4>
                  <p class="text-sm text-gray-500 truncate"
                     :class="{ 'text-elder-sm': userStore.isElderMode }"
                     :title="getLastMessage(chat)">
                    {{ getLastMessage(chat) }}
                  </p>
                  <span class="text-xs text-gray-400"
                        :class="{ 'text-elder-sm': userStore.isElderMode }">
                    {{ formatTime(chat.updatedAt) }}
                  </span>
                </div>
                
                <!-- 空状态 -->
                <div v-if="filteredChatHistory.length === 0" class="text-center py-8">
                  <p class="text-sm text-gray-500" :class="{ 'text-elder-sm': userStore.isElderMode }">
                    {{ searchQuery ? t('noSearchResults') : t('noChatHistory') }}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </Teleport>

      <!-- 主对话区域 -->
      <main class="flex-1 flex flex-col min-h-0 w-full">
        <div class="relative flex-1 min-h-0">
          <!-- 对话消息区域 -->
          <div 
            class="absolute inset-0 overflow-y-auto custom-scrollbar p-4 transition-all duration-300" 
            ref="messagesContainer"
            @scroll="handleScroll"
          >
            <!-- 欢迎消息 -->
            <div v-if="!chatStore.hasMessages" class="text-center py-12">
              <div class="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4"
                   :class="{ 'w-20 h-20': userStore.isElderMode }">
                <SparklesIcon class="h-8 w-8 text-primary-500" :class="{ 'h-10 w-10': userStore.isElderMode }" />
              </div>
              <h3 class="text-lg font-semibold text-gray-900 mb-2"
                  :class="{ 'text-elder-lg': userStore.isElderMode }">
                {{ getWelcomeTitle() }}
              </h3>
              <p class="text-gray-600 mb-6 max-w-md mx-auto"
                 :class="{ 'text-elder-base': userStore.isElderMode }">
                {{ getWelcomeMessage() }}
              </p>
              
              <!-- 快速开始话题 -->
              <div class="max-w-md mx-auto">
                <h4 class="text-sm font-medium text-gray-700 mb-3"
                    :class="{ 'text-elder-base': userStore.isElderMode }">
                  {{ t('youCanChatAbout') }}
                </h4>
                <div class="grid grid-cols-1 gap-2">
                  <button
                    v-for="topic in quickTopics"
                    :key="topic.id"
                    @click="sendQuickTopic(topic.text)"
                    class="p-3 text-left bg-gray-50 hover:bg-gray-100 rounded-lg transition-colors duration-200"
                    :class="{ 'p-4 text-elder-base': userStore.isElderMode }"
                  >
                    {{ topic.text }}
                  </button>
                </div>
              </div>
            </div>

            <!-- 对话消息列表 -->
            <div v-else class="space-y-4">
              <div
                v-for="message in chatStore.messages"
                :key="message.id"
                :class="[
                  'flex',
                  message.type === 'user' ? 'justify-end' : 'justify-start'
                ]"
              >
                <!-- AI消息 -->
                <div v-if="message.type === 'ai'" class="flex items-start space-x-3 max-w-3xl">
                  <div class="w-8 h-8 bg-primary-500 rounded-full flex items-center justify-center flex-shrink-0"
                       :class="{ 'w-10 h-10': userStore.isElderMode }">
                    <SparklesIcon class="h-4 w-4 text-white" :class="{ 'h-5 w-5': userStore.isElderMode }" />
                  </div>
                  <div class="chat-bubble-ai">
                    <!-- 思考过程显示 -->
                    <div v-if="message.thinking" class="mb-3">
                      <!-- 思考过程中的显示 -->
                      <div v-if="message.isStreaming" class="mb-2">
                        <div class="flex items-center mb-2">
                          <CpuChipIcon class="h-4 w-4 text-gray-600 mr-2" />
                          <span class="text-sm font-medium text-gray-700">AI正在思考...</span>
                        </div>
                        <div class="text-sm text-gray-500 italic">
                          {{ message.thinking }}
                          <span class="inline-block w-2 h-4 bg-gray-400 ml-1 animate-pulse"></span>
                        </div>
                      </div>
                      
                      <!-- 思考完成后的摘要显示 -->
                      <div v-else class="space-y-2">
                        <div class="flex items-center justify-between p-3 bg-gray-50 border border-gray-200 rounded-lg">
                          <div class="flex items-center">
                            <CpuChipIcon class="h-4 w-4 text-gray-600 mr-2" />
                            <span class="text-sm font-medium text-gray-700">
                              已深度思考（用时{{ message.thinkingTime || 0 }}秒）
                            </span>
                          </div>
                          <button
                            @click="toggleThinkingExpansion(message.id, $event)"
                            class="flex items-center text-gray-500 hover:text-gray-700 transition-colors duration-200"
                          >
                            <ChevronUpIcon v-if="message.thinkingExpanded" class="h-4 w-4" />
                            <ChevronDownIcon v-else class="h-4 w-4" />
                          </button>
                        </div>
                        
                        <!-- 思考过程内容（可展开/收起） -->
                        <div v-if="message.thinkingExpanded" class="mt-2">
                          <div class="text-sm text-gray-500 italic">
                            {{ message.thinking }}
                          </div>
                        </div>
                      </div>
                    </div>
                    
                    <!-- 主要回答内容 -->
                    <div>
                      <span v-html="formatMessage(message.content)"></span>
                      <!-- 流式响应中的光标动画 -->
                      <span v-if="message.isStreaming && !message.thinking" class="inline-block w-2 h-4 bg-primary-500 ml-1 animate-pulse"></span>
                    </div>
                    
                    <!-- AI回复操作按钮 -->
                    <div v-if="!message.isStreaming && message.content" class="flex items-center space-x-2 mt-3 pt-2 border-t border-gray-100">
                      <!-- 复制按钮 -->
                      <button
                        @click="copyMessage(message.content)"
                        class="flex items-center space-x-1 px-2 py-1 text-xs text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded transition-colors duration-200"
                        :class="{ 'px-3 py-1.5 text-sm': userStore.isElderMode }"
                        :title="t('copyMessage')"
                      >
                        <svg class="w-3 h-3" :class="{ 'w-4 h-4': userStore.isElderMode }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                        </svg>
                        <span class="hidden sm:inline">复制</span>
                      </button>
                      
                      <!-- 重新生成按钮 -->
                      <button
                        @click="regenerateMessage(message.id)"
                        :disabled="chatStore.isLoading"
                        class="flex items-center space-x-1 px-2 py-1 text-xs text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
                        :class="{ 'px-3 py-1.5 text-sm': userStore.isElderMode }"
                        :title="t('regenerateMessage')"
                      >
                        <svg class="w-3 h-3" :class="{ 'w-4 h-4': userStore.isElderMode }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                        </svg>
                        <span class="hidden sm:inline">重新生成</span>
                      </button>
                      
                      <!-- 点赞按钮 -->
                      <button
                        @click="likeMessage(message.id)"
                        class="flex items-center space-x-1 px-2 py-1 text-xs text-gray-500 hover:text-green-600 hover:bg-green-50 rounded transition-colors duration-200"
                        :class="[
                          { 'px-3 py-1.5 text-sm': userStore.isElderMode },
                          { 'text-green-600 bg-green-50': message.userFeedback === 'like' }
                        ]"
                        :title="t('likeMessage')"
                      >
                        <svg class="w-3 h-3" :class="{ 'w-4 h-4': userStore.isElderMode }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 10h4.764a2 2 0 011.789 2.894l-3.5 7A2 2 0 0115.263 21h-4.017c-.163 0-.326-.02-.485-.06L7 20m7-10V5a2 2 0 00-2-2h-.095c-.5 0-.905.405-.905.905 0 .714-.211 1.412-.608 2.006L7 11v9m7-10h-2M7 20H5a2 2 0 01-2-2v-6a2 2 0 012-2h2.5" />
                        </svg>
                        <span class="hidden sm:inline">点赞</span>
                      </button>
                      
                      <!-- 踩按钮 -->
                      <button
                        @click="dislikeMessage(message.id)"
                        class="flex items-center space-x-1 px-2 py-1 text-xs text-gray-500 hover:text-red-600 hover:bg-red-50 rounded transition-colors duration-200"
                        :class="[
                          { 'px-3 py-1.5 text-sm': userStore.isElderMode },
                          { 'text-red-600 bg-red-50': message.userFeedback === 'dislike' }
                        ]"
                        :title="t('dislikeMessage')"
                      >
                        <svg class="w-3 h-3" :class="{ 'w-4 h-4': userStore.isElderMode }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14H5.236a2 2 0 01-1.789-2.894l3.5-7A2 2 0 018.737 3h4.018c.163 0 .326.02.485.06L17 4m-7 10v5a2 2 0 002 2h.096c.5 0 .905-.405.905-.905 0-.714.211-1.412.608-2.006L17 13V4m-7 10H8m7 0h2a2 2 0 012 2v6a2 2 0 01-2 2h-2.5" />
                        </svg>
                        <span class="hidden sm:inline">踩</span>
                      </button>
                    </div>
                    
                    <span class="text-xs text-gray-400 mt-2 block"
                          :class="{ 'text-elder-sm': userStore.isElderMode }">
                      {{ formatTime(message.timestamp) }}
                      <span v-if="message.isStreaming" class="ml-2 text-primary-500">
                        {{ message.thinking ? '正在思考...' : '正在输出...' }}
                      </span>
                    </span>
                  </div>
                </div>

                <!-- 用户消息 -->
                <div v-else-if="message.type === 'user'" class="flex items-start space-x-3 max-w-3xl justify-end w-full">
                  <div :class="{'chat-bubble-user': editingMessageId !== message.id, 'w-[85%] sm:w-full sm:max-w-xl': editingMessageId === message.id}">
                    <!-- 正常显示模式 -->
                    <div v-if="editingMessageId !== message.id">
                      <div>{{ message.content }}</div>
                      
                      <!-- 用户消息操作按钮 -->
                      <div class="flex items-center space-x-2 mt-3">
                        <!-- 复制按钮 -->
                        <button
                          @click="copyUserMessage(message.content)"
                          class="flex items-center space-x-1 px-2 py-1 text-xs text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded transition-colors duration-200"
                          :class="{ 'px-3 py-1.5 text-sm': userStore.isElderMode }"
                          :title="t('copyMessage')"
                        >
                          <svg class="w-3 h-3" :class="{ 'w-4 h-4': userStore.isElderMode }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                          </svg>
                          <span class="hidden sm:inline">复制</span>
                        </button>
                        
                        <!-- 编辑按钮 -->
                        <button
                          @click="startInlineEdit(message.id, message.content)"
                          class="flex items-center space-x-1 px-2 py-1 text-xs text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded transition-colors duration-200"
                          :class="{ 'px-3 py-1.5 text-sm': userStore.isElderMode }"
                          :title="t('editMessage')"
                        >
                          <svg class="w-3 h-3" :class="{ 'w-4 h-4': userStore.isElderMode }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                          </svg>
                          <span class="hidden sm:inline">编辑</span>
                        </button>
                      </div>
                    </div>
                    
                    <!-- 编辑模式 -->
                    <div v-else>
                      <!-- 编辑输入框容器 -->
                      <div class="edit-container">
                        <textarea
                          v-model="editingContent"
                          @keydown="handleEditKeyDown"
                          @input="adjustEditTextareaHeight"
                          class="edit-textarea text-gray-900"
                          :class="[
                            { 
                              'text-elder-base min-h-[60px] max-h-[120px]': userStore.isElderMode,
                              'min-h-[48px] max-h-[96px]': !userStore.isElderMode
                            }
                          ]"
                          rows="2"
                          maxlength="1000"
                          :ref="`editInput-${message.id}`"
                          placeholder="编辑您的消息..."
                        ></textarea>
                        
                        <!-- 操作区域 -->
                        <div class="mt-2 flex flex-col items-end space-y-2">
                          <!-- 操作按钮 -->
                          <div class="flex items-center space-x-2">
                            <button
                              @click="cancelInlineEdit"
                              class="px-4 py-2 text-sm text-gray-600 hover:text-gray-800 bg-gray-100 hover:bg-gray-200 rounded-lg transition-all duration-200"
                              :class="{ 'px-5 py-2.5 text-base': userStore.isElderMode }"
                            >
                              {{ t('cancel') }}
                            </button>
                            <button
                              @click="confirmInlineEdit(message.id)"
                              :disabled="!editingContent.trim() || chatStore.isLoading"
                              class="px-4 py-2 text-sm text-white bg-primary-500 hover:bg-primary-600 disabled:opacity-50 disabled:cursor-not-allowed rounded-lg transition-all duration-200"
                              :class="{ 'px-5 py-2.5 text-base': userStore.isElderMode }"
                            >
                              {{ t('send') }}
                            </button>
                          </div>
                          <!-- 字数统计 -->
                          <div class="w-full text-right">
                            <span class="text-xs text-gray-500"
                                  :class="{ 'text-elder-sm': userStore.isElderMode }">
                              {{ editingContent.length }}/1000
                            </span>
                          </div>
                        </div>
                      </div>
                    </div>
                    
                    
                    <!-- 时间戳（只在非编辑模式显示） -->
                    <span v-if="editingMessageId !== message.id" class="text-xs opacity-75 mt-2 block"
                          :class="{ 'text-elder-sm': userStore.isElderMode }">
                      {{ formatTime(message.timestamp) }}
                    </span>
                  </div>
                  <div class="w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 overflow-hidden"
                       :class="{ 'w-10 h-10': userStore.isElderMode }"
                       :style="getUserAvatarStyle()">
                    <img v-if="userStore.user?.avatar && !userAvatarLoadError" 
                         :src="userStore.user.avatar" 
                         :alt="userStore.user?.nickname || userStore.user?.username || '头像'"
                         class="w-full h-full object-cover rounded-full"
                         @error="handleUserAvatarError"
                         @load="handleUserAvatarLoad" />
                    <span v-else-if="!userStore.user?.avatar || userAvatarLoadError" class="text-white font-bold text-sm" :class="{ 'text-base': userStore.isElderMode }">
                      {{ getUserInitials() }}
                    </span>
                  </div>
                </div>

                <!-- 系统消息 -->
                <div v-else-if="message.type === 'system'" class="flex justify-center">
                  <div class="bg-yellow-50 border border-yellow-200 rounded-lg p-4 max-w-md text-center">
                    <ExclamationTriangleIcon class="h-6 w-6 text-yellow-600 mx-auto mb-2" />
                    <p class="text-sm text-yellow-800"
                       :class="{ 'text-elder-base': userStore.isElderMode }">
                      {{ message.content }}
                    </p>
                  </div>
                </div>
              </div>

            </div>
          </div>

          <!-- "查看最新信息"按钮 -->
          <transition
            enter-active-class="transition-opacity duration-300"
            leave-active-class="transition-opacity duration-300"
            enter-from-class="opacity-0"
            leave-to-class="opacity-0"
          >
            <button
              v-if="showScrollToBottomButton"
              @click="scrollToBottom"
              class="absolute bottom-4 left-1/2 -translate-x-1/2 z-10 bg-white/90 backdrop-blur-sm text-primary-500 rounded-full shadow-lg px-4 py-2 flex items-center text-sm font-medium hover:bg-primary-50 transition-all duration-300 ring-1 ring-gray-200"
            >
              <ChevronDownIcon class="h-4 w-4 mr-2" />
              <span>查看最新信息</span>
            </button>
          </transition>
        </div>

        <!-- 输入区域 -->
        <div 
          class="p-4 safe-area-inset-bottom flex-shrink-0 transition-all duration-300" 
          :class="{ 
            'p-6': userStore.isElderMode
          }"
        >
          <div class="max-w-4xl mx-auto">
            <!-- 语音输入提示（老年模式优先显示） -->
            <div v-if="userStore.isElderMode && speechStore.isSupported" 
                 class="mb-4 p-3 bg-blue-50 border border-blue-200 rounded-lg">
              <div class="flex items-center">
                <MicrophoneIcon class="h-5 w-5 text-blue-500 mr-2" />
                <span class="text-elder-sm text-blue-700">
                  {{ t('voiceInputSuggestion') }}
                </span>
              </div>
            </div>

            <!-- 输入容器 -->
            <div class="bg-white rounded-2xl shadow-lg border border-gray-100 p-4 transition-all duration-200 hover:shadow-xl">
              <!-- 文本输入框 -->
              <div class="relative mb-3">
                <textarea
                  v-model="inputMessage"
                  @keydown="handleKeyDown"
                  @input="adjustTextareaHeight"
                  :placeholder="getInputPlaceholder()"
                  :disabled="chatStore.isLoading"
                  class="w-full resize-none border-0 bg-transparent px-2 py-2 focus:outline-none transition-colors duration-200"
                  :class="[
                    { 
                      'text-elder-base min-h-[60px] max-h-[120px]': userStore.isElderMode,
                      'min-h-[48px] max-h-[96px]': !userStore.isElderMode,
                      'opacity-50': chatStore.isLoading
                    }
                  ]"
                  rows="1"
                  maxlength="1000"
                  ref="textInput"
                ></textarea>
                
                <!-- 字数统计 -->
                <div class="absolute bottom-1 right-2 text-xs text-gray-400"
                     :class="{ 'text-elder-sm bottom-2 right-3': userStore.isElderMode }">
                  {{ inputMessage.length }}/1000
                </div>
              </div>


              <!-- 底部控制栏 -->
              <div class="flex items-center justify-between">
                <!-- 左侧功能按钮组 -->
                <div class="flex items-center space-x-1 sm:space-x-2">
                  <!-- 模型选择 -->
                  <div class="relative">
                    <button
                      @click="showModelDropdown = !showModelDropdown"
                      class="flex items-center space-x-1 px-2 sm:px-3 py-1.5 rounded-full bg-gray-50 hover:bg-gray-100 transition-colors duration-200 text-xs sm:text-sm font-medium text-gray-700"
                      :class="{ 'bg-primary-50 text-primary-700': showModelDropdown }"
                    >
                      <span class="hidden sm:inline">{{ selectedModel }}</span>
                      <span class="sm:hidden">AI</span>
                      <ChevronDownIcon class="h-3 w-3" />
                    </button>
                    
                    <!-- 模型下拉菜单 -->
                    <div v-if="showModelDropdown" 
                         class="absolute bottom-full left-0 mb-2 w-32 sm:w-40 bg-white rounded-lg shadow-lg border border-gray-200 py-1 z-10">
                      <button
                        @click="selectedModel = 'DeepSeek'; showModelDropdown = false"
                        class="w-full text-left px-3 py-2 text-xs sm:text-sm text-gray-700 hover:bg-gray-100"
                        :class="{ 'bg-primary-50 text-primary-700': selectedModel === 'DeepSeek' }"
                      >
                        DeepSeek
                      </button>
                      <button
                        @click="selectedModel = 'GPT-4'; showModelDropdown = false"
                        class="w-full text-left px-3 py-2 text-xs sm:text-sm text-gray-700 hover:bg-gray-100"
                        :class="{ 'bg-primary-50 text-primary-700': selectedModel === 'GPT-4' }"
                      >
                        GPT-4
                      </button>
                      <button
                        @click="selectedModel = 'Claude'; showModelDropdown = false"
                        class="w-full text-left px-3 py-2 text-xs sm:text-sm text-gray-700 hover:bg-gray-100"
                        :class="{ 'bg-primary-50 text-primary-700': selectedModel === 'Claude' }"
                      >
                        Claude
                      </button>
                    </div>
                  </div>

                  <!-- 深度思考按钮 -->
                  <button
                    @click="isDeepThinking = !isDeepThinking"
                    class="flex items-center space-x-1 px-2 sm:px-3 py-1.5 rounded-full transition-colors duration-200 text-xs sm:text-sm font-medium"
                    :class="isDeepThinking 
                      ? 'bg-blue-100 text-blue-700' 
                      : 'bg-gray-50 text-gray-700 hover:bg-gray-100'"
                  >
                    <CpuChipIcon class="h-3 w-3" />
                    <span class="hidden sm:inline">R1 深度思考</span>
                    <span class="sm:hidden">R1</span>
                  </button>

                  <!-- 联网搜索按钮 -->
                  <button
                    @click="isWebSearch = !isWebSearch"
                    class="flex items-center space-x-1 px-2 sm:px-3 py-1.5 rounded-full transition-colors duration-200 text-xs sm:text-sm font-medium"
                    :class="isWebSearch 
                      ? 'bg-green-100 text-green-700' 
                      : 'bg-gray-50 text-gray-700 hover:bg-gray-100'"
                  >
                    <GlobeAltIcon class="h-3 w-3" />
                    <span class="hidden sm:inline">联网搜索</span>
                    <span class="sm:hidden">搜索</span>
                  </button>
                </div>

                <!-- 右侧操作按钮组 -->
                <div class="flex items-center space-x-1 sm:space-x-2">
                  <!-- 语音输入按钮 -->
                  <button
                    v-if="speechStore.isSupported"
                    @click="toggleVoiceInput"
                    :disabled="chatStore.isLoading"
                    :class="[
                      'flex-shrink-0 rounded-full transition-all duration-200 flex items-center justify-center',
                      userStore.isElderMode ? 'w-10 h-10' : 'w-8 h-8',
                      speechStore.isListening 
                        ? 'bg-red-500 hover:bg-red-600 animate-pulse' 
                        : 'bg-gray-100 hover:bg-gray-200',
                      chatStore.isLoading ? 'opacity-50 cursor-not-allowed' : ''
                    ]"
                  >
                    <MicrophoneIcon class="h-4 w-4 text-gray-600" 
                                   :class="speechStore.isListening ? 'text-white' : 'text-gray-600'" />
                  </button>

                  <!-- 发送按钮 -->
                  <button
                    @click="sendMessage"
                    :disabled="!inputMessage.trim() || chatStore.isLoading"
                    :class="[
                      'flex-shrink-0 rounded-full transition-all duration-200 flex items-center justify-center',
                      userStore.isElderMode ? 'w-10 h-10' : 'w-8 h-8',
                      (!inputMessage.trim() || chatStore.isLoading) 
                        ? 'bg-gray-100 cursor-not-allowed' 
                        : 'bg-primary-500 hover:bg-primary-600 active:scale-95'
                    ]"
                  >
                    <PaperAirplaneIcon class="h-4 w-4 text-white" />
                  </button>
                </div>
              </div>
            </div>

            <!-- 底部提示文字 -->
            <div class="mt-2 text-center">
              <p class="text-xs text-gray-400">
                内容由AI生成，仅供参考
              </p>
            </div>

            <!-- 语音识别结果显示 -->
            <div v-if="speechStore.transcript && speechStore.isListening" 
                 class="mt-3 p-3 bg-blue-50 border border-blue-200 rounded-lg rounded-2xl">
              <p class="text-sm text-blue-800"
                 :class="{ 'text-elder-base': userStore.isElderMode }">
                {{ t('listening') }} {{ speechStore.transcript }}
              </p>
            </div>

            <!-- 语音错误提示 -->
            <div v-if="speechStore.error" 
                 class="mt-3 p-3 bg-red-50 border border-red-200 rounded-lg rounded-2xl">
              <p class="text-sm text-red-800"
                 :class="{ 'text-elder-base': userStore.isElderMode }">
                {{ speechStore.error }}
              </p>
            </div>
          </div>
        </div>
      </main>

      <!-- 情绪监测侧边栏（桌面端） -->
      <aside v-if="!isMobile" class="w-64 card-bg border-l p-4" style="border-color: var(--color-primary-100);">
        <h3 class="text-lg font-semibold text-gray-900 mb-4"
            :class="{ 'text-elder-lg': userStore.isElderMode }">
          {{ t('emotionMonitoring') }}
        </h3>
        
        <!-- 当前情绪 -->
        <div class="mb-6">
          <div class="flex items-center justify-between mb-2">
            <span class="text-sm font-medium text-gray-700"
                  :class="{ 'text-elder-sm': userStore.isElderMode }">
              {{ t('currentEmotion') }}
            </span>
            <div class="emotion-indicator"
                 :class="[
                   chatStore.currentEmotionLabel.bgColor,
                   { 'w-5 h-5': userStore.isElderMode }
                 ]">
            </div>
          </div>
          <p class="text-lg font-semibold"
             :class="[
               chatStore.currentEmotionLabel.color,
               { 'text-elder-base': userStore.isElderMode }
             ]">
            {{ chatStore.currentEmotionLabel.name }}
          </p>
          <div class="mt-2 bg-gray-200 rounded-full h-2">
            <div class="bg-primary-500 h-2 rounded-full transition-all duration-300"
                 :style="{ width: `${chatStore.currentEmotion.score}%` }">
            </div>
          </div>
        </div>

        <!-- 情绪趋势 -->
        <div class="mb-6">
          <h4 class="text-sm font-medium text-gray-700 mb-3"
              :class="{ 'text-elder-sm': userStore.isElderMode }">
            {{ t('emotionTrend') }}
          </h4>
          <div class="space-y-2">
            <div class="flex items-center justify-between">
              <span class="text-sm text-gray-600"
                    :class="{ 'text-elder-sm': userStore.isElderMode }">
                {{ t('overallStatus') }}
              </span>
              <span class="text-sm font-medium"
                    :class="[
                      getTrendColor(),
                      { 'text-elder-sm': userStore.isElderMode }
                    ]">
                {{ getTrendText() }}
              </span>
            </div>
          </div>
        </div>

        <!-- 建议 -->
        <div>
          <h4 class="text-sm font-medium text-gray-700 mb-3"
              :class="{ 'text-elder-sm': userStore.isElderMode }">
            {{ t('personalizedSuggestions') }}
          </h4>
          <div class="space-y-2">
            <div v-for="suggestion in emotionSuggestions" :key="suggestion.id"
                 class="p-3 rounded-lg" style="background-color: var(--color-primary-50);">
              <p class="text-sm text-gray-700"
                 :class="{ 'text-elder-sm': userStore.isElderMode }">
                {{ suggestion.text }}
              </p>
            </div>
          </div>
        </div>
      </aside>
    </div>



    <!-- 紧急求助弹窗 -->
    <Teleport to="body">
      <EmergencyModal v-if="showEmergencyModal" @close="showEmergencyModal = false" />
    </Teleport>

    <!-- 正反馈模态框 -->
    <PositiveFeedbackModal 
      :visible="showPositiveFeedback"
      :message-id="currentFeedbackMessageId"
      @close="closePositiveFeedback"
      @submit="handlePositiveFeedbackSubmit"
    />

    <!-- 负反馈模态框 -->
    <NegativeFeedbackModal 
      :visible="showNegativeFeedback"
      :message-id="currentFeedbackMessageId"
      @close="closeNegativeFeedback"
      @submit="handleNegativeFeedbackSubmit"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { useChatStore } from '@/stores/chat'
import { useSpeechStore } from '@/stores/speech'
import {
  ArrowLeftIcon,
  EllipsisVerticalIcon,
  XMarkIcon,
  SparklesIcon,
  UserIcon,
  MicrophoneIcon,
  PaperAirplaneIcon,
  ExclamationTriangleIcon,
  ChevronDownIcon,
  ChevronUpIcon,
  ChevronLeftIcon,
  ChevronRightIcon,
  CpuChipIcon,
  GlobeAltIcon,
  MagnifyingGlassIcon,
  PlusIcon,
  Bars3Icon
} from '@heroicons/vue/24/outline'
import EmergencyModal from '@/components/EmergencyModal.vue'
import LanguageSwitcher from '@/components/LanguageSwitcher.vue'
import PositiveFeedbackModal from '@/components/PositiveFeedbackModal.vue'
import NegativeFeedbackModal from '@/components/NegativeFeedbackModal.vue'
import { t } from '@/stores/language'

const router = useRouter()
const userStore = useUserStore()
const chatStore = useChatStore()
const speechStore = useSpeechStore()

// 响应式状态
const inputMessage = ref('')
const showEmergencyModal = ref(false)
const messagesContainer = ref(null)
const textInput = ref(null)
const isMobile = ref(window.innerWidth < 768)
const showScrollToBottomButton = ref(false)

// 输入模块新功能状态
const selectedModel = ref('DeepSeek')
const isDeepThinking = ref(false)
const isWebSearch = ref(false)
const showModelDropdown = ref(false)

// 侧边栏状态
const isSidebarCollapsed = ref(true) // 默认收起（移动端和桌面端都收起）
const isSidebarClosing = ref(false) // 控制侧边栏关闭动画
const searchQuery = ref('')

// 编辑状态
const editingMessageId = ref(null) // 当前正在编辑的消息ID
const editingContent = ref('') // 编辑中的内容

// 反馈模态框状态
const showPositiveFeedback = ref(false)
const showNegativeFeedback = ref(false)
const currentFeedbackMessageId = ref('')

// 用户头像加载状态
const userAvatarLoadError = ref(false)

// 快速话题（根据年龄段定制）
const quickTopics = computed(() => {
  const topics = {
    teen: [
      { id: 1, text: t('studyPressure') },
      { id: 2, text: t('parentConflicts') },
      { id: 3, text: t('lonelyAtSchool') },
      { id: 4, text: t('confusedAboutFuture') }
    ],
    young: [
      { id: 1, text: t('workPressure') },
      { id: 2, text: t('relationshipProblems') },
      { id: 3, text: t('careerPlanningConfusion') },
      { id: 4, text: t('alwaysAnxious') }
    ],
    middle: [
      { id: 1, text: t('workFamilyBalance') },
      { id: 2, text: t('childEducationWorries') },
      { id: 3, text: t('careerBottleneckFeeling') },
      { id: 4, text: t('healthConcerns') }
    ],
    elder: [
      { id: 1, text: t('oftenLonely') },
      { id: 2, text: t('communicationDifficultiesWithChildren') },
      { id: 3, text: t('difficultyAdaptingToRetirement') },
      { id: 4, text: t('healthWorriesElder') }
    ]
  }
  
  return topics[userStore.ageGroup] || topics.young
})

// 情绪建议
const emotionSuggestions = computed(() => {
  const suggestions = [
    { id: 1, text: t('deepBreathing') },
    { id: 2, text: t('moderateExercise') },
    { id: 3, text: t('adequateSleep') }
  ]
  
  // 根据当前情绪状态提供个性化建议
  if (chatStore.currentEmotion.label === 'anxious') {
    suggestions.unshift({ id: 0, text: t('mindfulnessMeditation') })
  }
  
  return suggestions
})

// 过滤后的聊天历史
const filteredChatHistory = computed(() => {
  if (!searchQuery.value) {
    return chatStore.chatHistory
  }
  
  return chatStore.chatHistory.filter(chat => 
    chat.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    getLastMessage(chat).toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

// 计算属性
const getWelcomeTitle = () => {
  const titles = {
    teen: t('teenWelcomeTitle'),
    young: t('youngWelcomeTitle'),
    middle: t('middleWelcomeTitle'),
    elder: t('elderWelcomeTitle')
  }
  return titles[userStore.ageGroup] || t('welcomeBack')
}

const getWelcomeMessage = () => {
  const messages = {
    teen: t('teenWelcomeMessage'),
    young: t('youngWelcomeMessage'),
    middle: t('middleWelcomeMessage'),
    elder: t('elderWelcomeMessage')
  }
  return messages[userStore.ageGroup] || t('professionalAI')
}

const getInputPlaceholder = () => {
  if (userStore.isElderMode) {
    // 移动端老年模式使用更短的文本
    if (isMobile.value) {
      return t('inputPlaceholderElderMobile')
    }
    return t('inputPlaceholderElderDesktop')
  }
  return t('inputPlaceholderDefault')
}

// 方法
// 调整输入框高度
const adjustTextareaHeight = () => {
  if (!textInput.value) return
  
  // 重置高度以获取正确的scrollHeight
  textInput.value.style.height = 'auto'
  
  // 设置新高度，但不超过最大高度
  const maxHeight = userStore.isElderMode ? 120 : 96 // px
  const newHeight = Math.min(textInput.value.scrollHeight, maxHeight)
  textInput.value.style.height = `${newHeight}px`
}

const sendMessage = async () => {
  if (!inputMessage.value.trim() || chatStore.isLoading) return
  
  const messageText = inputMessage.value.trim()
  inputMessage.value = ''
  
  // 重置输入框高度
  if (textInput.value) {
    textInput.value.style.height = 'auto'
  }
  
  try {
    // 使用真实的API发送消息，传递深度思考和联网搜索参数
    await chatStore.sendMessageToBackend(messageText, 'text', {
      deep_thinking: isDeepThinking.value,
      web_search: isWebSearch.value
    })
    
    // 滚动到底部
    scrollToBottom()
    
    // 后端已经处理了情绪识别，这里不需要额外处理
    
  } catch (error) {
    console.error('发送消息失败:', error)
    
    // 显示错误提示
    if (window.$notification) {
      window.$notification.error('发送消息失败，请稍后重试')
    }
  }
}

// 这些模拟函数已经被真实的后端API替代，不再需要

const handleKeyDown = (event) => {
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault()
    sendMessage()
  }
}

const toggleVoiceInput = async () => {
  if (!speechStore.isSupported) {
    if (window.$notification) {
      window.$notification.error(t('browserNotSupportSpeech'))
    }
    return
  }
  
  if (speechStore.isListening) {
    speechStore.stopListening()
  } else {
    // 请求麦克风权限
    const hasPermission = await speechStore.requestMicrophonePermission()
    if (!hasPermission) {
      if (window.$notification) {
        window.$notification.error(t('microphonePermissionNeeded'))
      }
      return
    }
    
    speechStore.startListening()
  }
}

const sendQuickTopic = (topic) => {
  inputMessage.value = topic
  sendMessage()
}

const createNewChat = async () => {
  await chatStore.createNewChat()
  // 创建新对话后关闭侧边栏（移动端和桌面端都关闭）
  isSidebarCollapsed.value = true
}

const toggleSidebar = () => {
  if (isMobile.value && !isSidebarCollapsed.value) {
    // 移动端关闭侧边栏时，先播放滑出动画
    isSidebarClosing.value = true
    setTimeout(() => {
      isSidebarCollapsed.value = true
      isSidebarClosing.value = false
    }, 300) // 等待动画完成
  } else {
    isSidebarCollapsed.value = !isSidebarCollapsed.value
  }
}

const clearCurrentChat = () => {
  chatStore.clearMessages()
  if (window.$notification) {
    window.$notification.success(t('dialogCleared'))
  }
}

const loadHistoryChat = async (chatId) => {
  await chatStore.loadChat(chatId)
  // 切换对话后关闭侧边栏（移动端和桌面端都关闭）
  isSidebarCollapsed.value = true
}

const scrollToBottom = () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTo({
        top: messagesContainer.value.scrollHeight,
        behavior: 'smooth'
      })
    }
  })
}

const autoScrollToBottom = () => {
  if (messagesContainer.value) {
    const { scrollTop, scrollHeight, clientHeight } = messagesContainer.value
    // 当用户视口距离底部小于屏幕高度的20%时，我们认为他"在底部"，进行自动滚动
    // 移动端和桌面端都使用相对距离，确保在不同设备上都有良好的体验
    const threshold = window.innerHeight * 0.20
    const isNearBottom = scrollHeight - scrollTop - clientHeight < threshold
    if (isNearBottom) {
      scrollToBottom()
    } else {
      // 否则，用户已经滚动上去了，我们只显示提示按钮，不打断他的浏览
      showScrollToBottomButton.value = true
    }
  }
}

const handleScroll = () => {
  if (messagesContainer.value) {
    const { scrollTop, scrollHeight, clientHeight } = messagesContainer.value
    // 使用相对屏幕高度的20%作为阈值，比自动滚动的25%稍小一些
    // 这样可以在用户稍微滚动时就能显示"查看最新信息"按钮
    const threshold = window.innerHeight * 0.20
    const isNearBottom = scrollHeight - scrollTop - clientHeight < threshold
    showScrollToBottomButton.value = !isNearBottom
  }
}

const formatMessage = (content) => {
  // 简单的消息格式化（实际可能需要更复杂的处理）
  return content.replace(/\n/g, '<br>')
}

const formatTime = (timestamp) => {
  const now = Date.now()
  const diff = now - timestamp
  
  if (diff < 60000) return t('justNow')
  if (diff < 3600000) return `${Math.floor(diff / 60000)}${t('minutesAgo')}`
  if (diff < 86400000) return `${Math.floor(diff / 3600000)}${t('hoursAgo')}`
  
  return new Date(timestamp).toLocaleDateString()
}

const getLastMessage = (chat) => {
  if (chat.messages && chat.messages.length > 0) {
    const lastMessage = chat.messages[chat.messages.length - 1]
    return lastMessage.content
  }
  return t('noMessages')
}

const getEmotionColor = (emotion) => {
  const colors = {
    happy: 'bg-emotion-happy',
    sad: 'bg-emotion-sad',
    anxious: 'bg-emotion-anxious',
    angry: 'bg-emotion-angry',
    neutral: 'bg-emotion-neutral'
  }
  return colors[emotion] || colors.neutral
}

const getEmotionName = (emotion) => {
  const names = {
    happy: t('happy'),
    sad: t('sad'),
    anxious: t('anxious'),
    angry: t('angry'),
    neutral: t('neutral')
  }
  return names[emotion] || t('neutral')
}

const getTrendColor = () => {
  switch (chatStore.emotionTrend) {
    case 'improving': return 'text-green-600'
    case 'declining': return 'text-red-600'
    default: return 'text-gray-600'
  }
}

const getTrendText = () => {
  switch (chatStore.emotionTrend) {
    case 'improving': return t('improving')
    case 'declining': return t('needsAttention')
    default: return t('stable')
  }
}

// 切换思考过程展开/收起状态
const toggleThinkingExpansion = (messageId, event) => {
  // 阻止事件冒泡，防止触发其他点击事件
  if (event) {
    event.stopPropagation()
    event.preventDefault()
  }
  
  // 记录当前滚动位置
  const currentScrollTop = messagesContainer.value?.scrollTop || 0
  
  const message = chatStore.messages.find(m => m.id === messageId)
  if (message) {
    message.thinkingExpanded = !message.thinkingExpanded
    
    // 在下一个tick中恢复滚动位置
    nextTick(() => {
      if (messagesContainer.value) {
        messagesContainer.value.scrollTop = currentScrollTop
      }
    })
  }
}

// 复制消息到剪贴板
const copyMessage = async (content) => {
  try {
    // 移除HTML标签，获取纯文本
    const textContent = content.replace(/<[^>]*>/g, '')
    
    // 优先使用现代 Clipboard API
    if (navigator.clipboard && navigator.clipboard.writeText) {
      await navigator.clipboard.writeText(textContent)
    } else {
      // 降级到传统方法
      const textArea = document.createElement('textarea')
      textArea.value = textContent
      textArea.style.position = 'fixed'
      textArea.style.left = '-999999px'
      textArea.style.top = '-999999px'
      document.body.appendChild(textArea)
      textArea.focus()
      textArea.select()
      
      try {
        const successful = document.execCommand('copy')
        if (!successful) {
          throw new Error('execCommand failed')
        }
      } finally {
        document.body.removeChild(textArea)
      }
    }
    
    if (window.$notification) {
      window.$notification.success('已复制到剪贴板')
    }
  } catch (error) {
    console.error('复制失败:', error)
    if (window.$notification) {
      window.$notification.error('复制失败，请手动复制')
    }
  }
}

// 重新生成消息
const regenerateMessage = async (messageId) => {
  try {
    // 找到要重新生成的消息
    const messageIndex = chatStore.messages.findIndex(m => m.id === messageId)
    if (messageIndex === -1) return
    
    // 找到对应的用户消息（通常是前一条消息）
    let userMessageIndex = messageIndex - 1
    while (userMessageIndex >= 0 && chatStore.messages[userMessageIndex].type !== 'user') {
      userMessageIndex--
    }
    
    if (userMessageIndex === -1) {
      if (window.$notification) {
        window.$notification.error('找不到对应的用户消息')
      }
      return
    }
    
    const userMessage = chatStore.messages[userMessageIndex]
    
    // 删除当前的AI回复
    chatStore.messages.splice(messageIndex, 1)
    
    // 重新发送用户消息
    await chatStore.sendMessageToBackend(userMessage.content, 'text', {
      deep_thinking: isDeepThinking.value,
      web_search: isWebSearch.value
    })
    
    // 滚动到底部
    scrollToBottom()
    
  } catch (error) {
    console.error('重新生成失败:', error)
    if (window.$notification) {
      window.$notification.error('重新生成失败，请稍后重试')
    }
  }
}

// 点赞消息
const likeMessage = (messageId) => {
  const message = chatStore.messages.find(m => m.id === messageId)
  if (message) {
    // 如果已经点赞，则取消点赞
    if (message.userFeedback === 'like') {
      message.userFeedback = null
    } else {
      message.userFeedback = 'like'
      // 显示正反馈模态框
      currentFeedbackMessageId.value = messageId
      showPositiveFeedback.value = true
    }
  }
}

// 踩消息
const dislikeMessage = (messageId) => {
  const message = chatStore.messages.find(m => m.id === messageId)
  if (message) {
    // 如果已经踩，则取消踩
    if (message.userFeedback === 'dislike') {
      message.userFeedback = null
    } else {
      message.userFeedback = 'dislike'
      // 显示负反馈模态框
      currentFeedbackMessageId.value = messageId
      showNegativeFeedback.value = true
    }
  }
}

// 关闭正反馈模态框
const closePositiveFeedback = () => {
  showPositiveFeedback.value = false
  currentFeedbackMessageId.value = ''
}

// 关闭负反馈模态框
const closeNegativeFeedback = () => {
  showNegativeFeedback.value = false
  currentFeedbackMessageId.value = ''
}

// 处理正反馈提交
const handlePositiveFeedbackSubmit = (feedbackData) => {
  console.log('正反馈提交:', feedbackData)
  // 这里可以添加额外的处理逻辑
}

// 处理负反馈提交
const handleNegativeFeedbackSubmit = (feedbackData) => {
  console.log('负反馈提交:', feedbackData)
  // 这里可以添加额外的处理逻辑
}

// 复制用户消息
const copyUserMessage = async (content) => {
  try {
    // 优先使用现代 Clipboard API
    if (navigator.clipboard && navigator.clipboard.writeText) {
      await navigator.clipboard.writeText(content)
    } else {
      // 降级到传统方法
      const textArea = document.createElement('textarea')
      textArea.value = content
      textArea.style.position = 'fixed'
      textArea.style.left = '-999999px'
      textArea.style.top = '-999999px'
      document.body.appendChild(textArea)
      textArea.focus()
      textArea.select()
      
      try {
        const successful = document.execCommand('copy')
        if (!successful) {
          throw new Error('execCommand failed')
        }
      } finally {
        document.body.removeChild(textArea)
      }
    }
    
    if (window.$notification) {
      window.$notification.success('已复制到剪贴板')
    }
  } catch (error) {
    console.error('复制失败:', error)
    if (window.$notification) {
      window.$notification.error('复制失败，请手动复制')
    }
  }
}

// 开始原地编辑
const startInlineEdit = (messageId, content) => {
  editingMessageId.value = messageId
  editingContent.value = content
  // 聚焦到编辑输入框
  nextTick(() => {
    const editInput = document.querySelector(`[ref="editInput-${messageId}"]`)
    if (editInput) {
      editInput.focus()
      editInput.select()
      // 确保内容正确设置
      editInput.value = content
    }
  })
}

// 取消原地编辑
const cancelInlineEdit = () => {
  editingMessageId.value = null
  editingContent.value = ''
}

// 确认原地编辑并重新发送
const confirmInlineEdit = async (messageId) => {
  if (!editingContent.value.trim()) {
    cancelInlineEdit()
    return
  }
  
  try {
    const newContent = editingContent.value.trim()
    const messageIndex = chatStore.messages.findIndex(m => m.id === messageId)
    
    if (messageIndex === -1) {
      cancelInlineEdit()
      return
    }
    
    // 删除该用户消息之后的所有AI回复
    const messagesToRemove = []
    for (let i = messageIndex + 1; i < chatStore.messages.length; i++) {
      if (chatStore.messages[i].type === 'ai') {
        messagesToRemove.push(i)
      } else {
        // 遇到下一个用户消息就停止
        break
      }
    }
    
    // 从后往前删除，避免索引变化
    for (let i = messagesToRemove.length - 1; i >= 0; i--) {
      chatStore.messages.splice(messagesToRemove[i], 1)
    }
    
    // 更新用户消息内容
    chatStore.messages[messageIndex].content = newContent
    
    // 立即清空编辑状态，让消息恢复正常显示
    cancelInlineEdit()
    
    // 滚动到底部
    scrollToBottom()
    
    // 异步获取AI回复，不阻塞界面更新
    getAIResponseOnly(newContent, {
      deep_thinking: isDeepThinking.value,
      web_search: isWebSearch.value
    }).catch(error => {
      console.error('获取AI回复失败:', error)
      if (window.$notification) {
        window.$notification.error('获取AI回复失败，请稍后重试')
      }
    })
    
  } catch (error) {
    console.error('编辑消息失败:', error)
    if (window.$notification) {
      window.$notification.error('编辑消息失败，请稍后重试')
    }
  }
}

// 处理编辑输入框的键盘事件
const handleEditKeyDown = (event) => {
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault()
    // 找到当前编辑的消息ID
    const messageId = editingMessageId.value
    if (messageId) {
      confirmInlineEdit(messageId)
    }
  } else if (event.key === 'Escape') {
    event.preventDefault()
    cancelInlineEdit()
  }
}

// 调整编辑输入框高度
const adjustEditTextareaHeight = (event) => {
  const textarea = event.target
  // 重置高度以获取正确的scrollHeight
  textarea.style.height = 'auto'
  
  // 设置新高度，但不超过最大高度
  const maxHeight = userStore.isElderMode ? 120 : 96 // px
  const newHeight = Math.min(textarea.scrollHeight, maxHeight)
  textarea.style.height = `${newHeight}px`
}

// 用户头像相关方法
const getUserAvatarStyle = () => {
  if (userStore.user?.avatar && !userAvatarLoadError.value) {
    return `background-image: url(${userStore.user.avatar}); background-size: cover; background-position: center;`
  }
  return 'background-color: var(--color-primary-500);'
}

const getUserInitials = () => {
  const name = userStore.user?.nickname || userStore.user?.username || userStore.user?.name || t('user')
  return name.slice(0, 2).toUpperCase()
}

const handleUserAvatarError = () => {
  console.warn('用户头像加载失败，使用默认显示')
  userAvatarLoadError.value = true
}

const handleUserAvatarLoad = () => {
  userAvatarLoadError.value = false
}

// 只获取AI回复，不创建新用户消息
const getAIResponseOnly = async (content, options = {}) => {
  chatStore.setLoading(true)
  let aiMessageId = null

  try {
    // 创建AI消息占位符
    aiMessageId = Date.now() + 1
    const aiMessage = {
      id: aiMessageId,
      content: '',
      type: 'ai',
      timestamp: Date.now(),
      isStreaming: true,
      thinking: '',
      thinkingTime: 0,
      thinkingExpanded: true
    }
    chatStore.messages.push(aiMessage)
    
    // 使用chatService直接发送消息，不创建用户消息
    const { chatService } = await import('@/services/chatService')
    
    await chatService.sendMessageStream(
      content,
      'text',
      chatStore.currentChatId,
      // onChunk回调
      (chunk) => {
        if (chunk.type === 'chunk') {
          const messageIndex = chatStore.messages.findIndex(m => m.id === aiMessageId)
          if (messageIndex !== -1) {
            chatStore.messages[messageIndex].content += chunk.content
          }
        } else if (chunk.type === 'thinking') {
          const messageIndex = chatStore.messages.findIndex(m => m.id === aiMessageId)
          if (messageIndex !== -1) {
            if (!chatStore.messages[messageIndex].thinking) {
              chatStore.messages[messageIndex].thinking = ''
              chatStore.messages[messageIndex].thinkingStartTime = Date.now()
            }
            chatStore.messages[messageIndex].thinking += chunk.content
            
            if (chatStore.messages[messageIndex].thinkingStartTime) {
              const currentThinkingTime = Math.round((Date.now() - chatStore.messages[messageIndex].thinkingStartTime) / 1000)
              chatStore.messages[messageIndex].thinkingTime = currentThinkingTime
            }
          }
        }
      },
      // onComplete回调
      (complete) => {
        const messageIndex = chatStore.messages.findIndex(m => m.id === aiMessageId)
        if (messageIndex !== -1) {
          chatStore.messages[messageIndex].content = complete.fullContent
          chatStore.messages[messageIndex].isStreaming = false
          chatStore.messages[messageIndex].id = complete.messageId
          
          if (chatStore.messages[messageIndex].thinkingStartTime) {
            const thinkingDuration = Math.round((Date.now() - chatStore.messages[messageIndex].thinkingStartTime) / 1000)
            chatStore.messages[messageIndex].thinkingTime = thinkingDuration
          }
        }
        
        if (complete.sessionId) {
          chatStore.currentChatId = complete.sessionId
        }
      },
      // onError回调
      (error) => {
        console.error('流式响应错误:', error)
        const messageIndex = chatStore.messages.findIndex(m => m.id === aiMessageId)
        if (messageIndex !== -1) {
          chatStore.messages[messageIndex].content = '抱歉，AI服务暂时不可用，请稍后再试。'
          chatStore.messages[messageIndex].isStreaming = false
        }
      },
      options
    )
    
  } catch (error) {
    console.error('获取AI回复失败:', error)
    if (aiMessageId) {
      chatStore.messages = chatStore.messages.filter(m => m.id !== aiMessageId)
    }
    throw error
  } finally {
    chatStore.setLoading(false)
  }
}

// 监听语音识别结果
watch(() => speechStore.transcript, (newTranscript) => {
  if (newTranscript && !speechStore.isListening) {
    // 语音识别完成，将结果填入输入框
    inputMessage.value = newTranscript
    speechStore.reset()
  }
})

// 监听用户头像变化，重置错误状态
watch(() => userStore.user?.avatar, (newAvatar) => {
  if (newAvatar) {
    userAvatarLoadError.value = false
  }
}, { immediate: true })

// 监听窗口大小变化
const handleResize = () => {
  const wasMobile = isMobile.value
  isMobile.value = window.innerWidth < 768
  
  // 无论从桌面端切换到移动端，还是从移动端切换到桌面端，都保持侧边栏收起状态
  // 用户需要手动点击按钮来展开侧边栏
}

// 生命周期
onMounted(async () => {
  try {
    // 加载会话历史
    await chatStore.loadChatHistory()
    
    // 如果有历史会话，加载最新的会话消息
    if (chatStore.chatHistory.length > 0) {
      const latestChat = chatStore.chatHistory[0] // 最新的会话
      await chatStore.loadChat(latestChat.id)
    } else {
      // 如果没有历史会话，创建一个新的
      await chatStore.createNewChat()
    }
  } catch (error) {
    console.error('初始化聊天失败:', error)
    // 降级到本地创建
    if (!chatStore.currentChatId) {
      await chatStore.createNewChat()
    }
  }
  
  // 监听窗口大小变化
  window.addEventListener('resize', handleResize)
  
  // 点击外部关闭菜单
  document.addEventListener('click', (e) => {
    if (!e.target.closest('.relative')) {
      showModelDropdown.value = false
    }
  })
  
  // 滚动到底部
  scrollToBottom()
})

// 监听消息变化，自动滚动到底部（但排除思考展开状态变化）
watch(() => chatStore.messages, (newMessages, oldMessages) => {
  // 检查是否是思考展开状态的变化
  if (oldMessages && newMessages.length === oldMessages.length) {
    let isOnlyThinkingExpansionChange = true
    for (let i = 0; i < newMessages.length; i++) {
      const newMsg = newMessages[i]
      const oldMsg = oldMessages[i]
      if (!oldMsg || 
          newMsg.id !== oldMsg.id || 
          newMsg.content !== oldMsg.content || 
          newMsg.thinking !== oldMsg.thinking ||
          newMsg.isStreaming !== oldMsg.isStreaming) {
        isOnlyThinkingExpansionChange = false
        break
      }
    }
    
    // 如果只是思考展开状态的变化，不滚动
    if (isOnlyThinkingExpansionChange) {
      return
    }
  }
  
  nextTick(() => {
    autoScrollToBottom()
  })
}, { deep: true })

// 监听流式响应状态，在流式响应时也自动滚动
watch(() => chatStore.messages.filter(m => m.isStreaming), () => {
  nextTick(() => {
    autoScrollToBottom()
  })
}, { deep: true })

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  speechStore.stopListening()
})
</script>

<style scoped>
/* 自动调整文本框高度 */
textarea {
  min-height: 44px;
  max-height: 120px;
  resize: none;
  overflow-y: auto;
}

/* 消息气泡样式增强 */
.chat-bubble-ai {
  animation: slideInLeft 0.3s ease-out;
}

.chat-bubble-user {
  animation: slideInRight 0.3s ease-out;
  background-color: #fef3e7; /* 浅橙色背景，比页面背景略深 */
  color: #1f2937; /* 深灰色文字 */
  padding: 12px 16px;
  border-radius: 12px;
  border: 1px solid #fed7aa; /* 浅橙色边框 */
  max-width: 100%;
  word-wrap: break-word;
}

@keyframes slideInLeft {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes slideInRight {
  from {
    opacity: 0;
    transform: translateX(20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

/* 语音按钮脉冲动画 */
@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7);
  }
  70% {
    box-shadow: 0 0 0 10px rgba(239, 68, 68, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(239, 68, 68, 0);
  }
}

.animate-pulse {
  animation: pulse 2s infinite;
}

/* 滚动条样式 */
.custom-scrollbar {
  scrollbar-width: thin;
  scrollbar-color: #cbd5e1 #f1f5f9;
}

.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: #f1f5f9;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 3px;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .w-80 {
    width: 100%;
  }
  
  .w-64 {
    display: none;
  }
}

/* 高对比度支持 */
@media (prefers-contrast: high) {
  .chat-bubble-ai,
  .chat-bubble-user {
    border: 2px solid currentColor;
  }
  
  .bg-primary-500 {
    border: 2px solid white;
  }
}

/* 减少动画支持 */
@media (prefers-reduced-motion: reduce) {
  .chat-bubble-ai,
  .chat-bubble-user {
    animation: none;
  }
  
  .animate-pulse {
    animation: none;
  }
}

/* 确保布局正确 */
.h-screen {
  height: 100vh;
  height: 100dvh; /* 动态视窗高度，适配移动端 */
}

/* 确保flex布局正确工作 */
.min-h-0 {
  min-height: 0;
}

/* 用户消息操作按钮样式 */
.user-action-button {
  transition: all 0.2s ease;
}



/* 编辑框样式 */
.edit-container {
  position: relative;
  background: white;
  border-radius: 12px;
  padding: 12px;
  transition: all 0.2s ease;
  border: 2px solid #d1d5db;
}

.edit-container:focus-within {
  border-color: var(--color-primary-500);
  box-shadow: 0 0 0 2px var(--color-primary-100);
}

.edit-textarea {
  width: 100%;
  resize: none;
  border: none;
  outline: none;
  background: transparent;
}

/* 移动端适配 */
@media (max-width: 768px) {
  .user-action-button {
    padding: 8px 12px;
    font-size: 14px;
  }
  
  .edit-container {
    padding: 8px;
    margin: 0 8px; /* 移动端添加左右边距 */
    max-width: calc(100% - 16px); /* 限制最大宽度 */
  }
  
  .edit-textarea {
    min-height: 40px !important;
    max-height: 70px !important;
  }
  
  .edit-buttons {
    flex-direction: column;
    gap: 4px;
  }
  
  .edit-buttons .flex {
    width: 100%;
    justify-content: space-between;
  }
}

/* 老年模式适配 */
@media (min-width: 769px) {
  .elder-edit-textarea {
    min-height: 70px !important;
    max-height: 120px !important;
    line-height: 1.6;
  }
}

/* 移动端侧边栏滑入动画 */
.slide-in-left {
  animation: slideInLeft 0.3s ease-out;
}

@keyframes slideInLeft {
  from {
    transform: translateX(-100%);
  }
  to {
    transform: translateX(0);
  }
}

/* 移动端侧边栏滑出动画 */
.slide-out-left {
  animation: slideOutLeft 0.3s ease-in;
}

@keyframes slideOutLeft {
  from {
    transform: translateX(0);
  }
  to {
    transform: translateX(-100%);
  }
}

/* 打印样式 */
@media print {
  .fixed,
  button,
  .border-l,
  .border-r {
    display: none !important;
  }
  
  .chat-bubble-ai,
  .chat-bubble-user {
    border: 1px solid #ccc !important;
    break-inside: avoid;
  }
}
</style>