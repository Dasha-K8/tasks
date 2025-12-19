from PlaywrightProject.pages.base1_page import BasePage
from PlaywrightProject.pages.cart_page import CartPage
from PlaywrightProject.pages.product_page import ProductPage

TITLE = "#header_container"
SORT = ".product_sort_container"
SELECT_OPTION = "lohi"
ALL_PRICES = ".inventory_item_price"
PRODUCT = ".inventory_item:has-text('Sauce Labs Backpack')"
PRODUCT_BUTTON = ".inventory_item_name"
CART_BUTTON = '.shopping_cart_link'
INVENTORY_ITEM = ".inventory_item"
MENU = "#react-burger-menu-btn"
ABOUT_BUTTON = "#about_sidebar_link"

class InventoryPage(BasePage):
    def title(self):
        return self.page.locator(TITLE).text_content()

    def count_products(self):
        return self.page.locator(INVENTORY_ITEM).count()

    def select_sort(self):
        self.page.locator(SORT).select_option(SELECT_OPTION)

    def all_prices_text(self):
        return self.page.locator(".inventory_item_price").all_text_contents()

    def open_product(self):
        product = self.page.locator(PRODUCT)
        product.locator(PRODUCT_BUTTON).click()
        return ProductPage(self.page)

    def open_cart_page(self):
        self.page.locator(CART_BUTTON).click()
        return CartPage(self.page)

    def open_about_page(self):
        self.page.locator(MENU).click()
        self.page.locator(ABOUT_BUTTON).click()
