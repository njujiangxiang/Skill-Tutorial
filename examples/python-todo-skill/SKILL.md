# 名称
待办事项 Skill (Python 版)

# 描述
管理个人待办事项，支持创建、完成、删除任务

# 版本
1.0.0

# 作者
大龙虾

# 语言
Python 3.9+

# 触发词
- 待办
- 任务
- todo
- 提醒

# 工具
## create_todo
- 描述：创建新任务
- 参数:
  - title (string, 必需): 任务标题
  - priority (string, 可选): 优先级 (high/medium/low)
- 返回：任务对象

## complete_todo
- 描述：完成任务
- 参数:
  - id (string, 必需): 任务 ID
- 返回：成功/失败

## list_todos
- 描述：查看任务列表
- 参数:
  - status (string, 可选): 状态 (pending/completed/all)
- 返回：任务列表

## delete_todo
- 描述：删除任务
- 参数:
  - id (string, 必需): 任务 ID
- 返回：成功/失败

# 存储
- 本地 JSON 文件存储
- 路径：~/.openclaw/data/todos.json

# 示例对话
用户：创建一个待办，明天开会
AI: 已创建任务：明天开会

用户：查看我的待办
AI: 你有 3 个待办事项...

用户：完成第一个任务
AI: 已完成任务：明天开会

# 许可证
MIT
