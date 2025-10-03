# Omnisolace 全栈项目

## 项目简介

Omnisolace 是一个全年龄段AI心理疏导机器人系统，包含前端（Vue 3）和后端（Django）两个部分。该系统为不同年龄段的用户提供个性化的心理健康服务，支持青少年、青年、中年和老年四种用户模式。

## 技术架构

### 前端技术栈
- **框架**: Vue 3 (Composition API)
- **构建工具**: Vite 5.0
- **状态管理**: Pinia
- **路由**: Vue Router 4
- **样式**: Tailwind CSS 3.3
- **UI组件**: Headless UI Vue + Heroicons
- **HTTP客户端**: Axios
- **PWA支持**: Vite PWA Plugin

### 后端技术栈
- **框架**: Django 4.2.7 + Django REST Framework 3.14.0
- **数据库**: MySQL 8.0+ (主数据库)
- **缓存**: Redis 5.0.1 (缓存和会话存储)
- **认证**: JWT (JSON Web Token)
- **AI服务**: OpenAI GPT-3.5/4 + DeepSeek API
- **语音服务**: Azure Cognitive Services Speech
- **异步任务**: Celery 5.3.4 (可选)
- **WebSocket**: Django Channels 4.0.0

## 环境要求

### 系统要求
- **Python**: 3.8+
- **Node.js**: >= 16.0.0
- **MySQL**: 8.0+
- **Redis**: 5.0+ (可选)
- **Git**: 最新版本

### 开发工具
- **IDE**: VS Code / PyCharm
- **数据库管理**: MySQL Workbench / DBeaver
- **API测试**: Postman / Insomnia

## 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/WINDGAND/Omnisolace.git
cd Omnisolace
```

### 2. 后端配置

```bash
# 进入后端目录
cd backend

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp env.example .env
# 编辑 .env 文件，配置数据库和API密钥

# 创建数据库
mysql -u root -p
CREATE DATABASE omnisolace CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
exit

# 运行数据库迁移
python manage.py makemigrations
python manage.py migrate

# 创建超级用户
python manage.py createsuperuser
```

### 3. 前端配置

```bash
# 进入前端目录
cd ../frontend

# 安装依赖
npm install
# 或使用 yarn
yarn install

# 配置环境变量
cp env.example .env.local
# 编辑 .env.local 文件，配置API地址
```

### 4. 启动服务

**重要：请按以下顺序启动服务**

#### 步骤1：启动后端服务

```bash
# 在 backend 目录下
cd backend
python manage.py runserver 0.0.0.0:8000
```

后端服务将在 `http://localhost:8000` 启动

#### 步骤2：启动前端服务

```bash
# 在新的终端窗口中，在 frontend 目录下
cd frontend
npm run dev
# 或使用启动脚本
# Windows: src\scripts\start.bat
# Linux/Mac: ./src/scripts/start.sh
```

前端服务将在 `http://localhost:5174` 启动

### 5. 验证服务

- **后端API**: 访问 `http://localhost:8000/api/system/status`
- **前端应用**: 访问 `http://localhost:5174`
- **管理后台**: 访问 `http://localhost:8000/admin/`

## 详细配置说明

### 后端环境变量配置

编辑 `backend/.env` 文件：

```env
# Django 配置
SECRET_KEY=django-insecure-your-secret-key-here-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# 数据库配置
DB_NAME=omnisolace
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_PORT=3306

# Redis 配置（可选）
REDIS_URL=redis://localhost:6379/0

# AI 服务配置（必需）
OPENAI_API_KEY=your_openai_api_key_here
DEEPSEEK_API_KEY=your_deepseek_api_key_here

# Azure Speech 服务（可选）
AZURE_SPEECH_KEY=your_azure_speech_key
AZURE_SPEECH_REGION=eastus
```

### 前端环境变量配置

编辑 `frontend/.env.local` 文件：

```env
# 应用基础配置
VITE_APP_TITLE=Omnisolace
VITE_APP_VERSION=1.0.0
VITE_APP_DESCRIPTION=全年龄段AI心理疏导机器人

# API 配置
VITE_API_BASE_URL=http://localhost:8000/api
VITE_API_TIMEOUT=10000

# 开发环境配置
VITE_DEV_PORT=5174
VITE_DEV_HOST=localhost

# 功能开关
VITE_ENABLE_MOCK=false
VITE_ENABLE_DEBUG=true
VITE_ENABLE_PWA=true
VITE_ENABLE_OFFLINE=true
```

