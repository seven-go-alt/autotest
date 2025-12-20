# -*- coding: utf-8 -*-
"""
文章相关测试数据
"""

class PostTestData:
    """文章测试数据"""
    
    # ========== ReqRes 文章数据 ==========
    NEW_POST = {
        'title': 'Test Post',
        'body': 'This is a test post',
        'userId': 1
    }
    
    UPDATED_POST = {
        'title': 'Updated Test Post',
        'body': 'This is an updated test post',
        'userId': 1,
        'id': 1
    }
    
    # ========== JSONPlaceholder 文章数据 ==========
    JP_NEW_POST = {
        'title': 'JSONPlaceholder Test Post',
        'body': 'Testing JSONPlaceholder API',
        'userId': 1
    }
    
    JP_UPDATED_POST = {
        'title': 'Updated JSONPlaceholder Post',
        'body': 'Updated content',
        'userId': 1,
        'id': 1
    }
    
    # ========== 查询参数 ==========
    POST_QUERY_PARAMS = {
        'by_user': {'userId': 1},
        'by_id': {'id': 1},
        'pagination': {'_start': 0, '_limit': 10}
    }
