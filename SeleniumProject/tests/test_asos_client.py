import pytest
from SeleniumProject.pages.home_page import HomePage

search_input = "shoes"
size_text = "UK 9.5"

def authentication(browser,email):
    home = HomePage(browser)
    home.open_home_page()
    auth = home.join()
    text = auth.form_text()
    assert "Hi friend!" in text
    assert "Enter your email to sign in or join" in text
    auth.sign_in(email)
    return auth

def open_men_section(browser):
    home = HomePage(browser)
    home.open_home_page()
    men = home.open_men_section()
    assert "/men/" in browser.current_url
    men.click_shop_now()
    men.deliver_and_close()
    return men

def test_home(browser):
    home = HomePage(browser)
    home.open_home_page()
    tittle_text = home.tittle_text()
    assert "The biggest brands" in tittle_text

def test_search(browser):
    home = HomePage(browser)
    home.open_home_page()
    search_page = home.search(search_input)
    banner = search_page.banner_text()
    assert "Your search results for" in banner
    assert "Shoes" in banner


@pytest.mark.parametrize("email", ["pythonSelenium@gmail.com"])
def test_positive_auth(browser, email):
    authentication(browser, email)


@pytest.mark.parametrize("email, expected_message", [
    ("123gmail.com", "Oops! Please type in your correct email address"),
    ("123@gmail", "Oops! Please type in your correct email address"),
    ("dasha.com", "Oops! Please type in your correct email address"),
    (" ", "Oops! You need to type your email here")
])
def test_negative_sign_in(browser, email, expected_message):
    auth = authentication(browser, email)
    assert expected_message == auth.error_text()



def test_add_product_to_cart(browser):
   men = open_men_section(browser)
   men.filter_nike()
   men.count_products_text("1 style found")
   product = men.open_product()
   product_text = product.get_product_text()
   assert "Nike Zoom Vomero 5 trainers in black and pink" in product_text
   product.choose_color_brown()
   product_text = product.get_product_text()
   assert "Nike Zoom Vomero 5 trainers in brown" in product_text
   product.select_size(size_text)
   product.click_add_to_cart()


