# -*- coding: utf-8 -*-
"""
业务操作封装层 - 封装常用业务流程
使用底层操作组合成完整的业务功能
"""

import logging
from typing import Optional, List, Dict
from utils.ui_operations import UIOperations
from tests.ui_layer.locators.saucedemo_locators import SauceDemoLocators
from tests.ui_layer.locators.baidu_locators import BaiduLocators

logger = logging.getLogger(__name__)


class SauceDemoOperations:
    """SauceDemo业务操作封装"""
    
    def __init__(self, ui_ops: UIOperations):
        """
        初始化SauceDemo操作
        
        Args:
            ui_ops: UIOperations实例
        """
        self.ui = ui_ops
        self.locators = SauceDemoLocators()
    
    def login(self, username: str, password: str):
        """登录操作"""
        logger.info(f"执行登录操作: 用户名={username}")
        try:
            self.ui.fill(self.locators.LOGIN_USERNAME_INPUT, username)
            self.ui.fill(self.locators.LOGIN_PASSWORD_INPUT, password)
            self.ui.click(self.locators.LOGIN_BUTTON)
            # 等待登录完成
            self.ui.wait_for_element(self.locators.PRODUCTS_CONTAINER, timeout=10000)
            logger.info("登录操作完成")
        except Exception as e:
            logger.error(f"登录失败: {e}")
            raise
    
    def verify_login_success(self):
        """验证登录成功"""
        logger.info("验证登录成功")
        self.ui.assert_element_exists(self.locators.PRODUCTS_CONTAINER)
        logger.info("登录成功验证通过")
    
    def verify_login_failed(self, expected_error: Optional[str] = None):
        """验证登录失败"""
        logger.info("验证登录失败")
        self.ui.assert_element_exists(self.locators.LOGIN_ERROR_CONTAINER)
        if expected_error:
            self.ui.assert_text_contains(self.locators.LOGIN_ERROR_CONTAINER, expected_error)
        logger.info("登录失败验证通过")
    
    def add_product_to_cart(self, product_index: int = 0):
        """添加产品到购物车"""
        logger.info(f"添加产品到购物车: 索引={product_index}")
        products = self.ui.page.query_selector_all(self.locators.PRODUCT_ITEM)
        if product_index >= len(products):
            error_msg = f"产品索引超出范围: {product_index}，总数: {len(products)}"
            logger.error(error_msg)
            raise IndexError(error_msg)
        
        product = products[product_index]
        add_btn = product.query_selector(self.locators.PRODUCT_ADD_BTN)
        if add_btn:
            add_btn.click()
            logger.info(f"产品已添加到购物车: 索引={product_index}")
        else:
            logger.warning(f"未找到添加按钮: 索引={product_index}")
    
    def add_multiple_products_to_cart(self, indices: List[int]):
        """添加多个产品到购物车"""
        for index in indices:
            self.add_product_to_cart(index)
    
    def verify_cart_count(self, expected_count: int):
        """验证购物车数量"""
        count_text = self.ui.get_text(self.locators.SHOPPING_CART_BADGE)
        actual_count = int(count_text) if count_text else 0
        if actual_count != expected_count:
            raise AssertionError(f"购物车数量不匹配。期望: {expected_count}，实际: {actual_count}")
    
    def go_to_cart(self):
        """前往购物车"""
        self.ui.click(self.locators.SHOPPING_CART_LINK)
        self.ui.wait_for_element(self.locators.CHECKOUT_BUTTON)
    
    def go_to_checkout(self):
        """前往结账"""
        self.ui.click(self.locators.CHECKOUT_BUTTON)
        self.ui.wait_for_element(self.locators.CHECKOUT_FIRST_NAME)
    
    def fill_checkout_info(self, first_name: str, last_name: str, postal_code: str):
        """填写结账信息"""
        self.ui.fill(self.locators.CHECKOUT_FIRST_NAME, first_name)
        self.ui.fill(self.locators.CHECKOUT_LAST_NAME, last_name)
        self.ui.fill(self.locators.CHECKOUT_POSTAL_CODE, postal_code)
    
    def complete_checkout(self):
        """完成结账"""
        self.ui.click(self.locators.CHECKOUT_CONTINUE_BTN)
        self.ui.wait_for_element(self.locators.CHECKOUT_FINISH_BTN)
        self.ui.click(self.locators.CHECKOUT_FINISH_BTN)
    
    def verify_order_complete(self):
        """验证订单完成"""
        self.ui.assert_element_exists(self.locators.ORDER_COMPLETE_MSG)
        self.ui.assert_text_contains(self.locators.ORDER_COMPLETE_MSG, "Thank you")
    
    def complete_purchase_flow(self, username: str, password: str, 
                               product_indices: List[int],
                               first_name: str, last_name: str, postal_code: str):
        """完整的购买流程"""
        self.login(username, password)
        self.verify_login_success()
        self.add_multiple_products_to_cart(product_indices)
        self.verify_cart_count(len(product_indices))
        self.go_to_cart()
        self.go_to_checkout()
        self.fill_checkout_info(first_name, last_name, postal_code)
        self.complete_checkout()
        self.verify_order_complete()
    
    def sort_products(self, sort_option: str):
        """排序产品
        Args:
            sort_option: 排序选项 (az, za, lohi, hilo)
        """
        option_map = {
            "az": "az",
            "za": "za",
            "lohi": "lohi",  # 价格从低到高
            "hilo": "hilo"   # 价格从高到低
        }
        value = option_map.get(sort_option.lower())
        if not value:
            raise ValueError(f"不支持的排序选项: {sort_option}")
        self.ui.select_option(self.locators.SORT_DROPDOWN, value)
        # 等待排序完成
        self.ui.page.wait_for_timeout(500)
    
    def get_product_names(self) -> List[str]:
        """获取所有产品名称"""
        return self.ui.get_all_texts(self.locators.PRODUCT_NAME)
    
    def get_product_prices(self) -> List[str]:
        """获取所有产品价格"""
        return self.ui.get_all_texts(self.locators.PRODUCT_PRICE)
    
    def logout(self):
        """退出登录"""
        self.ui.click(self.locators.HAMBURGER_MENU)
        self.ui.wait_for_element(self.locators.MENU_LOGOUT)
        self.ui.click(self.locators.MENU_LOGOUT)
    
    def remove_product_from_cart(self, product_index: int = 0):
        """从购物车移除产品"""
        cart_items = self.ui.page.query_selector_all(self.locators.CART_ITEM)
        if product_index >= len(cart_items):
            raise IndexError(f"购物车产品索引超出范围: {product_index}")
        
        product = cart_items[product_index]
        remove_btn = product.query_selector(self.locators.PRODUCT_REMOVE_BTN)
        if remove_btn:
            remove_btn.click()
    
    def get_cart_item_count(self) -> int:
        """获取购物车中的产品数量"""
        return self.ui.get_element_count(self.locators.CART_ITEM)
    
    def continue_shopping(self):
        """继续购物（从购物车返回产品列表）"""
        self.ui.click(self.locators.CONTINUE_SHOPPING_BTN)
        self.ui.wait_for_element(self.locators.PRODUCTS_CONTAINER)
    
    def verify_product_count(self, expected_count: int):
        """验证产品列表数量"""
        actual_count = self.ui.get_element_count(self.locators.PRODUCT_ITEM)
        if actual_count != expected_count:
            raise AssertionError(f"产品数量不匹配。期望: {expected_count}，实际: {actual_count}")
    
    def get_all_product_names(self) -> List[str]:
        """获取所有产品名称列表"""
        return self.get_product_names()
    
    def filter_products_by_price_range(self, min_price: float = None, max_price: float = None):
        """根据价格范围筛选产品（示例方法）"""
        prices = self.get_product_prices()
        filtered_products = []
        
        for i, price_text in enumerate(prices):
            # 提取价格数值（移除$符号）
            try:
                price_value = float(price_text.replace('$', '').strip())
                if min_price and price_value < min_price:
                    continue
                if max_price and price_value > max_price:
                    continue
                filtered_products.append(i)
            except ValueError:
                continue
        
        return filtered_products


