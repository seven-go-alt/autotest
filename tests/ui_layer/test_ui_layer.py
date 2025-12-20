# -*- coding: utf-8 -*-
"""
UI 层测试 - Python 版本
使用 pytest 和 Playwright
"""

import pytest
from playwright.sync_api import sync_playwright
from tests.ui_layer.locators.saucedemo_locators import SauceDemoLocators
from tests.ui_layer.locators.baidu_locators import BaiduLocators


class TestSauceDemoUI:
    """SauceDemo 应用 UI 测试"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """测试前置条件"""
        playwright = sync_playwright().start()
        self.browser = playwright.chromium.launch(headless=False)
        self.context = self.browser.new_context()
        self.page = self.context.new_page()
        self.locators = SauceDemoLocators()
        yield
        self.page.close()
        self.context.close()
        self.browser.close()
        playwright.stop()
    
    def test_login_success(self):
        """测试成功登录"""
        self.page.goto('https://www.saucedemo.com/')
        self.page.fill(self.locators.LOGIN_USERNAME_INPUT, 'standard_user')
        self.page.fill(self.locators.LOGIN_PASSWORD_INPUT, 'secret_sauce')
        self.page.click(self.locators.LOGIN_BUTTON)
        
        # 验证登录成功
        self.page.wait_for_selector(self.locators.PRODUCTS_CONTAINER)
        assert self.page.query_selector(self.locators.PRODUCTS_CONTAINER) is not None
    
    def test_login_failure_wrong_password(self):
        """测试登录失败 - 错误密码"""
        self.page.goto('https://www.saucedemo.com/')
        self.page.fill(self.locators.LOGIN_USERNAME_INPUT, 'standard_user')
        self.page.fill(self.locators.LOGIN_PASSWORD_INPUT, 'wrong_password')
        self.page.click(self.locators.LOGIN_BUTTON)
        
        # 验证错误提示出现
        error_element = self.page.query_selector(self.locators.LOGIN_ERROR_CONTAINER)
        assert error_element is not None
        assert 'password' in error_element.text_content().lower()
    
    def test_add_to_cart(self):
        """测试添加产品到购物车"""
        # 登录
        self.page.goto('https://www.saucedemo.com/')
        self.page.fill(self.locators.LOGIN_USERNAME_INPUT, 'standard_user')
        self.page.fill(self.locators.LOGIN_PASSWORD_INPUT, 'secret_sauce')
        self.page.click(self.locators.LOGIN_BUTTON)
        self.page.wait_for_selector(self.locators.PRODUCTS_CONTAINER)
        
        # 添加产品
        products = self.page.query_selector_all(self.locators.PRODUCT_ITEM)
        add_btn = products[0].query_selector(self.locators.PRODUCT_ADD_BTN)
        add_btn.click()
        
        # 验证购物车
        badge = self.page.query_selector(self.locators.SHOPPING_CART_BADGE)
        assert badge is not None
        assert badge.text_content() == '1'
    
    def test_complete_purchase_flow(self):
        """测试完整的购买流程"""
        # 登录
        self.page.goto('https://www.saucedemo.com/')
        self.page.fill(self.locators.LOGIN_USERNAME_INPUT, 'standard_user')
        self.page.fill(self.locators.LOGIN_PASSWORD_INPUT, 'secret_sauce')
        self.page.click(self.locators.LOGIN_BUTTON)
        self.page.wait_for_selector(self.locators.PRODUCTS_CONTAINER)
        
        # 添加产品
        products = self.page.query_selector_all(self.locators.PRODUCT_ITEM)
        for i in range(2):
            add_btn = products[i].query_selector(self.locators.PRODUCT_ADD_BTN)
            add_btn.click()
        
        # 进入购物车
        self.page.click(self.locators.SHOPPING_CART_LINK)
        self.page.wait_for_selector(self.locators.CHECKOUT_BUTTON)
        
        # 结账
        self.page.click(self.locators.CHECKOUT_BUTTON)
        self.page.wait_for_selector(self.locators.CHECKOUT_FIRST_NAME)
        
        # 填写信息
        self.page.fill(self.locators.CHECKOUT_FIRST_NAME, 'John')
        self.page.fill(self.locators.CHECKOUT_LAST_NAME, 'Doe')
        self.page.fill(self.locators.CHECKOUT_POSTAL_CODE, '12345')
        
        # 完成结账
        self.page.click(self.locators.CHECKOUT_CONTINUE_BTN)
        self.page.click(self.locators.CHECKOUT_FINISH_BTN)
        
        # 验证订单完成
        order_msg = self.page.query_selector(self.locators.ORDER_COMPLETE_MSG)
        assert order_msg is not None
        assert 'Thank you' in order_msg.text_content()


class TestBaiduSearch:
    """百度搜索 UI 测试"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """测试前置条件"""
        playwright = sync_playwright().start()
        self.browser = playwright.chromium.launch(headless=False)
        self.context = self.browser.new_context()
        self.page = self.context.new_page()
        self.locators = BaiduLocators()
        yield
        self.page.close()
        self.context.close()
        self.browser.close()
        playwright.stop()
    
    def test_search_keyword(self):
        """测试搜索功能"""
        self.page.goto('https://www.baidu.com/')
        
        # 搜索
        self.page.fill(self.locators.SEARCH_INPUT, 'Python')
        self.page.click(self.locators.SEARCH_BUTTON)
        
        # 验证结果
        self.page.wait_for_selector(self.locators.SEARCH_RESULTS_CONTAINER)
        results = self.page.query_selector_all(self.locators.SEARCH_RESULT_ITEM)
        assert len(results) > 0
    
    def test_search_results_contain_keyword(self):
        """测试搜索结果包含关键词"""
        self.page.goto('https://www.baidu.com/')
        
        # 搜索
        keyword = 'Robot Framework'
        self.page.fill(self.locators.SEARCH_INPUT, keyword)
        self.page.click(self.locators.SEARCH_BUTTON)
        
        # 验证至少一个结果包含关键词
        self.page.wait_for_selector(self.locators.SEARCH_RESULT_TITLE)
        titles = self.page.query_selector_all(self.locators.SEARCH_RESULT_TITLE)
        
        found = False
        for title in titles[:5]:
            if keyword in title.text_content():
                found = True
                break
        
        assert found, f"搜索结果中未找到关键词: {keyword}"
    
    def test_multiple_searches(self):
        """测试多次搜索"""
        self.page.goto('https://www.baidu.com/')
        
        keywords = ['Python', 'JavaScript', 'Go']
        
        for keyword in keywords:
            self.page.fill(self.locators.SEARCH_INPUT, keyword)
            self.page.click(self.locators.SEARCH_BUTTON)
            
            # 验证结果
            self.page.wait_for_selector(self.locators.SEARCH_RESULTS_CONTAINER)
            results = self.page.query_selector_all(self.locators.SEARCH_RESULT_ITEM)
            assert len(results) > 0
            
            # 返回首页继续搜索
            self.page.goto('https://www.baidu.com/')


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
