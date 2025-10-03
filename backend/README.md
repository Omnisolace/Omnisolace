# Omnisolace 后端项目

## 项目简介

Omnisolace 是一个全年龄段AI心理疏导机器人后端系统，基于 Django 4.2 + Django REST Framework 构建。该系统为不同年龄段的用户提供个性化的心理健康服务，支持青少年、青年、中年和老年四种用户模式。

## 技术栈

- **框架**: Django 4.2.7 + Django REST Framework 3.14.0
- **数据库**: MySQL 8.0+ (主数据库)
- **缓存**: Redis 5.0.1 (缓存和会话存储)
- **认证**: JWT (JSON Web Token)
- **AI服务**: OpenAI GPT-3.5/4 + DeepSeek API
- **语音服务**: Azure Cognitive Services Speech
- **异步任务**: Celery 5.3.4 (可选)
- **WebSocket**: Django Channels 4.0.0
- **部署**: Gunicorn + WhiteNoise

## 项目结构

```
backend/
├── apps/                    # 应用模块
│   ├── users/              # 用户管理
│   │   ├── models.py       # 用户模型
│   │   ├── views.py        # 用户视图
│   │   ├── serializers.py  # 序列化器
│   │   └── urls.py         # 用户路由
│   ├── chat/               # 聊天系统
│   │   ├── models.py       # 聊天模型
│   │   ├── views.py        # 聊天视图
│   │   ├── serializers.py  # 序列化器
│   │   └── urls.py         # 聊天路由
│   ├── emotion/            # 情绪分析
│   ├── profile/            # 心理档案
│   ├── emergency/          # 紧急求助
│   └── common/             # 公共功能
├── omnisolace/             # 项目配置
│   ├── settings.py         # 主配置文件
│   ├── urls.py            # URL路由
│   ├── wsgi.py            # WSGI配置
│   └── asgi.py            # ASGI配置
├── utils/                  # 工具模块
│   ├── middleware.py       # 自定义中间件
│   ├── permissions.py     # 权限控制
│   ├── responses.py       # 响应工具
│   └── handlers.py        # 异常处理
├── services/              # 服务层
│   └── ai_service.py      # AI服务
├── database/              # 数据库相关
│   └── mysql_schema.sql   # 数据库结构
├── logs/                  # 日志文件
├── tmp/                   # 临时文件
├── media/                 # 媒体文件
├── requirements.txt       # 依赖包
├── manage.py             # Django管理脚本
├── test_api.py           # API测试脚本
├── env.example           # 环境变量示例
└── DEEPSEEK_INTEGRATION_GUIDE.md  # DeepSeek集成指南
```

## 环境要求

- **Python**: 3.8+
- **MySQL**: 8.0+
- **Redis**: 5.0+ (可选)
- **Node.js**: 16+ (前端开发)

## 安装步骤

### 1. 克隆项目

```bash
git clone https://github.com/WINDGAND/Omnisolace.git
cd Omnisolace/backend
```

### 2. 创建虚拟环境

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置环境变量

```bash
# 复制环境变量示例文件
cp env.example .env

# 编辑 .env 文件，配置必要的环境变量
```

**重要环境变量配置：**

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

# Redis 配置
REDIS_URL=redis://localhost:6379/0

# AI 服务配置
OPENAI_API_KEY=your_openai_api_key_here
DEEPSEEK_API_KEY=your_deepseek_api_key_here

# Azure Speech 服务
AZURE_SPEECH_KEY=your_azure_speech_key
AZURE_SPEECH_REGION=eastus
```

### 5. 数据库配置

#### 创建数据库

```bash
# 登录MySQL
mysql -u root -p

# 创建数据库
CREATE DATABASE omnisolace CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 退出MySQL
exit
```

#### 运行数据库迁移

```bash
# 创建迁移文件
python manage.py makemigrations

# 执行迁移
python manage.py migrate

# 创建超级用户
python manage.py createsuperuser
```

### 6. 启动服务

#### 开发环境

```bash
# 启动Django开发服务器
python manage.py runserver 0.0.0.0:8000

# 启动Redis (可选)
redis-server

