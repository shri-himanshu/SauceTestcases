import pytest
from selenium import webdriver
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


def test_valid_login(driver, test_params, request):
    login_page = LoginPage(driver)
    logger.info(f"Executing test case: {request.node.name}")
    params = test_params[request.node.name]
    url = "".join([SauceDemoAPIs.base_url.value, SauceDemoAPIs.login.value])
    logger.info(f"Test Params: Username {params['user']} and Password {params['password']}")
    login_page.login(url, params['user'], params['password'])
    expected_url = "".join([SauceDemoAPIs.base_url.value, getattr(SauceDemoAPIs, params['expected_url']).value])
    assert driver.current_url == expected_url, "Login Unsuccessful or redirection to unexpected page."
    logger.info("Login Successful")


def test_invalid_login(driver, test_params, request):
    login_page = LoginPage(driver)
    logger.info(f"Executing test case: {request.node.name}")
    params = test_params[request.node.name]
    url = "".join([SauceDemoAPIs.base_url.value, SauceDemoAPIs.login.value])
    login_page.login(url, params['user'], params['password'])
    error_message = login_page.get_error_message(err_msg=params['expected_error'])
    assert error_message == params['expected_error'], "Unexpected error message received"
    logger.info(f"Login Failed! with expected error message for user : {params['user']}")
