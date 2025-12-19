from PlaywrightProject.pages.base1_page import BasePage
from PlaywrightProject.pages.checkout_page import CheckoutPage

CART_ITEM = ".inventory_item_name"
CHECKOUT = "#checkout"

class CartPage(BasePage):
    def product_in_cart(self):
        return self.page.locator(CART_ITEM).text_content()

    def checkout_click(self):
        self.page.locator(CHECKOUT).click()
        return CheckoutPage (self.page)