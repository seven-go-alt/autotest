# -*- coding: utf-8 -*-
"""
测试数据管理器
集中管理测试数据，支持多环境配置和数据生成
"""

import json
import random
import string
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class TestDataManager:
    """测试数据管理器 - 提供测试数据的加载、生成和管理功能"""
    
    def __init__(self, data_dir: Optional[Path] = None):
        """
        初始化测试数据管理器
        
        Args:
            data_dir: 测试数据目录路径
        """
        self.data_dir = data_dir or Path(__file__).parent.parent / "tests" / "data"
        self._cache: Dict[str, Any] = {}
    
    def load_json_data(self, filename: str, use_cache: bool = True) -> Dict[str, Any]:
        """
        从 JSON 文件加载测试数据
        
        Args:
            filename: JSON 文件名
            use_cache: 是否使用缓存
        
        Returns:
            解析后的 JSON 数据
        """
        if use_cache and filename in self._cache:
            logger.debug(f"从缓存加载数据: {filename}")
            return self._cache[filename]
        
        file_path = self.data_dir / filename
        if not file_path.exists():
            raise FileNotFoundError(f"测试数据文件不存在: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if use_cache:
            self._cache[filename] = data
        
        logger.info(f"已加载测试数据: {filename}")
        return data
    
    def get_test_user(self, user_type: str = "standard") -> Dict[str, str]:
        """
        获取测试用户数据
        
        Args:
            user_type: 用户类型 (standard, locked_out, problem, performance_glitch)
        
        Returns:
            包含用户名和密码的字典
        """
        users = {
            "standard": {"username": "standard_user", "password": "secret_sauce"},
            "locked_out": {"username": "locked_out_user", "password": "secret_sauce"},
            "problem": {"username": "problem_user", "password": "secret_sauce"},
            "performance_glitch": {"username": "performance_glitch_user", "password": "secret_sauce"},
            "invalid": {"username": "invalid_user", "password": "wrong_password"}
        }
        
        if user_type not in users:
            raise ValueError(f"不支持的用户类型: {user_type}")
        
        return users[user_type]
    
    @staticmethod
    def generate_random_string(length: int = 10, include_digits: bool = True) -> str:
        """
        生成随机字符串
        
        Args:
            length: 字符串长度
            include_digits: 是否包含数字
        
        Returns:
            随机字符串
        """
        chars = string.ascii_letters
        if include_digits:
            chars += string.digits
        return ''.join(random.choice(chars) for _ in range(length))
    
    @staticmethod
    def generate_random_email(domain: str = "test.com") -> str:
        """
        生成随机邮箱地址
        
        Args:
            domain: 邮箱域名
        
        Returns:
            随机邮箱地址
        """
        username = TestDataManager.generate_random_string(8).lower()
        return f"{username}@{domain}"
    
    @staticmethod
    def generate_random_phone(country_code: str = "+86") -> str:
        """
        生成随机手机号
        
        Args:
            country_code: 国家代码
        
        Returns:
            随机手机号
        """
        if country_code == "+86":
            # 中国手机号格式
            prefix = random.choice(['130', '131', '132', '133', '134', '135', '136', '137', '138', '139',
                                   '150', '151', '152', '153', '155', '156', '157', '158', '159',
                                   '180', '181', '182', '183', '184', '185', '186', '187', '188', '189'])
            suffix = ''.join([str(random.randint(0, 9)) for _ in range(8)])
            return f"{country_code}{prefix}{suffix}"
        else:
            # 默认格式
            number = ''.join([str(random.randint(0, 9)) for _ in range(10)])
            return f"{country_code}{number}"
    
    @staticmethod
    def generate_user_data(
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        email: Optional[str] = None
    ) -> Dict[str, str]:
        """
        生成用户数据
        
        Args:
            first_name: 名字（可选，不提供则随机生成）
            last_name: 姓氏（可选，不提供则随机生成）
            email: 邮箱（可选，不提供则随机生成）
        
        Returns:
            用户数据字典
        """
        first_names = ["John", "Jane", "Michael", "Sarah", "David", "Emily", "Robert", "Lisa"]
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis"]
        
        return {
            "first_name": first_name or random.choice(first_names),
            "last_name": last_name or random.choice(last_names),
            "email": email or TestDataManager.generate_random_email(),
            "phone": TestDataManager.generate_random_phone(),
            "timestamp": datetime.now().isoformat()
        }
    
    @staticmethod
    def generate_address_data(country: str = "US") -> Dict[str, str]:
        """
        生成地址数据
        
        Args:
            country: 国家代码
        
        Returns:
            地址数据字典
        """
        us_addresses = {
            "street": f"{random.randint(100, 9999)} {random.choice(['Main', 'Oak', 'Pine', 'Maple', 'Cedar'])} St",
            "city": random.choice(["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"]),
            "state": random.choice(["NY", "CA", "IL", "TX", "AZ"]),
            "postal_code": f"{random.randint(10000, 99999)}",
            "country": "United States"
        }
        
        cn_addresses = {
            "street": f"{random.choice(['中山', '人民', '解放', '建设', '和平'])}路{random.randint(1, 999)}号",
            "city": random.choice(["北京", "上海", "广州", "深圳", "杭州"]),
            "province": random.choice(["北京市", "上海市", "广东省", "浙江省"]),
            "postal_code": f"{random.randint(100000, 999999)}",
            "country": "中国"
        }
        
        return us_addresses if country == "US" else cn_addresses
    
    def clear_cache(self):
        """清空数据缓存"""
        self._cache.clear()
        logger.info("测试数据缓存已清空")
    
    def get_checkout_data(self) -> Dict[str, str]:
        """
        获取结账信息数据
        
        Returns:
            结账信息字典
        """
        return {
            "first_name": "John",
            "last_name": "Doe",
            "postal_code": "12345"
        }
    
    def get_random_checkout_data(self) -> Dict[str, str]:
        """
        获取随机结账信息数据
        
        Returns:
            随机结账信息字典
        """
        user_data = self.generate_user_data()
        address_data = self.generate_address_data()
        
        return {
            "first_name": user_data["first_name"],
            "last_name": user_data["last_name"],
            "postal_code": address_data["postal_code"]
        }


# 全局实例
test_data_manager = TestDataManager()
