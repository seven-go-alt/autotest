# -*- coding: utf-8 -*-
"""
API 层测试 - Python 版本
使用 pytest 和 requests 库
"""

import pytest
import requests
from tests.api_layer.config.api_config import APIConfig, HTTPMethod, ResponseStatus, APIEndpoints
from tests.api_layer.data.user_data import UserTestData
from tests.api_layer.data.post_data import PostTestData
from tests.api_layer.data.common_data import CommonTestData, generate_user_data


class TestReqResAPI:
    """ReqRes API 测试类"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """测试前置条件"""
        self.base_url = APIEndpoints.REQRES['base']
        self.session = requests.Session()
        self.session.headers.update(APIConfig.DEFAULT_HEADERS)
        yield
        self.session.close()
    
    def test_get_users(self):
        """测试获取用户列表"""
        url = f"{self.base_url}{APIEndpoints.REQRES['users']}"
        response = self.session.get(url, params={'page': 1})
        
        assert response.status_code == ResponseStatus.OK
        data = response.json()
        assert 'data' in data
        assert 'page' in data
        assert isinstance(data['data'], list)
    
    def test_get_single_user(self):
        """测试获取单个用户"""
        url = f"{self.base_url}{APIEndpoints.REQRES['users']}/1"
        response = self.session.get(url)
        
        assert response.status_code == ResponseStatus.OK
        data = response.json()
        assert 'data' in data
        assert data['data']['id'] == 1
    
    def test_create_user(self):
        """测试创建用户"""
        url = f"{self.base_url}{APIEndpoints.REQRES['users']}"
        payload = UserTestData.NEW_USER
        response = self.session.post(url, json=payload)
        
        assert response.status_code == ResponseStatus.CREATED
        data = response.json()
        assert 'id' in data
        assert 'createdAt' in data
        assert data['name'] == UserTestData.NEW_USER['name']
    
    def test_update_user(self):
        """测试更新用户"""
        url = f"{self.base_url}{APIEndpoints.REQRES['users']}/1"
        payload = UserTestData.UPDATED_USER
        response = self.session.put(url, json=payload)
        
        assert response.status_code == ResponseStatus.OK
        data = response.json()
        assert 'updatedAt' in data
    
    def test_delete_user(self):
        """测试删除用户"""
        url = f"{self.base_url}{APIEndpoints.REQRES['users']}/1"
        response = self.session.delete(url)
        
        assert response.status_code == ResponseStatus.NO_CONTENT
    
    def test_login_success(self):
        """测试成功登录"""
        url = f"{self.base_url}{APIEndpoints.REQRES['login']}"
        payload = UserTestData.VALID_LOGIN
        response = self.session.post(url, json=payload)
        
        assert response.status_code == ResponseStatus.OK
        data = response.json()
        assert 'token' in data
        assert data['token'] is not None
    
    def test_login_missing_password(self):
        """测试登录失败 - 缺少密码"""
        url = f"{self.base_url}{APIEndpoints.REQRES['login']}"
        payload = UserTestData.INVALID_LOGIN_NO_PASSWORD
        response = self.session.post(url, json=payload)
        
        assert response.status_code == ResponseStatus.BAD_REQUEST
        data = response.json()
        assert 'error' in data
    
    def test_user_not_found(self):
        """测试用户不存在"""
        url = f"{self.base_url}{APIEndpoints.REQRES['users']}/999"
        response = self.session.get(url)
        
        assert response.status_code == ResponseStatus.NOT_FOUND


class TestHTTPBinAPI:
    """HTTPBin API 测试类"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """测试前置条件"""
        self.base_url = APIEndpoints.HTTPBIN['base']
        self.session = requests.Session()
        self.session.headers.update(APIConfig.DEFAULT_HEADERS)
        yield
        self.session.close()
    
    def test_get_request(self):
        """测试 GET 请求"""
        url = f"{self.base_url}{APIEndpoints.HTTPBIN['get']}"
        response = self.session.get(url)
        
        assert response.status_code == ResponseStatus.OK
        data = response.json()
        assert 'url' in data
        assert 'headers' in data
        assert 'args' in data
    
    def test_post_request(self):
        """测试 POST 请求"""
        url = f"{self.base_url}{APIEndpoints.HTTPBIN['post']}"
        payload = {'name': 'Test User', 'email': 'test@example.com'}
        response = self.session.post(url, json=payload)
        
        assert response.status_code == ResponseStatus.OK
        data = response.json()
        assert 'json' in data
        assert data['json']['name'] == 'Test User'
    
    def test_put_request(self):
        """测试 PUT 请求"""
        url = f"{self.base_url}{APIEndpoints.HTTPBIN['put']}"
        payload = {'id': 1, 'updated': True}
        response = self.session.put(url, json=payload)
        
        assert response.status_code == ResponseStatus.OK
        data = response.json()
        assert 'json' in data
    
    def test_delete_request(self):
        """测试 DELETE 请求"""
        url = f"{self.base_url}{APIEndpoints.HTTPBIN['delete']}"
        response = self.session.delete(url)
        
        assert response.status_code == ResponseStatus.OK
    
    def test_query_parameters(self):
        """测试查询参数"""
        url = f"{self.base_url}{APIEndpoints.HTTPBIN['get']}"
        params = {'key1': 'value1', 'key2': 'value2'}
        response = self.session.get(url, params=params)
        
        assert response.status_code == ResponseStatus.OK
        data = response.json()
        assert data['args']['key1'] == 'value1'
        assert data['args']['key2'] == 'value2'
    
    def test_custom_headers(self):
        """测试自定义请求头"""
        url = f"{self.base_url}{APIEndpoints.HTTPBIN['headers']}"
        headers = {'X-Custom-Header': 'custom-value', 'X-Another': 'another-value'}
        response = self.session.get(url, headers=headers)
        
        assert response.status_code == ResponseStatus.OK
    
    def test_status_code_200(self):
        """测试状态码 200"""
        url = f"{self.base_url}{APIEndpoints.HTTPBIN['status']}/200"
        response = self.session.get(url)
        
        assert response.status_code == ResponseStatus.OK
    
    def test_status_code_404(self):
        """测试状态码 404"""
        url = f"{self.base_url}{APIEndpoints.HTTPBIN['status']}/404"
        response = self.session.get(url)
        
        assert response.status_code == ResponseStatus.NOT_FOUND
    
    def test_get_ip(self):
        """测试获取 IP"""
        url = f"{self.base_url}{APIEndpoints.HTTPBIN['ip']}"
        response = self.session.get(url)
        
        assert response.status_code == ResponseStatus.OK
        data = response.json()
        assert 'origin' in data


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
