# DeepSeek API 集成指南

## 概述

本指南将帮助你将DeepSeek API集成到Omnisolace心理辅导系统中，实现真实的AI对话功能。

## 已完成的集成工作

### 1. 后端集成
- ✅ 创建了 `services/ai_service.py` - DeepSeek AI服务类
- ✅ 更新了 `apps/chat/views.py` - 集成DeepSeek API调用
- ✅ 添加了环境变量配置
- ✅ 更新了依赖包

### 2. 前端集成
- ✅ 更新了 `Chat.vue` - 使用真实API替代模拟数据
- ✅ 保持了现有的用户界面和交互逻辑

## 配置步骤

### 1. 获取DeepSeek API密钥

1. 访问 [DeepSeek官网](https://platform.deepseek.com/)
2. 注册账号并登录
3. 在API管理页面创建新的API密钥
4. 复制生成的API密钥

### 2. 配置环境变量

在 `backend/.env` 文件中添加以下配置：

```bash
# DeepSeek API 配置
DEEPSEEK_API_KEY=your_actual_deepseek_api_key_here
DEEPSEEK_MODEL=deepseek-chat
```

### 3. 安装依赖

在backend目录下运行：

```bash
pip install -r requirements.txt
```

### 4. 重启后端服务

```bash
python manage.py runserver
```

## 功能特性

### 1. 智能对话
- 支持多轮对话，保持上下文
- 根据用户年龄段提供个性化回复
- 支持流式响应，提升用户体验

### 2. 情绪分析
- 自动分析用户消息的情绪状态
- 提供情绪趋势分析
- 根据情绪状态调整回复策略

### 3. 年龄段适配
- **青少年**: 关注学习压力、人际关系
- **年轻人**: 工作压力、情感问题、职业规划
- **中年人**: 家庭关系、工作压力、健康担忧
- **老年人**: 孤独感、健康担忧、适应退休生活

## API接口说明

### 发送消息接口
```
POST /api/v1/chat/send/
```

请求体：
```json
{
  "content": "用户消息内容",
  "message_type": "text",
  "session_id": "会话ID（可选）"
}
```

响应：
```json
{
  "success": true,
  "message": "消息发送成功",
  "data": {
    "user_message": {...},
    "ai_message": {...},
    "session_id": "会话ID"
  }
}
```

### 流式响应
支持Server-Sent Events (SSE)流式响应，实时显示AI回复内容。

## 错误处理

### 常见错误及解决方案

1. **API密钥无效**
   - 检查 `DEEPSEEK_API_KEY` 是否正确设置
   - 确认API密钥是否有效且有足够额度

2. **网络连接问题**
   - 检查网络连接
   - 确认DeepSeek API服务是否正常

3. **请求超时**
   - 检查网络延迟
   - 考虑增加超时时间设置

## 监控和日志

### 日志记录
系统会自动记录以下信息：
- API调用成功/失败
- 响应时间
- 错误信息
- 用户情绪分析结果

### 性能监控
- 响应时间统计
- API调用频率
- 错误率监控

## 安全考虑

### 1. API密钥安全
- 不要在代码中硬编码API密钥
- 使用环境变量存储敏感信息
- 定期轮换API密钥

### 2. 数据隐私
- 用户消息会发送到DeepSeek API
- 确保符合数据保护法规
- 考虑敏感信息的脱敏处理

### 3. 访问控制
- 实施适当的访问限制
- 监控API使用情况
- 防止滥用

## 测试验证

### 1. 功能测试
```bash
# 测试发送消息
curl -X POST http://localhost:8000/api/v1/chat/send/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"content": "你好，我最近感到焦虑", "message_type": "text"}'
```

### 2. 前端测试
1. 打开聊天界面
2. 发送测试消息
3. 验证AI回复是否正常
4. 检查情绪分析是否工作

## 故障排除

### 1. 检查服务状态
```bash
# 检查后端服务
curl http://localhost:8000/api/system/status

# 检查AI服务配置
curl http://localhost:8000/api/system/health
```

### 2. 查看日志
```bash
# 查看Django日志
tail -f backend/logs/django.log

# 查看应用日志
grep "DeepSeek" backend/logs/django.log
```

## 性能优化

### 1. 缓存策略
- 缓存常用回复模板
- 实施智能缓存机制

### 2. 并发处理
- 使用异步处理提升性能
- 实施请求队列管理

### 3. 资源管理
- 监控API使用量
- 实施智能限流

## 后续改进

### 1. 功能增强
- 支持更多AI模型选择
- 添加对话质量评估
- 实现个性化学习

### 2. 用户体验
- 优化响应速度
- 改进错误提示
- 增强交互体验

### 3. 数据分析
- 用户行为分析
- 对话效果评估
- 情绪趋势统计

## 联系支持

如果在集成过程中遇到问题，请：
1. 查看本文档的故障排除部分
2. 检查系统日志
3. 联系技术支持团队

---

**注意**: 请确保在生产环境中使用前进行充分测试，并遵循相关的数据保护和安全规范。
