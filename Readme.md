# Web Application Test Scripts

This repository contains the test scripts for automating the testing of web applications using the framework provided in the SauceFramework repository.

## Prerequisites

- Python 3.8+
- SauceFramework package

## Setup Instructions

1. Clone the repository:
    ```bash
    git clone <repository_url>
    cd WebAppTests
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

   4. Install the WebAppFramework package:
       ```bash
       pip install -e /path/to/SauceFramework
       ```
       or alternatively you can set the SauseFramework root as PYTHONPATH
       ```
      export PYTHONPATH="<path to SauceFramework>"
      ```
## Running Tests

To run the tests, use the following command:
```bash
pytest --params-file=C:\Users\shrivh1\PycharmProjects\SauceDemoRepos\SauseTestcases\tests_params\params.json --html-report=C:\Users\shrivh1\Downloads\sauce_reports C:\Users\shrivh1\PycharmProjects\SauceDemoRepos\SauseTestcases\testcases\test_performance_user.py --no-header --no-summary -q in C:\Users\shrivh1\PycharmProjects\SauceDemoRepos\SauseTestcases
```
NOTE: The testcase scripts are not exhaustive and can be expanded as per the use cases need to be validated.
