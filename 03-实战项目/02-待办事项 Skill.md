# 02 - 待办事项 Skill 实战

## 🎯 项目目标

实现一个待办事项管理 Skill，支持：
- ✅ 创建任务
- ✅ 完成任务
- ✅ 删除任务
- ✅ 查看任务列表
- ✅ 本地存储

## 📁 项目结构

```
todo-skill/
├── SKILL.md
├── index.js
├── package.json
├── src/
│   ├── todo.js         # 任务管理
│   └── storage.js      # 本地存储
└── tests/
    └── todo.test.js
```

## 🚀 完整实现

### Step 1: SKILL.md

```markdown
# 名称
待办事项 Skill

# 描述
管理个人待办事项，支持创建、完成、删除任务

# 版本
1.0.0

# 作者
大龙虾

# 触发词
- 待办
- 任务
- todo
- 提醒

# 工具
## createTodo
- 描述：创建新任务
- 参数:
  - title (string, 必需): 任务标题
  - priority (string, 可选): 优先级 (high/medium/low)
- 返回：任务对象

## completeTodo
- 描述：完成任务
- 参数:
  - id (string, 必需): 任务 ID
- 返回：成功/失败

## listTodos
- 描述：查看任务列表
- 参数:
  - status (string, 可选): 状态 (pending/completed/all)
- 返回：任务列表

# 示例对话
用户：创建一个待办，明天开会
AI: 已创建任务：明天开会

用户：查看我的待办
AI: 你有 3 个待办事项...
```

### Step 2: 本地存储

```javascript
// src/storage.js
import { promises as fs } from 'fs';
import path from 'path';

const DATA_DIR = path.join(process.env.HOME || '.', '.openclaw', 'data');
const TODO_FILE = path.join(DATA_DIR, 'todos.json');

async function ensureDir() {
  await fs.mkdir(DATA_DIR, { recursive: true });
}

async function readData() {
  await ensureDir();
  
  try {
    const data = await fs.readFile(TODO_FILE, 'utf-8');
    return JSON.parse(data);
  } catch {
    return { todos: [], nextId: 1 };
  }
}

async function writeData(data) {
  await ensureDir();
  await fs.writeFile(TODO_FILE, JSON.stringify(data, null, 2));
}

export const storage = {
  async getAll() {
    const data = await readData();
    return data.todos;
  },
  
  async getById(id) {
    const todos = await this.getAll();
    return todos.find(t => t.id === id);
  },
  
  async create(todo) {
    const data = await readData();
    const newTodo = {
      id: String(data.nextId++),
      title: todo.title,
      priority: todo.priority || 'medium',
      status: 'pending',
      createdAt: new Date().toISOString(),
      completedAt: null,
    };
    
    data.todos.push(newTodo);
    await writeData(data);
    
    return newTodo;
  },
  
  async complete(id) {
    const data = await readData();
    const todo = data.todos.find(t => t.id === id);
    
    if (!todo) {
      throw new Error(`任务不存在：${id}`);
    }
    
    todo.status = 'completed';
    todo.completedAt = new Date().toISOString();
    
    await writeData(data);
    return todo;
  },
  
  async delete(id) {
    const data = await readData();
    const index = data.todos.findIndex(t => t.id === id);
    
    if (index === -1) {
      throw new Error(`任务不存在：${id}`);
    }
    
    data.todos.splice(index, 1);
    await writeData(data);
    
    return true;
  },
};
```

### Step 3: 任务管理

```javascript
// src/todo.js
import { storage } from './storage.js';

export async function createTodo(params) {
  const { title, priority } = params;
  
  if (!title || typeof title !== 'string') {
    throw new Error('任务标题不能为空');
  }
  
  if (title.length > 200) {
    throw new Error('任务标题过长');
  }
  
  const validPriorities = ['high', 'medium', 'low'];
  if (priority && !validPriorities.includes(priority)) {
    throw new Error(`优先级必须是：${validPriorities.join('/')}`);
  }
  
  const todo = await storage.create({ title, priority });
  
  return {
    success: true,
    data: {
      message: `已创建任务：${todo.title}`,
      todo,
    },
  };
}

export async function completeTodo(params) {
  const { id } = params;
  
  if (!id) {
    throw new Error('任务 ID 不能为空');
  }
  
  try {
    const todo = await storage.complete(id);
    return {
      success: true,
      data: {
        message: `已完成任务：${todo.title}`,
        todo,
      },
    };
  } catch (error) {
    return {
      success: false,
      error: {
        code: 'TODO_NOT_FOUND',
        message: error.message,
      },
    };
  }
}

export async function listTodos(params) {
  const { status = 'pending' } = params;
  
  let todos = await storage.getAll();
  
  if (status !== 'all') {
    todos = todos.filter(t => t.status === status);
  }
  
  // 按优先级和创建时间排序
  const priorityOrder = { high: 0, medium: 1, low: 2 };
  todos.sort((a, b) => {
    if (a.status !== b.status) {
      return a.status === 'pending' ? -1 : 1;
    }
    if (priorityOrder[a.priority] !== priorityOrder[b.priority]) {
      return priorityOrder[a.priority] - priorityOrder[b.priority];
    }
    return new Date(b.createdAt) - new Date(a.createdAt);
  });
  
  return {
    success: true,
    data: {
      count: todos.length,
      todos: todos.map(t => ({
        id: t.id,
        title: t.title,
        priority: t.priority,
        status: t.status,
        createdAt: t.createdAt,
      })),
    },
  };
}

export async function deleteTodo(params) {
  const { id } = params;
  
  if (!id) {
    throw new Error('任务 ID 不能为空');
  }
  
  try {
    await storage.delete(id);
    return {
      success: true,
      data: {
        message: `已删除任务`,
      },
    };
  } catch (error) {
    return {
      success: false,
      error: {
        code: 'TODO_NOT_FOUND',
        message: error.message,
      },
    };
  }
}
```

### Step 4: 入口文件

```javascript
// index.js
export {
  createTodo,
  completeTodo,
  listTodos,
  deleteTodo,
} from './src/todo.js';

export default {
  tools: {
    createTodo,
    completeTodo,
    listTodos,
    deleteTodo,
  },
};
```

## 📚 下一步

- [03-新闻聚合 Skill.md](./03-新闻聚合 Skill.md) - 新闻聚合技能
