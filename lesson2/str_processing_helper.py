from unicodedata import category


def clean_punctuation(input_str):
    """
    Очищает строку от знаков пунктуации
    :param input_str: входная строка для пробразования
    :return: строка, очищенная от знаков пунктуации
    """
    return "".join(ch for ch in input_str if category(ch)[0] != 'P')


def clean_spaces(input_str):
    """
    Очищает строку от пробелов
    :param input_str: входная строка для пробразования
    :return: строка, очищенная от пробелов
    """
    return "".join(ch for ch in input_str if category(ch)[0] != 'Z')


def clean_string(input_str):
    """
    Очищает строку от пробелов, знаков пунктуации, символов Unicode
    :param input_str: входная строка для пробразования
    :return: строка, очищенная от пробелов, знаков пунктуации, символов Unicode
    """
    return "".join(ch for ch in input_str if category(ch)[0] not in ('Z', 'P', 'C'))


def try_parse(input_str, parse_method=int):
    """
    Преобразует строку в число заданным методом, если это возможно.
    При ошибке преобразования возвращает None
    :param input_str: входная строка для пробразования
    :param parse_method: метод преобразования. По умолчанию int
    :return: число, в которое была преобразована входная строка или None
    """
    try:
        return parse_method(input_str)
    except ValueError as e:
        return None
