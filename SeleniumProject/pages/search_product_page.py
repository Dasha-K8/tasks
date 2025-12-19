from SeleniumProject.pages.base_page import BasePage
from selenium.webdriver.common.by import By

BANNER_TEXT = (By.ID, "search-term-banner")

class SearchProductPage(BasePage):

    def banner_text(self):
        return self.find(BANNER_TEXT).text
