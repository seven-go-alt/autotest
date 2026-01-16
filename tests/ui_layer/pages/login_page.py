# -*- coding: utf-8 -*-
"""
登录页面对象
封装登录页面的所有操作
"""

from robot.api.deco import keyword
from robot.api import logger
from .base_page import BasePage
from ..locators.saucedemo_locators import SauceDemoLocators


class LoginPage(BasePage):
    """登录页面对象"""
    
    def __init__(self, base_keywords=None):
        super().__init__(base_keywords)
        self.locators = SauceDemoLocators()
    
    @keyword("输入用户名")
    def enter_username(self, username):
        """输入用户名"""
        self.input_text(self.locators.LOGIN_USERNAME_INPUT, username)
        logger.info(f"已输入用户名: {username}")
    
    @keyword("输入密码")
    def enter_password(self, password):
        """输入密码"""
        self.input_text(self.locators.LOGIN_PASSWORD_INPUT, password)
        logger.info("已输入密码")
    
    @keyword("点击登录按钮")
    def click_login_button(self):
        """点击登录按钮"""
        self.click(self.locators.LOGIN_BUTTON)
        logger.info("已点击登录按钮")
    
    @keyword("执行登录操作")
    def perform_login(self, username, password):
        """执行完整的登录操作"""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()
        logger.info(f"已执行登录操作: {username}")
    
    @keyword("验证登录错误提示")
    def verify_login_error(self, expected_error_message=None):
        """验证登录错误提示是否存在"""
        self.element_should_exist(self.locators.LOGIN_ERROR_CONTAINER)
        if expected_error_message:
            self.text_should_contain(self.locators.LOGIN_ERROR_CONTAINER, expected_error_message)
        logger.info("登录错误提示验证通过")
    
    @keyword("获取登录错误消息")
    def get_login_error_message(self):
        """获取登录错误消息文本"""
        error_text = self.get_text(self.locators.LOGIN_ERROR_CONTAINER)
        logger.info(f"登录错误消息: {error_text}")
        return error_text
    
    @keyword("验证登录页面显示")
    def verify_login_page_displayed(self):
        """验证登录页面已显示"""
        self.element_should_exist(self.locators.LOGIN_USERNAME_INPUT)
        self.element_should_exist(self.locators.LOGIN_PASSWORD_INPUT)
        self.element_should_exist(self.locators.LOGIN_BUTTON)
        logger.info("登录页面已显示")
