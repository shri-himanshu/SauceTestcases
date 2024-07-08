import pytest

from pages.endpoints import SauceDemoAPIs
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage, inventory_items, item_links, dropdown
from utils.driver_factory import get_driver
from utils.logger import setup_logger

logger = setup_logger(__name__)


@pytest.fixture
def driver():
    driver = get_driver('chrome')
    yield driver
    driver.quit()


def test_problem_user_item_img(driver, test_params, request):
    # creating instances for all page classes
    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)

    # Login as performance glitch user
    params = test_params[request.node.name]
    url = "".join([SauceDemoAPIs.base_url.value, SauceDemoAPIs.login.value])

    login_page.login(url, params['user'], params['password'])

    # Verify login success
    expected_url = "".join([SauceDemoAPIs.base_url.value, getattr(SauceDemoAPIs, params['expected_url']).value])
    assert driver.current_url == expected_url, "Login Unsuccessful or redirection to unexpected page."

    # Compare the image sources which displayed on Inventory Home and Item links
    img_src_dict = {}

    for item in params['items']:
        img_src_dict[item] = [inventory_page.check_inventory_img_source(item)]

    for item in params['items']:
        inventory_page.item_title_link(item)
        img_src_dict[item].append(inventory_page.item_link_img_src())
        assert img_src_dict[item][0] == img_src_dict[item][1], "Images are not matching between Inventory page and " \
                                                               "Item page"
        logger.info(f"Both Images at Inventory Home and Item title page are same!")
        inventory_page.back_to_products()




