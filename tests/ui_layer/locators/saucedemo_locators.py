# -*- coding: utf-8 -*-
"""
SauceDemo 网站定位器
URL: https://www.saucedemo.com
"""

from .base_locators import BaseLocators


class SauceDemoLocators(BaseLocators):
    """SauceDemo 应用的 UI 定位器"""
    
    # ========== 登录页面 ==========
    LOGIN_USERNAME_INPUT = "id=user-name"
    LOGIN_PASSWORD_INPUT = "id=password"
    LOGIN_BUTTON = "id=login-button"
    LOGIN_ERROR_CONTAINER = "css=h3[data-test='error']"
    
    # ========== 产品列表页面 ==========
    PRODUCTS_CONTAINER = "id=inventory_container"
    PRODUCT_ITEM = "css=.inventory_item"
    PRODUCT_NAME = "css=.inventory_item_name"
    PRODUCT_PRICE = "css=.inventory_item_price"
    PRODUCT_ADD_BTN = "css=.btn_primary.btn_inventory"
    PRODUCT_REMOVE_BTN = "css=.btn_secondary.btn_inventory"
    
    # ========== 购物车 ==========
    SHOPPING_CART_LINK = "id=shopping_cart_container"
    SHOPPING_CART_BADGE = "css=.shopping_cart_badge"
    CART_ITEM = "css=.cart_item"
    CART_ITEM_QUANTITY = "css=.cart_quantity"
    CHECKOUT_BUTTON = "id=checkout"
    CONTINUE_SHOPPING_BTN = "id=continue-shopping"
    
    # ========== 检出页面 ==========
    CHECKOUT_FIRST_NAME = "id=first-name"
    CHECKOUT_LAST_NAME = "id=last-name"
    CHECKOUT_POSTAL_CODE = "id=postal-code"
    CHECKOUT_CONTINUE_BTN = "id=continue"
    CHECKOUT_FINISH_BTN = "id=finish"
    ORDER_COMPLETE_MSG = "css=.complete-header"
    
    # ========== 页面菜单 ==========
    HAMBURGER_MENU = "id=react-burger-menu-btn"
    MENU_LOGOUT = "id=logout_sidebar_link"
    MENU_INVENTORY = "id=inventory_sidebar_link"
    MENU_CART = "id=cart_sidebar_link"
    
    # ========== 排序和过滤 ==========
    SORT_DROPDOWN = "css=select[data-test='product_sort_container']"
