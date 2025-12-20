# -*- coding: utf-8 -*-
"""
基础关键字库：通用的 UI 交互操作
- 浏览器操作
- 元素交互
- 等待和验证
"""

from robot.api.deco import keyword
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn
from playwright.sync_api import sync_playwright, expect


class BaseKeywords:
    """基础关键字库 - 通用 UI 操作"""
    
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    
    def __init__(self):
        self.page = None
        self.browser = None
        self.context = None
        self.playwright = None
    
    @keyword("打开浏览器")
    def open_browser(self, url, browser_type="chromium"):
        """打开浏览器并导航到指定 URL"""
        try:
            self.playwright = sync_playwright().start()
            if browser_type == "chromium":
                self.browser = self.playwright.chromium.launch(headless=False)
            elif browser_type == "firefox":
                self.browser = self.playwright.firefox.launch(headless=False)
            elif browser_type == "webkit":
                self.browser = self.playwright.webkit.launch(headless=False)
            
            self.context = self.browser.new_context()
            self.page = self.context.new_page()
            self.page.goto(url)
            logger.info(f"浏览器已打开，访问 URL: {url}")
        except Exception as e:
            logger.error(f"打开浏览器失败: {str(e)}")
            raise
    
    @keyword("关闭浏览器")
    def close_browser(self):
        """关闭浏览器"""
        try:
            if self.page:
                self.page.close()
            if self.context:
                self.context.close()
            if self.browser:
                self.browser.close()
            if self.playwright:
                self.playwright.stop()
            logger.info("浏览器已关闭")
        except Exception as e:
            logger.error(f"关闭浏览器失败: {str(e)}")
            raise
    
    @keyword("导航到")
    def navigate_to(self, url):
        """导航到指定 URL"""
        if not self.page:
            raise RuntimeError("浏览器未初始化")
        self.page.goto(url)
        logger.info(f"导航到: {url}")
    
    @keyword("点击")
    def click(self, locator):
        """点击元素"""
        if not self.page:
            raise RuntimeError("浏览器未初始化")
        self.page.click(locator)
        logger.info(f"点击元素: {locator}")
    
    @keyword("输入")
    def input_text(self, locator, text):
        """在输入框中输入文本"""
        if not self.page:
            raise RuntimeError("浏览器未初始化")
        self.page.fill(locator, text)
        logger.info(f"输入文本 '{text}' 到: {locator}")
    
    @keyword("清空输入框")
    def clear_input(self, locator):
        """清空输入框"""
        if not self.page:
            raise RuntimeError("浏览器未初始化")
        self.page.fill(locator, "")
        logger.info(f"清空输入框: {locator}")
    
    @keyword("获取文本")
    def get_text(self, locator):
        """获取元素的文本内容"""
        if not self.page:
            raise RuntimeError("浏览器未初始化")
        text = self.page.text_content(locator)
        logger.info(f"获取文本: {locator} = {text}")
        return text
    
    @keyword("验证元素存在")
    def element_should_exist(self, locator):
        """验证元素存在"""
        if not self.page:
            raise RuntimeError("浏览器未初始化")
        element = self.page.query_selector(locator)
        if not element:
            raise AssertionError(f"元素不存在: {locator}")
        logger.info(f"元素存在: {locator}")
    
    @keyword("验证文本包含")
    def text_should_contain(self, locator, expected_text):
        """验证元素文本包含指定内容"""
        if not self.page:
            raise RuntimeError("浏览器未初始化")
        text = self.page.text_content(locator)
        if expected_text not in text:
            raise AssertionError(f"文本不匹配。期望包含: {expected_text}，实际: {text}")
        logger.info(f"文本验证通过: {locator} 包含 '{expected_text}'")
    
    @keyword("等待元素出现")
    def wait_for_element(self, locator, timeout=5000):
        """等待元素出现"""
        if not self.page:
            raise RuntimeError("浏览器未初始化")
        self.page.wait_for_selector(locator, timeout=timeout)
        logger.info(f"元素已出现: {locator}")
    
    @keyword("获取属性值")
    def get_attribute(self, locator, attribute):
        """获取元素的属性值"""
        if not self.page:
            raise RuntimeError("浏览器未初始化")
        value = self.page.get_attribute(locator, attribute)
        logger.info(f"获取属性: {locator} - {attribute} = {value}")
        return value
    
    @keyword("选择下拉框选项")
    def select_option(self, locator, option_value):
        """选择下拉框的选项"""
        if not self.page:
            raise RuntimeError("浏览器未初始化")
        self.page.select_option(locator, option_value)
        logger.info(f"选择选项: {locator} - {option_value}")
    
    @keyword("获取页面标题")
    def get_page_title(self):
        """获取页面标题"""
        if not self.page:
            raise RuntimeError("浏览器未初始化")
        title = self.page.title()
        logger.info(f"页面标题: {title}")
        return title
    
    @keyword("刷新页面")
    def reload_page(self):
        """刷新页面"""
        if not self.page:
            raise RuntimeError("浏览器未初始化")
        self.page.reload()
        logger.info("页面已刷新")
