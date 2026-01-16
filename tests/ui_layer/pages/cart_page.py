# -*- coding: utf-8 -*-
"""
购物车页面对象
封装购物车页面的所有操作
"""

from robot.api.deco import keyword
from robot.api import logger
from .base_page import BasePage
from ..locators.saucedemo_locators import SauceDemoLocators


class CartPage(BasePage):
    """购物车页面对象"""
    
    def __init__(self, base_keywords=None):
        super().__init__(base_keywords)
        self.locators = SauceDemoLocators()
    
    @keyword("导航到购物车")
    def navigate_to_cart(self):
        """点击购物车图标导航到购物车页面"""
        self.click(self.locators.SHOPPING_CART_LINK)
        self.wait_for_page_load()
        logger.info("已导航到购物车页面")
    
    @keyword("验证购物车页面已加载")
    def verify_cart_page_loaded(self):
        """验证购物车页面已加载"""
        self.element_should_exist(self.locators.CHECKOUT_BUTTON)
        logger.info("购物车页面已加载")
    
    @keyword("获取购物车商品数量")
    def get_cart_item_count(self):
        """获取购物车中的商品数量"""
        count = self.get_element_count(self.locators.CART_ITEM)
        logger.info(f"购物车商品数量: {count}")
        return count
    
    @keyword("验证购物车商品数量")
    def verify_cart_item_count(self, expected_count):
        """验证购物车中的商品数量"""
        actual_count = self.get_cart_item_count()
        if int(actual_count) != int(expected_count):
            raise AssertionError(f"购物车商品数量不匹配。期望: {expected_count}，实际: {actual_count}")
        logger.info(f"购物车商品数量验证通过: {actual_count}")
    
    @keyword("获取购物车徽章数量")
    def get_cart_badge_count(self):
        """获取购物车图标上的徽章数量"""
        try:
            badge = self.page.query_selector(self.locators.SHOPPING_CART_BADGE)
            if badge:
                count_text = badge.text_content()
                count = int(count_text) if count_text else 0
                logger.info(f"购物车徽章数量: {count}")
                return count
            else:
                logger.info("购物车徽章不存在（购物车为空）")
                return 0
        except Exception as e:
            logger.info(f"获取购物车徽章数量失败: {e}")
            return 0
    
    @keyword("验证购物车徽章数量")
    def verify_cart_badge_count(self, expected_count):
        """验证购物车图标上的徽章数量"""
        actual_count = self.get_cart_badge_count()
        if int(actual_count) != int(expected_count):
            raise AssertionError(f"购物车徽章数量不匹配。期望: {expected_count}，实际: {actual_count}")
        logger.info(f"购物车徽章数量验证通过: {actual_count}")
    
    @keyword("点击结账按钮")
    def click_checkout_button(self):
        """点击结账按钮"""
        self.click(self.locators.CHECKOUT_BUTTON)
        logger.info("已点击结账按钮")
    
    @keyword("点击继续购物按钮")
    def click_continue_shopping_button(self):
        """点击继续购物按钮"""
        self.click(self.locators.CONTINUE_SHOPPING_BTN)
        logger.info("已点击继续购物按钮")
    
    @keyword("移除购物车中的商品")
    def remove_cart_item(self, item_index=0):
        """移除购物车中指定索引的商品"""
        items = self.page.query_selector_all(self.locators.CART_ITEM)
        if item_index >= len(items):
            raise IndexError(f"商品索引超出范围: {item_index}")
        
        item = items[item_index]
        # 查找移除按钮（在购物车页面中）
        remove_btn = item.query_selector("css=.cart_button")
        if remove_btn:
            remove_btn.click()
            logger.info(f"已移除购物车中的商品 {item_index}")
        else:
            raise ValueError(f"商品 {item_index} 没有找到移除按钮")
    
    @keyword("验证购物车为空")
    def verify_cart_is_empty(self):
        """验证购物车为空"""
        count = self.get_cart_item_count()
        if count != 0:
            raise AssertionError(f"购物车不为空，包含 {count} 个商品")
        logger.info("购物车为空验证通过")
