from SeleniumProject.pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

PRODUCT_TEXT = (By.CSS_SELECTOR, "h1.jcdpl")
COLOUR_BROWN = (By.XPATH, './/a[@aria-label="BROWN"]')
SIZE_SELECT = (By.ID, "variantSelector")
ADD_BUTTON = (By.CSS_SELECTOR, '[data-testid="add-button"]')


class ProductPage(BasePage):

    PRODUCT_NAME = "Nike Zoom Vomero 5 trainers in black and pink"
    PRODUCT_NAME_BROWN = "Nike Zoom Vomero 5 trainers in brown"

    def get_product_text(self):
        self.wait_visibility(PRODUCT_TEXT)
        return self.find(PRODUCT_TEXT).text

    def choose_color_brown(self):
        self.find(COLOUR_BROWN).click()

    def select_size(self, size_text):
        size_select = self.find(SIZE_SELECT)
        select = Select(size_select)
        select.select_by_visible_text(size_text)

    def click_add_to_cart(self):
        self.find(ADD_BUTTON).click()
