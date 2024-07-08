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


def test_error_user_add_remove_items(driver, test_params, request):
    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)

    # Login as error user
    params = test_params[request.node.name]
    url = "".join([SauceDemoAPIs.base_url.value, SauceDemoAPIs.login.value])
    login_page.login(url, params['user'], params['password'])

    # Verify login success
    expected_url = "".join([SauceDemoAPIs.base_url.value, getattr(SauceDemoAPIs, params['expected_url']).value])
    assert driver.current_url == expected_url, "Login Unsuccessful or redirection to unexpected page."

    # Add Inventory Item and check if any exception raised
    try:
        inventory_page.add_to_cart(params['inventory_add'])
    except Exception as add_err:
        logger.error(f"Error : {add_err}")
    # Remove added Items and check for any exceptions
    for item in params['inventory_add']:
        try:
            inventory_page.remove_from_cart(item)
        except Exception as err:
            logger.error(f"Error : {err}")


