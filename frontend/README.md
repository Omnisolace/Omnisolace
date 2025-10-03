# Omnisolace 前端项目

## 项目简介

Omnisolace 是一个全年龄段AI心理疏导机器人前端系统，基于 Vue 3 + Vite + Tailwind CSS 构建。该项目为不同年龄段的用户提供个性化的心理健康服务，支持青少年、青年、中年和老年四种用户模式。

## 技术栈

- **框架**: Vue 3 (Composition API)
- **构建工具**: Vite 5.0
- **状态管理**: Pinia
- **路由**: Vue Router 4
- **样式**: Tailwind CSS 3.3
- **UI组件**: Headless UI Vue + Heroicons
- **HTTP客户端**: Axios
- **PWA支持**: Vite PWA Plugin
- **开发工具**: Stylelint、PostCSS

## 项目结构

```
frontend/
├── public/                     # 静态资源
│   ├── favicon.ico            # 网站图标
│   ├── manifest.json          # PWA清单文件
│   ├── sw.js                  # Service Worker
│   └── images/                # 图片资源
├── src/                       # 源代码
│   ├── components/            # Vue组件
│   │   ├── BottomNavigation.vue    # 底部导航
│   │   ├── SideNavigation.vue      # 侧边栏导航
│   │   ├── EmergencyModal.vue      # 紧急求助弹窗
│   │   ├── EditProfileModal.vue    # 编辑资料弹窗
│   │   ├── PsychProfileModal.vue   # 心理档案弹窗
│   │   ├── LanguageSwitcher.vue    # 语言切换器
│   │   └── ...                 # 其他组件
│   ├── views/                 # 页面组件
│   │   ├── Home.vue          # 首页
│   │   ├── Login.vue          # 登录页
│   │   ├── Chat.vue           # 聊天页
│   │   ├── Profile.vue        # 个人中心
│   │   └── NotFound.vue       # 404页面
│   ├── stores/                # Pinia状态管理
│   │   ├── user.js           # 用户状态
│   │   ├── chat.js           # 聊天状态
│   │   ├── language.js       # 语言状态
│   │   └── speech.js         # 语音状态
│   ├── services/             # 服务层
│   │   └── chatService.js    # 聊天服务
│   ├── utils/                 # 工具函数
│   │   ├── api.js            # API封装
│   │   ├── constants.js      # 常量定义
│   │   └── speech.js         # 语音工具
│   ├── router/               # 路由配置
│   │   └── index.js          # 路由定义
│   ├── App.vue               # 根组件
│   ├── main.js              # 入口文件
│   └── style.css            # 全局样式
├── package.json             # 项目配置
├── vite.config.js           # Vite配置
├── tailwind.config.js       # Tailwind配置
├── postcss.config.js        # PostCSS配置
├── env.example              # 环境变量示例
└── README.md               # 项目说明
```

## 环境要求

- **Node.js**: >= 16.0.0
- **npm**: >= 8.0.0 或 **yarn**: >= 1.22.0
- **现代浏览器**: 支持ES2015+的浏览器

## 安装步骤

### 1. 克隆项目

```bash
git clone <repository-url>
cd Omnisolace/frontend
```

### 2. 安装依赖

使用 npm:
```bash
npm install
```

或使用 yarn:
```bash
yarn install
```

### 3. 环境配置

复制环境变量示例文件：
```bash
cp env.example .env.local
```

编辑 `.env.local` 文件，配置必要的环境变量：

```env
# 应用基础配置
VITE_APP_TITLE=Omnisolace
VITE_APP_VERSION=1.0.0
VITE_APP_DESCRIPTION=全年龄段AI心理疏导机器人

# API 配置
VITE_API_BASE_URL=http://localhost:8000/api
VITE_API_TIMEOUT=10000

# 开发环境配置
VITE_DEV_PORT=5173
VITE_DEV_HOST=localhost

# 功能开关
VITE_ENABLE_MOCK=true
VITE_ENABLE_DEBUG=true
VITE_ENABLE_PWA=true
VITE_ENABLE_OFFLINE=true
```

## 开发指南

### 启动开发服务器

#### 方式一：使用npm/yarn命令

```bash
npm run dev
```

或

```bash
yarn dev
```

#### 方式二：使用项目提供的启动脚本

**Windows用户：**
```bash
# 启动开发服务器
src\scripts\start.bat

# 清理缓存后启动
src\scripts\start.bat --clean

# 构建生产版本
src\scripts\start.bat --build

# 预览生产版本
src\scripts\start.bat --preview
```

**Linux/Mac用户：**
```bash
# 启动开发服务器
./src/scripts/start.sh

# 清理缓存后启动
./src/scripts/start.sh --clean

# 构建生产版本
./src/scripts/start.sh --build

# 预览生产版本
./src/scripts/start.sh --preview
```

开发服务器将在 `http://localhost:5174` 启动（端口在 `vite.config.js` 中配置为5174）。

### 构建生产版本

```bash
npm run build
```

或

