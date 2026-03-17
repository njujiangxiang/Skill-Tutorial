# 05 - 智能助手 Skill 实战

## 🎯 项目目标

实现一个综合智能助手 Skill，整合多个功能：
- ✅ 天气查询
- ✅ 待办管理
- ✅ 新闻浏览
- ✅ 日程提醒
- ✅ 智能对话

## 📁 项目结构

```
assistant-skill/
├── SKILL.md
├── index.js
├── package.json
├── src/
│   ├── assistant.js     # 主逻辑
│   ├── weather.js       # 天气模块
│   ├── todo.js          # 待办模块
│   ├── news.js          # 新闻模块
│   └── dialog.js        # 对话模块
└── tests/
    └── assistant.test.js
```

## 🚀 完整实现

### Step 1: SKILL.md

```markdown
# 名称
智能助手 Skill

# 描述
综合智能助手，集成天气、待办、新闻等多种功能

# 版本
1.0.0

# 作者
大龙虾

# 触发词
- 助手
- 帮忙
- 提醒我
- 今天怎么样

# 功能模块
## 天气
- 查询当前天气
- 查询天气预报

## 待办
- 创建任务
- 查看任务
- 完成任务

## 新闻
- 浏览新闻
- 搜索新闻

## 提醒
- 设置提醒
- 查看提醒

# 示例对话
用户：今天怎么样？
AI: 今天北京晴，25°C。你有 3 个待办事项...

用户：提醒我明天开会
AI: 好的，已设置明天上午 9 点的会议提醒
```

### Step 2: 智能路由