# 启动Celery (可选)
celery -A omnisolace worker -l info
```

#### 生产环境

```bash
# 使用Gunicorn
gunicorn omnisolace.wsgi:application --bind 0.0.0.0:8000

# 使用Nginx反向代理
# 配置SSL证书
# 设置环境变量
```

## 核心功能

### 1. 用户管理系统

- **多年龄段支持**: 青少年、青年、中年、老年用户
- **家长监督模式**: 青少年用户的家长监督功能
- **游客模式**: 无需注册的临时使用
- **数据保护**: 敏感信息加密存储

### 2. 智能聊天系统

- **多模态交互**: 支持文本、语音、图片等多种输入方式
- **个性化回复**: 基于用户心理档案的定制化AI回复
- **危机检测**: 实时监测用户情绪状态，识别危机信号
- **会话管理**: 完整的聊天会话记录和管理

### 3. 情绪分析系统

- **实时情绪识别**: 基于文本和语音的情绪分析
- **情绪模式识别**: 分析用户的情绪变化规律
- **风险评估**: 多维度心理健康风险评估
- **预警系统**: 自动检测并预警高风险情况

### 4. 心理档案系统

- **个性化档案**: 基于用户数据的心理档案构建
- **测评系统**: 多种心理测评工具（PHQ-9、GAD-7等）
- **报告生成**: 自动生成心理健康报告
- **进展追踪**: 长期心理健康状况追踪

### 5. 紧急求助系统

- **紧急联系人**: 用户紧急联系人管理
- **自动报警**: 危机情况下的自动报警机制
- **专业转介**: 与专业心理服务机构的对接

## API接口

### 认证接口

- `POST /api/v1/auth/register/` - 用户注册
- `POST /api/v1/auth/login/` - 用户登录
- `POST /api/v1/auth/refresh/` - 刷新Token
- `POST /api/v1/auth/logout/` - 用户登出
- `POST /api/v1/auth/guest-login/` - 游客登录

### 用户管理接口

- `GET /api/v1/user/profile/` - 获取用户档案
- `PATCH /api/v1/user/profile/` - 更新用户档案
- `POST /api/v1/user/avatar/` - 上传头像
- `POST /api/v1/user/change-password/` - 修改密码

### 聊天接口

- `GET /api/v1/chat/sessions/` - 获取聊天会话列表
- `POST /api/v1/chat/sessions/` - 创建新会话
- `GET /api/v1/chat/sessions/{id}/messages/` - 获取会话消息
- `POST /api/v1/chat/send/` - 发送消息（支持流式响应）
- `DELETE /api/v1/chat/sessions/{id}/` - 删除会话
- `POST /api/v1/chat/feedback/` - 发送反馈

### 情绪分析接口

- `POST /api/v1/emotion/analyze/` - 分析情绪
- `GET /api/v1/emotion/history/` - 获取情绪历史
- `GET /api/v1/emotion/stats/` - 获取情绪统计

### 紧急求助接口

- `GET /api/v1/emergency/contacts/` - 获取紧急联系人
- `POST /api/v1/emergency/contacts/` - 添加紧急联系人
- `POST /api/v1/emergency/trigger/` - 触发紧急求助

### 系统接口

- `GET /api/system/status` - 系统状态检查
- `GET /api/system/health` - 健康检查

## 数据模型

### 核心模型

#### 用户模型 (User)
- 支持多年龄段用户（青少年、青年、中年、老年）
- 青少年用户家长监督功能
- 游客用户支持
- 敏感信息加密存储

#### 聊天会话 (ChatSession)
- 会话管理和状态跟踪
- 消息计数和持续时间统计
- 紧急会话标识
- 数据脱敏处理

#### 聊天消息 (ChatMessage)
- 多类型消息支持（文本、语音、图片）
- 情绪数据记录
- 危机检测标记
- AI回复元数据

#### 情绪日志 (EmotionLog)
- 多维度情绪识别
- 危机风险评估
- 情绪模式分析
- 上下文信息记录

## 安全机制

### 数据保护
- **加密存储**: 手机号等敏感信息加密
- **数据脱敏**: 聊天记录自动脱敏处理
- **访问控制**: 基于角色的权限管理
- **审计日志**: 完整的操作日志记录

### 危机干预
- **关键词检测**: 实时监测危机信号
- **风险评估**: 多维度风险等级评估
- **自动报警**: 高风险情况自动通知
- **专业转介**: 与专业机构对接

### 家长监督
- **使用时长限制**: 青少年用户使用时间控制
- **活动监控**: 家长可查看使用情况
- **内容过滤**: 不当内容自动过滤
- **同意机制**: 家长同意确认机制

## 测试

### 运行测试

```bash
# 运行所有测试
python manage.py test

