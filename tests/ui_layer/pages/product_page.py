# -*- coding: utf-8 -*-
"""
产品列表页面对象
封装产品列表页面的所有操作
"""

from robot.api.deco import keyword
from robot.api import logger
from .base_page import BasePage
from ..locators.saucedemo_locators import SauceDemoLocators


class ProductPage(BasePage):
    """产品列表页面对象"""
    
    def __init__(self, base_keywords=None):
        super().__init__(base_keywords)
        self.locators = SauceDemoLocators()
    
    @keyword("验证产品页面已加载")
    def verify_product_page_loaded(self):
        """验证产品页面已加载"""
        self.wait_for_element(self.locators.PRODUCTS_CONTAINER)
        self.element_should_exist(self.locators.PRODUCTS_CONTAINER)
        logger.info("产品页面已加载")
    
    @keyword("获取产品列表")
    def get_product_list(self):
        """获取产品列表元素"""
        products = self.page.query_selector_all(self.locators.PRODUCT_ITEM)
        logger.info(f"找到 {len(products)} 个产品")
        return products
    
    @keyword("获取产品数量")
    def get_product_count(self):
        """获取产品数量"""
        count = self.get_element_count(self.locators.PRODUCT_ITEM)
        logger.info(f"产品数量: {count}")
        return count
    
    @keyword("点击添加产品到购物车")
    def click_add_product_to_cart(self, product_index=0):
        """点击指定产品的添加到购物车按钮"""
        products = self.get_product_list()
        if product_index >= len(products):
            raise IndexError(f"产品索引超出范围: {product_index}，共有 {len(products)} 个产品")
        
        product = products[product_index]
        add_btn = product.query_selector(self.locators.PRODUCT_ADD_BTN)
        if not add_btn:
            raise ValueError(f"产品 {product_index} 没有找到添加按钮")
        add_btn.click()
        logger.info(f"已添加产品 {product_index} 到购物车")
    
    @keyword("移除产品从购物车")
    def remove_product_from_cart(self, product_index=0):
        """从购物车移除指定产品"""
        products = self.get_product_list()
        if product_index >= len(products):
            raise IndexError(f"产品索引超出范围: {product_index}")
        
        product = products[product_index]
        remove_btn = product.query_selector(self.locators.PRODUCT_REMOVE_BTN)
        if remove_btn:
            remove_btn.click()
            logger.info(f"已移除产品 {product_index} 从购物车")
        else:
            logger.warn(f"产品 {product_index} 未在购物车中")
    
    @keyword("获取产品名称")
    def get_product_name(self, product_index=0):
        """获取指定产品的名称"""
        products = self.get_product_list()
        if product_index >= len(products):
            raise IndexError(f"产品索引超出范围: {product_index}")
        
        product = products[product_index]
        name_element = product.query_selector(self.locators.PRODUCT_NAME)
        if not name_element:
            raise ValueError(f"产品 {product_index} 没有找到名称元素")
        name = name_element.text_content()
        logger.info(f"产品 {product_index} 名称: {name}")
        return name
    
    @keyword("获取产品价格")
    def get_product_price(self, product_index=0):
        """获取指定产品的价格"""
        products = self.get_product_list()
        if product_index >= len(products):
            raise IndexError(f"产品索引超出范围: {product_index}")
        
        product = products[product_index]
        price_element = product.query_selector(self.locators.PRODUCT_PRICE)
        if not price_element:
            raise ValueError(f"产品 {product_index} 没有找到价格元素")
        price_text = price_element.text_content()
        logger.info(f"产品 {product_index} 价格: {price_text}")
        return price_text
    
    @keyword("添加多个产品到购物车")
    def add_multiple_products_to_cart(self, *product_indices):
        """添加多个产品到购物车
        
        Args:
            *product_indices: 产品索引列表，例如: 0, 1, 2
        """
        for index in product_indices:
            self.click_add_product_to_cart(int(index))
        logger.info(f"已添加 {len(product_indices)} 个产品到购物车")
    
    @keyword("选择排序方式")
    def select_sort_option(self, sort_value):
        """选择产品排序方式
        
        Args:
            sort_value: 排序值，例如: 'az' (名称A-Z), 'za' (名称Z-A), 
                       'lohi' (价格低到高), 'hilo' (价格高到低)
        """
        self.select_option(self.locators.SORT_DROPDOWN, sort_value)
        logger.info(f"已选择排序方式: {sort_value}")
        # 等待排序完成
        self.wait_for_element(self.locators.PRODUCTS_CONTAINER)
    
    @keyword("验证产品已排序")
    def verify_products_sorted(self, sort_type='az'):
        """验证产品是否按指定方式排序"""
        products = self.get_product_list()
        if len(products) < 2:
            logger.info("产品数量少于2个，无需验证排序")
            return
        
        product_names = []
        for i in range(len(products)):
            name = self.get_product_name(i)
            product_names.append(name)
        
        sorted_names = sorted(product_names) if sort_type == 'az' else sorted(product_names, reverse=True)
        if product_names != sorted_names:
            raise AssertionError(f"产品未按 {sort_type} 排序")
        logger.info(f"产品排序验证通过: {sort_type}")
