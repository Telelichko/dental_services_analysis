# !pip install spacy
# !python -m spacy download ru_core_news_md

import pandas as pd
from googletrans import Translator
from Models.app_data import *
import re
import spacy


app_data = AppData()
translator = Translator()

city = app_data.get_city()
city_en = translator.translate(city, src='ru', dest='en').text

nlp = spacy.load('ru_core_news_md')


def get_clean_data_price_dental_services():
    data_price_dental_services = pd.read_csv(f'{FILES_DIR}/{city}_price_dental_services.csv', sep='|', header=0)

    return data_price_dental_services


def get_clean_data_dental_clinics():
    data_dental_clinics = pd.read_csv(f'{FILES_DIR}/{city}_dental_clinics.csv', sep='|', header=0)
    data_dental_clinics['clinic_rating'] = round(data_dental_clinics['clinic_rating'], 2)

    return data_dental_clinics


def get_clean_data_clinics_prices():
    data_clinics_prices = pd.read_csv(f'{FILES_DIR}/{city}_clinics_prices.csv', sep='|', header=0)
    data_clinics_prices = data_clinics_prices[data_clinics_prices['service_price_min'] != '-']
    del (data_clinics_prices['service_link'])

    return data_clinics_prices


def get_clean_data_doctors_stats():
    data_clinics_doctors = pd.read_csv(f'{FILES_DIR}/{city}_clinics_doctors_info.csv', sep='|', header=0)
    data_clinics_doctors = data_clinics_doctors[data_clinics_doctors['doctor_experience'] != '-']
    data_clinics_doctors = data_clinics_doctors.astype({'doctor_experience': 'int64'})

    data_doctors_stats = data_clinics_doctors.groupby(by=['clinic_name', 'clinic_link'])\
                            .agg({'doctor_experience': ['min', 'max', 'mean']}).round(2)

    return data_doctors_stats


def get_data_clinics_prices_total():
    data_dental_clinics = get_clean_data_dental_clinics()
    data_clinics_prices = get_clean_data_clinics_prices()
    data_doctors_stats = get_clean_data_doctors_stats()

    data_dental_clinics_with_doctor_stats = pd.merge(data_dental_clinics, data_doctors_stats, how='left',
                                                     on=['clinic_name', 'clinic_link'])

    data_dental_clinics_with_doctor_stats.columns = [*data_dental_clinics_with_doctor_stats.columns[:-3],
                                                     'doctor_experience_min', 'doctor_experience_max',
                                                     'doctor_experience_mean']

    data_clinics_prices_total = pd.merge(data_dental_clinics_with_doctor_stats, data_clinics_prices, how='right',
                                         on=['clinic_name', 'clinic_link'])

    data_clinics_prices_total.to_csv(f'{FILES_DIR}/{city}_data_clinics_prices_total.csv')

    return data_clinics_prices_total


def get_clinics_prices_total():
    return pd.read_csv(f'{FILES_DIR}/{city}_data_clinics_prices_total.csv', header=0)


def prepare_data_column(list_unique):
  prepared_data = list_unique.copy()
  for i, row in enumerate(prepared_data):
    row = row.lower()
    row = ''.join(''.join(elem) for elem in re.findall(r'.*- ([\w ]+) -.*|.*- ([\w ]+)|\"(.*)\"|(.*)', row)).strip()
    text_in_brackets = ''.join(re.findall(r'\((.+)\)', row))
    row = row.replace(text_in_brackets, '').replace('()', '').strip()
    prepared_data[i] = row

  return prepared_data


def clean_data_row(data_column, list_row_unique, list_row_unique_clean):
  dict_data_clean = {}
  if len(list_row_unique) != len(list_row_unique_clean):
    raise Exception('Length of list_row_unique and list_row_unique_clean are not equal.')
  for (elem, elem_clean) in zip(list_row_unique, list_row_unique_clean):
    dict_data_clean[elem] = elem_clean
  data_column = [dict_data_clean[elem] if elem in clean_data_row.keys() else elem for elem in data_column]

  return data_column


def get_list_noun_adjective(list_in):
  list_out = [' '.join([token.lemma_ for token in nlp(line) if token.pos_ in [noun, adjective]]) for line in list_in]

  return list_out


