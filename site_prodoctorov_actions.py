# !pip install googletrans==4.0.0-rc1

from Helpers import dom_helper
from app_data import *

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Keys

import re
import time
from googletrans import Translator

app_data = AppData()
translator = Translator()

city = app_data.get_city()
city_en = translator.translate(city, src='ru', dest='en').text


def test_get_dentistry_prices(driver):
    url_dental_services = f'{URL_SITE_PRODOCTOROV}{city_en.lower()}/{URL_PART_DENTAL_SERVICES}'
    driver.get(url_dental_services)

    list_prices_info = get_dental_prices_from_page(driver)
    file_helper.write_list_to_file(list_prices_info, '|', 'price_dental_services', header='category_name|service_name|service_price_min|service_link')

    return list_prices_info


def get_dental_prices_from_page(driver):
    list_prices_info = []
    list_categories_elements = dom_helper.get_elements(driver, dom_helper.xpath_category)
    for category in list_categories_elements:
        element_category_name = dom_helper.get_element_or_none(category, dom_helper.xpath_category_name)
        category_name = element_category_name.text if element_category_name else '-'
        list_services_elements = dom_helper.get_elements(category, dom_helper.xpath_service)
        for service in list_services_elements:
            element_service_name = dom_helper.get_element_or_none(service, dom_helper.xpath_service_name)
            service_name = element_service_name.text.strip()
            element_service_price = dom_helper.get_element_or_none(service, dom_helper.xpath_service_price)
            service_price_min = int(''.join(re.findall(r'\d+', element_service_price.text))) if element_service_price else '-'
            service_link = service.get_attribute('href')
            list_prices_info.append([category_name, service_name, service_price_min, service_link])


    return list_prices_info


def test_get_dental_clinics_common_info(driver):
    url_dentistry = f'{URL_SITE_PRODOCTOROV}{city_en.lower()}/{URL_PART_DENTISTRY}'
    driver.get(url_dentistry)

    list_clinics_common_info = get_dental_clinics_info_from_common_page(driver)
    file_helper.write_list_to_file(list_clinics_common_info, '|', f'{city}_dental_clinics', header='clinic_name|clinic_rating|clinic_address|clinic_phone|count_doctors|clinic_link')

    return list_clinics_common_info


def get_dental_clinics_info_from_common_page(driver):
    list_clinics_info = []
    list_clinics_elements = dom_helper.get_elements(driver, dom_helper.xpath_clinics)
    count_clinics_on_page = len(list_clinics_elements)

    element_header = dom_helper.get_element_or_none(driver, dom_helper.xpath_header)
    count_clinics = int(''.join(re.findall(r'\d+', element_header.get_attribute('data-counter'))))
    count_pages = count_clinics // count_clinics_on_page if count_clinics % count_clinics_on_page == 0 else count_clinics // count_clinics_on_page + 1

    for id_page in range(count_pages):
        list_clinics_elements = dom_helper.get_elements(driver, dom_helper.xpath_clinics)
        get_dental_clinics_from_one_page(list_clinics_elements, list_clinics_info)

        if id_page != count_pages - 1:
            button_next = dom_helper.get_element_or_none(driver, dom_helper.xpath_button_next)
            button_next.click()
            time.sleep(2)

    return list_clinics_info


def test_get_clinic_doctors_and_prices_info(driver):
    clinic_link = 'https://prodoctorov.ru/tomsk/lpu/83267-avrora/'
    list_clinic_prices = get_clinic_prices(driver, clinic_link)

    s = 0


def get_dental_clinics_from_one_page(list_elements_clinics_elements, list_clinics_info):
    for i, clinic in enumerate(list_elements_clinics_elements):
        element_clinic_name = dom_helper.get_element_or_none(clinic, dom_helper.xpath_clinics_name)
        clinic_name = element_clinic_name.text

        element_clinic_link = dom_helper.get_element_or_none(clinic, dom_helper.xpath_clinics_link)
        clinic_link = element_clinic_link.get_attribute('href')

        element_clinic_rating = dom_helper.get_element_or_none(clinic, dom_helper.xpath_clinic_rating)
        clinic_rating = float(''.join(re.findall(r'[\d.]+', element_clinic_rating.get_attribute('style')))) * 5 / 6 if element_clinic_rating else '-'

        element_clinic_address = dom_helper.get_element_or_none(clinic, dom_helper.xpath_clinic_address)
        clinic_address = f'{city}, {element_clinic_address.text}' if element_clinic_address else city

        element_clinic_phone = dom_helper.get_element_or_none(clinic, dom_helper.xpath_clinic_phone)
        clinic_phone = element_clinic_phone.text if element_clinic_phone else '-'

        element_count_doctors = dom_helper.get_element_or_none(clinic, dom_helper.xpath_count_doctors)
        count_doctors = element_count_doctors.text.split()[0] if element_count_doctors else '-'

        list_clinics_info.append([clinic_name, clinic_rating, clinic_address, clinic_phone, count_doctors, clinic_link])

    return list_clinics_info


def get_clinic_prices(driver, clinic_link):
    driver.get(f'{clinic_link}price')
    list_clinic_prices = get_dental_prices_from_page(driver)

    return list_clinic_prices



