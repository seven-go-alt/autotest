"""
Playwright 高级场景测试示例
包括多标签页、动态等待、JavaScript 交互、表单提交等复杂场景
"""
import pytest
from utils.playwright_helper import PlaywrightHelper
import config.settings as settings


class TestPlaywrightAdvancedScenarios:
    """Playwright 高级场景测试类"""
    
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        """测试前后的设置和清理"""
        self.helper = PlaywrightHelper()
        self.helper.start_browser()
        yield
        self.helper.quit()
    
    @pytest.mark.playwright
    @pytest.mark.smoke
    def test_multi_tab_navigation(self):
        """
        测试多标签页导航
        演示：打开页面 -> 新开标签页 -> 切换标签页 -> 验证内容
        """
        # 打开首页
        self.helper.navigate_to(settings.BASE_URL)
        first_page_title = self.helper.get_title()
        assert "Python" in first_page_title
        
        # 获取第一个链接
        page = self.helper.page
        links = page.query_selector_all("a")
        assert len(links) > 0, "页面没有找到链接"
        
        # 点击链接（在新窗口打开）
        with page.context.expect_page() as new_page_info:
            links[0].click(button="middle") if links[0].get_attribute("href") else None
        
        # 如果有新页面打开，验证新页面
        if new_page_info.value:
            new_page = new_page_info.value
            try:
                new_page.wait_for_load_state("networkidle")
                # 验证新页面的内容
                new_title = new_page.title()
                assert new_title, "新页面没有标题"
            finally:
                new_page.close()
    
    @pytest.mark.playwright
    def test_dynamic_content_waiting(self):
        """
        测试动态内容等待
        演示：等待动态加载的元素、处理 AJAX 请求
        """
        self.helper.navigate_to(settings.BASE_URL)
        
        # 等待主容器加载
        self.helper.wait_for_selector("div[role='main']")
        
        # 获取页面内容
        page_html = self.helper.page.content()
        assert "Python" in page_html, "页面内容加载失败"
        
        # 验证特定元素可见
        nav_element = self.helper.page.query_selector("nav")
        assert nav_element is not None, "导航元素加载失败"
    
    @pytest.mark.playwright
    def test_javascript_interaction(self):
        """
        测试 JavaScript 交互
        演示：执行 JS 脚本、获取动态内容、修改 DOM
        """
        self.helper.navigate_to(settings.BASE_URL)
        
        # 执行 JavaScript 获取页面信息
        page_info = self.helper.evaluate("""
            {
                title: document.title,
                url: window.location.href,
                width: window.innerWidth,
                height: window.innerHeight
            }
        """)
        
        assert page_info["title"], "无法获取页面标题"
        assert page_info["url"], "无法获取页面 URL"
        assert page_info["width"] > 0, "窗口宽度无效"
        
        # 获取所有标题
        heading_count = self.helper.evaluate("""
            document.querySelectorAll('h1, h2, h3').length
        """)
        assert heading_count > 0, "页面没有找到标题"
    
    @pytest.mark.playwright
    def test_scroll_and_load_more(self):
        """
        测试滚动和加载更多内容
        演示：向下滚动、等待新内容、重复加载
        """
        self.helper.navigate_to(settings.BASE_URL)
        
        page = self.helper.page
        
        # 获取初始内容高度
        initial_height = self.helper.evaluate("document.body.scrollHeight")
        
        # 滚动到底部
        for _ in range(3):
            page.evaluate("window.scrollBy(0, window.innerHeight)")
            page.wait_for_timeout(500)
        
        # 获取最终内容高度
        final_height = self.helper.evaluate("document.body.scrollHeight")
        
        # 验证页面被正确加载
        assert initial_height > 0, "初始页面高度无效"
        assert final_height > 0, "最终页面高度无效"
    
    @pytest.mark.playwright
    def test_form_submission(self):
        """
        测试表单提交
        演示：填充表单、提交、验证提交结果
        """
        self.helper.navigate_to(settings.BASE_URL)
        
        # 等待页面完全加载
        self.helper.page.wait_for_load_state("networkidle")
        
        # 查找搜索表单（如果存在）
        search_box = self.helper.page.query_selector("input[type='search']")
        if search_box:
            # 输入搜索内容
            search_box.fill("pytest")
            
            # 等待搜索建议（如果有）
            self.helper.page.wait_for_timeout(500)
            
            # 提交表单
            form = search_box.evaluate_handle("el => el.closest('form')")
            if form:
                form.evaluate("el => el.submit()")
                
                # 等待页面加载
                self.helper.page.wait_for_load_state("networkidle")
                
                # 验证搜索结果
                current_url = self.helper.get_url()
                assert current_url, "搜索后 URL 为空"
    
    @pytest.mark.playwright
    def test_network_interception(self):
        """
        测试网络拦截和请求验证
        演示：拦截网络请求、验证请求和响应
        """
        page = self.helper.page
        collected_requests = []
        collected_responses = []
        
        # 监听请求
        def handle_request(request):
            collected_requests.append({
                'url': request.url,
                'method': request.method,
                'resource_type': request.resource_type
            })
        
        # 监听响应
        def handle_response(response):
            collected_responses.append({
                'url': response.url,
                'status': response.status
            })
        
        page.on("request", handle_request)
        page.on("response", handle_response)
        
        # 导航
        self.helper.navigate_to(settings.BASE_URL)
        
        # 验证收集的请求
        assert len(collected_requests) > 0, "没有收集到任何请求"
        assert len(collected_responses) > 0, "没有收集到任何响应"
        
        # 验证主请求成功
        main_responses = [r for r in collected_responses if r['status'] == 200]
        assert len(main_responses) > 0, "没有成功的 HTTP 响应"
        
        # 清理监听器
        page.remove_listener("request", handle_request)
        page.remove_listener("response", handle_response)
    
    @pytest.mark.playwright
    def test_screenshot_on_viewport(self):
        """
        测试不同视口大小的截图
        演示：改变窗口大小、验证响应式设计
        """
        self.helper.navigate_to(settings.BASE_URL)
        
        viewports = [
            {"width": 1920, "height": 1080, "name": "desktop"},
            {"width": 768, "height": 1024, "name": "tablet"},
            {"width": 375, "height": 667, "name": "mobile"}
        ]
        
        for viewport in viewports:
            # 设置视口大小
            self.helper.page.set_viewport_size({
                "width": viewport["width"],
                "height": viewport["height"]
            })
            
            # 等待重排
            self.helper.page.wait_for_timeout(500)
            
            # 验证页面仍可访问
            title = self.helper.get_title()
            assert title, f"在 {viewport['name']} 视口无法获取标题"
            
            # 可选：保存不同视口的截图
            # screenshot_path = f"screenshot_{viewport['name']}.png"
            # self.helper.take_screenshot(screenshot_path)
    
    @pytest.mark.playwright
    def test_cookie_handling(self):
        """
        测试 Cookie 处理
        演示：设置 Cookie、获取 Cookie、验证 Cookie 生效
        """
        page = self.helper.page
        
        # 导航到页面
        self.helper.navigate_to(settings.BASE_URL)
        
        # 设置 Cookie
        page.context.add_cookies([
            {
                'name': 'test_cookie',
                'value': 'test_value',
                'url': settings.BASE_URL
            }
        ])
        
        # 获取所有 Cookie
        cookies = page.context.cookies()
        
        # 验证 Cookie 已设置
        cookie_names = [c['name'] for c in cookies]
        assert 'test_cookie' in cookie_names, "测试 Cookie 未被设置"
        
        # 验证 Cookie 值
        test_cookie = next((c for c in cookies if c['name'] == 'test_cookie'), None)
        assert test_cookie['value'] == 'test_value', "Cookie 值不匹配"
    
    @pytest.mark.playwright
    def test_error_handling_and_retry(self):
        """
        测试错误处理和重试机制
        演示：处理超时、网络错误、重试逻辑
        """
        page = self.helper.page
        max_retries = 3
        attempt = 0
        success = False
        
        while attempt < max_retries and not success:
            try:
                attempt += 1
                # 尝试导航
                self.helper.navigate_to(settings.BASE_URL)
                
                # 等待关键元素
                page.wait_for_selector("body", timeout=5000)
                
                # 验证页面加载
                title = self.helper.get_title()
                assert title, "页面标题为空"
                
                success = True
            except Exception as e:
                if attempt < max_retries:
                    page.wait_for_timeout(1000)  # 等待后重试
                else:
                    raise AssertionError(f"经过 {max_retries} 次尝试后仍然失败: {str(e)}")
        
        assert success, "无法成功导航到页面"


class TestPlaywrightPerformance:
    """Playwright 性能和负载测试"""
    
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        """测试前后的设置和清理"""
        self.helper = PlaywrightHelper()
        self.helper.start_browser()
        yield
        self.helper.quit()
    
    @pytest.mark.playwright
    def test_page_load_time(self):
        """
        测试页面加载时间
        演示：测量导航时间
        """
        page = self.helper.page
        
        import time
        start_time = time.time()
        
        self.helper.navigate_to(settings.BASE_URL)
        page.wait_for_load_state("networkidle")
        
        end_time = time.time()
        load_time = end_time - start_time
        
        # 验证页面在合理时间内加载
        assert load_time < 30, f"页面加载时间过长: {load_time:.2f}s"
        
        # 输出性能信息
        timing = page.evaluate("""
            {
                navigationStart: performance.timing.navigationStart,
                loadEventEnd: performance.timing.loadEventEnd
            }
        """)
        
        if timing['loadEventEnd'] > 0:
            total_time = timing['loadEventEnd'] - timing['navigationStart']
            print(f"页面总加载时间: {total_time}ms")
