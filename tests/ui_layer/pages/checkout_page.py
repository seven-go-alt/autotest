# -*- coding: utf-8 -*-
"""
结账页面对象
封装结账页面的所有操作
"""

from robot.api.deco import keyword
from robot.api import logger
from .base_page import BasePage
from ..locators.saucedemo_locators import SauceDemoLocators


class CheckoutPage(BasePage):
    """结账页面对象"""
    
    def __init__(self, base_keywords=None):
        super().__init__(base_keywords)
        self.locators = SauceDemoLocators()
    
    @keyword("验证结账信息页面已加载")
    def verify_checkout_info_page_loaded(self):
        """验证结账信息填写页面已加载"""
        self.element_should_exist(self.locators.CHECKOUT_FIRST_NAME)
        self.element_should_exist(self.locators.CHECKOUT_LAST_NAME)
        self.element_should_exist(self.locators.CHECKOUT_POSTAL_CODE)
        logger.info("结账信息页面已加载")
    
    @keyword("输入名字")
    def enter_first_name(self, first_name):
        """输入名字"""
        self.input_text(self.locators.CHECKOUT_FIRST_NAME, first_name)
        logger.info(f"已输入名字: {first_name}")
    
    @keyword("输入姓氏")
    def enter_last_name(self, last_name):
        """输入姓氏"""
        self.input_text(self.locators.CHECKOUT_LAST_NAME, last_name)
        logger.info(f"已输入姓氏: {last_name}")
    
    @keyword("输入邮政编码")
    def enter_postal_code(self, postal_code):
        """输入邮政编码"""
        self.input_text(self.locators.CHECKOUT_POSTAL_CODE, postal_code)
        logger.info(f"已输入邮政编码: {postal_code}")
    
    @keyword("填写结账信息")
    def fill_checkout_information(self, first_name, last_name, postal_code):
        """填写完整的结账信息"""
        self.enter_first_name(first_name)
        self.enter_last_name(last_name)
        self.enter_postal_code(postal_code)
        logger.info(f"已填写结账信息: {first_name} {last_name}, {postal_code}")
    
    @keyword("点击继续按钮")
    def click_continue_button(self):
        """点击继续按钮进入结账确认页面"""
        self.click(self.locators.CHECKOUT_CONTINUE_BTN)
        self.wait_for_page_load()
        logger.info("已点击继续按钮")
    
    @keyword("验证结账确认页面已加载")
    def verify_checkout_overview_loaded(self):
        """验证结账确认页面已加载"""
        self.element_should_exist(self.locators.CHECKOUT_FINISH_BTN)
        logger.info("结账确认页面已加载")
    
    @keyword("点击完成按钮")
    def click_finish_button(self):
        """点击完成按钮完成订单"""
        self.click(self.locators.CHECKOUT_FINISH_BTN)
        self.wait_for_page_load()
        logger.info("已点击完成按钮")
    
    @keyword("验证订单完成")
    def verify_order_complete(self, expected_message="Thank you"):
        """验证订单完成提示信息"""
        self.wait_for_element(self.locators.ORDER_COMPLETE_MSG)
        self.element_should_exist(self.locators.ORDER_COMPLETE_MSG)
        if expected_message:
            self.text_should_contain(self.locators.ORDER_COMPLETE_MSG, expected_message)
        logger.info("订单完成验证通过")
    
    @keyword("获取订单完成消息")
    def get_order_complete_message(self):
        """获取订单完成消息文本"""
        message = self.get_text(self.locators.ORDER_COMPLETE_MSG)
        logger.info(f"订单完成消息: {message}")
        return message
