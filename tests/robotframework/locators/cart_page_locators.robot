*** Settings ***
Documentation    SauceDemo 页面定位器 - 购物车页面

*** Variables ***
# ========== 购物车页面定位器 ==========
${CART_CONTAINER}                css=.cart_contents_container
${CART_LIST}                     css=.cart_list
${CART_ITEM}                     css=.cart_item
${CART_ITEM_NAME}                css=.cart_item_label
${CART_ITEM_PRICE}               css=.inventory_item_price

# ========== 购物车按钮 ==========
${CONTINUE_SHOPPING_BUTTON}      css=button#continue-shopping
${CHECKOUT_BUTTON}               css=button#checkout

# ========== 移除按钮 ==========
${REMOVE_FROM_CART}              css=button[data-test*="remove"]
