from global_constants import *
from Helpers.driver_helper import *
from Helpers import dom_helper
from app_data import *

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import requests
from bs4 import BeautifulSoup

import re


# TODO: need to get info from prodoctorov first
# TODO: need to add search on other pages if they exist
# TODO: add currency
def test_get_dentistry_prices(driver):
    driver.get(URL_SITE_32TOP)

    app_data = AppData
    choose_city(driver, app_data.get_city())

    button_price = dom_helper.get_menu_section(driver, 'Цены')
    button_price.click()

    list_prices_info = []
    list_dental_services_and_categories_elements = driver.get_elements(driver, '//tr[contains(@class, "js-cityServices-service")]')
    category_name = None
    for category_or_service in list_dental_services_and_categories_elements:
        element_class = category_or_service.get_attribute('class')
        if 'services-price-main__caption' in element_class:
            category_name = category_or_service.text
        elif 'childService' in element_class:
            element_service_name = dom_helper.get_element_or_none(category_or_service, './/td[contains(@class, "services-price-main_item_details")]/a/span')
            element_service_price = dom_helper.get_element_or_none(category_or_service, './/td[contains(@class, "services-price-main_item_value")]/div')
            service_price = element_service_price.text
            service_price_min = str(*re.findall(r'от ([\d\s]+) ₽', service_price)).replace(' ', '') if 'от' in service_price else '-'
            service_price_max = str(*re.findall(r'до ([\d\s]+) ₽', service_price)).replace(' ', '') if 'до' in service_price else '-'
            element_service_count_clinics = dom_helper.get_element_or_none(category_or_service, './/td[contains(@class, "services-price-main_item_value")]/span')
            service_count_clinics = int(*re.findall(r'\d+', element_service_count_clinics.text))

            list_prices_info.append([category_name, element_service_name.text, service_price_min, service_price_max, service_count_clinics])

    return list_prices_info


def test_get_dental_clinics(driver):
    driver.get(URL_SITE_32TOP)

    app_data = AppData()
    # choose_city(driver, app_data.get_city())

    button_clinics = dom_helper.get_menu_section(driver, 'Стоматологии')
    button_clinics.click()

    list_clinics_info = get_dental_clinics_info_from_common_page(driver)

    list_clinic_selfpage_info = []
    for i, clinic in enumerate(list_clinics_info[:1]):
        clinic_name = clinic[0]
        clinic_url = clinic[-1]
        # driver.get(clinic_url)

        time.sleep(1)
        # button_close = dom_helper.wait_element(driver, 30, '//span[contains(@class, "js-appointmentFormClose")]')
        # button_close.click()

        # After ~25 sec. page will be blocked by modal window -> need to save dom:
        session = requests.session()
        response = session.get(clinic_url)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        file_helper.write_text_to_file(html, 'soup', 'txt')

        html = driver.page_source
        file_helper.write_text_to_file(html, 'soup', 'txt')
        soup = BeautifulSoup(html, 'html.parser')

        list_element_doctor_experience = dom_helper.get_elements(driver, '\\div[@class="clinic-specialist__text" and contains(., "Стаж")]/b')
        doctor_experience_min, doctor_experience_max = None, None
        for experience in list_element_doctor_experience:
            experience_digits = str(*re.findall(r'\d+', experience))
            if not doctor_experience_min or doctor_experience_min > experience_digits:
                doctor_experience_min = experience_digits
            elif not doctor_experience_max or doctor_experience_max < experience_digits:
                doctor_experience_max = experience_digits

        list_clinics_info[i].append(doctor_experience_min, doctor_experience_max)

        button_expand_all_services = dom_helper.get_element_or_none(driver, '\\button[contains(@class, "showMore") and contains(@class, "clinic-price")]')
        if button_expand_all_services:
            button_expand_all_services.click()

        list_categories_services = dom_helper.get_element_or_none(driver, '\\div[@class="clinic-price__unit "]')
        list_clinic_services = []
        for category in list_categories_services:

            list_dental_services = dom_helper.get_element_or_none(category, '.\\div[contains(@class, "js-child_service")]')

            for service in list_dental_services:
                element_service_name = dom_helper.get_element_or_none(service, '.\\div[contains(@class="clinic-price__unit__price")]')
                service_name = element_service_name.text
                element_price = dom_helper.get_element_or_none(service, '.\\div[@class="clinic-price__unit__price"]')
                element_price_value = dom_helper.get_element_or_none(element_price, '.\\meta[@itemprop="priceCurrency"]')
                price_currency = element_price_value.get_atttribute('content') if element_price_value else '-'
                price_value = element_price_value.text
                price_min = str(*re.findall(r'от ([\d\s]+) ₽', price_value)).replace(' ', '') if 'от' in price_value else '-'
                price_max = str(*re.findall(r'до ([\d\s]+) ₽', price_value)).replace(' ', '') if 'до' in price_value else '-'
                element_paid_object = dom_helper.get_element_or_none(element_price, '.\\span[contains(@class, "price__features")]')
                paid_object = element_paid_object.text if element_paid_object else '-'

                # TODO: Add id for clinics
                list_clinic_services.append(clinic_name, service_name, price_min, price_max, price_currency, paid_object)

        #
        # list_element_doctor_experience = dom_helper.get_elements(driver, '\\div[@class="clinic-specialist__text" and contains(., "Стаж")]/b')
        # doctor_experience_min, doctor_experience_max = None, None
        # for experience in list_element_doctor_experience:
        #     experience_digits = str(*re.findall(r'\d+', experience))
        #     if not doctor_experience_min or doctor_experience_min > experience_digits:
        #         doctor_experience_min = experience_digits
        #     elif not doctor_experience_max or doctor_experience_max < experience_digits:
        #         doctor_experience_max = experience_digits
        #
        # list_clinics_info[i].append(doctor_experience_min, doctor_experience_max)
        #
        # button_expand_all_services = dom_helper.get_element_or_none(driver, '\\button[contains(@class, "showMore") and contains(@class, "clinic-price")]')
        # if button_expand_all_services:
        #     button_expand_all_services.click()
        #
        # list_categories_services = dom_helper.get_element_or_none(driver, '\\div[@class="clinic-price__unit "]')
        # list_clinic_services = []
        # for category in list_categories_services:
        #
        #     list_dental_services = dom_helper.get_element_or_none(category, '.\\div[contains(@class, "js-child_service")]')
        #
        #     for service in list_dental_services:
        #         element_service_name = dom_helper.get_element_or_none(service, '.\\div[contains(@class="clinic-price__unit__price")]')
        #         service_name = element_service_name.text
        #         element_price = dom_helper.get_element_or_none(service, '.\\div[@class="clinic-price__unit__price"]')
        #         element_price_value = dom_helper.get_element_or_none(element_price, '.\\meta[@itemprop="priceCurrency"]')
        #         price_currency = element_price_value.get_atttribute('content') if element_price_value else '-'
        #         price_value = element_price_value.text
        #         price_min = str(*re.findall(r'от ([\d\s]+) ₽', price_value)).replace(' ', '') if 'от' in price_value else '-'
        #         price_max = str(*re.findall(r'до ([\d\s]+) ₽', price_value)).replace(' ', '') if 'до' in price_value else '-'
        #         element_paid_object = dom_helper.get_element_or_none(element_price, '.\\span[contains(@class, "price__features")]')
        #         paid_object = element_paid_object.text if element_paid_object else '-'
        #
        #         # TODO: Add id for clinics
        #         list_clinic_services.append(clinic_name, service_name, price_min, price_max, price_currency, paid_object)

                s = 0

            # name, price_min, price_max, currency, part

            s = 0


    s = list_clinics_info

    return list_clinics_info


