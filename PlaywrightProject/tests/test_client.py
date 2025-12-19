from playwright.sync_api  import Page, BrowserContext
import pytest
from PlaywrightProject.pages.auth_page import AuthPage



def auth_client(page: Page, username, password):
    auth = AuthPage(page)
    auth.open()
    auth.fill_username(username)
    auth.fill_password(password)
    return auth


class TestAuth:

    @pytest.mark.parametrize("user_name, password", [("standard_user", "secret_sauce")])
    def test_positive_login(self, page: Page, user_name, password):
        auth = auth_client(page, user_name, password)
        auth.click_login()
        assert "/inventory.html" in page.url


    @pytest.mark.parametrize("user_name, password, message",
        [("standard_dasha", "secret_dasha",
         "Epic sadface: Username and password do not match any user in this service"),
        ("locked_out_user", "secret_sauce",
          "Epic sadface: Sorry, this user has been locked out."),
        ("standard_user", "",
          "Epic sadface: Password is required")])
    def test_negative_login(self, page: Page, user_name, password, message):
        auth = auth_client(page, user_name, password)
        auth.click_login()
        assert message in auth.get_error_text()


class TestProduct:
    def test_sort(self, page: Page):
        auth = auth_client(page, "standard_user", "secret_sauce")
        inventory = auth.click_login()
        title = inventory.title()
        assert "Products" in title
        assert inventory.count_products() > 0
        inventory.select_sort()
        all_prices_text = inventory.all_prices_text()
        prices = []
        for price in all_prices_text:
            clean_price = price.replace("$", "")
            prices.append(float(clean_price))
        assert prices == sorted(prices)


    def test_buy(self, page: Page):
        auth = auth_client(page, "standard_user", "secret_sauce")
        inventory = auth.click_login()
        product = inventory.open_product()
        product.add_to_cart()
        text = product.remove_text_button()
        assert "Remove" in text
        count_cart_badge = product.count_cart_badge()
        assert "1" in count_cart_badge
        cart = product.open_cart_page()
        text = cart.product_in_cart()
        assert "Sauce Labs Backpack" in text
        checkout = cart.checkout_click()
        checkout.input_first_name('Dasha')
        checkout.input_last_name('Karlova')
        checkout.input_postal_code('12345')
        checkout.continue_click()
        checkout.finish_clicked()
        text = checkout.complete_container_text()
        assert "Thank you for your order!" in text


class TestNewTab:

    def test_new_tab(self, page: Page, context: BrowserContext):
        auth = auth_client(page, "standard_user", "secret_sauce")
        inventory = auth.click_login()
        inventory.open_about_page()
        assert "saucelabs.com" in page.url


