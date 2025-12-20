# -*- coding: utf-8 -*-
"""
用户相关测试数据
"""

class UserTestData:
    """用户测试数据"""
    
    # ========== ReqRes 用户数据 ==========
    VALID_USER = {
        'id': 1,
        'email': 'george.bluth@reqres.in',
        'first_name': 'George',
        'last_name': 'Bluth',
        'avatar': 'https://reqres.in/img/faces/1-image.jpg'
    }
    
    NEW_USER = {
        'name': 'John Doe',
        'job': 'Software Engineer'
    }
    
    UPDATED_USER = {
        'name': 'Jane Doe',
        'job': 'Senior Engineer',
        'id': 1
    }
    
    # ========== 登录凭证 ==========
    VALID_LOGIN = {
        'email': 'eve.holt@reqres.in',
        'password': 'cityslicka'
    }
    
    INVALID_LOGIN_NO_PASSWORD = {
        'email': 'eve.holt@reqres.in'
    }
    
    INVALID_LOGIN_NO_EMAIL = {
        'password': 'cityslicka'
    }
    
    INVALID_LOGIN_WRONG_CREDENTIALS = {
        'email': 'wrong@reqres.in',
        'password': 'wrongpassword'
    }
    
    # ========== 用户列表参数 ==========
    USER_LIST_PARAMS = {
        'page_1': {'page': 1},
        'page_2': {'page': 2},
        'invalid_page': {'page': 999}
    }
