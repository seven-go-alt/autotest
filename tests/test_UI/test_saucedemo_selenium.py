"""
Selenium UI 测试示例（SauceDemo）
"""
import pytest


@pytest.mark.ui
@pytest.mark.selenium
@pytest.mark.smoke
class TestSauceDemoSelenium:
    """SauceDemo Selenium UI 测试"""

    @pytest.mark.parametrize(
        "username,password,should_succeed",
        [
            ("standard_user", "secret_sauce", True),
            ("locked_out_user", "secret_sauce", False),
        ],
    )
    def test_login_flow(self, selenium_driver, base_url, username, password, should_succeed):
        """登录流程校验（参数化成功/失败）"""
        helper = selenium_driver
        helper.navigate_to(base_url)

        helper.wait_for_element_visible("id", "user-name")
        helper.input_text("id", "user-name", username)
        helper.input_text("id", "password", password)
        helper.click("id", "login-button")

        if should_succeed:
            helper.wait_for_element_visible("css", ".inventory_list")
            assert "inventory" in helper.get_current_url()
        else:
            helper.wait_for_element_visible("css", "[data-test='error']")
            error_text = helper.get_text("css", "[data-test='error']")
            assert "locked out" in error_text.lower()

    def test_add_to_cart_and_checkout_overview(self, selenium_driver, base_url):
        """成功登录后，加入购物车并进入 Checkout 概览页"""
        helper = selenium_driver
        helper.navigate_to(base_url)

        helper.wait_for_element_visible("id", "user-name")
        helper.input_text("id", "user-name", "standard_user")
        helper.input_text("id", "password", "secret_sauce")
        helper.click("id", "login-button")

        # 添加商品
        helper.wait_for_element_visible("css", "button[data-test='add-to-cart-sauce-labs-backpack']")
        helper.click("css", "button[data-test='add-to-cart-sauce-labs-backpack']")

        # 进入购物车
        helper.click("css", ".shopping_cart_link")
        helper.wait_for_element_visible("css", ".cart_list")
        assert "cart" in helper.get_current_url()

        # 进入结账流程
        helper.click("id", "checkout")
        helper.wait_for_element_visible("id", "first-name")
        helper.input_text("id", "first-name", "Auto")
        helper.input_text("id", "last-name", "Tester")
        helper.input_text("id", "postal-code", "12345")
        helper.click("id", "continue")

        helper.wait_for_element_visible("css", ".summary_info")
        assert "checkout-step-two" in helper.get_current_url()