```javascript
// src/assistant.js
import { getWeather } from './weather.js';
import { createTodo, listTodos } from './todo.js';
import { getNews } from './news.js';
import { DialogManager } from './dialog.js';

class Assistant {
  constructor() {
    this.dialogManager = new DialogManager();
  }

  /**
   * 处理用户请求
   */
  async process(userId, input) {
    // 意图识别
    const intent = this.recognizeIntent(input);

    if (!intent) {
      return {
        message: '抱歉，我没有理解。您能再说一遍吗？',
      };
    }

    // 根据意图路由到不同模块
    switch (intent.name) {
      case 'weather_query':
        return await this.handleWeather(userId, input, intent);

      case 'todo_create':
        return await this.handleTodoCreate(userId, input, intent);

      case 'todo_list':
        return await this.handleTodoList(userId, input, intent);

      case 'news_browse':
        return await this.handleNews(userId, input, intent);

      case 'reminder_set':
        return await this.handleReminder(userId, input, intent);

      case 'greeting':
        return await this.handleGreeting(userId, input);

      default:
        return {
          message: '我还在学习这个功能，您能换个说法吗？',
        };
    }
  }

  /**
   * 意图识别
   */
  recognizeIntent(input) {
    const patterns = [
      {
        name: 'weather_query',
        patterns: [/(.*) 天气 (.*)/, /(.*) 气温 (.*)/, /(.*) 下雨 (.*)/],
      },
      {
        name: 'todo_create',
        patterns: [/创建 (.*) 待办/, /添加 (.*) 任务/, /提醒我 (.*)/],
      },
      {
        name: 'todo_list',
        patterns: [/我的待办/, /查看任务/, /有什么要做的/],
      },
      {
        name: 'news_browse',
        patterns: [/看看新闻/, /有什么新闻/, /头条/],
      },
      {
        name: 'reminder_set',
        patterns: [/提醒我 (.*)/, /设置提醒 (.*)/, /明天 (.*)/],
      },
      {
        name: 'greeting',
        patterns: [/你好/, /早上好/, /下午好/, /晚上好/],
      },
    ];

    for (const intent of patterns) {
      for (const pattern of intent.patterns) {
        const match = input.match(pattern);
        if (match) {
          return {
            name: intent.name,
            match,
          };
        }
      }
    }

    return null;
  }

  /**
   * 处理天气查询
   */
  async handleWeather(userId, input, intent) {
    // 提取城市
    const cityMatch = input.match(/(.*) 天气/);
    const city = cityMatch ? cityMatch[1] : '北京';

    const result = await getWeather({ city });

    if (result.success) {
      const data = result.data;
      return {
        message: `${data.city}今天${data.condition}，气温${data.temperature}°C，湿度${data.humidity}%。`,
      };
    } else {
      return {
        message: '抱歉，天气查询失败，请稍后再试。',
      };
    }
  }

  /**
   * 处理创建待办
   */
  async handleTodoCreate(userId, input, intent) {
    // 提取任务内容
    const taskMatch = input.match(/创建 (.*) 待办/) || 
                      input.match(/添加 (.*) 任务/) ||
                      input.match(/提醒我 (.*)/);
    
    if (!taskMatch) {
      return {
        message: '您想创建什么任务呢？',
      };
    }

    const title = taskMatch[1];
    const result = await createTodo({ title });

    if (result.success) {
      return {
        message: `好的，已创建任务：${title}`,
      };
    } else {
      return {
        message: '抱歉，任务创建失败。',
      };
    }
  }

  /**
   * 处理查看待办
   */
  async handleTodoList(userId, input, intent) {
    const result = await listTodos({ status: 'pending' });

    if (result.success && result.data.todos.length > 0) {
      const todos = result.data.todos;
      let message = `您有${todos.length}个待办事项：\n`;
      
      todos.forEach((todo, i) => {
        message += `${i + 1}. ${todo.title}\n`;
      });

      return { message };
    } else {
      return {
        message: '您目前没有待办事项。',
      };
    }
  }

  /**
   * 处理新闻浏览
   */
  async handleNews(userId, input, intent) {
    const result = await getNews({ limit: 5 });

    if (result.success) {
      let message = '热门新闻：\n';
      
      result.data.news.forEach((news, i) => {
        message += `${i + 1}. ${news.title}\n`;
      });

      return { message };
    } else {
      return {
        message: '抱歉，新闻获取失败。',
      };
    }
  }

  /**
   * 处理提醒设置
   */
  async handleReminder(userId, input, intent) {
    // 提取提醒内容
    const reminderMatch = input.match(/提醒我 (.*)/);
    
    if (!reminderMatch) {
      return {
        message: '您想设置什么提醒呢？',
      };
    }

    const content = reminderMatch[1];
    
    // 创建待办作为提醒
    const result = await createTodo({ 
      title: `提醒：${content}`,
      priority: 'high',
    });

    if (result.success) {
      return {
        message: `好的，已设置提醒：${content}`,
      };
    } else {
      return {
        message: '抱歉，提醒设置失败。',
      };
    }
  }

  /**
   * 处理问候
   */
  async handleGreeting(userId, input) {
    const hour = new Date().getHours();
    let greeting = '你好！';

    if (hour >= 5 && hour < 12) {
      greeting = '早上好！';
    } else if (hour >= 12 && hour < 18) {
      greeting = '下午好！';
    } else if (hour >= 18 && hour < 23) {
      greeting = '晚上好！';
    } else {
      greeting = '夜深了，早点休息吧！';
    }

    // 获取天气和待办作为补充信息
    try {
      const weather = await getWeather({ city: '北京' });
      const todos = await listTodos({ status: 'pending' });

      let message = `${greeting}`;
      
      if (weather.success) {
        message += ` 北京今天${weather.data.condition}，${weather.data.temperature}°C。`;
      }

      if (todos.success && todos.data.todos.length > 0) {
        message += ` 您有${todos.data.todos.length}个待办事项。`;
      }

      return { message };
    } catch {
      return { message: greeting };
    }
  }
}

export const assistant = new Assistant();
```

### Step 3: 入口文件

```javascript
// index.js
import { assistant } from './src/assistant.js';

export default {
  async process(userId, input) {
    return await assistant.process(userId, input);
  },
};
```

## 🎉 教程完成

恭喜你完成所有实战项目！现在你已经掌握了：
- ✅ 天气查询 Skill
- ✅ 待办事项 Skill
- ✅ 新闻聚合 Skill
- ✅ 文件管理 Skill
- ✅ 智能助手 Skill

可以开始创建自己的 Skill 了！