## 核心功能

### 1. 用户管理系统
- 多年龄段支持（青少年、青年、中年、老年）
- 家长监督模式
- 游客模式
- 数据保护

### 2. 智能聊天系统
- 多模态交互（文本、语音、图片）
- 个性化AI回复
- 危机检测
- 会话管理

### 3. 情绪分析系统
- 实时情绪识别
- 情绪模式分析
- 风险评估
- 预警系统

### 4. 心理档案系统
- 个性化档案
- 测评系统
- 报告生成
- 进展追踪

### 5. 紧急求助系统
- 紧急联系人管理
- 自动报警
- 专业转介

## API接口

### 认证接口
- `POST /api/v1/auth/register/` - 用户注册
- `POST /api/v1/auth/login/` - 用户登录
- `POST /api/v1/auth/refresh/` - 刷新Token
- `POST /api/v1/auth/logout/` - 用户登出
- `POST /api/v1/auth/guest-login/` - 游客登录

### 聊天接口
- `GET /api/v1/chat/sessions/` - 获取聊天会话列表
- `POST /api/v1/chat/sessions/` - 创建新会话
- `POST /api/v1/chat/send/` - 发送消息（支持流式响应）
- `DELETE /api/v1/chat/sessions/{id}/` - 删除会话

### 用户管理接口
- `GET /api/v1/user/profile/` - 获取用户档案
- `PATCH /api/v1/user/profile/` - 更新用户档案
- `POST /api/v1/user/avatar/` - 上传头像

## 测试

### 后端测试

```bash
# 运行所有测试
python manage.py test

# 运行API测试
python test_api.py
```

### 前端测试

```bash
# 样式检查
npx stylelint "src/**/*.{vue,css}"
```

## 部署

### 开发环境
按照上述"快速开始"步骤即可

### 生产环境

#### 后端部署
```bash
# 安装生产依赖
pip install gunicorn whitenoise

# 配置环境变量
export DEBUG=False
export SECRET_KEY=your-production-secret-key

# 收集静态文件
python manage.py collectstatic

# 使用Gunicorn启动
gunicorn omnisolace.wsgi:application --bind 0.0.0.0:8000
```

#### 前端部署
```bash
# 构建生产版本
npm run build

# 部署到静态服务器
# 将 dist/ 目录内容上传到服务器
```

## 常见问题

### 1. 端口冲突
- 后端默认端口：8000
- 前端默认端口：5174
- 可在配置文件中修改端口

### 2. 数据库连接失败
- 检查MySQL服务是否启动
- 验证数据库连接信息
- 确认用户权限

### 3. API连接失败
- 检查后端服务是否启动
- 验证API地址配置
- 检查CORS设置

### 4. AI服务配置
- 确保配置了正确的API密钥
- OpenAI API Key
- DeepSeek API Key

## 项目结构

```
Omnisolace/
├── frontend/                 # 前端项目
│   ├── src/                 # 源代码
│   ├── public/              # 静态资源
│   ├── package.json         # 依赖配置
│   └── README.md           # 前端说明
├── backend/                 # 后端项目
│   ├── apps/               # 应用模块
│   ├── omnisolace/         # 项目配置
│   ├── requirements.txt    # 依赖配置
│   └── README.md          # 后端说明
└── README.md              # 项目总说明
```

## 开发指南

### 代码规范
- 前端：遵循Vue 3 Composition API规范
- 后端：遵循PEP 8编码规范
- 使用Stylelint进行样式检查
- 编写完整的文档字符串

### 提交规范
```bash
# 功能开发
git commit -m "feat: 添加用户认证功能"

# 问题修复
git commit -m "fix: 修复聊天消息显示问题"

# 文档更新
git commit -m "docs: 更新API文档"
```

## 许可证

本项目采用MIT许可证。

## 联系方式

- 项目维护者：Omnisolace团队
- 邮箱：1969295061@qq.com
- 项目地址：[GitHub地址]

---

**注意**: 本项目涉及心理健康服务，请确保在部署前充分测试所有功能，并建立完善的监控和应急响应机制。
