from SeleniumProject.pages.base_page import BasePage
from selenium.webdriver.common.by import By
from SeleniumProject.pages.search_product_page import SearchProductPage
from SeleniumProject.pages.auth_page import AuthPage
from SeleniumProject.pages.men_page import MenPage

URL = 'https://www.asos.com/'
COOKIE_BUTTON = (By.ID, "onetrust-accept-btn-handler")
SEARCH = (By.ID, "chrome-search")
SEARCH_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
PROFILE_MENU = (By.CSS_SELECTOR, "[data-testid='myAccountIcon']")
JOIN_BUTTON = (By.CSS_SELECTOR, "[data-testid='signin-link']")
MEN_BUTTON = (By.XPATH, '//*[@id="men-floor"]')
TEXT_TITLE = (By.XPATH, "//span[contains(text(), 'The biggest brands')]")

class HomePage(BasePage):

    def open_home_page(self):
        self.browser.get(URL)
        self.browser.maximize_window()
        self.wait_clickable(COOKIE_BUTTON).click()

    def tittle_text(self):
        return self.find(TEXT_TITLE).text

    def search(self, text):
        self.wait_visibility(SEARCH).send_keys(text)
        self.find(SEARCH_BUTTON).click()
        return SearchProductPage(self.browser)

    def join(self):
        self.find(PROFILE_MENU).click()
        self.wait_clickable(JOIN_BUTTON).click()
        return AuthPage(self.browser)

    def open_men_section(self):
        self.wait_clickable(MEN_BUTTON).click()
        return MenPage(self.browser)
