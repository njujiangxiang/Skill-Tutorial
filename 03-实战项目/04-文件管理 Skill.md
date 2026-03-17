# 04 - 文件管理 Skill 实战

## 🎯 项目目标

实现一个文件管理 Skill，支持：
- ✅ 浏览目录
- ✅ 读取文件
- ✅ 搜索文件
- ✅ 文件操作（复制/移动/删除）

## 📁 项目结构

```
file-skill/
├── SKILL.md
├── index.js
├── package.json
├── src/
│   ├── file.js          # 文件操作
│   └── security.js      # 安全检查
└── tests/
    └── file.test.js
```

## 🚀 完整实现

### Step 1: SKILL.md

```markdown
# 名称
文件管理 Skill

# 描述
管理本地文件，支持浏览、读取、搜索等操作

# 版本
1.0.0

# 作者
大龙虾

# 触发词
- 文件
- 目录
- 文件夹
- 读取文件
- 查找文件

# 工具
## listDirectory
- 描述：列出目录内容
- 参数:
  - path (string, 必需): 目录路径
- 返回：文件和目录列表

## readFile
- 描述：读取文件内容
- 参数:
  - path (string, 必需): 文件路径
- 返回：文件内容

## searchFiles
- 描述：搜索文件
- 参数:
  - directory (string, 必需): 搜索目录
  - pattern (string, 必需): 文件名模式
- 返回：匹配的文件列表

## copyFile
- 描述：复制文件
- 参数:
  - from (string, 必需): 源路径
  - to (string, 必需): 目标路径
- 返回：成功/失败

# 安全
- 只允许访问指定目录
- 禁止访问系统文件
- 操作前需要确认

# 示例对话
用户：列出文档目录
AI: 文档目录包含...

用户：读取 readme.md
AI: 文件内容如下...
```

### Step 2: 安全检查

```javascript
// src/security.js
import path from 'path';

// 允许的目录白名单
const ALLOWED_DIRS = (process.env.ALLOWED_DIRS || process.env.HOME || '')
  .split(',')
  .map(d => d.trim())
  .filter(d => d);

/**
 * 检查路径是否安全
 * @param {string} requestedPath - 请求的路径
 * @returns {boolean}
 */
export function isPathSafe(requestedPath) {
  const resolved = path.resolve(requestedPath);
  return ALLOWED_DIRS.some(dir => resolved.startsWith(path.resolve(dir)));
}

/**
 * 验证路径
 * @param {string} requestedPath 
 * @returns {string} 解析后的绝对路径
 */
export function validatePath(requestedPath) {
  if (!isPathSafe(requestedPath)) {
    throw new Error(`访问被拒绝：${requestedPath}`);
  }
  return path.resolve(requestedPath);
}

/**
 * 防止路径遍历攻击
 * @param {string} inputPath 
 * @returns {string}
 */
export function sanitizePath(inputPath) {
  return path.normalize(inputPath).replace(/\.\./g, '');
}
```

### Step 3: 文件操作

