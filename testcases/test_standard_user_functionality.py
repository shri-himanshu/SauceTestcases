import time

import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage, inventory_items, item_links, dropdown
from pages.cart import CartPage, CheckoutStepOne, CheckoutStepTwo, CheckoutComplete
from pages.endpoints import SauceDemoAPIs
from utils.driver_factory import get_driver
from utils.logger import setup_logger

logger = setup_logger(__name__)


@pytest.fixture
def driver():
    driver = get_driver('chrome')
    yield driver
    driver.quit()


def test_standard_user_functionality(driver, test_params, request):
    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)
    cart = CartPage(driver)
    checkout1 = CheckoutStepOne(driver)
    checkout2 = CheckoutStepTwo(driver)
    checkout_complete = CheckoutComplete(driver)

    # Login as performance glitch user
    params = test_params[request.node.name]
    url = "".join([SauceDemoAPIs.base_url.value, SauceDemoAPIs.login.value])
    start_time = time.time()
    login_page.login(url, params['user'], params['password'])
    end_time = time.time()

    # Verify login success
    expected_url = "".join([SauceDemoAPIs.base_url.value, getattr(SauceDemoAPIs, params['expected_url']).value])
    assert driver.current_url == expected_url, "Login Unsuccessful or redirection to unexpected page."
    # Measure login time and compare with benchmarks
    login_time = end_time - start_time
    logger.info(f"{params['user']} took {login_time} ms to login.")
    # Attempt to add items to cart (some may fail)
    inventory_page.add_to_cart(params['inventory_add'])

    inventory_page.go_to_cart()

    cart.checkout()

    checkout1.fill_form(params['firstname'], params['lastname'], params['postalcode'])
    checkout1.continue_btn()

    checkout2.finish()

    checkout_msg = checkout_complete.checkout_complete_page()
    assert checkout_msg == "Checkout: Complete!", "Unable to checkout!"
    logger.info(f"User successfully checked out..")
    login_page.logout()
