"""
Playwright UI 测试示例（SauceDemo）
"""
import pytest


@pytest.mark.ui
@pytest.mark.playwright
@pytest.mark.smoke
class TestSauceDemoPlaywright:
    """SauceDemo Playwright UI 测试"""

    @pytest.mark.parametrize(
        "username,password,should_succeed",
        [
            ("standard_user", "secret_sauce", True),
            ("locked_out_user", "secret_sauce", False),
        ],
    )
    def test_login_flow(self, playwright_page, base_url, username, password, should_succeed):
        """登录流程校验（参数化成功/失败）"""
        helper = playwright_page
        helper.navigate_to(base_url)

        helper.wait_for_selector("#user-name")
        helper.fill("#user-name", username)
        helper.fill("#password", password)
        helper.click("#login-button")

        if should_succeed:
            helper.wait_for_selector(".inventory_list")
            assert "inventory" in helper.get_url()
        else:
            helper.wait_for_selector("[data-test='error']")
            error_text = helper.get_text("[data-test='error']")
            assert "locked out" in error_text.lower()

    def test_add_to_cart_and_checkout_overview(self, playwright_page, base_url):
        """成功登录后加入购物车并到达 Checkout 概览页"""
        helper = playwright_page
        helper.navigate_to(base_url)

        helper.wait_for_selector("#user-name")
        helper.fill("#user-name", "standard_user")
        helper.fill("#password", "secret_sauce")
        helper.click("#login-button")

        helper.wait_for_selector("button[data-test='add-to-cart-sauce-labs-backpack']")
        helper.click("button[data-test='add-to-cart-sauce-labs-backpack']")

        helper.click(".shopping_cart_link")
        helper.wait_for_selector(".cart_list")
        assert "cart" in helper.get_url()

        helper.click("#checkout")
        helper.wait_for_selector("#first-name")
        helper.fill("#first-name", "Auto")
        helper.fill("#last-name", "Tester")
        helper.fill("#postal-code", "12345")
        helper.click("#continue")

        helper.wait_for_selector(".summary_info")
        assert "checkout-step-two" in helper.get_url()

