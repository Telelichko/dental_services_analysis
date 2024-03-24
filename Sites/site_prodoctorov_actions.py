# !pip install googletrans==4.0.0-rc1

from Helpers import dom_helper
from Models.app_data import *

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
    file_helper.write_list_to_file(list_prices_info, '|', f'{city_en}_price_dental_services', header='category_name|service_name|service_price_min|service_link')

    return list_prices_info


def get_dental_prices_from_page(driver, clinic_name=None, clinic_link=None):
    list_prices_info = []
    list_categories_elements = dom_helper.get_elements(driver, dom_helper.xpath_category)
    for i_c, category in enumerate(list_categories_elements):
        element_category_name = dom_helper.get_element_or_none(category, dom_helper.xpath_category_name)
        category_name = element_category_name.text if element_category_name else '-'
        list_services_elements = dom_helper.get_elements(category, dom_helper.xpath_service)
        for i_s, service in enumerate(list_services_elements):
            element_service_name = dom_helper.get_element_or_none(service, dom_helper.xpath_service_name)
            service_name = element_service_name.text.strip()
            print(f'Get dental service {service_name} with category and service ids: {i_c, i_s} on page:', clinic_link if clinic_link else 'price common info')
            element_service_price = dom_helper.get_element_or_none(service, dom_helper.xpath_service_price)
            service_price_min = int(''.join(re.findall(r'\d+', element_service_price.text))) if element_service_price else '-'
            service_link = service.get_attribute('href')
            if clinic_name and clinic_link:
                list_prices_info.append([clinic_name, clinic_link, category_name, service_name, service_price_min, service_link])
            else:
                list_prices_info.append([category_name, service_name, service_price_min, service_link])

    return list_prices_info


def test_get_dental_clinics_common_info(driver):
    url_dentistry = f'{URL_SITE_PRODOCTOROV}{city_en.lower()}/{URL_PART_DENTISTRY}'
    driver.get(url_dentistry)

    list_clinics_common_info = get_dental_clinics_info_from_common_page(driver)
    file_helper.write_list_to_file(list_clinics_common_info, '|', f'{city_en}_dental_clinics', header='clinic_name|clinic_rating|clinic_address|clinic_phone|count_doctors|clinic_link')

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
            print('Page with clinics lists:', id_page+1)
            button_next = dom_helper.get_element_or_none(driver, dom_helper.xpath_button_next)
            button_next.click()
            time.sleep(2)

    return list_clinics_info


def test_get_clinic_doctors_and_prices_info(driver):
    list_clinics = file_helper.read_file(f'{city_en}_dental_clinics')[1:]
    list_clinics_prices, list_doctors_info = [], []
    for clinic in list_clinics:
        list_clinic = clinic.strip().split('|')
        clinic_name = list_clinic[0]
        clinic_link = list_clinic[-1]
        list_current_clinic_prices = get_clinic_prices(driver, clinic_name, clinic_link)
        list_current_doctors_info = get_doctors_info(driver, clinic_name, clinic_link)

        list_clinics_prices += list_current_clinic_prices
        list_doctors_info += list_current_doctors_info

    file_helper.write_list_to_file(list_clinics_prices, '|', f'{city_en}_clinics_prices', header='clinic_name|clinic_link|category_name|service_name|service_price_min|service_link')
    file_helper.write_list_to_file(list_doctors_info, '|', f'{city_en}_clinics_doctors_info', header='clinic_name|clinic_link|id_doctor|doctor_specialization|doctor_experience')

    return list_clinics_prices, list_doctors_info


def get_dental_clinics_from_one_page(list_elements_clinics_elements, list_clinics_info):
    for i, clinic in enumerate(list_elements_clinics_elements):
        element_clinic_name = dom_helper.get_element_or_none(clinic, dom_helper.xpath_clinics_name)
        clinic_name = element_clinic_name.text

        print(f'Get clinic "{clinic_name}" with number {i+1} from list.')

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


def get_clinic_prices(driver, clinic_name, clinic_link):
    print(f'Clinic name "{clinic_name}", link: {clinic_link}')
    driver.get(f'{clinic_link}price')
    list_clinic_prices = get_dental_prices_from_page(driver, clinic_name, clinic_link)

    return list_clinic_prices


def get_doctors_info(driver, clinic_name, clinic_link):
    driver.get(f'{clinic_link}vrachi')
    list_doctors_elements = dom_helper.get_elements(driver, dom_helper.xpath_doctor)
    list_doctors_info = []
    # TODO: Need to add button next click for some pages. As example: 'https://prodoctorov.ru/tomsk/lpu/12944-medstar/'
    for i, doctor in enumerate(list_doctors_elements):
        print(f'Search doctor of clinic "{clinic_name}" with id: {i}. Page link: {clinic_link}')
        doctor_specialization_element = dom_helper.get_element_or_none(doctor, dom_helper.xpath_doctor_specialization)
        doctor_specialization = doctor_specialization_element.text if doctor_specialization_element and doctor_specialization_element.text else '-'
        doctor_experience_element = dom_helper.get_element_or_none(doctor, dom_helper.xpath_doctor_experience)
        doctor_experience = int(''.join(re.findall(r'\d+', doctor_experience_element.text))) if doctor_experience_element and doctor_experience_element.text else '-'

        list_doctors_info.append([clinic_name, clinic_link, i, doctor_specialization, doctor_experience])

    return list_doctors_info
