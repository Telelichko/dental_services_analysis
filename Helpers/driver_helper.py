# !pip install webdriver-manager

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture()
def driver(request):
    # wd = get_driver_headless()
    wd = get_driver_ui(request)

    return wd


def get_driver_ui(request):
    # wd = webdriver.Chrome()
    wd = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    wd.maximize_window()
    wd.implicitly_wait(3)
    request.addfinalizer(wd.quit)

    return wd


def get_driver_headless():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')

    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--start-maximized")

    wd = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),
                          options=chrome_options)
    wd.implicitly_wait(10)

    return wd