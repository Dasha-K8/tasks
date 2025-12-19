from SeleniumProject.pages.base_page import BasePage
from selenium.webdriver.common.by import By

EMAIL_INPUT = (By.ID, "email")
CONTINUE_BUTTON = (By.XPATH, "//span[contains(text(),'Continue')]")
AUTH_FORM = (By.CLASS_NAME, "GcaCUXShwOU77PHR3xkH")
NEGATIVE_MESSAGE = (By.CLASS_NAME, "hgdilB1r9wGHTwyS5Aow")
SING_IN_BUTTON = (By.XPATH, "//button[.//span[normalize-space()='Sign in']]")


class AuthPage(BasePage):

    def continue_button(self):
        self.find(CONTINUE_BUTTON).click()

    def sign_in(self, email):
        self.find(EMAIL_INPUT).send_keys(email)
        self.continue_button()

    def form_text(self):
        return self.find(AUTH_FORM).text

    def error_text(self):
        return self.find(NEGATIVE_MESSAGE).text