def choose_city(driver, city):
    time.sleep(3)
    element_header = dom_helper.get_element_or_none(driver, '//h2')
    if city in element_header.text:
        return
    button_city = dom_helper.get_element_or_none(driver, '//span[contains(@class, "js-siteCity-select")]')
    if button_city.text == city:
        return
    button_city.click()

    input_city = dom_helper.get_element_or_none(driver, '//input[contains(@class, "js-city-popup-input")]')
    input_city.send_keys(city)

    button_city = dom_helper.get_element_or_none(driver, '//a[@class="popup-city__item__link active"]')
    button_city.click()


def get_dental_clinics_info_from_common_page(driver):
    list_clinics_info = []
    list_clinics_elements = dom_helper.get_elements(driver, '//div[@id="clinicList"]//div[@class="list-item"]')
    count_clinics_on_page = len(list_clinics_elements)
    # TODO: change to range() and ids
    for i, clinic in enumerate(list_clinics_elements):
        element_clinic_name = dom_helper.get_element_or_none(clinic, './/a[contains(@class, "bold-text list-item__name")]')
        clinic_link = element_clinic_name.get_attribute('href')
        clinic_name = element_clinic_name.text if element_clinic_name else '-'
        element_clinic_rating = dom_helper.get_element_or_none(clinic, './/span[contains(@class, "list-item__rating__text")]')
        clinic_rating = element_clinic_rating.text if element_clinic_rating else '-'
        element_clinic_address = dom_helper.get_element_or_none(clinic, './/a[contains(@class, "list-item__address")]')
        clinic_address = element_clinic_address.text if element_clinic_address else '-'

        list_clinics_info.append([clinic_name, clinic_rating, clinic_address, clinic_link])

        # if i + 1 == count_clinics_on_page:
        #     button_next = dom_helper.get_element_or_none(clinic, '//div[@id="paginator_bottom"]//li[@class="paginator-right-arrow"]')
        #     button_next.click()
        #
        #     list_clinics_elements = dom_helper.get_elements(driver, '//div[@id="clinicList"]//div[@class="list-item"]')
        #     count_clinics_on_page = len(list_clinics_elements)

    return list_clinics_info


