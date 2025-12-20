# -*- coding: utf-8 -*-
"""
API 基础配置
"""

from enum import Enum


class APIConfig:
    """API 配置类"""
    
    # ========== 环境配置 ==========
    ENVIRONMENTS = {
        'dev': {
            'base_url': 'http://localhost:8000',
            'timeout': 10,
            'verify_ssl': False
        },
        'staging': {
            'base_url': 'https://staging-api.example.com',
            'timeout': 15,
            'verify_ssl': True
        },
        'prod': {
            'base_url': 'https://api.example.com',
            'timeout': 20,
            'verify_ssl': True
        }
    }
    
    # ========== 默认环境 ==========
    DEFAULT_ENV = 'dev'
    
    # ========== 公共请求头 ==========
    DEFAULT_HEADERS = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    # ========== 认证配置 ==========
    AUTH_CONFIGS = {
        'api_key': {
            'type': 'header',
            'key': 'X-API-Key',
            'value': 'your_api_key_here'
        },
        'bearer_token': {
            'type': 'header',
            'key': 'Authorization',
            'value': 'Bearer your_token_here'
        },
        'basic_auth': {
            'type': 'basic',
            'username': 'user',
            'password': 'pass'
        }
    }


class HTTPMethod(Enum):
    """HTTP 方法枚举"""
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    PATCH = 'PATCH'
    DELETE = 'DELETE'
    HEAD = 'HEAD'
    OPTIONS = 'OPTIONS'


class APIEndpoints:
    """API 端点定义"""
    
    # ========== JSONPlaceholder 端点 ==========
    JSONPLACEHOLDER = {
        'base': 'https://jsonplaceholder.typicode.com',
        'posts': '/posts',
        'users': '/users',
        'comments': '/comments',
        'albums': '/albums',
        'photos': '/photos',
        'todos': '/todos'
    }
    
    # ========== ReqRes 端点 ==========
    REQRES = {
        'base': 'https://reqres.in',
        'users': '/api/users',
        'register': '/api/register',
        'login': '/api/login'
    }
    
    # ========== HTTPBin 端点 ==========
    HTTPBIN = {
        'base': 'https://httpbin.org',
        'get': '/get',
        'post': '/post',
        'put': '/put',
        'patch': '/patch',
        'delete': '/delete',
        'headers': '/headers',
        'ip': '/ip',
        'user_agent': '/user-agent',
        'status': '/status'
    }


class ResponseStatus:
    """HTTP 响应状态码"""
    
    # 成功响应
    OK = 200
    CREATED = 201
    ACCEPTED = 202
    NO_CONTENT = 204
    
    # 重定向
    MOVED_PERMANENTLY = 301
    FOUND = 302
    NOT_MODIFIED = 304
    
    # 客户端错误
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    CONFLICT = 409
    
    # 服务器错误
    INTERNAL_ERROR = 500
    BAD_GATEWAY = 502
    SERVICE_UNAVAILABLE = 503
