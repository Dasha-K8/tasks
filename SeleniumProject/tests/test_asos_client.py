import pytest
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from pages.page import (
    open_home_page,
    authentication,
    open_women_section,
    wait_clickable,
    wait_visibility,
    wait_present_in_element
)

SEARCH = (By.ID, "chrome-search")
SEARCH_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
BANNER_TEXT = (By.CLASS_NAME, "wrapper_Qlsg1")
NEGATIVE_MESSAGE = (By.CLASS_NAME, "hgdilB1r9wGHTwyS5Aow")
BRAND_FILTER = (By.XPATH, "//button[.//span[text()='Brand']]")
SEARCH_INPUT = (By.XPATH, '//*[@id="searchBox"]')
NIKE_ELEMENT = (By.XPATH, "//div[contains(@class,'value') and contains(., 'Nike')]")
EXIT_CLICK = (By.CSS_SELECTOR, 'section#category-banner-wrapper')
COUNT_PRODUCT_SELECTOR = (By.XPATH, '//*[@id="plp"]/div/div/div[2]/div/p')
PRODUCT = (By.XPATH, '//*[@id="pta-product-208575690-0"]')
PRODUCT_BUTTON = (By.XPATH, '//*[@id="pta-product-208575690-4"]')
COLOUR_BROWN = (By.XPATH, './/a[@aria-label="BROWN"]')
SIZE_SELECT = (By.ID, "variantSelector")
ADD_BUTTON = (By.CSS_SELECTOR, '[data-testid="add-button"]')

def test_key_text(browser):
    open_home_page(browser)
    key_text = "The biggest brands"
    element = browser.find_element(By.XPATH, f"//*[contains(., '{key_text}')]")
    assert key_text in element.text


def test_search(browser):
    open_home_page(browser)
    wait_visibility(browser, SEARCH).send_keys("shoes")
    browser.find_element(*SEARCH_BUTTON).click()
    banner_text = browser.find_element(*BANNER_TEXT)
    assert "Your search results for:" in banner_text.text
    assert "Shoes" in banner_text.text

@pytest.mark.parametrize("email", ["pythonSelenium@gmail.com"])
def test_positive_join(browser, email):
    authentication(browser, email)


@pytest.mark.parametrize("email, expected_message", [
    ("123gmail.com", "Oops! Please type in your correct email address"),
    ("123@gmail", "Oops! Please type in your correct email address"),
    ("dasha.com", "Oops! Please type in your correct email address"),
    (" ", "Oops! You need to type your email here")
])
def test_negative_sign_in(browser, email, expected_message):
    authentication(browser, email)
    negative_element = browser.find_element(*NEGATIVE_MESSAGE)
    assert negative_element.text == expected_message


def test_add_product_to_cart(browser):
    browser = open_women_section(browser)
    wait_clickable(browser, BRAND_FILTER).click()
    wait_visibility(browser, SEARCH_INPUT).send_keys("Nike")
    browser.find_element(*NIKE_ELEMENT).click()
    browser.find_element(*EXIT_CLICK).click()
    wait_present_in_element(browser, COUNT_PRODUCT_SELECTOR, "17 styles found")
    product = wait_clickable(browser, PRODUCT)
    ActionChains(browser).move_to_element(product).click().perform()
    assert "Nike Zoom Vomero 5 trainers in black and pink" in browser.page_source
    browser.find_element(*COLOUR_BROWN).click()
    assert 'Nike Zoom Vomero 5 trainers in brown' in browser.page_source
    size_select = browser.find_element(*SIZE_SELECT)
    select = Select(size_select)
    select.select_by_visible_text("UK 9.5")
    browser.find_element(*ADD_BUTTON). click()


