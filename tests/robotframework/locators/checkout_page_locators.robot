*** Settings ***
Documentation    SauceDemo 页面定位器 - 结账页面

*** Variables ***
# ========== 结账信息页面（第一步）==========
${CHECKOUT_FIRST_NAME_INPUT}     css=input#first-name
${CHECKOUT_LAST_NAME_INPUT}      css=input#last-name
${CHECKOUT_POSTAL_CODE_INPUT}    css=input#postal-code
${CONTINUE_BUTTON}               css=button#continue
${CHECKOUT_CANCEL_BUTTON}        css=button#cancel

# ========== 订单概览页面（第二步）==========
${CHECKOUT_SUMMARY_CONTAINER}    css=.summary_info
${CHECKOUT_SUMMARY_SUBTOTAL}     css=.summary_subtotal_label
${CHECKOUT_SUMMARY_TAX}          css=.summary_tax_label
${CHECKOUT_SUMMARY_TOTAL}        css=.summary_total_label
${FINISH_BUTTON}                 css=button#finish

# ========== 订单完成页面（第三步）==========
${CHECKOUT_COMPLETE_CONTAINER}   css=.checkout_complete_container
${COMPLETE_MESSAGE}              css=.complete-header
${COMPLETE_TEXT}                 css=.complete-text
${BACK_TO_PRODUCTS_BUTTON}       css=button#back-to-products
