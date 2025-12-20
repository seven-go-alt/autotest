*** Settings ***
Documentation    SauceDemo 页面定位器 - 登录页面

*** Variables ***
# ========== 登录页面定位器 ==========
${LOGIN_USERNAME_INPUT}          id=user-name
${LOGIN_PASSWORD_INPUT}          id=password
${LOGIN_BUTTON}                  id=login-button
${LOGIN_ERROR_MESSAGE}           css:[data-test="error"]

# ========== 通用页面定位器 ==========
${PAGE_TITLE}                    css=.title
${HAMBURGER_MENU}                id=react-burger-menu-btn
${LOGOUT_BUTTON}                 id=logout_sidebar_link
