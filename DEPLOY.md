# Railway 全栈部署指南

本指南将帮助您将 Omnisolace 项目的前端、后端和数据库全部部署到 Railway 平台。

## 🎯 架构

```
Railway 项目
├── MySQL 数据库服务
├── Django 后端服务 (backend/)
└── Vue.js 前端服务 (frontend/)
```

---

## 📋 准备工作

1. **确保项目已推送到 GitHub**
   ```bash
   git add .
   git commit -m "Prepare for Railway deployment"
   git push
   ```

2. **创建 Railway 账户**
   - 访问 [railway.app](https://railway.app)
   - 使用 GitHub 账户登录

---

## 🚀 部署步骤

### 步骤 1: 创建 Railway 项目

1. 登录 Railway 后，点击 **"New Project"**
2. 选择 **"Deploy from GitHub repo"**
3. 选择您的 `omnisolace` 仓库
4. Railway 会自动尝试部署，先跳过（我们需要手动配置服务）

### 步骤 2: 添加 MySQL 数据库

1. 在项目页面，点击 **"New"** → **"Database"** → **"MySQL"**
2. Railway 会自动创建 MySQL 实例并提供连接信息
3. **重要**: Railway 会自动生成数据库环境变量，Django 设置已配置为自动识别，无需手动配置

### 步骤 3: 配置后端服务

1. 在项目中，点击 **"New"** → **"GitHub Repo"**，选择相同的仓库
2. 在后端服务设置中：
   - **Root Directory**: 设置为 `backend`
   - **Start Command**: 
     ```
     python manage.py migrate && gunicorn omnisolace.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120
     ```
3. 在 **"Variables"** 标签页添加环境变量：

```
SECRET_KEY=你的Django密钥（使用 openssl rand -hex 32 生成）
DEBUG=False
ALLOWED_HOSTS=*.railway.app
CORS_ALLOWED_ORIGINS=https://你的前端域名.railway.app（稍后填写）
```

**注意**: 数据库连接变量（MYSQLHOST, MYSQLPORT 等）由 Railway 自动提供，Django 会自动识别。

### 步骤 4: 配置前端服务

1. 在同一个项目中，点击 **"New"** → **"GitHub Repo"**，选择相同的仓库
2. 在前端服务设置中：
   - **Root Directory**: 设置为 `frontend`
   - **Build Command**: `npm install && npm run build`
   - **Start Command**: `npm run start`
3. 在 **"Variables"** 标签页添加环境变量：

```
VITE_API_BASE_URL=https://你的后端域名.railway.app/api
```

**注意**: 需要先部署后端服务获取 URL。

### 步骤 5: 配置服务 URL

1. **获取后端 URL**
   - 等待后端部署完成（通常 2-5 分钟）
   - 在后端服务页面，复制公共 URL（格式：`https://xxx.up.railway.app`）

2. **更新前端环境变量**
   - 在前端服务的 **Variables** 中更新：
     ```
     VITE_API_BASE_URL=https://后端URL/api
     ```
   - 点击服务右上角的 **"Deploy"** 按钮重新部署

3. **获取前端 URL**
   - 等待前端部署完成
   - 在前端服务页面，复制公共 URL

4. **更新后端 CORS**
   - 在后端服务的 **Variables** 中更新：
     ```
     CORS_ALLOWED_ORIGINS=https://前端URL
     ```
   - 点击 **"Deploy"** 按钮重新部署

---

## ✅ 验证部署

- [ ] 访问前端 URL，确认页面加载正常
- [ ] 测试用户注册功能
- [ ] 测试用户登录功能
- [ ] 测试主要功能（聊天、情绪分析等）
- [ ] 检查浏览器控制台无错误
- [ ] 检查网络请求是否成功
- [ ] 查看 Railway 日志确认服务正常运行

---

## 📝 环境变量参考

### 后端服务必需变量

```
SECRET_KEY=你的密钥
DEBUG=False
ALLOWED_HOSTS=*.railway.app
CORS_ALLOWED_ORIGINS=https://前端URL
```

数据库变量由 Railway 自动提供，无需手动配置。

### 前端服务必需变量

```
VITE_API_BASE_URL=https://后端URL/api
```

### 可选环境变量（根据需求添加）

- `OPENAI_API_KEY` - OpenAI API 密钥
- `AZURE_SPEECH_KEY` - Azure 语音服务密钥
- 其他第三方服务配置

---

## 🔄 自动部署

推送代码到 GitHub 后，Railway 会自动检测并重新部署相关服务。

---

## 💡 重要提示

1. **服务间通信**: Railway 会自动处理同一项目内服务的网络连接
2. **环境变量共享**: 数据库变量会自动在服务间共享
3. **日志查看**: 在服务页面可以查看实时日志
4. **重新部署**: 更新环境变量后，需要手动触发重新部署

---

## 🆘 常见问题

### 数据库迁移失败

**解决方案**:
- 检查数据库连接环境变量是否正确（Railway 自动提供）
- 在服务终端手动运行：`python manage.py migrate`
- 检查 MySQL 客户端库是否正确安装

### 前端无法连接后端

**解决方案**:
- 确认 `VITE_API_BASE_URL` 环境变量正确
- 确认后端 CORS 配置包含前端 URL
- 检查后端服务是否正常运行

### 环境变量不生效

**解决方案**:
- 更新环境变量后需要重新部署服务
- 确认变量名拼写正确
- 前端变量名必须以 `VITE_` 开头

---

## 💰 费用说明

- **免费额度**: $5/月
- **预估费用**: $3-7/月（Hobby 计划）
- 包含：MySQL 数据库 + 后端服务 + 前端服务

---

**祝您部署顺利！** 🚀

