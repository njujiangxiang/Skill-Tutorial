# 01 - 天气查询 Skill 实战

## 🎯 项目目标

实现一个完整的天气查询 Skill，支持：
- ✅ 查询当前天气
- ✅ 查询天气预报
- ✅ 多城市支持
- ✅ 数据缓存
- ✅ 错误处理

## 📁 项目结构

```
weather-skill/
├── SKILL.md
├── index.js
├── package.json
├── README.md
├── src/
│   ├── weather.js       # 天气查询
│   ├── formatter.js     # 结果格式化
│   └── cache.js         # 缓存工具
└── tests/
    └── weather.test.js
```

## 🚀 完整实现

### Step 1: 创建 SKILL.md

```markdown
# 名称
天气查询 Skill

# 描述
查询全球城市天气信息，支持当前天气和 7 天预报

# 版本
1.0.0

# 作者
大龙虾

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
- 返回：当前天气信息

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
## WEATHER_API_KEY
- 描述：天气 API 密钥
- 必需：是
- 获取：https://weatherapi.com

# 示例对话
用户：北京天气怎么样？
AI: 北京今天晴，气温 25°C，空气质量良好。

用户：上海未来 3 天天气
AI: 上海未来 3 天天气预报...
```

### Step 2: 实现天气查询

```javascript
// src/weather.js
import fetch from 'node-fetch';

const API_KEY = process.env.WEATHER_API_KEY;
const BASE_URL = 'https://api.weatherapi.com/v1';

/**
 * 查询当前天气
 * @param {Object} params 
 * @param {string} params.city - 城市名
 */
export async function getWeather(params) {
  const { city } = params;
  
  // 参数验证
  if (!city || typeof city !== 'string') {
    throw new Error('城市名不能为空');
  }
  
  try {
    const url = `${BASE_URL}/current.json?key=${API_KEY}&q=${encodeURIComponent(city)}`;
    const response = await fetch(url);
    
    if (!response.ok) {
      throw new Error(`天气 API 错误：${response.status}`);
    }
    
    const data = await response.json();
    
    return {
      success: true,
      data: formatCurrentWeather(data),
    };
  } catch (error) {
    return {
      success: false,
      error: {
        code: 'WEATHER_API_ERROR',
        message: error.message,
      },
    };
  }
}

/**
 * 查询天气预报
 * @param {Object} params
 * @param {string} params.city - 城市名
 * @param {number} params.days - 天数
 */
export async function getForecast(params) {
  const { city, days = 7 } = params;
  
  if (!city) {
    throw new Error('城市名不能为空');
  }
  
  if (days < 1 || days > 10) {
    throw new Error('天数必须在 1-10 之间');
  }
  
  try {
    const url = `${BASE_URL}/forecast.json?key=${API_KEY}&q=${encodeURIComponent(city)}&days=${days}`;
    const response = await fetch(url);
    
    if (!response.ok) {
      throw new Error(`天气 API 错误：${response.status}`);
    }
    
    const data = await response.json();
    
    return {
      success: true,
      data: formatForecast(data),
    };
  } catch (error) {
    return {
      success: false,
      error: {
        code: 'FORECAST_API_ERROR',
        message: error.message,
      },
    };
  }
}

function formatCurrentWeather(data) {
  return {
    city: data.location.name,
    country: data.location.country,
    temperature: Math.round(data.current.temp_c),
    condition: data.current.condition.text,
    humidity: data.current.humidity,
    windSpeed: data.current.wind_kph,
    feelsLike: Math.round(data.current.feelslike_c),
    updateTime: data.location.localtime,
  };
}

function formatForecast(data) {
  return {
    city: data.location.name,
    forecasts: data.forecast.forecastday.map(day => ({
      date: day.date,
      maxTemp: Math.round(day.day.maxtemp_c),
      minTemp: Math.round(day.day.mintemp_c),
      condition: day.day.condition.text,
      chanceOfRain: day.day.daily_chance_of_rain,
      avgHumidity: day.day.avghumidity,
    })),
  };
}
```

### Step 3: 实现缓存

```javascript
// src/cache.js
class Cache {
  constructor(ttl = 300000) { // 5 分钟
    this.cache = new Map();
    this.ttl = ttl;
  }
  
  async get(key) {
    const item = this.cache.get(key);
    if (!item) return null;
    
    if (Date.now() > item.expiry) {
      this.cache.delete(key);
      return null;
    }
    
    return item.data;
  }
  
  async set(key, data) {
    this.cache.set(key, {
      data,
      expiry: Date.now() + this.ttl,
    });
  }
}

export const weatherCache = new Cache();
```

### Step 4: 入口文件

```javascript
// index.js
import { getWeather, getForecast } from './src/weather.js';
import { weatherCache } from './src/cache.js';

// 带缓存的天气查询
async function getCachedWeather(params) {
  const cacheKey = `weather:${params.city}`;
  
  let data = await weatherCache.get(cacheKey);
  if (data) {
    return { ...data, fromCache: true };
  }
  
  data = await getWeather(params);
  await weatherCache.set(cacheKey, data);
  
  return { ...data, fromCache: false };
}

// 带缓存的天气预报
async function getCachedForecast(params) {
  const cacheKey = `forecast:${params.city}:${params.days || 7}`;
  
  let data = await weatherCache.get(cacheKey);
  if (data) {
    return { ...data, fromCache: true };
  }
  
  data = await getForecast(params);
  await weatherCache.set(cacheKey, data);
  
  return { ...data, fromCache: false };
}

// 导出工具
export default {
  tools: {
    getWeather: getCachedWeather,
    getForecast: getCachedForecast,
  },
};
```

### Step 5: package.json

```json
{
  "name": "weather-skill",
  "version": "1.0.0",
  "description": "天气查询 Skill",
  "type": "module",
  "main": "index.js",
  "scripts": {
    "test": "node --experimental-vm-modules node_modules/jest/bin/jest.js"
  },
  "dependencies": {
    "node-fetch": "^3.3.0"
  },
  "devDependencies": {
    "jest": "^29.0.0"
  }
}
```

## 🧪 测试

```javascript
// tests/weather.test.js
import { getWeather } from '../index.js';

global.fetch = jest.fn();

describe('天气查询', () => {
  beforeEach(() => {
    fetch.mockClear();
  });
  
  test('应该返回天气数据', async () => {
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        location: { name: '北京', country: '中国' },
        current: { temp_c: 25, condition: { text: '晴' }, humidity: 60 },
      }),
    });
    
    const result = await getWeather({ city: '北京' });
    
    expect(result.success).toBe(true);
    expect(result.data.city).toBe('北京');
    expect(result.data.temperature).toBe(25);
  });
  
  test('应该处理错误', async () => {
    fetch.mockResolvedValueOnce({
      ok: false,
      status: 404,
    });
    
    const result = await getWeather({ city: '北京' });
    
    expect(result.success).toBe(false);
  });
});
```

## 📚 下一步

- [02-待办事项 Skill.md](./02-待办事项 Skill.md) - 任务管理技能
