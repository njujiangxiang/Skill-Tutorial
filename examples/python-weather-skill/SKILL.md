# 名称
天气查询 Skill (Python 版)

# 描述
查询全球城市天气信息，支持当前天气和 7 天预报

# 版本
1.0.0

# 作者
大龙虾

# 语言
Python 3.9+

# 触发词
- 天气
- 气温
- 天气预报
- 下雨
- 温度

# 工具
## get_weather
- 描述：查询城市当前天气
- 参数:
  - city (string, 必需): 城市名称
- 返回：当前天气信息

## get_forecast
- 描述：查询天气预报
- 参数:
  - city (string, 必需): 城市名称
  - days (number, 可选): 天数，默认 7 天
- 返回：天气预报列表

## search_city
- 描述：搜索城市
- 参数:
  - query (string, 必需): 搜索关键词
- 返回：城市列表

# 依赖
- httpx >= 0.24.0
- python-dotenv >= 1.0.0

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

# 许可证
MIT
