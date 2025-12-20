*** Settings ***
Documentation    SauceDemo 页面定位器 - 商品列表页面

*** Variables ***
# ========== 商品列表页面定位器 ==========
${INVENTORY_CONTAINER}           css=.inventory_container
${INVENTORY_LIST}                css=.inventory_list
${INVENTORY_ITEM}                css=.inventory_item
${INVENTORY_ITEM_NAME}           css=.inventory_item_name
${INVENTORY_ITEM_PRICE}          css=.inventory_item_price

# ========== 添加购物车按钮 ==========
${ADD_TO_CART_BACKPACK}          css=button[data-test="add-to-cart-sauce-labs-backpack"]
${ADD_TO_CART_BIKE_LIGHT}        css=button[data-test="add-to-cart-sauce-labs-bike-light"]
${ADD_TO_CART_BOLT_SHIRT}        css=button[data-test="add-to-cart-sauce-labs-bolt-t-shirt"]
${ADD_TO_CART_FLEECE_JACKET}     css=button[data-test="add-to-cart-sauce-labs-fleece-jacket"]
${ADD_TO_CART_ONESIE}            css=button[data-test="add-to-cart-sauce-labs-onesie"]

# ========== 排序和过滤 ==========
${PRODUCT_SORT_DROPDOWN}         css=.product_sort_container select
${FILTER_BUTTON}                 css=.filter-button

# ========== 购物车图标 ==========
${SHOPPING_CART_LINK}            css=a.shopping_cart_link
${SHOPPING_CART_BADGE}           css=.shopping_cart_badge
