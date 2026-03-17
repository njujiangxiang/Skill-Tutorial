#!/usr/bin/env python3
"""
Skill 单元测试
"""

import pytest
import asyncio
from skill import [tool_name]


class TestSkill:
    """Skill 测试类"""
    
    @pytest.mark.asyncio
    async def test_normal_case(self):
        """测试正常情况"""
        params = {
            '[param_name]': '测试值'
        }
        
        result = await [tool_name](params)
        
        assert result['success'] is True
        assert 'data' in result
        assert result['data']['value'] == '测试值'
    
    @pytest.mark.asyncio
    async def test_missing_param(self):
        """测试缺少参数的情况"""
        params = {}
        
        with pytest.raises(ValueError, match='不能为空'):
            await [tool_name](params)
    
    @pytest.mark.asyncio
    async def test_invalid_type(self):
        """测试参数类型错误"""
        params = {
            '[param_name]': 123  # 应该是字符串
        }
        
        with pytest.raises(ValueError, match='必须是字符串'):
            await [tool_name](params)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
