from PlaywrightProject.pages.base1_page import BasePage

FIRST_NAME = "#first-name"
LAST_NAME = "#last-name"
POSTAL_CODE = "#postal-code"
CONTINUE_BUTTON = "#continue"
FINISH_BUTTON = "#finish"
COMPLETE_CONTAINER = ".complete-header"


class CheckoutPage(BasePage):
    def input_first_name(self, first_name):
        self.page.locator(FIRST_NAME).fill(first_name)

    def input_last_name(self, last_name):
        self.page.locator(LAST_NAME).fill(last_name)

    def input_postal_code(self, postal_code):
        self.page.locator(POSTAL_CODE).fill(postal_code)

    def continue_click(self):
        self.page.locator(CONTINUE_BUTTON).click()

    def finish_clicked(self):
        self.page.locator(FINISH_BUTTON).click()

    def complete_container_text(self):
        return self.page.locator(COMPLETE_CONTAINER).text_content()