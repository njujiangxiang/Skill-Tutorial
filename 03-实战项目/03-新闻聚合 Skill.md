# 03 - 新闻聚合 Skill 实战

## 🎯 项目目标

实现一个新闻聚合 Skill，支持：
- ✅ 多来源新闻聚合
- ✅ 分类浏览
- ✅ 关键词搜索
- ✅ 个性化推荐

## 📁 项目结构

```
news-skill/
├── SKILL.md
├── index.js
├── package.json
├── src/
│   ├── news.js          # 新闻获取
│   ├── sources.js       # 新闻源管理
│   └── filter.js        # 新闻过滤
└── tests/
    └── news.test.js
```

## 🚀 完整实现

### Step 1: SKILL.md

```markdown
# 名称
新闻聚合 Skill

# 描述
聚合多个新闻源，提供分类浏览和搜索功能

# 版本
1.0.0

# 作者
大龙虾

# 触发词
- 新闻
- 头条
- 资讯
- 科技新闻
- 行业新闻

# 工具
## getNews
- 描述：获取新闻列表
- 参数:
  - category (string, 可选): 分类
  - limit (number, 可选): 数量，默认 10
- 返回：新闻列表

## searchNews
- 描述：搜索新闻
- 参数:
  - keyword (string, 必需): 关键词
  - limit (number, 可选): 数量
- 返回：相关新闻

## getSources
- 描述：获取新闻源列表
- 参数：无
- 返回：新闻源列表

# 示例对话
用户：看看今天的新闻
AI: 这是今天的热门新闻...

用户：科技新闻
AI: 科技类新闻...

用户：搜索 AI 相关新闻
AI: 找到 10 篇关于 AI 的新闻...
```

### Step 2: 新闻获取

```javascript
// src/news.js
import fetch from 'node-fetch';

// 新闻源配置
const NEWS_SOURCES = [
  {
    name: '科技日报',
    url: 'https://api.example.com/tech',
    category: 'technology',
  },
  {
    name: '财经新闻',
    url: 'https://api.example.com/finance',
    category: 'finance',
  },
  {
    name: '体育新闻',
    url: 'https://api.example.com/sports',
    category: 'sports',
  },
];

/**
 * 获取新闻
 * @param {Object} params
 * @param {string} params.category - 分类
 * @param {number} params.limit - 数量
 */
export async function getNews(params) {
  const { category, limit = 10 } = params;

  try {
    // 获取指定分类的新闻源
    const sources = category
      ? NEWS_SOURCES.filter(s => s.category === category)
      : NEWS_SOURCES;

    // 并行获取多个新闻源的新闻
    const newsPromises = sources.map(source =>
      fetchNewsFromSource(source, limit)
    );

    const results = await Promise.allSettled(newsPromises);

    // 合并所有新闻
    let allNews = [];
    for (const result of results) {
      if (result.status === 'fulfilled') {
        allNews = allNews.concat(result.value);
      } else {
        console.error('获取新闻失败:', result.reason);
      }
    }

    // 按时间排序
    allNews.sort((a, b) => new Date(b.publishedAt) - new Date(a.publishedAt));

    // 限制数量
    allNews = allNews.slice(0, limit);

    return {
      success: true,
      data: {
        count: allNews.length,
        news: allNews,
      },
    };
  } catch (error) {
    return {
      success: false,
      error: {
        code: 'NEWS_API_ERROR',
        message: error.message,
      },
    };
  }
}

async function fetchNewsFromSource(source, limit) {
  const response = await fetch(source.url);
  
  if (!response.ok) {
    throw new Error(`${source.name} API 错误`);
  }

  const data = await response.json();

  return data.articles.map(article => ({
    ...article,
    source: source.name,
    category: source.category,
  }));
}

/**
 * 搜索新闻
 * @param {Object} params
 * @param {string} params.keyword - 关键词
 * @param {number} params.limit - 数量
 */
export async function searchNews(params) {
  const { keyword, limit = 10 } = params;

  if (!keyword || keyword.trim().length === 0) {
    throw new Error('搜索关键词不能为空');
  }

  try {
    // 获取所有新闻
    const allNewsResult = await getNews({ limit: 100 });
    
    if (!allNewsResult.success) {
      throw new Error('获取新闻失败');
    }

    // 过滤相关新闻
    const filtered = allNewsResult.data.news.filter(news =>
      news.title.toLowerCase().includes(keyword.toLowerCase()) ||
      news.description?.toLowerCase().includes(keyword.toLowerCase())
    );

    return {
      success: true,
      data: {
        count: filtered.length,
        keyword,
        news: filtered.slice(0, limit),
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
 * 获取新闻源列表
 */
export async function getSources() {
  return {
    success: true,
    data: {
      sources: NEWS_SOURCES.map(s => ({
        name: s.name,
        category: s.category,
        url: s.url,
      })),
    },
  };
}
```

### Step 3: 入口文件

```javascript
// index.js
export { getNews, searchNews, getSources } from './src/news.js';

export default {
  tools: {
    getNews,
    searchNews,
    getSources,
  },
};
```

## 📚 下一步

- [04-文件管理 Skill.md](./04-文件管理 Skill.md) - 文件操作技能
