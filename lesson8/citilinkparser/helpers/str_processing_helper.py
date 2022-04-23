from unicodedata import category
import re


def try_parse(input_str, parse_method=int):
    """
    Преобразует строку в число заданным методом, если это возможно.
    При ошибке преобразования возвращает None.
    :param input_str: входная строка для пробразования
    :param parse_method: метод преобразования. По умолчанию int
    :return: число, в которое была преобразована входная строка или None
    """
    try:
        return parse_method(input_str)
    except ValueError as e:
        return None


def clean_spaces(input_str):
    """
    Очищает строку от пробелов
    :param input_str: входная строка для пробразования
    :return: строка, очищенная от пробелов
    """
    return "".join(ch for ch in input_str if category(ch)[0] != 'Z')


def extract_and_try_parse(input_str):
    """
    Извлекает из заданной строки input_str все цифры и преобразует в целое число, если это возможно.
    При ошибке преобразования возвращает None.
    :param input_str: входная строка
    :return: целое число, в которое была преобразована входная строка или None
    """
    # Убирает все символы кроме цифр
    number_str = re.sub('[^0-9]', '', input_str)
    return try_parse(number_str)


def extract_and_try_parse_float(input_str):
    """
    Извлекает из заданной строки input_str все цифры преобразует в вещественное число, если это возможно.
    При ошибке преобразования возвращает None.
    :param input_str: входная строка
    :return: вещественное число, в которое была преобразована входная строка или None
    """
    # Убирает все символы кроме цифр и десятичного разделителя
    number_str = re.sub('[^0-9.]', '', input_str)
    return try_parse(number_str, parse_method=float)


def extract_letters(input_str):
    """
    Извлекает из заданной строки input_str все буквы.
    :param input_str: входная строка
    :return: строка, состоящая только из букв
    """
    # Убирает все символы кроме букв
    return re.sub('[^a-яА-яa-zA-Z]', '', input_str)


def clean_controls_and_strip(input_str):
    """
    Очищает строку от специальных символов и удаляет пробелы по краям.
    :param input_str: входная строка
    :return: очищенная строка
    """
    return "".join(ch for ch in input_str if category(ch)[0] != 'C').strip()