```bash
yarn build
```

构建文件将输出到 `dist/` 目录。

### 预览生产构建

```bash
npm run preview
```

或

```bash
yarn preview
```

### 代码检查

项目使用Stylelint进行样式检查，可以通过以下方式运行：

```bash
# 使用npx运行stylelint
npx stylelint "src/**/*.{vue,css}"

# 或使用yarn
yarn stylelint "src/**/*.{vue,css}"
```

## 项目特性

### 1. 多年龄段适配

项目支持四种用户模式：

- **青少年模式** (12-18岁): 家长监督、内容过滤、学习支持
- **青年模式** (19-35岁): 职业支持、情感建议、压力管理
- **中年模式** (36-59岁): 家庭平衡、职业指导、健康关怀
- **老年模式** (60岁+): 语音优先、大字体、家庭支持

### 2. 主题系统

支持多种色彩主题：
- 暖阳橘 (默认)
- 柔粉棕
- 琥珀黄
- 焦糖棕
- 樱花粉

### 3. PWA支持

- 离线缓存
- 推送通知
- 应用安装
- 自动更新

### 4. 响应式设计

- 移动端优先
- 桌面端适配
- 老年模式大字体
- 无障碍支持

### 5. 语音功能

- 语音输入
- 语音输出
- 多语言支持
- 情绪识别

## 核心功能

### 用户认证
- 手机号登录/注册
- 游客模式
- 自动登录
- 安全登出

### 聊天系统
- 实时对话
- 流式响应
- 情绪分析
- 危机预警
- 历史记录

### 个人中心
- 用户资料
- 心理档案
- 情绪统计
- 设置管理

### 紧急求助
- 一键求助
- 紧急联系人
- 危机干预
- 专业转介

## API集成

项目使用统一的API服务层，支持：

- 用户认证API
- 聊天对话API
- 情绪分析API
- 文件上传API
- 系统配置API

API配置在 `src/utils/api.js` 中，支持：
- 请求拦截
- 响应拦截
- 错误处理
- 自动重试
- 离线缓存

## 部署指南

### 1. 开发环境部署

```bash
# 安装依赖
npm install

# 配置环境变量
cp env.example .env.local

# 启动开发服务器
npm run dev
```

### 2. 生产环境部署

```bash
# 构建生产版本
npm run build

# 部署到静态服务器
# 将 dist/ 目录内容上传到服务器
```

### 3. 静态服务器部署

构建完成后，可以将 `dist/` 目录部署到任何静态文件服务器：

- **Apache**: 将 `dist/` 内容复制到网站根目录
- **Nginx**: 配置静态文件服务
- **CDN**: 上传到云存储服务
- **GitHub Pages**: 推送到gh-pages分支

## 开发工具

### VS Code推荐插件

- Vue Language Features (Volar)
- Tailwind CSS IntelliSense
- Stylelint
- Auto Rename Tag
- Vue VSCode Snippets
- PostCSS Language Support

### 调试工具

- Vue DevTools
- Network面板
- Console日志
- 断点调试

## 常见问题

### 1. 端口冲突

如果5174端口被占用，可以修改 `vite.config.js` 中的端口配置：

```javascript
server: {
  port: 3000, // 修改为其他端口
}
```

或者使用启动脚本的端口参数（如果支持）：
```bash
# Windows
src\scripts\start.bat --port 3000

# Linux/Mac  
./src/scripts/start.sh --port 3000
```

### 2. API连接失败

检查以下配置：
- 后端服务是否启动
- API地址是否正确
- 网络连接是否正常
- CORS配置是否正确

### 3. 构建失败

常见解决方案：
- 清除node_modules重新安装
- 检查Node.js版本
- 查看具体错误信息
- 检查环境变量配置

### 4. PWA功能异常

确保：
- HTTPS环境（生产环境）
- Service Worker正确注册
- Manifest文件配置正确
- 浏览器支持PWA

## 贡献指南

### 代码规范

- 使用Stylelint进行样式检查
- 遵循Vue 3 Composition API规范
- 使用Tailwind CSS进行样式开发
- 编写清晰的注释
- 使用PostCSS进行样式处理
- 遵循ES6+语法规范

### 提交规范

```bash
# 功能开发
git commit -m "feat: 添加用户认证功能"

# 问题修复
git commit -m "fix: 修复聊天消息显示问题"

# 文档更新
git commit -m "docs: 更新API文档"
```

### 分支管理

- `main`: 主分支，用于生产环境
- `develop`: 开发分支，用于功能集成
- `feature/*`: 功能分支
- `hotfix/*`: 热修复分支

## 许可证

本项目采用 MIT 许可证。详情请查看 LICENSE 文件。

## 联系方式

如有问题或建议，请通过以下方式联系：

- 项目Issues: [GitHub Issues]
- 邮箱: [1969295061@qq.com]
- 文档: [项目文档地址]

---

**注意**: 请确保在部署前仔细阅读环境配置部分，并根据实际需求调整相关配置。
