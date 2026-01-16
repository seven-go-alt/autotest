# -*- coding: utf-8 -*-
"""
优化后的 UI 层测试 - Python 版本
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
    
    @pytest.mark.smoke
    @pytest.mark.critical
    def test_login_success(self, standard_user):
        """测试成功登录 - 使用标准用户"""
        self.saucedemo.login(standard_user['username'], standard_user['password'])
        self.saucedemo.verify_login_success()
    
    @pytest.mark.smoke
    def test_login_failure_wrong_password(self, invalid_user):
        """测试登录失败 - 错误密码"""
        self.saucedemo.login(invalid_user['username'], invalid_user['password'])
        self.saucedemo.verify_login_failed()
    
    @pytest.mark.regression
    def test_login_failure_empty_username(self):
        """测试登录失败 - 空用户名"""
        self.saucedemo.login('', 'secret_sauce')
        self.saucedemo.verify_login_failed()
    
    @pytest.mark.regression
    def test_login_failure_empty_password(self):
        """测试登录失败 - 空密码"""
        self.saucedemo.login('standard_user', '')
        self.saucedemo.verify_login_failed()
    
    @pytest.mark.regression
    def test_login_failure_empty_credentials(self):
        """测试登录失败 - 空凭证"""
        self.saucedemo.login('', '')
        self.saucedemo.verify_login_failed()
    
    @pytest.mark.smoke
    def test_add_to_cart(self, standard_user):
        """测试添加产品到购物车"""
        self.saucedemo.login(standard_user['username'], standard_user['password'])
        self.saucedemo.add_product_to_cart(0)
        self.saucedemo.verify_cart_count(1)
    
    @pytest.mark.regression
    def test_add_multiple_products_to_cart(self, standard_user):
        """测试添加多个产品到购物车"""
        self.saucedemo.login(standard_user['username'], standard_user['password'])
        self.saucedemo.add_multiple_products_to_cart([0, 1, 2])
        self.saucedemo.verify_cart_count(3)
    
    @pytest.mark.critical
    @pytest.mark.integration
    def test_complete_purchase_flow(self, standard_user, checkout_data):
        """测试完整的购买流程"""
        self.saucedemo.complete_purchase_flow(
            username=standard_user['username'],
            password=standard_user['password'],
            product_indices=[0, 1],
            first_name=checkout_data['first_name'],
            last_name=checkout_data['last_name'],
            postal_code=checkout_data['postal_code']
        )
    
    @pytest.mark.regression
    def test_product_sorting(self, standard_user):
        """测试产品排序功能"""
        self.saucedemo.login(standard_user['username'], standard_user['password'])
        
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
    
    @pytest.mark.smoke
    def test_logout(self, standard_user):
        """测试退出登录"""
        self.saucedemo.login(standard_user['username'], standard_user['password'])
        self.saucedemo.verify_login_success()
        self.saucedemo.logout()
        # 验证返回登录页面
        self.ui_ops.assert_element_exists("id=user-name")
    
    @pytest.mark.regression
    def test_remove_product_from_cart(self, standard_user):
        """测试从购物车移除产品"""
        self.saucedemo.login(standard_user['username'], standard_user['password'])
        # 添加两个产品
        self.saucedemo.add_multiple_products_to_cart([0, 1])
        self.saucedemo.verify_cart_count(2)
        
        # 前往购物车
        self.saucedemo.go_to_cart()
        
        # 移除一个产品
        self.saucedemo.remove_product_from_cart(0)
        
        # 验证购物车数量
        cart_count = self.saucedemo.get_cart_item_count()
        assert cart_count == 1, f"购物车应该有1个产品，实际: {cart_count}"
    
    @pytest.mark.regression
    def test_continue_shopping(self, standard_user):
        """测试继续购物功能"""
        self.saucedemo.login(standard_user['username'], standard_user['password'])
        self.saucedemo.add_product_to_cart(0)
        self.saucedemo.go_to_cart()
        self.saucedemo.continue_shopping()
        # 验证返回产品列表页面
        self.ui_ops.assert_element_exists(self.saucedemo.locators.PRODUCTS_CONTAINER)
    
    @pytest.mark.regression
    def test_product_count(self, standard_user):
        """测试产品列表数量"""
        self.saucedemo.login(standard_user['username'], standard_user['password'])
        # SauceDemo 通常有6个产品
        self.saucedemo.verify_product_count(6)
    
    @pytest.mark.performance
    @pytest.mark.slow
    def test_page_load_performance(self, standard_user):
        """测试页面加载性能"""
        import time
        start_time = time.time()
        
        self.saucedemo.login(standard_user['username'], standard_user['password'])
        
        load_time = time.time() - start_time
        # 验证登录在3秒内完成
        assert load_time < 3.0, f"登录耗时过长: {load_time:.2f}秒"


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
    
    @pytest.mark.smoke
    def test_search_keyword(self):
        """测试搜索功能"""
        self.baidu.search('Python')
        self.baidu.verify_search_results_exist()
    
    @pytest.mark.regression
    def test_search_results_contain_keyword(self):
        """测试搜索结果包含关键词"""
        keyword = 'Robot Framework'
        self.baidu.search(keyword)
        self.baidu.verify_search_results_contain_keyword(keyword)
    
    @pytest.mark.regression
    def test_multiple_searches(self):
        """测试多次搜索"""
        keywords = ['Python', 'JavaScript', 'Go']
        
        for keyword in keywords:
            self.baidu.complete_search_flow(keyword)
            # 返回首页继续搜索
            self.ui_ops.navigate_to('https://www.baidu.com/')
    
    @pytest.mark.regression
    def test_search_result_count(self):
        """测试搜索结果数量"""
        self.baidu.search('自动化测试')
        count = self.baidu.get_search_result_count()
        assert count > 0, "应该有搜索结果"
    
    @pytest.mark.regression
    def test_search_empty_keyword(self):
        """测试搜索空关键词"""
        # 搜索空关键词应该不会有结果或保持在首页
        self.baidu.search('')
        # 验证仍在百度首页
        current_url = self.ui_ops.get_current_url()
        assert 'baidu.com' in current_url


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