class BaiduOperations:
    """百度搜索业务操作封装"""
    
    def __init__(self, ui_ops: UIOperations):
        """
        初始化百度操作
        
        Args:
            ui_ops: UIOperations实例
        """
        self.ui = ui_ops
        self.locators = BaiduLocators()
    
    def search(self, keyword: str):
        """执行搜索"""
        self.ui.fill(self.locators.SEARCH_INPUT, keyword)
        self.ui.click(self.locators.SEARCH_BUTTON)
        self.ui.wait_for_element(self.locators.SEARCH_RESULTS_CONTAINER, timeout=10000)
    
    def verify_search_results_exist(self):
        """验证搜索结果存在"""
        self.ui.assert_element_exists(self.locators.SEARCH_RESULTS_CONTAINER)
        results = self.ui.get_element_count(self.locators.SEARCH_RESULT_ITEM)
        if results == 0:
            raise AssertionError("搜索结果为空")
    
    def verify_search_results_contain_keyword(self, keyword: str, check_count: int = 5):
        """验证搜索结果包含关键词"""
        titles = self.ui.get_all_texts(self.locators.SEARCH_RESULT_TITLE)
        found = False
        for title in titles[:check_count]:
            if keyword in title:
                found = True
                break
        if not found:
            raise AssertionError(f"搜索结果中未找到关键词: {keyword}")
    
    def get_search_result_count(self) -> int:
        """获取搜索结果数量"""
        return self.ui.get_element_count(self.locators.SEARCH_RESULT_ITEM)
    
    def complete_search_flow(self, keyword: str):
        """完整的搜索流程"""
        self.search(keyword)
        self.verify_search_results_exist()
        self.verify_search_results_contain_keyword(keyword)
