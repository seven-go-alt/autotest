# -*- coding: utf-8 -*-
"""
基础页面对象
所有页面对象的基类，提供通用的页面操作方法
"""

from robot.api.deco import keyword
from robot.api import logger
from ..keywords.base_keywords import BaseKeywords


class BasePage(BaseKeywords):
    """基础页面对象 - 所有页面的基类"""
    
    def __init__(self, base_keywords=None):
        """初始化页面对象
        
        Args:
            base_keywords: BaseKeywords 实例，如果提供则共享浏览器实例
        """
        if base_keywords:
            # 共享浏览器实例
            self.page = base_keywords.page
            self.browser = base_keywords.browser
            self.context = base_keywords.context
            self.playwright = base_keywords.playwright
        else:
            super().__init__()
    
    @keyword("页面应该包含文本")
    def page_should_contain_text(self, text, timeout=5000):
        """验证页面包含指定文本"""
        if not self.page:
            raise RuntimeError("浏览器未初始化")
        self.page.wait_for_load_state("networkidle", timeout=timeout)
        content = self.page.content()
        if text not in content:
            raise AssertionError(f"页面不包含文本: {text}")
        logger.info(f"页面包含文本: {text}")
    
    @keyword("页面标题应该是")
    def page_title_should_be(self, expected_title):
        """验证页面标题"""
        actual_title = self.get_page_title()
        if actual_title != expected_title:
            raise AssertionError(f"页面标题不匹配。期望: {expected_title}，实际: {actual_title}")
        logger.info(f"页面标题验证通过: {actual_title}")
    
    @keyword("页面URL应该包含")
    def page_url_should_contain(self, expected_url_part):
        """验证页面URL包含指定部分"""
        if not self.page:
            raise RuntimeError("浏览器未初始化")
        actual_url = self.page.url
        if expected_url_part not in actual_url:
            raise AssertionError(f"URL不包含: {expected_url_part}，实际: {actual_url}")
        logger.info(f"URL验证通过: {actual_url} 包含 {expected_url_part}")
    
    @keyword("等待页面加载完成")
    def wait_for_page_load(self, timeout=30000):
        """等待页面加载完成"""
        if not self.page:
            raise RuntimeError("浏览器未初始化")
        self.page.wait_for_load_state("networkidle", timeout=timeout)
        logger.info("页面加载完成")
    
    @keyword("获取当前URL")
    def get_current_url(self):
        """获取当前页面URL"""
        if not self.page:
            raise RuntimeError("浏览器未初始化")
        url = self.page.url
        logger.info(f"当前URL: {url}")
        return url
    
    @keyword("返回上一页")
    def go_back(self):
        """返回上一页"""
        if not self.page:
            raise RuntimeError("浏览器未初始化")
        self.page.go_back()
        logger.info("已返回上一页")
    
    @keyword("获取元素数量")
    def get_element_count(self, locator):
        """获取匹配的元素数量"""
        if not self.page:
            raise RuntimeError("浏览器未初始化")
        count = len(self.page.query_selector_all(locator))
        logger.info(f"元素数量 {locator}: {count}")
        return count
    
    @keyword("元素数量应该是")
    def element_count_should_be(self, locator, expected_count):
        """验证元素数量"""
        actual_count = self.get_element_count(locator)
        if int(actual_count) != int(expected_count):
            raise AssertionError(f"元素数量不匹配。期望: {expected_count}，实际: {actual_count}")
        logger.info(f"元素数量验证通过: {actual_count}")
