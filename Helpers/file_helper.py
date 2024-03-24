from global_constants import *
import json


def write_list_to_file(list_x2_to_save, separator, file_name, file_extension='csv', header=None):
    text = '\n'.join(separator.join(map(str, row)) for row in list_x2_to_save)
    text = f'{header}\n{text}' if header else text
    write_text_to_file(text, file_name, file_extension)


def write_text_to_file(text, file_name, file_extension):
    with open(f'{FILES_DIR}\\{file_name}.{file_extension}', 'w', encoding='utf-8') as f:
        f.write(text)


def read_file(file_name, file_extension='csv'):
    with open(f'{FILES_DIR}\\{file_name}.{file_extension}', 'r', encoding='utf-8') as f:
        return f.readlines()


def read_json(file_name):
    data = None
    with open(f'{ROOT_DIR}\\{file_name}.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    return data


def write_json(text, file_path, file_name):
    with open(f'{file_path}\\{file_name}.json', 'w', encoding='utf-8') as f:
        json.dump(text, f)
