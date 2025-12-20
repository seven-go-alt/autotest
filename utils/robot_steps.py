# -*- coding: utf-8 -*-
"""
步骤层（操作层）：包装基础操作，如点击、填充、等待等
- 基于定位器层与 Playwright Helper
- 提供复用的基础操作
"""
from robot.api.deco import keyword
from robot.api import logger
from utils.playwright_helper import PlaywrightHelper
from utils.robot_locators import Locators

class StepsLibrary:
    """步骤层库：基础交互操作"""

    def __init__(self):
        self.helper = None
        self.locators = Locators()

    @keyword("Initialize Browser")
    def init_browser(self, browser_type="chromium", headless=True):
        """初始化浏览器"""
        self.helper = PlaywrightHelper(browser=browser_type, headless=headless)
        self.helper.start_browser()
        logger.info(f"Browser initialized: {browser_type}")

    @keyword("Navigate To")
    def navigate_to(self, url):
        """导航到 URL"""
        if not self.helper:
            raise RuntimeError("Browser not initialized")
        self.helper.navigate_to(url)
        logger.info(f"Navigated to: {url}")

    @keyword("Click Element By Name")
    def click_element_by_name(self, element_name):
        """按元素名称点击"""
        if not self.helper:
            raise RuntimeError("Browser not initialized")
        locator = self.locators.get_locator(element_name)
        self.helper.click(locator)
        logger.info(f"Clicked: {element_name}")

    @keyword("Fill Input By Name")
    def fill_input_by_name(self, element_name, text):
        """按元素名称填充输入框"""
        if not self.helper:
            raise RuntimeError("Browser not initialized")
        locator = self.locators.get_locator(element_name)
        self.helper.fill(locator, text)
        logger.info(f"Filled {element_name} with: {text}")

    @keyword("Wait For Element By Name")
    def wait_for_element_by_name(self, element_name, timeout=30):
        """等待元素出现"""
        if not self.helper:
            raise RuntimeError("Browser not initialized")
        locator = self.locators.get_locator(element_name)
        self.helper.wait_for_selector(locator, timeout=timeout)
        logger.info(f"Element found: {element_name}")

    @keyword("Get Page Title")
    def get_page_title(self):
        """获取页面标题"""
        if not self.helper:
            raise RuntimeError("Browser not initialized")
        return self.helper.get_title()

    @keyword("Get Element Text")
    def get_element_text(self, element_name):
        """获取元素文本"""
        if not self.helper:
            raise RuntimeError("Browser not initialized")
        locator = self.locators.get_locator(element_name)
        return self.helper.get_text(locator)

    @keyword("Take Screenshot")
    def take_screenshot(self, filename="screenshot.png"):
        """截图"""
        if not self.helper:
            raise RuntimeError("Browser not initialized")
        return self.helper.take_screenshot(filename)

    @keyword("Close Browser")
    def close_browser(self):
        """关闭浏览器"""
        if self.helper:
            self.helper.quit()
            self.helper = None
            logger.info("Browser closed")
