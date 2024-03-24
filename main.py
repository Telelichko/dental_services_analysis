from Sites import site_prodoctorov_actions
from Helpers.driver_helper import *
from Models.app_data import *
import data_preprocessing


def test_get_info(driver):
    list_prices = site_prodoctorov_actions.test_get_dentistry_prices(driver)
    list_clinics = site_prodoctorov_actions.test_get_dental_clinics_common_info(driver)
    list_clinics_prices, list_doctors_info = site_prodoctorov_actions.test_get_clinic_doctors_and_prices_info(driver)
    data_clinics_prices_total = data_preprocessing.get_data_clinics_prices_total()

    s = 0


if __name__ == '__main__':
    app_data = AppData()
    s = app_data.get_city()

    test_get_info(driver)

    s = 0





