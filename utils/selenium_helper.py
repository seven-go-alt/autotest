"""
Selenium 工具类
提供常用的 Selenium 操作封装
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from pathlib import Path
import config.settings as settings
import logging

logger = logging.getLogger(__name__)


class SeleniumHelper:
    """Selenium 辅助类"""
    
    def __init__(self, browser=None, headless=None, screenshot_on_failure=True):
        """
        初始化浏览器驱动
        
        Args:
            browser: 浏览器类型 (chrome/firefox/edge)
            headless: 是否无头模式
            screenshot_on_failure: 失败时是否自动截图
        """
        self.browser = browser or settings.BROWSER
        self.headless = headless if headless is not None else settings.HEADLESS
        self.screenshot_on_failure = screenshot_on_failure
        self.driver = None
        self.wait = None
        
    def start_browser(self):
        """启动浏览器，优先支持 Docker/远程模式"""
        if self.browser == "chrome":
            options = ChromeOptions()
            if self.headless:
                options.add_argument("--headless=new")
            for opt in settings.BROWSER_OPTIONS["chrome"]["options"]:
                options.add_argument(opt)
            # 防自动化检测参数
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option("useAutomationExtension", False)
            # 设置用户代理
            options.add_argument(
                "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
            )

            if settings.SELENIUM_REMOTE_URL:
                # 远程运行（适用于 Docker + selenium/standalone-chrome）
                self.driver = webdriver.Remote(
                    command_executor=settings.SELENIUM_REMOTE_URL,
                    options=options,
                )
            else:
                service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=options)

        elif self.browser == "firefox":
            options = FirefoxOptions()
            if self.headless:
                options.add_argument("--headless")
            if settings.SELENIUM_REMOTE_URL:
                self.driver = webdriver.Remote(
                    command_executor=settings.SELENIUM_REMOTE_URL,
                    options=options,
                )
            else:
                service = Service(GeckoDriverManager().install())
                self.driver = webdriver.Firefox(service=service, options=options)

        elif self.browser == "edge":
            options = EdgeOptions()
            if self.headless:
                options.add_argument("--headless")
            if settings.SELENIUM_REMOTE_URL:
                self.driver = webdriver.Remote(
                    command_executor=settings.SELENIUM_REMOTE_URL,
                    options=options,
                )
            else:
                service = Service(EdgeChromiumDriverManager().install())
                self.driver = webdriver.Edge(service=service, options=options)
        else:
            raise ValueError(f"不支持的浏览器类型: {self.browser}")

        # 设置窗口大小
        window_size = settings.BROWSER_OPTIONS[self.browser]["window_size"]
        self.driver.set_window_size(*window_size)

        # 初始化等待对象
        self.wait = WebDriverWait(self.driver, settings.TIMEOUT)

        return self.driver
    
    def quit(self):
        """关闭浏览器"""
        if self.driver:
            self.driver.quit()
            self.driver = None
    
    def navigate_to(self, url):
        """导航到指定 URL"""
        self.driver.get(url)
    
    def find_element(self, locator_type, locator_value, timeout=None):
        """
        查找元素
        
        Args:
            locator_type: 定位类型 (id/name/class/xpath/css/link_text/partial_link_text/tag)
            locator_value: 定位值
            timeout: 超时时间（秒）
        """
        wait = WebDriverWait(self.driver, timeout or settings.TIMEOUT)
        by_map = {
            "id": By.ID,
            "name": By.NAME,
            "class": By.CLASS_NAME,
            "xpath": By.XPATH,
            "css": By.CSS_SELECTOR,
            "link_text": By.LINK_TEXT,
            "partial_link_text": By.PARTIAL_LINK_TEXT,
            "tag": By.TAG_NAME
        }
        by = by_map.get(locator_type.lower())
        if not by:
            raise ValueError(f"不支持的定位类型: {locator_type}")
        
        return wait.until(EC.presence_of_element_located((by, locator_value)))
    
    def click(self, locator_type, locator_value, timeout=None):
        """点击元素"""
        element = self.find_element(locator_type, locator_value, timeout)
        element.click()
    
    def input_text(self, locator_type, locator_value, text, timeout=None):
        """输入文本"""
        element = self.find_element(locator_type, locator_value, timeout)
        element.clear()
        element.send_keys(text)
    
    def get_text(self, locator_type, locator_value, timeout=None):
        """获取元素文本"""
        element = self.find_element(locator_type, locator_value, timeout)
        return element.text
    
    def wait_for_element_visible(self, locator_type, locator_value, timeout=None):
        """等待元素可见"""
        wait = WebDriverWait(self.driver, timeout or settings.TIMEOUT)
        by_map = {
            "id": By.ID,
            "name": By.NAME,
            "class": By.CLASS_NAME,
            "xpath": By.XPATH,
            "css": By.CSS_SELECTOR,
            "link_text": By.LINK_TEXT,
            "partial_link_text": By.PARTIAL_LINK_TEXT,
            "tag": By.TAG_NAME
        }
        by = by_map.get(locator_type.lower())
        wait.until(EC.visibility_of_element_located((by, locator_value)))
    
    def get_title(self):
        """获取页面标题"""
        return self.driver.title
    
    def get_current_url(self):
        """获取当前 URL"""
        return self.driver.current_url
    
    def take_screenshot(self, filename):
        """截图"""
        filepath = settings.REPORTS_DIR / filename
        self.driver.save_screenshot(str(filepath))
        return filepath
