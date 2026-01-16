# -*- coding: utf-8 -*-
"""
UI操作封装层 - 供Python用例使用
将底层操作封装成高级操作，使用例专注于业务逻辑
"""

import logging
from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext, TimeoutError as PlaywrightTimeoutError
from typing import Optional, List, Dict, Any, Literal
import config.settings as settings
from utils.retry_decorator import retry_on_failure

logger = logging.getLogger(__name__)


class UIOperations:
    """UI操作封装类 - 提供高级操作接口"""
    
    def __init__(self, browser_type: str = "chromium", headless: bool = False, debug_mode: bool = False):
        """
        初始化UI操作
        
        Args:
            browser_type: 浏览器类型 (chromium/firefox/webkit)
            headless: 是否无头模式
            debug_mode: 调试模式（启用元素高亮和详细日志）
        """
        self.browser_type = browser_type
        self.headless = headless
        self.debug_mode = debug_mode
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self._screenshot_counter = 0
        
        logger.info(f"初始化 UIOperations: browser={browser_type}, headless={headless}, debug={debug_mode}")
    
    def start_browser(self, url: Optional[str] = None):
        """启动浏览器并可选导航到URL"""
        logger.info(f"启动浏览器: {self.browser_type}")
        self.playwright = sync_playwright().start()
        
        browser_map = {
            "chromium": self.playwright.chromium,
            "firefox": self.playwright.firefox,
            "webkit": self.playwright.webkit
        }
        
        browser_launcher = browser_map.get(self.browser_type)
        if not browser_launcher:
            raise ValueError(f"不支持的浏览器类型: {self.browser_type}")
        
        # 启动浏览器，调试模式下启用慢速模式
        launch_options = {"headless": self.headless}
        if self.debug_mode:
            launch_options["slow_mo"] = 100  # 慢速模式，便于观察
        
        self.browser = browser_launcher.launch(**launch_options)
        
        viewport = settings.BROWSER_OPTIONS.get("chrome", {}).get("window_size", (1920, 1080))
        self.context = self.browser.new_context(
            viewport={"width": viewport[0], "height": viewport[1]},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            record_video_dir=str(settings.REPORTS_DIR / "videos") if self.debug_mode else None,
        )
        
        self.page = self.context.new_page()
        logger.info("浏览器启动成功")
        
        if url:
            self.navigate_to(url)
        
        return self.page
    
    def close_browser(self):
        """关闭浏览器"""
        logger.info("关闭浏览器")
        try:
            if self.context:
                self.context.close()
            if self.browser:
                self.browser.close()
            if self.playwright:
                self.playwright.stop()
            logger.info("浏览器已关闭")
        except Exception as e:
            logger.error(f"关闭浏览器时出错: {e}")
    
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
    
    # ========== 增强功能 ==========
    
    def smart_wait(self, locator: str, condition: Literal["visible", "hidden", "attached", "detached"] = "visible", 
                   timeout: Optional[int] = None) -> bool:
        """
        智能等待 - 等待元素满足特定条件
        
        Args:
            locator: 元素定位器
            condition: 等待条件 (visible/hidden/attached/detached)
            timeout: 超时时间（秒）
        
        Returns:
            是否成功等待到元素
        """
        self._ensure_page()
        timeout_ms = (timeout or settings.TIMEOUT) * 1000
        try:
            self.page.wait_for_selector(locator, timeout=timeout_ms, state=condition)
            logger.debug(f"智能等待成功: {locator} ({condition})")
            return True
        except PlaywrightTimeoutError:
            logger.warning(f"智能等待超时: {locator} ({condition})")
            return False
    
    @retry_on_failure(max_attempts=3, delay=0.5, exceptions=(PlaywrightTimeoutError,))
    def click_with_retry(self, locator: str, timeout: Optional[int] = None):
        """
        带重试的点击操作 - 处理偶发性点击失败
        
        Args:
            locator: 元素定位器
            timeout: 超时时间（秒）
        """
        self._ensure_page()
        timeout_ms = (timeout or settings.TIMEOUT) * 1000
        
        if self.debug_mode:
            self.highlight_element(locator)
        
        self.page.click(locator, timeout=timeout_ms)
        logger.info(f"点击元素: {locator}")
    
    def highlight_element(self, locator: str, duration: float = 0.5):
        """
        高亮元素 - 调试模式下突出显示元素
        
        Args:
            locator: 元素定位器
            duration: 高亮持续时间（秒）
        """
        if not self.debug_mode:
            return
        
        self._ensure_page()
        try:
            self.page.evaluate(f"""
                (locator) => {{
                    const element = document.querySelector('{locator}'.replace('css=', '').replace('id=', '#'));
                    if (element) {{
                        element.style.border = '3px solid red';
                        element.style.backgroundColor = 'yellow';
                        setTimeout(() => {{
                            element.style.border = '';
                            element.style.backgroundColor = '';
                        }}, {duration * 1000});
                    }}
                }}
            """)
        except Exception as e:
            logger.debug(f"元素高亮失败: {e}")
    
    def auto_screenshot(self, name: Optional[str] = None) -> Path:
        """
        自动截图 - 保存当前页面截图
        
        Args:
            name: 截图文件名（可选）
        
        Returns:
            截图文件路径
        """
        self._ensure_page()
        
        if name is None:
            self._screenshot_counter += 1
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            name = f"screenshot_{timestamp}_{self._screenshot_counter}.png"
        
        if not name.endswith('.png'):
            name += '.png'
        
        filepath = settings.REPORTS_DIR / "screenshots" / name
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        self.page.screenshot(path=str(filepath), full_page=True)
        logger.info(f"截图已保存: {filepath}")
        
        return filepath
    
    def wait_for_network_idle(self, timeout: int = 30):
        """
        等待网络空闲 - 等待所有网络请求完成
        
        Args:
            timeout: 超时时间（秒）
        """
        self._ensure_page()
        try:
            self.page.wait_for_load_state("networkidle", timeout=timeout * 1000)
            logger.debug("网络已空闲")
        except PlaywrightTimeoutError:
            logger.warning(f"等待网络空闲超时: {timeout}秒")
    
    def execute_javascript(self, script: str) -> Any:
        """
        执行 JavaScript 代码
        
        Args:
            script: JavaScript 代码
        
        Returns:
            执行结果
        """
        self._ensure_page()
        result = self.page.evaluate(script)
        logger.debug(f"执行 JavaScript: {script[:50]}...")
        return result
    
    def get_attribute(self, locator: str, attribute: str) -> Optional[str]:
        """
        获取元素属性值
        
        Args:
            locator: 元素定位器
            attribute: 属性名
        
        Returns:
            属性值
        """
        self._ensure_page()
        return self.page.get_attribute(locator, attribute)
    
    def is_element_enabled(self, locator: str) -> bool:
        """
        检查元素是否可用
        
        Args:
            locator: 元素定位器
        
        Returns:
            是否可用
        """
        self._ensure_page()
        return self.page.is_enabled(locator)
    
    def wait_for_text_change(self, locator: str, initial_text: str, timeout: int = 10) -> bool:
        """
        等待元素文本变化
        
        Args:
            locator: 元素定位器
            initial_text: 初始文本
            timeout: 超时时间（秒）
        
        Returns:
            文本是否已变化
        """
        self._ensure_page()
        import time
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            current_text = self.get_text(locator)
            if current_text != initial_text:
                logger.debug(f"文本已变化: {initial_text} -> {current_text}")
                return True
            time.sleep(0.5)
        
        logger.warning(f"等待文本变化超时: {locator}")
        return False
    
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

