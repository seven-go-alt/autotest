#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
框架优化功能单元测试
测试新增的工具类和功能
"""

import pytest
import logging
from utils.retry_decorator import retry_on_failure
from utils.test_data_manager import TestDataManager

logging.basicConfig(level=logging.INFO)


class TestRetryDecorator:
    """测试重试装饰器"""
    
    def test_retry_success_on_third_attempt(self):
        """测试第三次尝试成功"""
        attempt_count = [0]
        
        @retry_on_failure(max_attempts=3, delay=0.1)
        def unstable_function():
            attempt_count[0] += 1
            if attempt_count[0] < 3:
                raise ValueError("模拟失败")
            return "成功"
        
        result = unstable_function()
        assert result == "成功"
        assert attempt_count[0] == 3
    
    def test_retry_failure_after_max_attempts(self):
        """测试达到最大重试次数后失败"""
        @retry_on_failure(max_attempts=2, delay=0.1)
        def always_fail():
            raise ValueError("总是失败")
        
        with pytest.raises(ValueError, match="总是失败"):
            always_fail()
    
    def test_retry_immediate_success(self):
        """测试立即成功（无需重试）"""
        @retry_on_failure(max_attempts=3, delay=0.1)
        def immediate_success():
            return "立即成功"
        
        result = immediate_success()
        assert result == "立即成功"


class TestTestDataManager:
    """测试数据管理器测试"""
    
    @pytest.fixture
    def manager(self):
        """创建测试数据管理器实例"""
        return TestDataManager()
    
    def test_get_standard_user(self, manager):
        """测试获取标准用户"""
        user = manager.get_test_user("standard")
        assert user["username"] == "standard_user"
        assert user["password"] == "secret_sauce"
    
    def test_get_invalid_user(self, manager):
        """测试获取无效用户"""
        user = manager.get_test_user("invalid")
        assert user["username"] == "invalid_user"
        assert user["password"] == "wrong_password"
    
    def test_get_unsupported_user_type(self, manager):
        """测试获取不支持的用户类型"""
        with pytest.raises(ValueError, match="不支持的用户类型"):
            manager.get_test_user("unknown_type")
    
    def test_generate_random_string(self, manager):
        """测试生成随机字符串"""
        random_str = manager.generate_random_string(10)
        assert len(random_str) == 10
        assert random_str.isalnum()
    
    def test_generate_random_email(self, manager):
        """测试生成随机邮箱"""
        email = manager.generate_random_email()
        assert "@" in email
        assert email.endswith("@test.com")
    
    def test_generate_random_phone(self, manager):
        """测试生成随机手机号"""
        phone = manager.generate_random_phone()
        assert phone.startswith("+86")
        assert len(phone) == 14  # +86 + 11位数字
    
    def test_generate_user_data(self, manager):
        """测试生成用户数据"""
        user_data = manager.generate_user_data()
        assert "first_name" in user_data
        assert "last_name" in user_data
        assert "email" in user_data
        assert "phone" in user_data
        assert "timestamp" in user_data
    
    def test_generate_user_data_with_custom_values(self, manager):
        """测试使用自定义值生成用户数据"""
        user_data = manager.generate_user_data(
            first_name="Test",
            last_name="User",
            email="test@example.com"
        )
        assert user_data["first_name"] == "Test"
        assert user_data["last_name"] == "User"
        assert user_data["email"] == "test@example.com"
    
    def test_get_checkout_data(self, manager):
        """测试获取结账数据"""
        checkout = manager.get_checkout_data()
        assert checkout["first_name"] == "John"
        assert checkout["last_name"] == "Doe"
        assert checkout["postal_code"] == "12345"
    
    def test_generate_address_data_us(self, manager):
        """测试生成美国地址数据"""
        address = manager.generate_address_data("US")
        assert "street" in address
        assert "city" in address
        assert "state" in address
        assert "postal_code" in address
        assert address["country"] == "United States"
    
    def test_generate_address_data_cn(self, manager):
        """测试生成中国地址数据"""
        address = manager.generate_address_data("CN")
        assert "street" in address
        assert "city" in address
        assert "province" in address
        assert "postal_code" in address
        assert address["country"] == "中国"


class TestFixtures:
    """测试 pytest fixtures"""
    
    def test_standard_user_fixture(self, standard_user):
        """测试标准用户 fixture"""
        assert standard_user["username"] == "standard_user"
        assert standard_user["password"] == "secret_sauce"
    
    def test_invalid_user_fixture(self, invalid_user):
        """测试无效用户 fixture"""
        assert invalid_user["username"] == "invalid_user"
        assert invalid_user["password"] == "wrong_password"
    
    def test_checkout_data_fixture(self, checkout_data):
        """测试结账数据 fixture"""
        assert "first_name" in checkout_data
        assert "last_name" in checkout_data
        assert "postal_code" in checkout_data
    
    def test_random_user_data_fixture(self, random_user_data):
        """测试随机用户数据 fixture"""
        assert "first_name" in random_user_data
        assert "last_name" in random_user_data
        assert "email" in random_user_data
        assert "@" in random_user_data["email"]
    
    def test_test_environment_fixture(self, test_environment):
        """测试环境配置 fixture"""
        assert "base_url" in test_environment
        assert "api_base_url" in test_environment
        assert "browser" in test_environment
        assert "headless" in test_environment
        assert "timeout" in test_environment


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
