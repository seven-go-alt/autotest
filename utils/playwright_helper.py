"""
Playwright 工具类
提供常用的 Playwright 操作封装
"""
from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext
import config.settings as settings


class PlaywrightHelper:
    """Playwright 辅助类"""
    
    def __init__(self, browser=None, headless=None):
        """
        初始化 Playwright
        
        Args:
            browser: 浏览器类型 (chromium/firefox/webkit)
            headless: 是否无头模式
        """
        self.browser_type = browser or settings.PLAYWRIGHT_BROWSER or "chromium"
        self.headless = headless if headless is not None else settings.PLAYWRIGHT_HEADLESS
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        
    def start_browser(self):
        """启动浏览器"""
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
        
        # 创建上下文
        viewport = settings.BROWSER_OPTIONS.get("chrome", {}).get("window_size", (1920, 1080))
        self.context = self.browser.new_context(
            viewport={"width": viewport[0], "height": viewport[1]},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        )
        
        # 创建页面
        self.page = self.context.new_page()
        
        return self.page
    
    def quit(self):
        """关闭浏览器"""
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
    
    def navigate_to(self, url):
        """导航到指定 URL"""
        self.page.goto(url)
    
    def click(self, selector, timeout=None):
        """点击元素"""
        timeout_ms = (timeout or settings.TIMEOUT) * 1000
        self.page.click(selector, timeout=timeout_ms)
    
    def fill(self, selector, text, timeout=None):
        """填充输入框"""
        timeout_ms = (timeout or settings.TIMEOUT) * 1000
        self.page.fill(selector, text, timeout=timeout_ms)
    
    def get_text(self, selector, timeout=None):
        """获取元素文本"""
        timeout_ms = (timeout or settings.TIMEOUT) * 1000
        return self.page.text_content(selector, timeout=timeout_ms)
    
    def wait_for_selector(self, selector, timeout=None, state="visible"):
        """等待元素"""
        timeout_ms = (timeout or settings.TIMEOUT) * 1000
        self.page.wait_for_selector(selector, timeout=timeout_ms, state=state)
    
    def get_title(self):
        """获取页面标题"""
        return self.page.title()
    
    def get_url(self):
        """获取当前 URL"""
        return self.page.url
    
    def take_screenshot(self, filename):
        """截图"""
        filepath = settings.REPORTS_DIR / filename
        self.page.screenshot(path=str(filepath))
        return filepath
    
    def wait_for_load_state(self, state="load"):
        """等待页面加载状态"""
        self.page.wait_for_load_state(state)
    
    def evaluate(self, script):
        """执行 JavaScript"""
        return self.page.evaluate(script)

