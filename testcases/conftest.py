import pytest
import os
import datetime
from utils.params_json_parser import ParamsParser


def pytest_addoption(parser):
    parser.addoption("--params-file", action="store", default="params.json",
                     help="Path to the JSON file with test parameters")
    parser.addoption("--html-report", action="store", help="Path to the HTML report file")



@pytest.fixture(scope="session")
def params(pytestconfig):
    params_file = pytestconfig.getoption("--params-file")
    parser = ParamsParser(params_file)
    return parser


@pytest.fixture
def test_params(request, params):
    test_file_name = os.path.basename(request.module.__file__)
    return params.get_params(test_file_name)


def pytest_configure(config):
    html_option = config.getoption("--html-report")
    if html_option:
        timestamp = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
        report_filename = f"report_{timestamp}.html"
        new_html_path = os.path.join(html_option, report_filename)
        config.option.htmlpath = new_html_path


@pytest.fixture(scope="function", autouse=True)
def test_case_name_fixture(request):
    module = request.module

    # Get all functions defined in the module that start with 'test_'
    test_functions = [
        item for item in dir(module)
        if callable(getattr(module, item)) and item.startswith('test_')
    ]

    print("All test functions in this module:", test_functions)
