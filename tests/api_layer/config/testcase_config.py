# -*- coding: utf-8 -*-
"""
API 测试用例配置
定义各个 API 测试的详细配置
"""

class APITestCaseConfig:
    """API 测试用例配置"""
    
    # ========== ReqRes API 配置 ==========
    REQRES_USERS_GET = {
        'name': '获取用户列表',
        'method': 'GET',
        'endpoint': '/api/users',
        'base_url': 'https://reqres.in',
        'params': {'page': 1},
        'expected_status': 200,
        'expected_fields': ['data', 'page', 'per_page', 'total', 'total_pages']
    }
    
    REQRES_USER_GET = {
        'name': '获取单个用户',
        'method': 'GET',
        'endpoint': '/api/users/{id}',
        'base_url': 'https://reqres.in',
        'params': {'id': 1},
        'expected_status': 200,
        'expected_fields': ['data', 'support']
    }
    
    REQRES_USER_CREATE = {
        'name': '创建用户',
        'method': 'POST',
        'endpoint': '/api/users',
        'base_url': 'https://reqres.in',
        'expected_status': 201,
        'expected_fields': ['id', 'createdAt']
    }
    
    REQRES_USER_UPDATE = {
        'name': '更新用户',
        'method': 'PUT',
        'endpoint': '/api/users/{id}',
        'base_url': 'https://reqres.in',
        'params': {'id': 1},
        'expected_status': 200,
        'expected_fields': ['updatedAt']
    }
    
    REQRES_USER_DELETE = {
        'name': '删除用户',
        'method': 'DELETE',
        'endpoint': '/api/users/{id}',
        'base_url': 'https://reqres.in',
        'params': {'id': 1},
        'expected_status': 204
    }
    
    REQRES_LOGIN_SUCCESS = {
        'name': '登录成功',
        'method': 'POST',
        'endpoint': '/api/login',
        'base_url': 'https://reqres.in',
        'expected_status': 200,
        'expected_fields': ['token']
    }
    
    REQRES_LOGIN_FAILED = {
        'name': '登录失败 - 缺少密码',
        'method': 'POST',
        'endpoint': '/api/login',
        'base_url': 'https://reqres.in',
        'expected_status': 400,
        'expected_fields': ['error']
    }
    
    # ========== JSONPlaceholder API 配置 ==========
    JSONPLACEHOLDER_POSTS_GET = {
        'name': '获取所有文章',
        'method': 'GET',
        'endpoint': '/posts',
        'base_url': 'https://jsonplaceholder.typicode.com',
        'expected_status': 200,
        'expected_fields': ['userId', 'id', 'title', 'body']
    }
    
    JSONPLACEHOLDER_POST_CREATE = {
        'name': '创建文章',
        'method': 'POST',
        'endpoint': '/posts',
        'base_url': 'https://jsonplaceholder.typicode.com',
        'expected_status': 201,
        'expected_fields': ['id']
    }
    
    # ========== HTTPBin API 配置 ==========
    HTTPBIN_GET = {
        'name': 'HTTPBin GET 测试',
        'method': 'GET',
        'endpoint': '/get',
        'base_url': 'https://httpbin.org',
        'expected_status': 200,
        'expected_fields': ['url', 'headers', 'args']
    }
    
    HTTPBIN_POST = {
        'name': 'HTTPBin POST 测试',
        'method': 'POST',
        'endpoint': '/post',
        'base_url': 'https://httpbin.org',
        'expected_status': 200,
        'expected_fields': ['url', 'json', 'headers']
    }
    
    HTTPBIN_STATUS = {
        'name': 'HTTPBin 状态码测试',
        'method': 'GET',
        'endpoint': '/status/{code}',
        'base_url': 'https://httpbin.org',
        'params': {'code': 200},
        'expected_status': 200
    }
