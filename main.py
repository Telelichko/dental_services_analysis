import time

import requests
from bs4 import BeautifulSoup

import site_prodoctorov_actions
from Helpers.driver_helper import *
from Helpers import file_helper, dom_helper
from app_data import *


def test_get_info(driver):
    # list_prices = site_prodoctorov_actions.test_get_dentistry_prices(driver)
    # list_clinics = site_prodoctorov_actions.test_get_dental_clinics_common_info(driver)

    list_clinic_prices = site_prodoctorov_actions.test_get_clinic_doctors_and_prices_info(driver)

    s = 0


if __name__ == '__main__':
    app_data = AppData()
    s = app_data.get_city()

    test_get_info(driver)

    s = 0





