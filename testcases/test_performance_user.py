import time

import pytest
from pages.login_page import LoginPage
from pages.endpoints import SauceDemoAPIs
from utils.driver_factory import get_driver
from utils.logger import setup_logger

logger = setup_logger(__name__)


@pytest.fixture
def driver():
    driver = get_driver('chrome')
    yield driver
    driver.quit()


def test_performance_user_login(driver, test_params, request):
    login_page = LoginPage(driver)
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
    assert login_time < params['max_latency'], "Login time exceeded expected benchmark"
    login_page.logout()






