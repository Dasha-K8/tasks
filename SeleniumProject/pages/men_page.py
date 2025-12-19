from SeleniumProject.pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from SeleniumProject.pages.product_page import ProductPage


SHOP_NOW_LOCATOR = (By.XPATH, "(//a[.//span[text()='SHOP NOW']])[1]")
DELIVER_ELSEWHERE_BUTTON = (By.XPATH, "//button[.//span[text()='Deliver elsewhere']]")
CLOSE_BUTTON = (By.XPATH, "//button[@data-testid='close-button']")
BRAND_FILTER = (By.XPATH, "//button[span[text()='Brand']]")
NIKE_ELEMENT = (By.XPATH, "//label[div[contains(text(), 'Nike')]]")
SEARCH_INPUT = (By.XPATH, '//*[@id="searchBox"]')
EXIT_CLICK = (By.CSS_SELECTOR, 'section#category-banner-wrapper')
COUNT_PRODUCT_SELECTOR = (By.XPATH, '//*[@id="plp"]/div/div/div[2]/div/p')
PRODUCT = (By.ID, "product-208575690")

class MenPage(BasePage):

    def click_shop_now(self):
        button = self.wait_clickable(SHOP_NOW_LOCATOR)
        ActionChains(self.browser).move_to_element(button).click().perform()

    def deliver_and_close(self):
        self.wait_clickable(DELIVER_ELSEWHERE_BUTTON).click()
        self.wait_clickable(CLOSE_BUTTON).click()

    def filter_nike(self):
        self.wait_clickable(BRAND_FILTER).click()
        self.wait_clickable(SEARCH_INPUT).send_keys("Nike")
        self.find(NIKE_ELEMENT).click()
        self.find(EXIT_CLICK).click()

    def count_products_text(self, text):
        return self.wait_present_in_element(COUNT_PRODUCT_SELECTOR, text)

    def open_product(self):
        product = self.wait_clickable(PRODUCT)
        ActionChains(self.browser).move_to_element(product).click().perform()
        return ProductPage(self.browser)

