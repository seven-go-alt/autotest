# -*- coding: utf-8 -*-
"""
UI 层测试 - Python 版本
使用 pytest 和封装好的操作层
用例专注于业务逻辑，不关心底层实现
"""

import pytest
from utils.ui_operations import UIOperations
from utils.business_operations import SauceDemoOperations, BaiduOperations


class TestSauceDemoUI:
    """SauceDemo 应用 UI 测试"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """测试前置条件"""
        self.ui_ops = UIOperations(browser_type="chromium", headless=False)
        self.ui_ops.start_browser('https://www.saucedemo.com/')
        self.saucedemo = SauceDemoOperations(self.ui_ops)
        yield
        self.ui_ops.close_browser()
    
    def test_login_success(self):
        """测试成功登录"""
        self.saucedemo.login('standard_user', 'secret_sauce')
        self.saucedemo.verify_login_success()
    
    def test_login_failure_wrong_password(self):
        """测试登录失败 - 错误密码"""
        self.saucedemo.login('standard_user', 'wrong_password')
        self.saucedemo.verify_login_failed()
    
    def test_add_to_cart(self):
        """测试添加产品到购物车"""
        self.saucedemo.login('standard_user', 'secret_sauce')
        self.saucedemo.add_product_to_cart(0)
        self.saucedemo.verify_cart_count(1)
    
    def test_add_multiple_products_to_cart(self):
        """测试添加多个产品到购物车"""
        self.saucedemo.login('standard_user', 'secret_sauce')
        self.saucedemo.add_multiple_products_to_cart([0, 1, 2])
        self.saucedemo.verify_cart_count(3)
    
    def test_complete_purchase_flow(self):
        """测试完整的购买流程"""
        self.saucedemo.complete_purchase_flow(
            username='standard_user',
            password='secret_sauce',
            product_indices=[0, 1],
            first_name='John',
            last_name='Doe',
            postal_code='12345'
        )
    
    def test_product_sorting(self):
        """测试产品排序功能"""
        self.saucedemo.login('standard_user', 'secret_sauce')
        
        # 获取排序前的产品名称
        names_before = self.saucedemo.get_product_names()
        
        # 按名称从A到Z排序
        self.saucedemo.sort_products('az')
        names_after_az = self.saucedemo.get_product_names()
        
        # 验证排序生效
        assert names_before != names_after_az, "排序应该改变产品顺序"
        assert names_after_az == sorted(names_after_az), "产品应该按字母顺序排列"
        
        # 按价格从低到高排序
        self.saucedemo.sort_products('lohi')
        prices = self.saucedemo.get_product_prices()
        # 验证价格排序（简单验证）
        assert len(prices) > 0, "应该获取到产品价格"
    
    def test_logout(self):
        """测试退出登录"""
        self.saucedemo.login('standard_user', 'secret_sauce')
        self.saucedemo.verify_login_success()
        self.saucedemo.logout()
        # 验证返回登录页面
        self.ui_ops.assert_element_exists("id=user-name")


class TestBaiduSearch:
    """百度搜索 UI 测试"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """测试前置条件"""
        self.ui_ops = UIOperations(browser_type="chromium", headless=False)
        self.ui_ops.start_browser('https://www.baidu.com/')
        self.baidu = BaiduOperations(self.ui_ops)
        yield
        self.ui_ops.close_browser()
    
    def test_search_keyword(self):
        """测试搜索功能"""
        self.baidu.search('Python')
        self.baidu.verify_search_results_exist()
    
    def test_search_results_contain_keyword(self):
        """测试搜索结果包含关键词"""
        keyword = 'Robot Framework'
        self.baidu.search(keyword)
        self.baidu.verify_search_results_contain_keyword(keyword)
    
    def test_multiple_searches(self):
        """测试多次搜索"""
        keywords = ['Python', 'JavaScript', 'Go']
        
        for keyword in keywords:
            self.baidu.complete_search_flow(keyword)
            # 返回首页继续搜索
            self.ui_ops.navigate_to('https://www.baidu.com/')
    
    def test_search_result_count(self):
        """测试搜索结果数量"""
        self.baidu.search('自动化测试')
        count = self.baidu.get_search_result_count()
        assert count > 0, "应该有搜索结果"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