def get_value_from_common_list(data_cell, list_common):
  is_cell_include_list_common = True
  for common_line in list_common:
    for i, common_word in enumerate(common_line.split()):
      if common_word.lower() in data_cell:
        is_cell_include_list_common = True
        if i == len(common_line) - 1:
          break
      else:
        is_cell_include_list_common = False
        break
    if is_cell_include_list_common:
      break

  return common_line if is_cell_include_list_common else None


def prepare_service_column():
    data_clinics_prices_total = get_clinics_prices_total()
    list_service_names_unique = list(data_clinics_prices_total['service_name'].unique())
    list_services_names_clean = prepare_data_column(list_service_names_unique)
    data_clinics_prices_total['service_name_noun_adjective'] = get_list_noun_adjective(data_clinics_prices_total['service_name'])

    data_clinics_prices_total['service_name_common'] = data_clinics_prices_total['service_name_noun_adjective'].apply(
        get_value_from_common_list, args=([list_services_names_clean]))

    list_from_common_services_unique = ['аппарат', 'керамика', 'брекет', 'протез', 'вестибулопластика',
                                        'временной коронка', 'гемисекция зуб', 'герметизация взрослый',
                                        'герметизация ребёнок', 'чистка зуб', 'гингивопластика', 'гингивэктомия',
                                        'золотой коронка', 'зубной мост', 'имплант', 'исправление прикус ребёнок',
                                        'иссечение капюшон зуб мудрость', 'капа выравнивание зуб',
                                        'керамический брекет', 'керамический виниры', 'керамический коронка',
                                        'композитный виниры', 'коронка диоксид цирконий', 'кт зубной ряд',
                                        'культевая вкладка', 'кюретаж пародонтального карман', 'отбеливание зуб',
                                        'лечение альвеолита', 'лечение гингивита', 'лечение детский кариес',
                                        'лечение детский пульпит', 'лечение зуб наркоз', 'лечение канал',
                                        'лечение кариес', 'лечение молочный зуб', 'лечение пародонтита',
                                        'лечение пародонтоз', 'лечение периодонтит', 'лечение периостит',
                                        'лечение пульпит', 'лингвальные брекет', 'люминиры', 'металлический брекет',
                                        'металлокерамический коронка', 'наращивание зуб', 'отбеливание зуб',
                                        'панорамный снимок зуб', 'плазмолифтинг десна', 'пластик уздечка губа',
                                        'пластик уздечка язык', 'пластинка выравнивание зуб', 'пластмассовый коронка',
                                        'пломбирование молочный зуб', 'покрытие зуб защитный лак',
                                        'покрытие зуб фторлаком', 'прозрачный брекет', 'резекция верхушка корень зуб',
                                        'реставрация зуб', 'реставрация молочный зуб', 'ретейнеры', 'сапфировый брекет',
                                        'серебрение молочный зуб', 'синус', 'скайсы зуб', 'сложный удаление зуб',
                                        'снимок зуб', 'снятие брекет', 'снятие зубной отложение', 'страз зуб',
                                        'трейнеры зуб', 'удаление зуб', 'удаление зубной камень',
                                        'удаление импланта зуб', 'удаление инородный тело зубной канал',
                                        'удаление киста зуб', 'удаление пломба', 'удаление экзостоз',
                                        'фарфоровый коронка', 'фотоотбеливание зуб', 'фторирование зуб', 'чистка зуб',
                                        'чистка зуб ультразвук', 'шинирование зуб', 'шинирование челюсть',
                                        'шлифовка полировка зуб', 'элайнеры']
    list_from_clinic_services_unique = ['временной зуб', 'временной пломба', 'отбеливание зуб', 'зуб пломба',
                                        'восстановление зуб', 'шинирование зуб', 'установка искусственого зуб',
                                        'установка коронка', 'ультразвуковой обработка', 'удаление зуб',
                                        'трепанация зуб', 'снятие коронка', 'снятие оттиск', 'ремонт протез',
                                        'коронка зуб временной', 'коронка зуб керамический', 'консультация',
                                        'обработка корневой канал', 'лечение канал']

    list_common_services_unique = sorted(list(set(list_from_common_services_unique + list_from_clinic_services_unique)))

