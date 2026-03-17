#!/usr/bin/env python3
"""
天气查询 Skill - Python 版本
查询全球城市天气信息，支持当前天气和预报
"""

import os
import json
import asyncio
from datetime import datetime
from typing import Dict, Any, Optional, List
import httpx


class WeatherSkill:
    """天气查询 Skill"""
    
    def __init__(self):
        self.api_key = os.getenv('WEATHER_API_KEY', '')
        self.base_url = 'https://api.weatherapi.com/v1'
        self.cache = {}
        self.cache_ttl = 300  # 5 分钟缓存
    
    async def get_weather(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        查询当前天气
        
        Args:
            params: 参数对象
                - city: 城市名称 (必需)
        
        Returns:
            天气信息
        """
        city = params.get('city')
        
        # 参数验证
        if not city or not isinstance(city, str):
            raise ValueError('城市名不能为空')
        
        if len(city) > 100:
            raise ValueError('城市名过长')
        
        # 检查缓存
        cache_key = f'weather:{city}'
        if cache_key in self.cache:
            cached = self.cache[cache_key]
            if datetime.now().timestamp() < cached['expires']:
                cached['data']['fromCache'] = True
                return {
                    'success': True,
                    'data': cached['data']
                }
        
        try:
            # 调用天气 API
            url = f'{self.base_url}/current.json'
            query_params = {
                'key': self.api_key,
                'q': city
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=query_params, timeout=10.0)
                
                if response.status_code != 200:
                    raise Exception(f'天气 API 错误：{response.status_code}')
                
                data = response.json()
            
            # 格式化结果
            result = self._format_current_weather(data)
            
            # 存入缓存
            self.cache[cache_key] = {
                'data': result,
                'expires': datetime.now().timestamp() + self.cache_ttl
            }
            
            return {
                'success': True,
                'data': result
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': {
                    'code': 'WEATHER_API_ERROR',
                    'message': str(e)
                }
            }
    
    async def get_forecast(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        查询天气预报
        
        Args:
            params: 参数对象
                - city: 城市名称 (必需)
                - days: 天数 (可选，默认 7 天)
        
        Returns:
            天气预报列表
        """
        city = params.get('city')
        days = params.get('days', 7)
        
        # 参数验证
        if not city:
            raise ValueError('城市名不能为空')
        
        if not isinstance(days, int) or days < 1 or days > 10:
            raise ValueError('天数必须在 1-10 之间')
        
        try:
            # 调用天气预报 API
            url = f'{self.base_url}/forecast.json'
            query_params = {
                'key': self.api_key,
                'q': city,
                'days': days
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=query_params, timeout=10.0)
                
                if response.status_code != 200:
                    raise Exception(f'天气 API 错误：{response.status_code}')
                
                data = response.json()
            
            # 格式化结果
            result = self._format_forecast(data)
            
            return {
                'success': True,
                'data': result
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': {
                    'code': 'FORECAST_API_ERROR',
                    'message': str(e)
                }
            }
    
    def _format_current_weather(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """格式化当前天气数据"""
        return {
            'city': data['location']['name'],
            'country': data['location']['country'],
            'temperature': round(data['current']['temp_c']),
            'condition': data['current']['condition']['text'],
            'humidity': data['current']['humidity'],
            'windSpeed': data['current']['wind_kph'],
            'feelsLike': round(data['current']['feelslike_c']),
            'updateTime': data['location']['localtime'],
        }
    
    def _format_forecast(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """格式化天气预报数据"""
        return {
            'city': data['location']['name'],
            'forecasts': [
                {
                    'date': day['date'],
                    'maxTemp': round(day['day']['maxtemp_c']),
                    'minTemp': round(day['day']['mintemp_c']),
                    'condition': day['day']['condition']['text'],
                    'chanceOfRain': day['day']['daily_chance_of_rain'],
                    'avgHumidity': day['day']['avghumidity'],
                }
                for day in data['forecast']['forecastday']
            ]
        }
    
    async def search_city(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        搜索城市
        
        Args:
            params: 参数对象
                - query: 搜索关键词 (必需)
        
        Returns:
            城市列表
        """
        query = params.get('query')
        
        if not query:
            raise ValueError('搜索关键词不能为空')
        
        try:
            url = f'{self.base_url}/search.json'
            query_params = {
                'key': self.api_key,
                'q': query
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=query_params, timeout=10.0)
                
                if response.status_code != 200:
                    raise Exception(f'搜索 API 错误：{response.status_code}')
                
                cities = response.json()
            
            return {
                'success': True,
                'data': {
                    'count': len(cities),
                    'cities': [
                        {
                            'name': city['name'],
                            'region': city['region'],
                            'country': city['country'],
                        }
                        for city in cities
                    ]
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': {
                    'code': 'CITY_SEARCH_ERROR',
                    'message': str(e)
                }
            }


# Skill 导出
skill = WeatherSkill()

# 工具函数导出
async def get_weather(params: Dict[str, Any]) -> Dict[str, Any]:
    """查询当前天气"""
    return await skill.get_weather(params)

async def get_forecast(params: Dict[str, Any]) -> Dict[str, Any]:
    """查询天气预报"""
    return await skill.get_forecast(params)

async def search_city(params: Dict[str, Any]) -> Dict[str, Any]:
    """搜索城市"""
    return await skill.search_city(params)


# 测试代码
if __name__ == '__main__':
    async def test():
        # 测试天气查询
        result = await get_weather({'city': '北京'})
        print('天气查询结果:', json.dumps(result, ensure_ascii=False, indent=2))
        
        # 测试天气预报
        result = await get_forecast({'city': '上海', 'days': 3})
        print('天气预报结果:', json.dumps(result, ensure_ascii=False, indent=2))
    
    asyncio.run(test())
