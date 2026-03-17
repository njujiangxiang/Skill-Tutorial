# 02 - Skill 架构详解

## 🏗️ 整体架构

Skill 系统采用**分层架构**，从用户请求到 Skill 执行经过多个处理阶段。

```
┌─────────────────────────────────────────────────────────────┐
│                      用户请求                                │
└────────────────────────────┬────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────┐
│                   OpenClaw Core                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  1. 意图识别 (Intent Recognition)                     │  │
│  │     - 分析用户输入                                    │  │
│  │     - 提取关键信息                                    │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  2. Skill 匹配 (Skill Matching)                        │  │
│  │     - 查找匹配的 Skill                               │  │
│  │     - 确定优先级                                     │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  3. 工具调用 (Tool Invocation)                        │  │
│  │     - 参数提取                                       │  │
│  │     - 执行工具函数                                   │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  4. 结果处理 (Result Processing)                      │  │
│  │     - 格式化结果                                     │  │
│  │     - 生成回复                                       │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────┐
│                      Skill 层                                │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                 │
│  │ Skill A  │  │ Skill B  │  │ Skill C  │                 │
│  └──────────┘  └──────────┘  └──────────┘                 │
└─────────────────────────────────────────────────────────────┘
```

## 📦 核心组件

### 1. Skill 管理器 (Skill Manager)

**职责**: 管理 Skill 的生命周期

```javascript
class SkillManager {
  constructor() {
    this.skills = new Map();
  }

  // 注册 Skill
  register(skill) {
    this.skills.set(skill.name, skill);
  }

  // 卸载 Skill
  unregister(name) {
    this.skills.delete(name);
  }

  // 查找 Skill
  find(intent) {
    for (const skill of this.skills.values()) {
      if (skill.match(intent)) {
        return skill;
      }
    }
    return null;
  }

  // 列出所有 Skill
  list() {
    return Array.from(this.skills.values());
  }
}
```

### 2. 意图识别器 (Intent Recognizer)

**职责**: 分析用户输入，识别意图

```javascript
class IntentRecognizer {
  constructor() {
    this.patterns = new Map();
  }

  // 注册意图模式
  registerPattern(intent, patterns) {
    this.patterns.set(intent, patterns);
  }

  // 识别意图
  recognize(input) {
    input = input.toLowerCase();
    
    for (const [intent, patterns] of this.patterns) {
      for (const pattern of patterns) {
        if (pattern.test(input)) {
          return { intent, input };
        }
      }
    }
    
    return null;
  }
}

// 使用示例
const recognizer = new IntentRecognizer();
recognizer.registerPattern('weather', [
  /(.*) 天气 (.*)/,
  /(.*) 气温 (.*)/,
  /(.*) 下雨 (.*)/,
]);

const intent = recognizer.recognize('北京天气怎么样');
// 返回：{ intent: 'weather', input: '北京天气怎么样' }
```

### 3. 工具注册表 (Tool Registry)

**职责**: 管理可用的工具函数

```javascript
class ToolRegistry {
  constructor() {
    this.tools = new Map();
  }

  // 注册工具
  register(name, fn, schema) {
    this.tools.set(name, { fn, schema });
  }

  // 获取工具
  get(name) {
    return this.tools.get(name);
  }

  // 列出所有工具
  list() {
    return Array.from(this.tools.entries()).map(([name, { schema }]) => ({
      name,
      schema,
    }));
  }
}

// 使用示例
const registry = new ToolRegistry();
registry.register('getWeather', getWeather, {
  type: 'function',
  parameters: {
    type: 'object',
    properties: {
      city: { type: 'string', description: '城市名' },
    },
    required: ['city'],
  },
});
```

### 4. 执行引擎 (Execution Engine)

**职责**: 执行工具函数并处理结果

```javascript
class ExecutionEngine {
  constructor(toolRegistry) {
    this.registry = toolRegistry;
  }

  async execute(toolName, params) {
    const tool = this.registry.get(toolName);
    if (!tool) {
      throw new Error(`工具不存在：${toolName}`);
    }

    try {
      // 验证参数
      this.validateParams(params, tool.schema);
      
      // 执行工具
      const result = await tool.fn(params);
      
      // 处理结果
      return this.processResult(result);
    } catch (error) {
      return this.handleError(error);
    }
  }

  validateParams(params, schema) {
    // 参数验证逻辑
  }

  processResult(result) {
    // 结果处理逻辑
    return result;
  }

  handleError(error) {
    // 错误处理逻辑
    throw error;
  }
}
```

## 🔄 执行流程

### 完整流程

```
1. 用户输入
   ↓
2. 意图识别
   ↓
3. Skill 匹配
   ↓
4. 参数提取
   ↓
5. 工具调用
   ↓
6. 结果处理
   ↓
7. 生成回复
```

### 详细步骤

#### Step 1: 用户输入

```javascript
const userInput = "北京今天天气怎么样？";
```

