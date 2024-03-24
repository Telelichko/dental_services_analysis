import time


# TODO: Xpaths for elements from global_constants.URL_SITE_PRODOCTOROV site
xpath_category = './/div[@class="b-services-list__category" or @data-qa="lpu_services_service_group"]'
xpath_category_name = './/a[@class="b-services-list__caption"] | .//div[@data-qa="lpu_services_service_class_name_text"]'
xpath_service = './/a[contains(@class, "b-services-list__service")] | .//div[@data-qa="lpu_services_service"]'
xpath_service_name = './/span[@class="b-services-list__name"] | .//div[contains(@class, "b-lpu-services__service-name")]'
xpath_service_price = './/span[@class="b-services-list__price" or @data-qa="lpu_services_service_price_full_button"]'

xpath_clinics = './/div[contains(@class, "appointments_page")]//div[@class="b-card__row"]'
xpath_clinics_name = './/span[@data-qa="lpu_card_heading_lpu_name"]'
xpath_clinics_link = './/a[@data-qa="lpu_card_heading"]'
xpath_clinic_rating = './/div[@class="b-stars-rate__progress"]'
xpath_clinic_address = './/span[@data-qa="lpu_card_btn_addr_text"]'
xpath_clinic_phone = './/span[@data-qa="lpu_card_btn_phone_text"]'
xpath_count_doctors = './/div[@data-qa="lpu_card_subheading_doctors_count"]'

xpath_doctor = '//div[@class="b-doctor-card__top"]'
xpath_doctor_specialization = './/div[@class="b-doctor-card__spec"]'
xpath_doctor_experience = './/div[@class="b-doctor-card__experience-years"]'

xpath_header = './/h1'
xpath_button_next = './/i[contains(@class, "ui-icon-arrow-right")]'


def get_menu_section(driver, menu_name):
    return get_element_or_none(driver, f'//div[@class="menu-sections__section " and contains(., "{menu_name}")]')


def get_elements(driver, locator):
    return driver.find_elements('xpath', locator)


def get_element_or_none(driver, locator):
    list_elements = get_elements(driver, locator)
    if len(list_elements) > 0:
        return list_elements[0]
    else:
        return None


def wait_element(driver, wait_time, locator):
    start_time = time.time()
    element = None
    while not element and start_time - time.time() <= wait_time * 1000:
        element = get_element_or_none(driver, locator)
        time.sleep(250)

    return element
