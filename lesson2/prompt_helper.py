from str_processing_helper import try_parse

# Используемы по умолчанию символ выхода из цикла ввода
QUIT_SYMBOL = 'q'


def prompt_job_name(quit_symbol=QUIT_SYMBOL):
    """
    Запрашивает у пользователя название вакансии
    :param quit_symbol: символ выхода из цикла ввода названия вакансии
    :return: название вакансии
    """
    while True:
        job_name = input(f'Введите название вакансии (или {quit_symbol} для выхода): ')

        if job_name.lower() == quit_symbol.lower():
            return None

        if not job_name.split():
            print('Название вакансии не должно быть пустым')
        else:
            return job_name


def prompt_pages_count(quit_symbol=QUIT_SYMBOL):
    """
    Запрашивает у пользователя число страниц (число запросов)
    :param quit_symbol:  символ выхода из цикла ввода числа страниц
    :return: число страниц (число запросов)
    """
    while True:
        pages_count_str = input(f'Введите количество страниц для запроса (или {quit_symbol} для выхода): ')
        pages_count = try_parse(pages_count_str)

        if pages_count_str.lower() == quit_symbol.lower():
            return None

        if pages_count is None or pages_count < 1:
            print('Число страниц должно быть целым положительным числом')
        else:
            return pages_count
