import json
import pandas

# Используемая по умолчанию кодировка
ENCODING = 'utf-8'


def write_list_to_json(input_list, file_name, encoding=ENCODING, ensure_ascii=True):
    """
    Записывает список в json-файл с заданным именем
    :param input_list: список, который будет записан в файл
    :param file_name: имя файла, куда будут записаны данные
    :param encoding: кодировка
    :param ensure_ascii: экранирование ASCII-символов
    """
    with open(file_name, 'w', encoding=encoding) as f:
        json.dump(input_list, f, ensure_ascii=ensure_ascii)


def write_list_to_csv(input_list, file_name, encoding=ENCODING):
    """
    Записывает список словарей в csv-файл
    :param input_list: список словарей, который будет записан в файл
    :param file_name: имя файла, куда будут записаны данные
    :param encoding: кодировка
    """
    list_df = pandas.json_normalize(input_list)
    list_df.to_csv(file_name, sep=';', encoding=encoding, index=False)