# 运行特定应用测试
python manage.py test apps.chat

# 运行API测试
python test_api.py
```

### API测试脚本

项目提供了完整的API测试脚本 `test_api.py`，可以测试所有主要接口：

```bash
# 运行完整API测试
python test_api.py

# 测试特定功能
python test_api.py --test-auth
python test_api.py --test-chat
python test_api.py --test-emotion
```

## 部署指南

### 开发环境部署

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 配置环境变量
cp env.example .env
# 编辑 .env 文件

# 3. 数据库迁移
python manage.py makemigrations
python manage.py migrate

# 4. 创建超级用户
python manage.py createsuperuser

# 5. 启动服务
python manage.py runserver 0.0.0.0:8000
```

### 生产环境部署

```bash
# 1. 安装生产依赖
pip install gunicorn whitenoise

# 2. 配置环境变量
export DEBUG=False
export SECRET_KEY=your-production-secret-key

# 3. 收集静态文件
python manage.py collectstatic

# 4. 使用Gunicorn启动
gunicorn omnisolace.wsgi:application --bind 0.0.0.0:8000
```

### Nginx配置示例

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /static/ {
        alias /path/to/your/staticfiles/;
    }
    
    location /media/ {
        alias /path/to/your/media/;
    }
}
```

## 监控和日志

### 日志系统
- **请求日志**: 所有API请求记录
- **错误日志**: 异常和错误信息
- **安全日志**: 安全相关事件记录
- **业务日志**: 业务操作记录

### 性能监控
- **响应时间**: API响应时间监控
- **错误率**: 错误率统计
- **资源使用**: CPU、内存使用情况
- **数据库性能**: 查询性能监控

## 开发工具

### 推荐工具
- **IDE**: PyCharm / VS Code
- **数据库管理**: MySQL Workbench / DBeaver
- **API测试**: Postman / Insomnia
- **版本控制**: Git

### 代码规范
- 遵循PEP 8编码规范
- 编写完整的文档字符串
- 添加必要的测试用例
- 保持代码简洁和可读性

## 常见问题

### 1. 数据库连接失败

检查以下配置：
- MySQL服务是否启动
- 数据库连接信息是否正确
- 用户权限是否足够

### 2. Redis连接失败

```bash
# 检查Redis服务
redis-cli ping

# 启动Redis服务
redis-server
```

### 3. AI服务配置

确保配置了正确的API密钥：
- OpenAI API Key
- DeepSeek API Key
- Azure Speech Key

### 4. 静态文件问题

```bash
# 收集静态文件
python manage.py collectstatic

# 检查静态文件配置
python manage.py findstatic admin/css/base.css
```

## 贡献指南

### 开发流程
1. Fork项目
2. 创建功能分支
3. 编写代码和测试
4. 提交Pull Request

### 代码规范
- 遵循PEP 8编码规范
- 编写完整的文档字符串
- 添加必要的测试用例
- 保持代码简洁和可读性

## 许可证

本项目采用MIT许可证，详见LICENSE文件。

## 联系方式

- 项目维护者：Omnisolace团队
- 邮箱：1969295061@qq.com
- 项目地址：[GitHub地址]

## 更新日志

### v1.0.0 (2024-01-01)
- 初始版本发布
- 基础聊天功能
- 情绪分析系统
- 用户管理系统
- 心理档案功能
- 紧急求助系统

---

**注意**: 本项目涉及心理健康服务，请确保在部署前充分测试所有功能，并建立完善的监控和应急响应机制。