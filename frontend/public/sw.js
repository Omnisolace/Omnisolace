// Service Worker for Omnisolace PWA
const CACHE_NAME = 'omnisolace-v1.0.1'
const STATIC_CACHE_NAME = 'omnisolace-static-v1.0.1'
const DYNAMIC_CACHE_NAME = 'omnisolace-dynamic-v1.0.1'

// 需要缓存的静态资源
const STATIC_ASSETS = [
  '/',
  '/index.html',
  '/src/main.js',
  '/src/style.css',
  '/manifest.json',
  '/favicon.ico',
  '/pwa-192x192.png',
  '/pwa-512x512.png'
]

// 需要缓存的API端点
const API_CACHE_PATTERNS = [
  /\/api\/user/,
  /\/api\/chat/,
  /\/api\/emotion/
]

// 安装事件 - 缓存静态资源
self.addEventListener('install', (event) => {
  console.log('Service Worker 安装中...')
  
  event.waitUntil(
    caches.open(STATIC_CACHE_NAME)
      .then((cache) => {
        console.log('缓存静态资源...')
        return cache.addAll(STATIC_ASSETS)
      })
      .then(() => {
        console.log('静态资源缓存完成')
        return self.skipWaiting()
      })
      .catch((error) => {
        console.error('静态资源缓存失败:', error)
      })
  )
})

// 激活事件 - 清理旧缓存
self.addEventListener('activate', (event) => {
  console.log('Service Worker 激活中...')
  
  event.waitUntil(
    caches.keys()
      .then((cacheNames) => {
        return Promise.all(
          cacheNames.map((cacheName) => {
            if (cacheName !== STATIC_CACHE_NAME && 
                cacheName !== DYNAMIC_CACHE_NAME &&
                cacheName.startsWith('omnisolace-')) {
              console.log('删除旧缓存:', cacheName)
              return caches.delete(cacheName)
            }
          })
        )
      })
      .then(() => {
        console.log('Service Worker 激活完成')
        return self.clients.claim()
      })
  )
})

// 拦截网络请求
self.addEventListener('fetch', (event) => {
  const { request } = event
  const url = new URL(request.url)
  
  // 忽略非 HTTP/HTTPS 请求
  if (!url.protocol.startsWith('http')) {
    return
  }
  
  // 处理导航请求（页面请求）
  if (request.mode === 'navigate') {
    event.respondWith(handleNavigationRequest(request))
    return
  }
  
  // 处理静态资源请求
  if (isStaticAsset(request)) {
    event.respondWith(handleStaticAssetRequest(request))
    return
  }
  
  // 处理API请求
  if (isApiRequest(request)) {
    event.respondWith(handleApiRequest(request))
    return
  }
  
  // 其他请求使用网络优先策略
  event.respondWith(
    fetch(request).catch(() => {
      console.log('网络请求失败，尝试从缓存获取:', request.url)
      return caches.match(request)
    })
  )
})

// 处理导航请求（页面请求）
async function handleNavigationRequest(request) {
  try {
    // 先尝试网络请求
    const networkResponse = await fetch(request)
    
    // 如果网络请求成功，缓存并返回
    if (networkResponse.ok) {
      const cache = await caches.open(DYNAMIC_CACHE_NAME)
      cache.put(request, networkResponse.clone())
      return networkResponse
    }
  } catch (error) {
    console.log('导航请求网络失败:', error)
  }
  
  // 网络失败时从缓存获取
  const cachedResponse = await caches.match(request)
  if (cachedResponse) {
    return cachedResponse
  }
  
  // 如果缓存也没有，返回离线页面
  const offlineResponse = await caches.match('/')
  return offlineResponse || new Response('页面暂时无法访问', {
    status: 503,
    statusText: 'Service Unavailable',
    headers: { 'Content-Type': 'text/plain; charset=utf-8' }
  })
}

// 处理静态资源请求
async function handleStaticAssetRequest(request) {
  // 缓存优先策略
  const cachedResponse = await caches.match(request)
  if (cachedResponse) {
    return cachedResponse
  }
  
  try {
    const networkResponse = await fetch(request)
    if (networkResponse.ok) {
      const cache = await caches.open(STATIC_CACHE_NAME)
      cache.put(request, networkResponse.clone())
      return networkResponse
    }
  } catch (error) {
    console.log('静态资源网络请求失败:', error)
  }
  
  return new Response('资源暂时无法访问', {
    status: 503,
    statusText: 'Service Unavailable'
  })
}