#### Step 2: 意图识别

```javascript
const intent = recognizer.recognize(userInput);
// { intent: 'weather', entities: { city: '北京' } }
```

#### Step 3: Skill 匹配

```javascript
const skill = skillManager.find(intent);
// 返回匹配的 WeatherSkill
```

#### Step 4: 参数提取

```javascript
const params = skill.extractParams(userInput, intent);
// { city: '北京', date: '今天' }
```

#### Step 5: 工具调用

```javascript
const result = await skill.execute('getWeather', params);
// { temperature: 25, condition: '晴', ... }
```

#### Step 6: 结果处理

```javascript
const formatted = skill.formatResult(result);
// "北京今天晴，气温 25°C"
```

#### Step 7: 生成回复

```javascript
const response = await ai.generateResponse(formatted);
// "北京今天天气很好，晴空万里，气温 25°C，适合户外活动。"
```

## 🔌 Skill 接口

### 基础接口

```typescript
interface Skill {
  // Skill 名称
  name: string;
  
  // Skill 描述
  description: string;
  
  // 触发词
  triggers: string[];
  
  // 可用工具
  tools: Tool[];
  
  // 匹配意图
  match(intent: Intent): boolean;
  
  // 提取参数
  extractParams(input: string, intent: Intent): any;
  
  // 执行工具
  execute(toolName: string, params: any): Promise<any>;
  
  // 格式化结果
  formatResult(result: any): string;
}
```

### 工具接口

```typescript
interface Tool {
  // 工具名称
  name: string;
  
  // 工具描述
  description: string;
  
  // 参数 schema
  schema: JSONSchema;
  
  // 执行函数
  execute(params: any): Promise<any>;
}
```

## 📊 数据流

```
┌──────────────────────────────────────────────────────────────┐
│  用户输入："北京天气怎么样？"                                 │
└────────────────────┬─────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────┐
│  意图识别                                                     │
│  - intent: weather                                           │
│  - entities: { city: "北京" }                                │
└────────────────────┬─────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────┐
│  Skill 匹配                                                    │
│  - 匹配到：WeatherSkill                                      │
└────────────────────┬─────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────┐
│  工具调用：getWeather({ city: "北京" })                        │
└────────────────────┬─────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────┐
│  API 请求                                                      │
│  GET https://api.weather.com/v1/current?city=北京             │
└────────────────────┬─────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────┐
│  API 响应                                                      │
│  { temperature: 25, condition: "晴", humidity: 60 }          │
└────────────────────┬─────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────┐
│  结果格式化                                                   │
│  "北京今天晴，气温 25°C，湿度 60%"                            │
└────────────────────┬─────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────┐
│  AI 生成回复                                                   │
│  "北京今天天气很好，晴空万里..."                              │
└──────────────────────────────────────────────────────────────┘
```

## 🎯 最佳实践

### 1. 单一职责

```javascript
// ✅ 好的设计
class WeatherSkill {
  // 只负责天气相关
}

class TodoSkill {
  // 只负责任务管理
}

// ❌ 不好的设计
class AllInOneSkill {
  // 什么都做，难以维护
}
```

### 2. 清晰接口

```javascript
// ✅ 清晰的接口定义
const tool = {
  name: 'getWeather',
  description: '查询指定城市的天气',
  schema: {
    type: 'object',
    properties: {
      city: { type: 'string', description: '城市名' },
    },
    required: ['city'],
  },
};

// ❌ 模糊的接口
const tool = {
  name: 'doSomething',
  description: '做一些事情',
  schema: {},
};
```

### 3. 错误处理

```javascript
// ✅ 完善的错误处理
async function getWeather(city) {
  try {
    const response = await fetch(apiUrl);
    if (!response.ok) {
      throw new Error(`API 错误：${response.status}`);
    }
    return await response.json();
  } catch (error) {
    logger.error('天气查询失败', error);
    throw new Error('天气查询失败，请稍后重试');
  }
}

// ❌ 缺少错误处理
async function getWeather(city) {
  const response = await fetch(apiUrl);
  return await response.json();
}
```

### 4. 日志记录

```javascript
// ✅ 完整的日志
class WeatherSkill {
  async execute(toolName, params) {
    logger.info(`执行工具：${toolName}`, params);
    
    const start = Date.now();
    const result = await this.tools[toolName](params);
    const duration = Date.now() - start;
    
    logger.info(`工具执行完成：${toolName}`, { 
      duration, 
      result 
    });
    
    return result;
  }
}
```

## 📚 下一步

- [03-Skill 规范.md](./03-Skill 规范.md) - 学习 Skill 规范
- [04-环境搭建.md](./04-环境搭建.md) - 配置开发环境

## 🔗 参考资源

- [OpenClaw 架构文档](https://docs.openclaw.ai/architecture)
- [Skill 开发指南](https://docs.openclaw.ai/skills/development)
