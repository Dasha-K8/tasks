from PlaywrightProject.pages.base1_page import BasePage
from PlaywrightProject.pages.inventory_page import InventoryPage

URL = "https://www.saucedemo.com/"

USERNAME = "#user-name"
PASSWORD = "#password"
LOGIN_BUTTON = "#login-button"
TITLE = "#title"
ERROR_MESSAGE = ".error-message-container"

class AuthPage(BasePage):

    def open(self):
        self.page.goto(URL)

    def fill_username(self, username):
        self.page.locator(USERNAME).fill(username)

    def fill_password(self, password):
        self.page.locator(PASSWORD).fill(password)

    def click_login(self):
        self.page.locator(LOGIN_BUTTON).click()
        return InventoryPage(self.page)

    def get_error_text(self):
        return self.page.locator(ERROR_MESSAGE).inner_text()