```javascript
// src/file.js
import * as fs from 'fs/promises';
import * as path from 'path';
import { validatePath, isPathSafe } from './security.js';

/**
 * 列出目录内容
 */
export async function listDirectory(params) {
  const { path: dirPath } = params;

  try {
    const safePath = validatePath(dirPath);
    const entries = await fs.readdir(safePath, { withFileTypes: true });

    const files = [];
    const directories = [];

    for (const entry of entries) {
      // 跳过隐藏文件
      if (entry.name.startsWith('.')) continue;

      const item = {
        name: entry.name,
        path: path.join(safePath, entry.name),
        type: entry.isDirectory() ? 'directory' : 'file',
      };

      if (entry.isFile()) {
        item.size = (await fs.stat(item.path)).size;
        files.push(item);
      } else {
        directories.push(item);
      }
    }

    return {
      success: true,
      data: {
        path: safePath,
        directories,
        files,
        total: directories.length + files.length,
      },
    };
  } catch (error) {
    return {
      success: false,
      error: {
        code: 'LIST_DIR_ERROR',
        message: error.message,
      },
    };
  }
}

/**
 * 读取文件
 */
export async function readFile(params) {
  const { path: filePath } = params;

  try {
    const safePath = validatePath(filePath);

    // 检查文件是否存在
    await fs.access(safePath);

    // 检查是否是文本文件
    const ext = path.extname(safePath).toLowerCase();
    const textExtensions = ['.txt', '.md', '.json', '.js', '.ts', '.html', '.css'];
    
    if (!textExtensions.includes(ext)) {
      return {
        success: false,
        error: {
          code: 'UNSUPPORTED_FORMAT',
          message: `不支持的文件格式：${ext}`,
        },
      };
    }

    const content = await fs.readFile(safePath, 'utf-8');
    const stats = await fs.stat(safePath);

    return {
      success: true,
      data: {
        path: safePath,
        name: path.basename(safePath),
        size: stats.size,
        content,
        lines: content.split('\n').length,
      },
    };
  } catch (error) {
    return {
      success: false,
      error: {
        code: 'READ_FILE_ERROR',
        message: error.message,
      },
    };
  }
}

/**
 * 搜索文件
 */
export async function searchFiles(params) {
  const { directory, pattern } = params;

  try {
    const safeDir = validatePath(directory);
    const results = [];

    async function scanDir(dir) {
      const entries = await fs.readdir(dir, { withFileTypes: true });

      for (const entry of entries) {
        if (entry.name.startsWith('.')) continue;

        const fullPath = path.join(dir, entry.name);

        // 检查是否匹配
        if (entry.name.includes(pattern.replace('*', ''))) {
          results.push({
            name: entry.name,
            path: fullPath,
            type: entry.isDirectory() ? 'directory' : 'file',
          });
        }

        // 递归搜索子目录
        if (entry.isDirectory()) {
          await scanDir(fullPath);
        }
      }
    }

    await scanDir(safeDir);

    return {
      success: true,
      data: {
        directory: safeDir,
        pattern,
        count: results.length,
        results,
      },
    };
  } catch (error) {
    return {
      success: false,
      error: {
        code: 'SEARCH_ERROR',
        message: error.message,
      },
    };
  }
}

/**
 * 复制文件
 */
export async function copyFile(params) {
  const { from, to } = params;

  try {
    // 验证源路径和目标路径都在允许的目录内
    if (!isPathSafe(from) || !isPathSafe(to)) {
      throw new Error('操作被拒绝：路径不在允许的目录内');
    }

    const safeFrom = path.resolve(from);
    const safeTo = path.resolve(to);

    // 确保目标目录存在
    await fs.mkdir(path.dirname(safeTo), { recursive: true });

    // 复制文件
    await fs.copyFile(safeFrom, safeTo);

    return {
      success: true,
      data: {
        message: `文件已从 ${from} 复制到 ${to}`,
      },
    };
  } catch (error) {
    return {
      success: false,
      error: {
        code: 'COPY_FILE_ERROR',
        message: error.message,
      },
    };
  }
}

/**
 * 移动文件
 */
export async function moveFile(params) {
  const { from, to } = params;

  try {
    if (!isPathSafe(from) || !isPathSafe(to)) {
      throw new Error('操作被拒绝');
    }

    const safeFrom = path.resolve(from);
    const safeTo = path.resolve(to);

    await fs.mkdir(path.dirname(safeTo), { recursive: true });
    await fs.rename(safeFrom, safeTo);

    return {
      success: true,
      data: {
        message: `文件已从 ${from} 移动到 ${to}`,
      },
    };
  } catch (error) {
    return {
      success: false,
      error: {
        code: 'MOVE_FILE_ERROR',
        message: error.message,
      },
    };
  }
}

/**
 * 删除文件
 */
export async function deleteFile(params) {
  const { path: filePath } = params;

  try {
    if (!isPathSafe(filePath)) {
      throw new Error('操作被拒绝');
    }

    const safePath = path.resolve(filePath);

    // 防止删除根目录
    if (safePath === path.resolve('/') || safePath.match(/^[A-Z]:\\/i)) {
      throw new Error('不允许删除根目录');
    }

    await fs.unlink(safePath);

    return {
      success: true,
      data: {
        message: `文件已删除：${filePath}`,
      },
    };
  } catch (error) {
    return {
      success: false,
      error: {
        code: 'DELETE_FILE_ERROR',
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
  listDirectory,
  readFile,
  searchFiles,
  copyFile,
  moveFile,
  deleteFile,
} from './src/file.js';

export default {
  tools: {
    listDirectory,
    readFile,
    searchFiles,
    copyFile,
    moveFile,
    deleteFile,
  },
};
```

## 📚 下一步

- [05-智能助手 Skill.md](./05-智能助手 Skill.md) - 综合助手技能
