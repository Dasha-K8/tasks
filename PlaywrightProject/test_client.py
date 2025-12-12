from playwright.sync_api  import Page, expect, BrowserContext
import pytest


BASE_URL = "https://www.saucedemo.com/"

def go_to_page(page: Page, url: str = BASE_URL):
    page.goto(url)

def login_client(page: Page, username="standard_user", password="secret_sauce"):
    go_to_page(page)
    page.locator("#user-name").fill(username)
    page.locator("#password").fill(password)
    page.locator("#login-button").click()
    expect(page.locator(".title")).to_have_text("Products")

def add_to_cart(page: Page):
    login_client(page)
    product = page.locator(".inventory_item:has-text('Sauce Labs Backpack')")
    button = product.locator("button")
    button.click()
    expect(button).to_have_text("Remove")
    expect(page.locator(".shopping_cart_badge")).to_have_text("1")
    page.locator('.shopping_cart_link').click()
    expect(page.locator(".cart_item:has-text('Sauce Labs Backpack')")).to_have_count(1)


class TestLogin:

    def test_login(self, page: Page):
        login_client(page)
        assert "/inventory.html" in page.url
        assert page.locator(".inventory_item").count() > 0


    @pytest.mark.parametrize("user_name, password, message",
        [("standard_dasha", "secret_dasha",
         "Epic sadface: Username and password do not match any user in this service"),
        ("locked_out_user", "secret_sauce",
          "Epic sadface: Sorry, this user has been locked out."),
        ("standard_user", "",
          "Epic sadface: Password is required")])
    def test_negative_login(self, page: Page, user_name, password, message):
        go_to_page(page)
        page.locator("#user-name").fill(user_name)
        page.locator("#password").fill(password)
        page.locator("#login-button").click()
        assert page.locator(".error-message-container").is_visible()
        text = page.locator(".error-message-container").inner_text()
        assert message in text


class TestSort:
    def test_sort(self, page: Page):
        login_client(page)
        sort = page.locator(".product_sort_container")
        sort.select_option("lohi")
        all_prices_text = page.locator(".inventory_item_price").all_text_contents()
        prices = []
        for price in all_prices_text:
            clean_price = price.replace("$", "")
            prices.append(float(clean_price))
        assert prices == sorted(prices)


    def test_new_tab(self, page: Page, context: BrowserContext):
        login_client(page)
        page.locator("#react-burger-menu-btn").click()
        page.locator("#about_sidebar_link").click()
        assert "saucelabs.com" in page.url


    def test_buy(self, page: Page):
        add_to_cart(page)
        page.locator('.btn.btn_action.btn_medium.checkout_button').click()
        page.locator("#first-name").fill("Dasha")
        page.locator("#last-name").fill("Karlova")
        page.locator("#postal-code").fill("12345")
        page.locator(".submit-button.btn.btn_primary.cart_button.btn_action").click()

        page.locator("#finish").click()
        expect(page.locator(".complete-header")).to_have_text("Thank you for your order!")

