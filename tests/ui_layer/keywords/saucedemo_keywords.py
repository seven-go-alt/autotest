# -*- coding: utf-8 -*-
"""
SauceDemo 应用关键字库
- 登录操作
- 产品购买流程
- 购物车操作
"""

from robot.api.deco import keyword
from robot.api import logger
from .base_keywords import BaseKeywords
from ..locators.saucedemo_locators import SauceDemoLocators


class SauceDemoKeywords(BaseKeywords):
    """SauceDemo 应用的业务关键字"""
    
    def __init__(self):
        super().__init__()
        self.locators = SauceDemoLocators()
    
    @keyword("登录 SauceDemo")
    def login_saucedemo(self, username, password):
        """使用用户名和密码登录 SauceDemo"""
        self.input_text(self.locators.LOGIN_USERNAME_INPUT, username)
        self.input_text(self.locators.LOGIN_PASSWORD_INPUT, password)
        self.click(self.locators.LOGIN_BUTTON)
        logger.info(f"已使用用户 {username} 登录")
    
    @keyword("添加产品到购物车")
    def add_product_to_cart(self, product_index=0):
        """添加产品到购物车"""
        products = self.page.query_selector_all(self.locators.PRODUCT_ITEM)
        if product_index >= len(products):
            raise IndexError(f"产品索引超出范围: {product_index}")
        
        product = products[product_index]
        add_btn = product.query_selector(self.locators.PRODUCT_ADD_BTN)
        add_btn.click()
        logger.info(f"已添加产品 {product_index} 到购物车")
    
    @keyword("验证购物车数量")
    def verify_cart_count(self, expected_count):
        """验证购物车中的产品数量"""
        count_text = self.get_text(self.locators.SHOPPING_CART_BADGE)
        if int(count_text) != int(expected_count):
            raise AssertionError(f"购物车数量不匹配。期望: {expected_count}，实际: {count_text}")
        logger.info(f"购物车数量验证通过: {count_text}")
    
    @keyword("前往购物车")
    def go_to_cart(self):
        """点击购物车链接"""
        self.click(self.locators.SHOPPING_CART_LINK)
        logger.info("已导航到购物车页面")
    
    @keyword("前往结账")
    def go_to_checkout(self):
        """点击结账按钮"""
        self.click(self.locators.CHECKOUT_BUTTON)
        logger.info("已前往结账页面")
    
    @keyword("填写结账信息")
    def fill_checkout_info(self, first_name, last_name, postal_code):
        """填写结账表单信息"""
        self.input_text(self.locators.CHECKOUT_FIRST_NAME, first_name)
        self.input_text(self.locators.CHECKOUT_LAST_NAME, last_name)
        self.input_text(self.locators.CHECKOUT_POSTAL_CODE, postal_code)
        logger.info(f"已填写结账信息: {first_name} {last_name}")
    
    @keyword("完成结账")
    def finish_checkout(self):
        """点击完成结账按钮"""
        self.click(self.locators.CHECKOUT_CONTINUE_BTN)
        self.click(self.locators.CHECKOUT_FINISH_BTN)
        logger.info("已完成结账")
    
    @keyword("验证订单完成")
    def verify_order_complete(self):
        """验证订单完成提示信息"""
        self.element_should_exist(self.locators.ORDER_COMPLETE_MSG)
        self.text_should_contain(self.locators.ORDER_COMPLETE_MSG, "Thank you")
        logger.info("订单完成验证通过")
    
    @keyword("退出登录")
    def logout(self):
        """退出登录"""
        self.click(self.locators.HAMBURGER_MENU)
        self.click(self.locators.MENU_LOGOUT)
        logger.info("已退出登录")
