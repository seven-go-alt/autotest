"""
API 测试示例
使用 requests 库进行 HTTP API 测试，包括 GET、POST、请求头验证等
"""
import pytest
import requests
import json
from config import settings

# API 基础 URL（可根据环境修改）
API_BASE_URL = "https://httpbin.org"  # 使用公开的测试 API


class TestAPIBasic:
    """基础 API 测试类"""
    
    @pytest.mark.api
    @pytest.mark.smoke
    def test_get_request(self):
        """
        测试 GET 请求
        示例：获取 IP 信息
        """
        response = requests.get(f"{API_BASE_URL}/ip")
        
        # 验证状态码
        assert response.status_code == 200, f"状态码不正确: {response.status_code}"
        
        # 验证响应内容
        data = response.json()
        assert "origin" in data, "响应中没有 'origin' 字段"
        assert data["origin"], "IP 地址为空"
    
    @pytest.mark.api
    def test_post_request(self):
        """
        测试 POST 请求
        示例：提交 JSON 数据
        """
        payload = {
            "name": "Test User",
            "email": "test@example.com",
            "age": 25
        }
        
        response = requests.post(
            f"{API_BASE_URL}/post",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        # 验证状态码
        assert response.status_code == 200, f"POST 请求失败: {response.status_code}"
        
        # 验证响应内容
        data = response.json()
        assert data["json"]["name"] == payload["name"]
        assert data["json"]["email"] == payload["email"]
    
    @pytest.mark.api
    def test_put_request(self):
        """
        测试 PUT 请求
        示例：更新资源
        """
        payload = {
            "id": 1,
            "title": "Updated Title",
            "completed": True
        }
        
        response = requests.put(
            f"{API_BASE_URL}/put",
            json=payload
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["json"]["title"] == payload["title"]
    
    @pytest.mark.api
    def test_delete_request(self):
        """
        测试 DELETE 请求
        """
        response = requests.delete(f"{API_BASE_URL}/delete")
        
        assert response.status_code == 200
        data = response.json()
        assert "url" in data
    
    @pytest.mark.api
    def test_request_with_headers(self):
        """
        测试带自定义请求头的请求
        """
        headers = {
            "User-Agent": "Custom API Client/1.0",
            "Authorization": "Bearer test-token",
            "Custom-Header": "Custom-Value"
        }
        
        response = requests.get(
            f"{API_BASE_URL}/headers",
            headers=headers
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # 验证请求头被服务器接收
        assert "User-Agent" in data["headers"]
        assert "Authorization" in data["headers"]
        assert data["headers"]["Custom-Header"] == "Custom-Value"
    
    @pytest.mark.api
    def test_request_with_query_params(self):
        """
        测试带查询参数的请求
        """
        params = {
            "page": 1,
            "limit": 10,
            "sort": "name"
        }
        
        response = requests.get(
            f"{API_BASE_URL}/get",
            params=params
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # 验证查询参数
        assert data["args"]["page"] == "1"
        assert data["args"]["limit"] == "10"
        assert data["args"]["sort"] == "name"
    
    @pytest.mark.api
    def test_response_content_type(self):
        """
        测试响应内容类型
        """
        response = requests.get(f"{API_BASE_URL}/json")
        
        # 验证 Content-Type
        assert "application/json" in response.headers.get("Content-Type", "")
        
        # 验证可以解析为 JSON
        data = response.json()
        assert isinstance(data, dict)
    
    @pytest.mark.api
    def test_response_headers(self):
        """
        测试响应头
        """
        response = requests.get(f"{API_BASE_URL}/response-headers", 
                               params={"Custom-Header": "test-value"})
        
        assert response.status_code == 200
        
        # 验证常见的响应头
        assert "Content-Type" in response.headers or "content-type" in response.headers


class TestAPIErrorHandling:
    """API 错误处理测试"""
    
    @pytest.mark.api
    def test_404_not_found(self):
        """
        测试 404 错误处理
        """
        response = requests.get(f"{API_BASE_URL}/status/404")
        
        assert response.status_code == 404
    
    @pytest.mark.api
    def test_500_server_error(self):
        """
        测试 500 错误处理
        """
        response = requests.get(f"{API_BASE_URL}/status/500")
        
        assert response.status_code == 500
    
    @pytest.mark.api
    def test_timeout_handling(self):
        """
        测试超时处理
        """
        with pytest.raises(requests.exceptions.Timeout):
            # 设置 1ms 超时，会导致超时
            requests.get(
                f"{API_BASE_URL}/delay/10",
                timeout=0.001
            )
    
    @pytest.mark.api
    def test_connection_error(self):
        """
        测试连接错误处理
        """
        with pytest.raises(requests.exceptions.ConnectionError):
            requests.get("http://invalid-domain-that-does-not-exist.com")
    
    @pytest.mark.api
    def test_invalid_json_response(self):
        """
        测试无效 JSON 响应处理
        """
        response = requests.get(f"{API_BASE_URL}/html")
        
        # 验证响应是 HTML 而不是 JSON
        with pytest.raises(json.JSONDecodeError):
            response.json()


class TestAPIAdvanced:
    """高级 API 测试"""
    
    @pytest.mark.api
    def test_form_data_submission(self):
        """
        测试 Form 数据提交
        """
        data = {
            "username": "testuser",
            "password": "testpass123",
            "remember": "on"
        }
        
        response = requests.post(
            f"{API_BASE_URL}/post",
            data=data
        )
        
        assert response.status_code == 200
        result = response.json()
        assert result["form"]["username"] == "testuser"
    
    @pytest.mark.api
    def test_file_upload(self):
        """
        测试文件上传
        """
        files = {
            "file": ("test.txt", "This is test content", "text/plain")
        }
        
        response = requests.post(
            f"{API_BASE_URL}/post",
            files=files
        )
        
        assert response.status_code == 200
    
    @pytest.mark.api
    def test_cookie_handling(self):
        """
        测试 Cookie 处理
        """
        session = requests.Session()
        
        # 第一个请求设置 Cookie
        response1 = requests.get(f"{API_BASE_URL}/cookies/set", params={"test": "value"})
        
        # 验证请求成功
        assert response1.status_code == 200
    
    @pytest.mark.api
    def test_redirect_handling(self):
        """
        测试重定向处理
        """
        # 跟随重定向
        response = requests.get(f"{API_BASE_URL}/redirect/3", allow_redirects=True)
        
        assert response.status_code == 200
        assert response.history, "没有检测到重定向"
        
        # 验证重定向链
        assert len(response.history) >= 1
    
    @pytest.mark.api
    def test_concurrent_requests(self):
        """
        测试并发请求
        """
        from concurrent.futures import ThreadPoolExecutor
        import time
        
        def make_request(request_num):
            response = requests.get(f"{API_BASE_URL}/get", 
                                   params={"request_num": request_num})
            return response.status_code == 200
        
        # 并发发送 5 个请求
        with ThreadPoolExecutor(max_workers=5) as executor:
            results = list(executor.map(make_request, range(1, 6)))
        
        # 验证所有请求成功
        assert all(results), "某些并发请求失败"
    
    @pytest.mark.api
    def test_response_time(self):
        """
        测试响应时间
        """
        response = requests.get(f"{API_BASE_URL}/get")
        
        # 响应时间通常在毫秒级别
        assert response.elapsed.total_seconds() < 30, "响应时间过长"
    
    @pytest.mark.api
    def test_large_payload(self):
        """
        测试大型数据负载
        """
        # 创建一个较大的 JSON 负载
        large_data = {
            f"key_{i}": f"value_{i}" * 100 for i in range(100)
        }
        
        response = requests.post(
            f"{API_BASE_URL}/post",
            json=large_data
        )
        
        assert response.status_code == 200
        result = response.json()
        assert len(result["json"]) == 100
    
    @pytest.mark.api
    def test_batch_api_calls(self):
        """
        测试批量 API 调用
        """
        results = []
        
        # 连续发送多个请求
        for i in range(5):
            response = requests.get(f"{API_BASE_URL}/get", params={"index": i})
            results.append(response.status_code == 200)
        
        assert all(results), "批量请求失败"


class TestAPIDataValidation:
    """API 数据验证测试"""
    
    @pytest.mark.api
    def test_response_schema_validation(self):
        """
        测试响应数据格式验证
        """
        response = requests.get(f"{API_BASE_URL}/get")
        data = response.json()
        
        # 验证必需字段
        required_fields = ["headers", "args", "url"]
        for field in required_fields:
            assert field in data, f"缺少必需字段: {field}"
    
    @pytest.mark.api
    def test_data_type_validation(self):
        """
        测试数据类型验证
        """
        response = requests.get(f"{API_BASE_URL}/get")
        data = response.json()
        
        # 验证字段类型
        assert isinstance(data["headers"], dict)
        assert isinstance(data["args"], dict)
        assert isinstance(data["url"], str)
    
    @pytest.mark.api
    def test_response_encoding(self):
        """
        测试响应编码
        """
        response = requests.get(f"{API_BASE_URL}/get")
        
        # 验证字符编码
        assert response.encoding is not None
        assert "utf" in response.encoding.lower()
    
    @pytest.mark.api
    def test_empty_response_handling(self):
        """
        测试空响应处理
        """
        # 有些 API 可能返回空响应或空 JSON
        response = requests.get(f"{API_BASE_URL}/get")
        
        # 验证至少有一些内容
        assert response.text
        assert len(response.content) > 0
