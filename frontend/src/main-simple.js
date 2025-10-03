import { createApp } from 'vue'

const App = {
  template: `
    <div id="app" style="min-height: 100vh; background: #f3f4f6; display: flex; align-items: center; justify-content: center;">
      <div style="background: white; padding: 2rem; border-radius: 0.5rem; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); text-align: center;">
        <h1 style="color: #1f2937; font-size: 2rem; font-weight: bold; margin-bottom: 1rem;">
          Omnisolace
        </h1>
        <p style="color: #6b7280; margin-bottom: 2rem;">
          全年龄段AI心理疏导机器人
        </p>
        <p style="color: #10b981; font-weight: 500;">
          ✅ 应用运行正常！
        </p>
        <p style="color: #6b7280; font-size: 0.875rem; margin-top: 1rem;">
          当前时间: {{ currentTime }}
        </p>
      </div>
    </div>
  `,
  data() {
    return {
      currentTime: new Date().toLocaleString()
    }
  },
  mounted() {
    setInterval(() => {
      this.currentTime = new Date().toLocaleString()
    }, 1000)
  }
}

const app = createApp(App)
app.mount('#app')
