# -*- coding: utf-8 -*-
"""
UI操作封装层 - 供Python用例使用
将底层操作封装成高级操作，使用例专注于业务逻辑
"""

from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext
from typing import Optional, List
import config.settings as settings


class UIOperations:
    """UI操作封装类 - 提供高级操作接口"""
    
    def __init__(self, browser_type: str = "chromium", headless: bool = False):
        """
        初始化UI操作
        
        Args:
            browser_type: 浏览器类型 (chromium/firefox/webkit)
            headless: 是否无头模式
        """
        self.browser_type = browser_type
        self.headless = headless
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
    
    def start_browser(self, url: Optional[str] = None):
        """启动浏览器并可选导航到URL"""
        self.playwright = sync_playwright().start()
        
        browser_map = {
            "chromium": self.playwright.chromium,
            "firefox": self.playwright.firefox,
            "webkit": self.playwright.webkit
        }
        
        browser_launcher = browser_map.get(self.browser_type)
        if not browser_launcher:
            raise ValueError(f"不支持的浏览器类型: {self.browser_type}")
        
        self.browser = browser_launcher.launch(headless=self.headless)
        
        viewport = settings.BROWSER_OPTIONS.get("chrome", {}).get("window_size", (1920, 1080))
        self.context = self.browser.new_context(
            viewport={"width": viewport[0], "height": viewport[1]},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        )
        
        self.page = self.context.new_page()
        
        if url:
            self.navigate_to(url)
        
        return self.page
    
    def close_browser(self):
        """关闭浏览器"""
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
    
    # ========== 基础操作 ==========
    
    def navigate_to(self, url: str):
        """导航到URL"""
        self._ensure_page()
        self.page.goto(url)
    
    def click(self, locator: str, timeout: int = None):
        """点击元素"""
        self._ensure_page()
        timeout_ms = (timeout or settings.TIMEOUT) * 1000
        self.page.click(locator, timeout=timeout_ms)
    
    def fill(self, locator: str, text: str, timeout: int = None):
        """填充输入框"""
        self._ensure_page()
        timeout_ms = (timeout or settings.TIMEOUT) * 1000
        self.page.fill(locator, text, timeout=timeout_ms)
    
    def get_text(self, locator: str, timeout: int = None) -> str:
        """获取元素文本"""
        self._ensure_page()
        timeout_ms = (timeout or settings.TIMEOUT) * 1000
        return self.page.text_content(locator, timeout=timeout_ms) or ""
    
    def wait_for_element(self, locator: str, timeout: int = None, state: str = "visible"):
        """等待元素出现"""
        self._ensure_page()
        timeout_ms = (timeout or settings.TIMEOUT) * 1000
        self.page.wait_for_selector(locator, timeout=timeout_ms, state=state)
    
    def is_element_visible(self, locator: str, timeout: int = 5000) -> bool:
        """检查元素是否可见"""
        self._ensure_page()
        try:
            self.page.wait_for_selector(locator, timeout=timeout, state="visible")
            return True
        except:
            return False
    
    def get_element_count(self, locator: str) -> int:
        """获取匹配的元素数量"""
        self._ensure_page()
        return len(self.page.query_selector_all(locator))
    
    # ========== 高级操作 ==========
    
    def fill_form(self, form_data: dict):
        """填充表单（字典形式）"""
        for locator, value in form_data.items():
            self.fill(locator, str(value))
    
    def click_multiple(self, locators: List[str], wait_between: float = 0.5):
        """依次点击多个元素"""
        import time
        for locator in locators:
            self.click(locator)
            time.sleep(wait_between)
    
    def get_all_texts(self, locator: str) -> List[str]:
        """获取所有匹配元素的文本列表"""
        self._ensure_page()
        elements = self.page.query_selector_all(locator)
        return [elem.text_content() or "" for elem in elements]
    
    def select_option(self, locator: str, value: str):
        """选择下拉框选项"""
        self._ensure_page()
        self.page.select_option(locator, value)
    
    def scroll_to_element(self, locator: str):
        """滚动到元素"""
        self._ensure_page()
        self.page.locator(locator).scroll_into_view_if_needed()
    
    def take_screenshot(self, filename: str = "screenshot.png"):
        """截图"""
        self._ensure_page()
        filepath = settings.REPORTS_DIR / filename
        self.page.screenshot(path=str(filepath))
        return filepath
    
    def get_page_title(self) -> str:
        """获取页面标题"""
        self._ensure_page()
        return self.page.title()
    
    def get_current_url(self) -> str:
        """获取当前URL"""
        self._ensure_page()
        return self.page.url
    
    def wait_for_url_contains(self, url_part: str, timeout: int = 30000):
        """等待URL包含指定部分"""
        self._ensure_page()
        self.page.wait_for_url(f"*{url_part}*", timeout=timeout)
    
    def wait_for_text(self, text: str, timeout: int = 30000):
        """等待页面出现指定文本"""
        self._ensure_page()
        self.page.wait_for_selector(f"text={text}", timeout=timeout)
    
    # ========== 验证操作 ==========
    
    def assert_element_exists(self, locator: str, timeout: int = 5000):
        """断言元素存在"""
        if not self.is_element_visible(locator, timeout):
            raise AssertionError(f"元素不存在: {locator}")
    
    def assert_text_contains(self, locator: str, expected_text: str):
        """断言元素文本包含指定内容"""
        actual_text = self.get_text(locator)
        if expected_text not in actual_text:
            raise AssertionError(f"文本不匹配。期望包含: {expected_text}，实际: {actual_text}")
    
    def assert_text_equals(self, locator: str, expected_text: str):
        """断言元素文本等于指定内容"""
        actual_text = self.get_text(locator)
        if actual_text.strip() != expected_text.strip():
            raise AssertionError(f"文本不匹配。期望: '{expected_text}'，实际: '{actual_text}'")
    
    def assert_element_count(self, locator: str, expected_count: int):
        """断言元素数量"""
        actual_count = self.get_element_count(locator)
        if actual_count != expected_count:
            raise AssertionError(f"元素数量不匹配。期望: {expected_count}，实际: {actual_count}")
    
    def assert_url_contains(self, expected_url_part: str):
        """断言URL包含指定部分"""
        actual_url = self.get_current_url()
        if expected_url_part not in actual_url:
            raise AssertionError(f"URL不包含: {expected_url_part}，实际: {actual_url}")
    
    def assert_page_title_contains(self, expected_text: str):
        """断言页面标题包含指定文本"""
        title = self.get_page_title()
        if expected_text not in title:
            raise AssertionError(f"页面标题不包含: {expected_text}，实际: {title}")
    
    # ========== 辅助方法 ==========
    
    def _ensure_page(self):
        """确保页面已初始化"""
        if not self.page:
            raise RuntimeError("浏览器未初始化，请先调用 start_browser()")
    
    def __enter__(self):
        """上下文管理器入口"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.close_browser()
