# -*- coding: utf-8 -*-
"""
菜单页面对象
封装侧边栏菜单的所有操作
"""

from robot.api.deco import keyword
from robot.api import logger
from .base_page import BasePage
from ..locators.saucedemo_locators import SauceDemoLocators


class MenuPage(BasePage):
    """菜单页面对象"""
    
    def __init__(self, base_keywords=None):
        super().__init__(base_keywords)
        self.locators = SauceDemoLocators()
    
    @keyword("打开菜单")
    def open_menu(self):
        """打开侧边栏菜单"""
        self.click(self.locators.HAMBURGER_MENU)
        # 等待菜单动画完成
        self.wait_for_element(self.locators.MENU_LOGOUT)
        logger.info("已打开菜单")
    
    @keyword("点击退出登录")
    def click_logout(self):
        """点击退出登录菜单项"""
        self.open_menu()
        self.click(self.locators.MENU_LOGOUT)
        self.wait_for_page_load()
        logger.info("已退出登录")
    
    @keyword("导航到产品列表")
    def navigate_to_inventory(self):
        """从菜单导航到产品列表"""
        self.open_menu()
        self.click(self.locators.MENU_INVENTORY)
        self.wait_for_page_load()
        logger.info("已导航到产品列表")
    
    @keyword("导航到购物车")
    def navigate_to_cart_from_menu(self):
        """从菜单导航到购物车"""
        self.open_menu()
        self.click(self.locators.MENU_CART)
        self.wait_for_page_load()
        logger.info("已从菜单导航到购物车")
