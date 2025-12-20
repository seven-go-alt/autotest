# -*- coding: utf-8 -*-
"""
Robot Framework 自定义库（示例）
提供一些高层关键字，内部调用现有的 Playwright / Selenium helper
"""
from robot.api.deco import keyword
from playwright.sync_api import sync_playwright
import os
from pathlib import Path
from robot.api import logger
import config.settings as settings

class RobotCustomLibrary:
    """简单的 Robot 自定义库，使用 Playwright 同步 API 实现常用关键字。"""

    def __init__(self):
        self._play = None
        self._browser = None
        self._page = None

    @keyword("Open Playwright Browser")
    def open_playwright_browser(self, headless=True, browser_name='chromium'):
        """启动 Playwright 浏览器并打开一个页面。
        headless: True/False
        browser_name: chromium/firefox/webkit
        返回：无
        """
        if self._play is None:
            self._play = sync_playwright().start()
        if browser_name.lower() == 'chromium':
            self._browser = self._play.chromium.launch(headless=headless)
        elif browser_name.lower() == 'firefox':
            self._browser = self._play.firefox.launch(headless=headless)
        else:
            self._browser = self._play.webkit.launch(headless=headless)
        self._page = self._browser.new_page()

    @keyword("Go To")
    def go_to(self, url):
        """打开 URL"""
        if not self._page:
            raise RuntimeError('Browser not opened. Call "Open Playwright Browser" first')
        self._page.goto(url)

    @keyword("Wait For Selector")
    def wait_for_selector(self, selector, timeout=30):
        """等待选择器出现，timeout 秒后超时（秒）"""
        if not self._page:
            raise RuntimeError('Browser not opened')
        # Playwright timeout 参数以毫秒为单位
        self._page.wait_for_selector(selector, timeout=int(float(timeout) * 1000))

    @keyword("Input Text")
    def input_text(self, selector, text):
        """在 selector 指定的元素输入文本"""
        if not self._page:
            raise RuntimeError('Browser not opened')
        self._page.fill(selector, text)

    @keyword("Click")
    def click(self, selector):
        """点击元素"""
        if not self._page:
            raise RuntimeError('Browser not opened')
        self._page.click(selector)

    @keyword("Take Screenshot")
    def take_screenshot(self, path='screenshot.png'):
        """截图并保存到 path"""
        if not self._page:
            raise RuntimeError('Browser not opened')
        # 保存到 reports 目录下
        reports_dir = Path(settings.REPORTS_DIR)
        reports_dir.mkdir(parents=True, exist_ok=True)
        dest = reports_dir / Path(path).name
        self._page.screenshot(path=str(dest))
        logger.info(f"Saved screenshot: {dest}")
        return str(dest)

    @keyword("Get Title")
    def get_title(self):
        """返回当前页面标题"""
        if not self._page:
            raise RuntimeError('Browser not opened')
        return self._page.title()

    @keyword("Set Viewport")
    def set_viewport(self, width: int = 1920, height: int = 1080):
        """设置页面视窗大小"""
        if not self._page:
            raise RuntimeError('Browser not opened')
        self._page.set_viewport_size({"width": int(width), "height": int(height)})

    @keyword("Set User Agent")
    def set_user_agent(self, ua: str):
        """设置 user-agent（需要在创建 context 前使用）"""
        # Playwright 需要在 context 创建时设置 UA；记录并用户自行使用
        logger.info("Set User Agent keyword called (use PlaywrightHelper to set before context creation)")

    @keyword("Close Playwright Browser")
    def close_playwright_browser(self):
        """关闭页面和浏览器"""
        try:
            if self._page:
                self._page.close()
            if self._browser:
                self._browser.close()
            if self._play:
                self._play.stop()
        finally:
            self._play = None
            self._browser = None
            self._page = None


# 为兼容性提供模块级包装函数，确保 Robot Framework 在通过模块导入时能发现关键字
_lib = RobotCustomLibrary()


@keyword("Open Playwright Browser")
def Open_Playwright_Browser(headless=True, browser_name='chromium'):
    return _lib.open_playwright_browser(headless=headless, browser_name=browser_name)


@keyword("Go To")
def Go_To(url):
    return _lib.go_to(url)


@keyword("Wait For Selector")
def Wait_For_Selector(selector, timeout=30):
    return _lib.wait_for_selector(selector, timeout=timeout)


@keyword("Input Text")
def Input_Text_Playwright(selector, text):
    return _lib.input_text(selector, text)


@keyword("Click")
def Click_Element(selector):
    return _lib.click(selector)


@keyword("Get Title")
def Get_Title():
    return _lib.get_title()


@keyword("Close Playwright Browser")
def Close_Playwright_Browser():
    return _lib.close_playwright_browser()
