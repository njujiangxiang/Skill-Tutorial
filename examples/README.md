# Python Skill 示例代码

本目录包含完整的 Python Skill 示例，可以直接运行和参考。

## 📦 示例列表

### 1. 天气查询 Skill

**位置**: `python-weather-skill/`

**功能**:
- ✅ 查询当前天气
- ✅ 查询天气预报
- ✅ 搜索城市
- ✅ 数据缓存

**安装依赖**:
```bash
cd python-weather-skill
pip install -r requirements.txt
```

**配置**:
```bash
export WEATHER_API_KEY="your-api-key"
```

**运行测试**:
```bash
python skill.py
```

**文件结构**:
```
python-weather-skill/
├── skill.py          # 主代码
├── requirements.txt  # 依赖
└── SKILL.md         # Skill 描述
```

### 2. 待办事项 Skill

**位置**: `python-todo-skill/`

**功能**:
- ✅ 创建任务
- ✅ 完成任务
- ✅ 删除任务
- ✅ 查看列表
- ✅ 本地存储

**安装依赖**:
```bash
cd python-todo-skill
# 无外部依赖，使用标准库
```

**运行测试**:
```bash
python skill.py
```

**文件结构**:
```
python-todo-skill/
├── skill.py          # 主代码
├── requirements.txt  # 依赖
└── SKILL.md         # Skill 描述
```

## 🚀 快速开始

### 1. 选择示例

根据你的需求选择一个示例：
- 想学习 API 调用 → 天气查询 Skill
- 想学习数据存储 → 待办事项 Skill

### 2. 安装依赖

```bash
cd python-weather-skill  # 或 python-todo-skill
pip install -r requirements.txt
```

### 3. 配置环境变量

```bash
# 天气 Skill 需要配置 API 密钥
export WEATHER_API_KEY="your-api-key"
```

### 4. 运行测试

```bash
python skill.py
```

### 5. 集成到 OpenClaw

```bash
# 安装 Skill
openclaw skills install .

# 测试 Skill
openclaw skills test weather-skill "北京天气怎么样？"
```

## 📝 代码说明

### 天气查询 Skill 关键点

```python
# 1. 异步 HTTP 请求
async with httpx.AsyncClient() as client:
    response = await client.get(url, params=query_params)

# 2. 参数验证
if not city or not isinstance(city, str):
    raise ValueError('城市名不能为空')

# 3. 缓存机制
cache_key = f'weather:{city}'
if cache_key in self.cache:
    # 使用缓存
    pass

# 4. 错误处理
try:
    # API 调用
    pass
except Exception as e:
    return {
        'success': False,
        'error': {'code': 'API_ERROR', 'message': str(e)}
    }
```

### 待办事项 Skill 关键点

```python
# 1. 本地 JSON 存储
def _read_data(self) -> Dict:
    with open(self.todo_file, 'r') as f:
        return json.load(f)

# 2. 任务 CRUD 操作
def create(self, title: str, priority: str) -> Dict:
    # 创建新任务
    pass

def complete(self, todo_id: str) -> Dict:
    # 完成任务
    pass

# 3. 数据排序
todos.sort(key=lambda t: (
    0 if t['status'] == 'pending' else 1,
    priority_order.get(t['priority'], 1),
    t['createdAt']
))
```

## 🎯 学习路径

### 初学者

1. 阅读 `skill.py` 代码
2. 理解参数验证
3. 运行测试
4. 修改代码实验

### 进阶学习

1. 添加新功能
2. 优化错误处理
3. 添加单元测试
4. 发布到 Skill Hub

## 📚 参考资源

- [Python 官方文档](https://docs.python.org/zh-cn/3/)
- [httpx 文档](https://www.python-httpx.org/)
- [OpenClaw Skill 规范](../../01-Skill 基础/03-Skill 规范.md)

## 🔗 相关教程

- [工具函数开发](../02-Skill 开发/02-工具函数开发.md)
- [测试与调试](../02-Skill 开发/04-测试与调试.md)
- [天气查询实战](../03-实战项目/01-天气查询 Skill.md)
- [待办事项实战](../03-实战项目/02-待办事项 Skill.md)

---

**维护**: 大龙虾 🦞  
**更新**: 2026-03-17
