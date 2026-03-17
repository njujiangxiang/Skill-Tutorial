#!/usr/bin/env python3
"""
待办事项 Skill - Python 版本
管理个人待办事项，支持创建、完成、删除任务
"""

import os
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path
import asyncio


class TodoStorage:
    """待办事项本地存储"""
    
    def __init__(self):
        self.data_dir = Path.home() / '.openclaw' / 'data'
        self.todo_file = self.data_dir / 'todos.json'
        self._ensure_dir()
    
    def _ensure_dir(self):
        """确保数据目录存在"""
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def _read_data(self) -> Dict[str, Any]:
        """读取数据"""
        if not self.todo_file.exists():
            return {'todos': [], 'nextId': 1}
        
        with open(self.todo_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _write_data(self, data: Dict[str, Any]):
        """写入数据"""
        self._ensure_dir()
        with open(self.todo_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def get_all(self) -> List[Dict[str, Any]]:
        """获取所有任务"""
        data = self._read_data()
        return data['todos']
    
    def get_by_id(self, todo_id: str) -> Optional[Dict[str, Any]]:
        """根据 ID 获取任务"""
        todos = self.get_all()
        for todo in todos:
            if todo['id'] == todo_id:
                return todo
        return None
    
    def create(self, title: str, priority: str = 'medium') -> Dict[str, Any]:
        """创建新任务"""
        data = self._read_data()
        
        new_todo = {
            'id': str(data['nextId']),
            'title': title,
            'priority': priority,
            'status': 'pending',
            'createdAt': datetime.now().isoformat(),
            'completedAt': None,
        }
        
        data['nextId'] += 1
        data['todos'].append(new_todo)
        self._write_data(data)
        
        return new_todo
    
    def complete(self, todo_id: str) -> Dict[str, Any]:
        """完成任务"""
        data = self._read_data()
        
        for todo in data['todos']:
            if todo['id'] == todo_id:
                todo['status'] = 'completed'
                todo['completedAt'] = datetime.now().isoformat()
                self._write_data(data)
                return todo
        
        raise ValueError(f'任务不存在：{todo_id}')
    
    def delete(self, todo_id: str) -> bool:
        """删除任务"""
        data = self._read_data()
        
        for i, todo in enumerate(data['todos']):
            if todo['id'] == todo_id:
                data['todos'].pop(i)
                self._write_data(data)
                return True
        
        raise ValueError(f'任务不存在：{todo_id}')
    
    def filter_by_status(self, status: str) -> List[Dict[str, Any]]:
        """按状态过滤任务"""
        todos = self.get_all()
        if status == 'all':
            return todos
        return [t for t in todos if t['status'] == status]


class TodoSkill:
    """待办事项 Skill"""
    
    def __init__(self):
        self.storage = TodoStorage()
    
    async def create_todo(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        创建新任务
        
        Args:
            params: 参数对象
                - title: 任务标题 (必需)
                - priority: 优先级 (可选，high/medium/low)
        
        Returns:
            创建结果
        """
        title = params.get('title')
        priority = params.get('priority', 'medium')
        
        # 参数验证
        if not title or not isinstance(title, str):
            raise ValueError('任务标题不能为空')
        
        if len(title) > 200:
            raise ValueError('任务标题过长')
        
        valid_priorities = ['high', 'medium', 'low']
        if priority not in valid_priorities:
            raise ValueError(f'优先级必须是：{"/".join(valid_priorities)}')
        
        # 创建任务
        todo = self.storage.create(title, priority)
        
        return {
            'success': True,
            'data': {
                'message': f'已创建任务：{title}',
                'todo': todo,
            }
        }
    
    async def complete_todo(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        完成任务
        
        Args:
            params: 参数对象
                - id: 任务 ID (必需)
        
        Returns:
            完成结果
        """
        todo_id = params.get('id')
        
        if not todo_id:
            raise ValueError('任务 ID 不能为空')
        
        try:
            todo = self.storage.complete(todo_id)
            return {
                'success': True,
                'data': {
                    'message': f'已完成任务：{todo["title"]}',
                    'todo': todo,
                }
            }
        except ValueError as e:
            return {
                'success': False,
                'error': {
                    'code': 'TODO_NOT_FOUND',
                    'message': str(e)
                }
            }
    
    async def list_todos(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        查看任务列表
        
        Args:
            params: 参数对象
                - status: 状态 (可选，pending/completed/all)
        
        Returns:
            任务列表
        """
        status = params.get('status', 'pending')
        
        todos = self.storage.filter_by_status(status)
        
        # 排序：按优先级和创建时间
        priority_order = {'high': 0, 'medium': 1, 'low': 2}
        todos.sort(key=lambda t: (
            0 if t['status'] == 'pending' else 1,
            priority_order.get(t['priority'], 1),
            t['createdAt']
        ), reverse=True)
        
        return {
            'success': True,
            'data': {
                'count': len(todos),
                'todos': [
                    {
                        'id': t['id'],
                        'title': t['title'],
                        'priority': t['priority'],
                        'status': t['status'],
                        'createdAt': t['createdAt'],
                    }
                    for t in todos
                ]
            }
        }
    
    async def delete_todo(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        删除任务
        
        Args:
            params: 参数对象
                - id: 任务 ID (必需)
        
        Returns:
            删除结果
        """
        todo_id = params.get('id')
        
        if not todo_id:
            raise ValueError('任务 ID 不能为空')
        
        try:
            self.storage.delete(todo_id)
            return {
                'success': True,
                'data': {
                    'message': '已删除任务',
                }
            }
        except ValueError as e:
            return {
                'success': False,
                'error': {
                    'code': 'TODO_NOT_FOUND',
                    'message': str(e)
                }
            }


# Skill 导出
skill = TodoSkill()

# 工具函数导出
async def create_todo(params: Dict[str, Any]) -> Dict[str, Any]:
    """创建新任务"""
    return await skill.create_todo(params)

async def complete_todo(params: Dict[str, Any]) -> Dict[str, Any]:
    """完成任务"""
    return await skill.complete_todo(params)

async def list_todos(params: Dict[str, Any]) -> Dict[str, Any]:
    """查看任务列表"""
    return await skill.list_todos(params)

async def delete_todo(params: Dict[str, Any]) -> Dict[str, Any]:
    """删除任务"""
    return await skill.delete_todo(params)


# 测试代码
if __name__ == '__main__':
    async def test():
        # 测试创建任务
        result = await create_todo({'title': '测试任务', 'priority': 'high'})
        print('创建任务:', json.dumps(result, ensure_ascii=False, indent=2))
        
        todo_id = result['data']['todo']['id']
        
        # 测试查看任务
        result = await list_todos({'status': 'pending'})
        print('任务列表:', json.dumps(result, ensure_ascii=False, indent=2))
        
        # 测试完成任务
        result = await complete_todo({'id': todo_id})
        print('完成任务:', json.dumps(result, ensure_ascii=False, indent=2))
        
        # 测试删除任务
        result = await delete_todo({'id': todo_id})
        print('删除任务:', json.dumps(result, ensure_ascii=False, indent=2))
    
    asyncio.run(test())
