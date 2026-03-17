# 03 - Skill 规范文档

## 📋 SKILL.md 规范

### 必需字段

```markdown
# 名称
[Skill 名称]

# 描述
[简短描述 Skill 的功能]

# 版本
[语义化版本号，如 1.0.0]

# 作者
[作者信息]
```

### 可选字段

```markdown
# 触发词
[触发 Skill 的关键词列表]

# 工具
[可用的工具函数列表]

# 依赖
[外部依赖列表]

# 配置
[配置项说明]

# 示例对话
[使用示例]

# 许可证
[许可证类型]
```

## 📝 完整示例

```markdown
# 名称
天气查询 Skill

# 描述
查询全球城市天气信息，支持当前天气和天气预报

# 版本
1.0.0

# 作者
大龙虾 <dalongxia@example.com>

# 触发词
- 天气
- 气温
- 天气预报
- 下雨
- 温度

# 工具
## getWeather
- 描述：查询城市当前天气
- 参数:
  - city (string, 必需): 城市名称
- 返回：天气信息对象

## getForecast
- 描述：查询天气预报
- 参数:
  - city (string, 必需): 城市名称
  - days (number, 可选): 天数，默认 7 天
- 返回：天气预报列表

# 依赖
- node-fetch >= 3.0.0
- node-cache >= 5.0.0

# 配置
## API_KEY
- 描述：天气 API 密钥
- 必需：是
- 来源：https://weatherapi.com

# 示例对话
## 示例 1: 查询当前天气
用户：北京天气怎么样？
AI: 北京今天晴，气温 25°C，空气质量良好。

## 示例 2: 查询天气预报
用户：上海未来 3 天天气
AI: 上海未来 3 天天气预报：
     今天：晴，25°C
     明天：多云，27°C
     后天：小雨，23°C

# 许可证
MIT
```

## 🔧 工具函数规范

### 函数签名

```javascript
/**
 * 工具函数描述
 * @param {Object} params - 参数对象
 * @param {string} params.city - 城市名称
 * @returns {Promise<Object>} - 结果对象
 */
async function getWeather(params) {
  // 实现
}
```

### 返回格式

```javascript
// ✅ 成功响应
{
  success: true,
  data: {
    // 实际数据
  }
}

// ❌ 失败响应
{
  success: false,
  error: {
    code: 'ERROR_CODE',
    message: '错误描述'
  }
}
```

## 📦 目录结构规范

### 基础结构

```
my-skill/
├── SKILL.md              # 必需：Skill 描述
├── index.js              # 必需：入口文件
├── package.json          # 推荐：依赖管理
├── README.md             # 推荐：使用说明
├── .gitignore            # 推荐：Git 忽略文件
└── tools/                # 推荐：工具函数目录
    ├── weather.js
    └── utils.js
```

### 高级结构

```
my-skill/
├── SKILL.md
├── index.js
├── package.json
├── README.md
├── src/
│   ├── index.js          # 主逻辑
│   ├── tools/            # 工具函数
│   │   ├── weather.js
│   │   └── forecast.js
│   └── utils/            # 工具类
│       ├── cache.js
│       └── logger.js
├── tests/                # 测试文件
│   └── weather.test.js
├── docs/                 # 文档
│   └── api.md
└── config/               # 配置
    └── default.json
```

## 🎯 命名规范

### 文件命名

```
✅ index.js
✅ weather-skill.js
✅ getWeather.js

❌ Index.js
❌ weatherSkill.js
❌ GetWeather.js
```

### 函数命名

```javascript
// ✅ 动词 + 名词
async function getWeather() {}
async function createTodo() {}
async function deleteFile() {}

// ❌ 模糊命名
async function doSomething() {}
async function handle() {}
```

### Skill 命名

```
✅ weather-skill
✅ todo-manager
✅ file-operations

❌ WeatherSkill
❌ todo_manager
❌ file
```

## 📊 版本规范

### 语义化版本

```
主版本号。次版本号。修订号
  ↑      ↑      ↑
  |      |      └─ 向后兼容的问题修正
  |      └──────── 向后兼容的功能新增
  └─────────────── 不兼容的 API 修改

示例：
1.0.0  - 初始版本
1.0.1  - 问题修正
1.1.0  - 功能新增
2.0.0  - 不兼容更新
```

### 更新日志

```markdown
# 更新日志

## [1.1.0] - 2026-03-17
### 新增
- 添加天气预报功能
- 支持多城市查询

### 修正
- 修复缓存问题
- 优化错误处理

## [1.0.0] - 2026-03-10
### 新增
- 初始版本
- 支持当前天气查询
```

## 🔒 安全规范

### 敏感信息

```javascript
// ✅ 从环境变量读取
const apiKey = process.env.WEATHER_API_KEY;

// ❌ 硬编码
const apiKey = 'sk-1234567890';
```

### 输入验证

```javascript
// ✅ 验证输入
async function getWeather(params) {
  if (!params.city || typeof params.city !== 'string') {
    throw new Error('城市名不能为空');
  }
  
  if (params.city.length > 100) {
    throw new Error('城市名过长');
  }
  
  // 继续处理
}

// ❌ 不验证输入
async function getWeather(params) {
  // 直接使用 params.city
}
```

### 错误处理

```javascript
// ✅ 不泄露敏感信息
try {
  const result = await api.call(params);
  return result;
} catch (error) {
  logger.error('API 调用失败', error);
  throw new Error('服务暂时不可用');
}

// ❌ 泄露内部信息
try {
  const result = await api.call(params);
  return result;
} catch (error) {
  throw new Error(`API 错误：${error.message} ${api.key}`);
}
```

## 📚 下一步

- [04-环境搭建.md](./04-环境搭建.md) - 配置开发环境
- [02-Skill 开发/01-SKILL.md 编写.md](../02-Skill 开发/01-SKILL.md 编写.md) - 学习编写 SKILL.md

## 🔗 参考资源

- [Skill 规范官方文档](https://docs.openclaw.ai/skills/spec)
- [示例 Skills](https://github.com/openclaw/skills)