// 处理API请求
async function handleApiRequest(request) {
  // 网络优先策略，支持离线回退
  try {
    const networkResponse = await fetch(request)
    
    if (networkResponse.ok) {
      // 只缓存GET请求的成功响应
      if (request.method === 'GET') {
        const cache = await caches.open(DYNAMIC_CACHE_NAME)
        cache.put(request, networkResponse.clone())
      }
      return networkResponse
    }
  } catch (error) {
    console.log('API请求网络失败:', error)
  }
  
  // 网络失败时，对于GET请求尝试从缓存获取
  if (request.method === 'GET') {
    const cachedResponse = await caches.match(request)
    if (cachedResponse) {
      console.log('从缓存返回API响应:', request.url)
      return cachedResponse
    }
  }
  
  // 返回离线响应
  return new Response(JSON.stringify({
    error: '网络连接不可用',
    message: '请检查网络连接后重试',
    offline: true
  }), {
    status: 503,
    statusText: 'Service Unavailable',
    headers: { 'Content-Type': 'application/json' }
  })
}

// 判断是否为静态资源
function isStaticAsset(request) {
  const url = new URL(request.url)
  return STATIC_ASSETS.some(asset => url.pathname.endsWith(asset)) ||
         url.pathname.match(/\.(js|css|png|jpg|jpeg|gif|svg|ico|woff|woff2|ttf)$/)
}

// 判断是否为API请求
function isApiRequest(request) {
  const url = new URL(request.url)
  return API_CACHE_PATTERNS.some(pattern => pattern.test(url.pathname))
}

// 监听消息事件
self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting()
  }
  
  if (event.data && event.data.type === 'GET_VERSION') {
    event.ports[0].postMessage({ version: CACHE_NAME })
  }
})

// 后台同步（如果支持）
if ('sync' in self.registration) {
  self.addEventListener('sync', (event) => {
    console.log('后台同步事件:', event.tag)
    
    if (event.tag === 'background-sync') {
      event.waitUntil(doBackgroundSync())
    }
  })
}

// 执行后台同步
async function doBackgroundSync() {
  try {
    // 这里可以添加需要后台同步的逻辑
    // 例如：同步离线时的对话记录、用户设置等
    console.log('执行后台同步...')
    
    // 示例：同步用户数据
    const cache = await caches.open(DYNAMIC_CACHE_NAME)
    const cachedRequests = await cache.keys()
    
    for (const request of cachedRequests) {
      if (request.url.includes('/api/')) {
        try {
          const response = await fetch(request)
          if (response.ok) {
            await cache.put(request, response)
          }
        } catch (error) {
          console.log('同步请求失败:', request.url, error)
        }
      }
    }
    
    console.log('后台同步完成')
  } catch (error) {
    console.error('后台同步失败:', error)
  }
}

// 推送通知处理
self.addEventListener('push', (event) => {
  console.log('收到推送消息:', event)
  
  const options = {
    body: '您有新的心理疏导建议',
    icon: '/pwa-192x192.png',
    badge: '/pwa-192x192.png',
    vibrate: [100, 50, 100],
    data: {
      dateOfArrival: Date.now(),
      primaryKey: 1
    },
    actions: [
      {
        action: 'explore',
        title: '查看详情',
        icon: '/pwa-192x192.png'
      },
      {
        action: 'close',
        title: '关闭',
        icon: '/pwa-192x192.png'
      }
    ]
  }
  
  event.waitUntil(
    self.registration.showNotification('Omnisolace', options)
  )
})

// 通知点击处理
self.addEventListener('notificationclick', (event) => {
  console.log('通知被点击:', event)
  
  event.notification.close()
  
  if (event.action === 'explore') {
    // 打开应用
    event.waitUntil(
      clients.openWindow('/')
    )
  } else if (event.action === 'close') {
    // 关闭通知
    event.notification.close()
  } else {
    // 默认行为：打开应用
    event.waitUntil(
      clients.openWindow('/')
    )
  }
})

// 错误处理
self.addEventListener('error', (event) => {
  console.error('Service Worker 错误:', event.error)
})

self.addEventListener('unhandledrejection', (event) => {
  console.error('Service Worker 未处理的Promise拒绝:', event.reason)
})

console.log('Service Worker 脚本加载完成')
