from PlaywrightProject.pages.base1_page import BasePage
from playwright.sync_api import expect
from PlaywrightProject.pages.cart_page import CartPage

ADD_TO_CART = "#add-to-cart"
REMOVE = "#remove"
CART_BADGE = ".shopping_cart_badge"

class ProductPage(BasePage):

    def add_to_cart(self):
        self.page.locator(ADD_TO_CART).click()

    def remove_text_button(self):
        return self.page.locator(REMOVE).text_content()

    def count_cart_badge(self):
        return self.page.locator(CART_BADGE).text_content()

    def open_cart_page(self):
        self.page.locator(CART_BADGE).click()
        return CartPage(self.page)
