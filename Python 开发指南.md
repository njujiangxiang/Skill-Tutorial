# Python Skill 开发指南

## 🐍 为什么选择 Python？

### 优势

- ✅ **语法简洁**: 代码易读易写
- ✅ **生态丰富**: 大量第三方库
- ✅ **异步支持**: asyncio 原生支持
- ✅ **数据科学**: 强大的数据处理能力
- ✅ **快速原型**: 开发效率高

### 适用场景

- API 集成
- 数据处理
- 机器学习
- 自动化脚本
- 快速原型开发

## 📦 环境搭建

### 1. 安装 Python

```bash
# macOS
brew install python@3.9

# Ubuntu/Debian
sudo apt install python3.9 python3-pip

# Windows
# 下载安装包：https://www.python.org/downloads/
```

### 2. 创建虚拟环境

```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
# macOS/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. 安装依赖

```bash
# 安装项目依赖
pip install -r requirements.txt

# 安装开发依赖
pip install -r requirements-dev.txt
```

### 4. 常用依赖

```txt
# HTTP 客户端
httpx>=0.24.0
requests>=2.28.0

# 环境变量
python-dotenv>=1.0.0

# 数据处理
pydantic>=1.10.0

# 测试
pytest>=7.0.0
pytest-asyncio>=0.21.0

# 代码质量
black>=23.0.0
flake8>=6.0.0
mypy>=1.0.0
```

## 🔧 开发规范

### 1. 代码风格

```python
# ✅ 好的代码风格
def get_weather(city: str) -> Dict[str, Any]:
    """查询天气"""
    if not city:
        raise ValueError('城市名不能为空')
    
    result = await fetch_weather(city)
    return format_result(result)

# ❌ 不好的代码风格
def getWeather(c):
    if not c: raise Exception('error')
    r=fetch(c)
    return r
```

### 2. 类型注解

```python
from typing import Dict, Any, Optional, List

# 函数签名
async def get_weather(
    city: str,
    days: Optional[int] = 7
) -> Dict[str, Any]:
    pass

# 类属性
class WeatherSkill:
    api_key: str
    cache: Dict[str, Any]
    
    def __init__(self) -> None:
        self.api_key = ''
        self.cache = {}
```

### 3. 错误处理

```python
# ✅ 完善的错误处理
async def get_weather(city: str) -> Dict[str, Any]:
    try:
        # 参数验证
        if not city:
            raise ValueError('城市名不能为空')
        
        # API 调用
        response = await client.get(url)
        response.raise_for_status()
        
        # 处理结果
        data = response.json()
        return {'success': True, 'data': data}
        
    except httpx.HTTPStatusError as e:
        return {
            'success': False,
            'error': {
                'code': 'API_ERROR',
                'message': f'API 请求失败：{e.response.status_code}'
            }
        }
    except Exception as e:
        logger.exception('天气查询失败')
        return {
            'success': False,
            'error': {
                'code': 'UNKNOWN_ERROR',
                'message': '服务暂时不可用'
            }
        }
```

### 4. 日志记录

```python
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# 使用日志
async def get_weather(city: str):
    logger.info(f'开始查询天气：{city}')
    
    try:
        result = await fetch(city)
        logger.info(f'天气查询成功：{city}')
        return result
    except Exception as e:
        logger.error(f'天气查询失败：{city}', exc_info=True)
        raise
```

## 🧪 测试

### 1. 单元测试

```python
# tests/test_weather.py
import pytest
from skill import get_weather

@pytest.mark.asyncio
async def test_get_weather():
    """测试天气查询"""
    params = {'city': '北京'}
    result = await get_weather(params)
    
    assert result['success'] is True
    assert 'data' in result
    assert result['data']['city'] == '北京'

@pytest.mark.asyncio
async def test_missing_city():
    """测试缺少城市参数"""
    with pytest.raises(ValueError):
        await get_weather({})
```

### 2. 运行测试

```bash
# 安装测试依赖
pip install pytest pytest-asyncio

# 运行所有测试
pytest tests/ -v

# 运行特定测试
pytest tests/test_weather.py::test_get_weather -v

# 生成覆盖率报告
pytest tests/ --cov=skill --cov-report=html
```

### 3. Mock 测试

```python
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_with_mock():
    """使用 Mock 测试"""
    mock_data = {'location': {'name': '北京'}}
    
    with patch('skill.httpx.AsyncClient.get') as mock_get:
        mock_get.return_value = AsyncMock(
            status_code=200,
            json=AsyncMock(return_value=mock_data)
        )
        
        result = await get_weather({'city': '北京'})
        
        assert result['success'] is True
```

## 📊 性能优化

### 1. 异步并发

```python
# ❌ 串行执行
async def get_all_weather(cities):
    results = []
    for city in cities:
        result = await get_weather(city)
        results.append(result)
    return results

# ✅ 并行执行
async def get_all_weather(cities):
    tasks = [get_weather(city) for city in cities]
    results = await asyncio.gather(*tasks)
    return results
```

### 2. 缓存

```python
from functools import lru_cache
import hashlib

class WeatherSkill:
    def __init__(self):
        self.cache = {}
        self.cache_ttl = 300
    
    def _get_cache_key(self, city: str) -> str:
        return f'weather:{city}'
    
    async def get_weather(self, city: str):
        cache_key = self._get_cache_key(city)
        
        # 检查缓存
        if cache_key in self.cache:
            cached = self.cache[cache_key]
            if time.time() < cached['expires']:
                return cached['data']
        
        # 获取新数据
        data = await self._fetch(city)
        
        # 存入缓存
        self.cache[cache_key] = {
            'data': data,
            'expires': time.time() + self.cache_ttl
        }
        
        return data
```

### 3. 连接池

```python
import httpx

class WeatherSkill:
    def __init__(self):
        # 创建连接池
        self.client = httpx.AsyncClient(
            limits=httpx.Limits(
                max_connections=100,
                max_keepalive_connections=20
            ),
            timeout=httpx.Timeout(10.0)
        )
    
    async def close(self):
        await self.client.aclose()
    
    async def get_weather(self, city: str):
        response = await self.client.get(url)
        return response.json()
```

## 🚀 部署

### 1. 打包

```bash
# 安装打包工具
pip install setuptools wheel

# 打包
python setup.py sdist bdist_wheel
```

### 2. 发布到 PyPI (可选)

```bash
# 安装 twine
pip install twine

# 发布
twine upload dist/*
```

### 3. Docker 部署

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "skill.py"]
```

## 📚 参考资源

- [Python 官方文档](https://docs.python.org/zh-cn/3/)
- [httpx 文档](https://www.python-httpx.org/)
- [pytest 文档](https://docs.pytest.org/)
- [异步编程](https://docs.python.org/zh-cn/3/library/asyncio.html)

---

**维护**: 大龙虾 🦞  
**更新**: 2026-03-17
