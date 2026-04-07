import json
import logging
import os
from enum import Enum
from pathlib import Path
from typing import Dict

import pytest
from playwright.sync_api import sync_playwright

from configs.settings import DEFAULT_CONFIGURATION_FILE
from framework.logger import logger
from framework.ui.browser.browser import Browser
from framework.ui.browser.window import DEFAULT_VIEWPORT_SIZE
from framework.ui.constants.timeouts import WaitTimeoutsMs
from framework.utils import file_utils
from framework.utils.config_parser import get_config_value

from dotenv import load_dotenv
from pathlib import Path

PROJECT_ROOT_DIR = Path(__file__).parent.resolve()
load_dotenv(PROJECT_ROOT_DIR / ".env")

class BrowserType(Enum):
    CHROMIUM = "chromium"
    FIREFOX = "firefox"
    WEBKIT = "webkit"


def _get_browser(playwright: sync_playwright, browser_type: BrowserType, headless: bool = False) -> Browser:
    browser_map = {
        BrowserType.FIREFOX: playwright.firefox,
        BrowserType.WEBKIT: playwright.webkit,
        BrowserType.CHROMIUM: playwright.chromium
    }
    browser = browser_map.get(browser_type, playwright.chromium)
    browser_instance = browser.launch(headless=headless)
    context = browser_instance.new_context(viewport=DEFAULT_VIEWPORT_SIZE)
    context.set_default_timeout(WaitTimeoutsMs.WAIT_PAGE_LOAD)

    page = context.new_page()

    custom_browser = Browser(page)
    return custom_browser


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption("--browser", action="store", default=BrowserType.CHROMIUM.value,
                     help="Choose a browser: chromium, firefox, webkit")
    parser.addoption("--headless", action="store_true", help="Run browser in headless mode")
    parser.addoption("--config", default=DEFAULT_CONFIGURATION_FILE,
                     help="Path to config file relative to the project root directory")


@pytest.hookimpl(tryfirst=True)
def pytest_configure():
    logger.setup_logger()
    logging.info("Test logging successfully configured for test execution.")


@pytest.fixture(scope="module")
def browser(request):
    browser_channel = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")

    with sync_playwright() as playwright:
        browser_instance = _get_browser(playwright, BrowserType(browser_channel), headless)
        yield browser_instance

        # Close the browser after the test is done
        browser_instance.page.close()
        browser_instance.page.context.browser.close()


@pytest.fixture(scope="module")
def set_basic_auth(browser: Browser, test_config: Dict[str, str]):
    user = get_config_value(test_config, "user", required=True)
    password = get_config_value(test_config, "password", required=True)

    browser.set_basic_authentication(user, password)


@pytest.fixture(scope="session")
def test_config(request) -> Dict[str, str]:
    config_file = request.config.getoption("--config")
    config_path = PROJECT_ROOT_DIR.joinpath(config_file).resolve()
    try:
        with open(config_path, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        raise Exception(f"Configuration file not fond at: {config_path}")
    return data


@pytest.fixture
def test_file_name(test_config: Dict[str, str]) -> str:
    return get_config_value(test_config, "download_file_name")


@pytest.fixture
def file_for_upload(test_config: Dict[str, str]) -> Path:
    file_name = get_config_value(test_config, "file_for_upload")
    resource_dir = get_config_value(test_config, "source_dir")
    file_path = Path(resource_dir, file_name).resolve()

    if not file_path.is_file():
        raise FileNotFoundError(f"File for upload not found: {file_path}")

    return file_path


@pytest.fixture
def download_dir(test_config: Dict[str, str]) -> Path:
    download_dir = get_config_value(test_config, "download_dir")
    return Path(download_dir).resolve()


@pytest.fixture
def cleanup_download_dir(download_dir: Path) -> Path:
    file_utils.remove_dir_if_exist(download_dir)
    try:
        yield download_dir
    finally:
        file_utils.remove_dir_if_exist(download_dir)



@pytest.fixture
def credentials():
    username = os.getenv("LOGIN_USERNAME")
    password = os.getenv("LOGIN_PASSWORD")

    if not username or not password:
        raise ValueError("Credentials are not set in .env file")

    return {
        "username": username,
        "password": password
    }


# def pytest_generate_tests(metafunc):
#     if "login_data" in metafunc.fixturenames:
#         import json
#         from pathlib import Path
#
#         config_path = Path("configs/test_data")
#
#         with open(config_path) as f:
#             data = json.load(f)["negative_login_tests"]
#
#         metafunc.parametrize("login_data", data)


def pytest_generate_tests(metafunc):
    import json
    from pathlib import Path

    base_path = Path(__file__).parent / "configs/test_data"

    # Negative login data
    if "login_data" in metafunc.fixturenames:
        with open(base_path / "configuration.json") as f:
            data = json.load(f)["negative_login_tests"]
        metafunc.parametrize("login_data", data)

    # Locked users data
    if "locked_user" in metafunc.fixturenames:
        with open(base_path / "locked_profiles.json") as f:
            data = json.load(f)
        metafunc.parametrize("locked_user", data)