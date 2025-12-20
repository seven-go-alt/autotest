# -*- coding: utf-8 -*-
"""
通用测试数据和工具函数
"""

class CommonTestData:
    """通用测试数据"""
    
    # ========== HTTP 方法 ==========
    HTTP_METHODS = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    
    # ========== 响应头 ==========
    EXPECTED_HEADERS = {
        'Content-Type': 'application/json',
        'Connection': 'keep-alive'
    }
    
    # ========== 超时时间 ==========
    TIMEOUT_SHORT = 5
    TIMEOUT_NORMAL = 10
    TIMEOUT_LONG = 30
    
    # ========== 重试配置 ==========
    RETRY_ATTEMPTS = 3
    RETRY_DELAY = 1


class ErrorMessages:
    """错误信息集合"""
    
    MISSING_EMAIL = 'Missing email or username'
    MISSING_PASSWORD = 'Missing password'
    USER_NOT_FOUND = 'Cannot find user'
    UNAUTHORIZED = 'Unauthorized'
    BAD_REQUEST = 'Bad Request'
    SERVER_ERROR = 'Internal Server Error'


def generate_user_data(first_name, last_name, email=None):
    """生成用户测试数据"""
    return {
        'first_name': first_name,
        'last_name': last_name,
        'email': email or f'{first_name.lower()}.{last_name.lower()}@example.com'
    }


def generate_post_data(title, body, user_id=1):
    """生成文章测试数据"""
    return {
        'title': title,
        'body': body,
        'userId': user_id
    }
