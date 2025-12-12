from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

AUTH_FORM = (By.CLASS_NAME, "GcaCUXShwOU77PHR3xkH")
COOKIE_BUTTON = (By.ID, "onetrust-accept-btn-handler")
CLOSE_BUTTON = (By.XPATH, "//button[@data-testid='close-button']")
CONTINUE_BUTTON = (By.XPATH, "//span[contains(text(),'Continue')]")
DELIVER_ELSEWHERE_BUTTON = (By.XPATH, "//button[.//span[text()='Deliver elsewhere']]")
EMAIL_INPUT = (By.ID, "email")
JOIN_BUTTON = (By.CSS_SELECTOR, "[data-testid='signin-link']")
PROFILE_MENU = (By.CSS_SELECTOR, "[data-testid='myAccountIcon']")
SHOP_NOW_LOCATOR = (By.XPATH, "(//a[.//span[text()='SHOP NOW']])[1]")
WOMEN_BUTTON = (By.XPATH, '//*[@id="women-floor"]')


def wait_clickable(browser, locator, timeout = 10):
    return WebDriverWait(browser, timeout).until(
        EC.element_to_be_clickable(locator)
    )

def wait_visibility(browser, locator, timeout = 10):
    return WebDriverWait(browser, timeout).until(
        EC.visibility_of_element_located(locator)
    )

def wait_present_in_element(browser, locator, text):
    return WebDriverWait(browser, 10).until(
        EC.text_to_be_present_in_element(locator, text)
    )

def open_home_page(browser):
    browser.maximize_window()
    browser.get('https://www.asos.com/')
    assert "asos.com" in browser.current_url
    wait_clickable(browser, COOKIE_BUTTON).click()

def deliver_and_close(browser):
    wait_clickable(browser, DELIVER_ELSEWHERE_BUTTON).click()
    wait_clickable(browser, CLOSE_BUTTON).click()

def authentication(browser, email):
    open_home_page(browser)
    browser.find_element(*PROFILE_MENU).click()
    wait_clickable(browser, JOIN_BUTTON).click()
    element = browser.find_element(*AUTH_FORM)
    assert "Hi friend!" in element.text
    assert "Enter your email to sign in or join for" in element.text
    browser.find_element(*EMAIL_INPUT).send_keys(email)
    browser.find_element(*CONTINUE_BUTTON).click()

def open_women_section(browser):
    open_home_page(browser)
    browser.find_element(*WOMEN_BUTTON).click()
    assert "/women/" in browser.current_url
    shop_now_button = wait_clickable(browser, SHOP_NOW_LOCATOR)
    ActionChains(browser).move_to_element(shop_now_button).click().perform()
    assert 'Just-dropped trainers' in browser.page_source
    deliver_and_close(browser)
    return browser
