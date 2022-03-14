# Необходимо собрать информацию о вакансиях на вводимую должность
# (используем input или через аргументы получаем должность) с сайтов HH(обязательно) и/или Superjob(по желанию).
# Приложение должно анализировать несколько страниц сайта (также вводим через input или аргументы).
# Получившийся список должен содержать в себе минимум:
# Наименование вакансии.
# Предлагаемую зарплату (разносим в три поля: минимальная и максимальная и валюта. цифры преобразуем к цифрам).
# Ссылку на саму вакансию.
# Сайт, откуда собрана вакансия.

# По желанию можно добавить ещё параметры вакансии (например, работодателя и расположение).
# Структура должна быть одинаковая для вакансий с обоих сайтов.
# Общий результат можно вывести с помощью dataFrame через pandas. Сохраните в json либо csv.


import requests
import time
from bs4 import BeautifulSoup as BS

from config import USER_AGENT
from str_processing_helper import clean_spaces, clean_punctuation, try_parse
from export_helper import write_list_to_json, write_list_to_csv
from prompt_helper import prompt_job_name, prompt_pages_count


def execute_requests(job_name, pages_count=1):
    """
    Выполняет заданное количество запросов для заданной вакансии
    :param job_name: название вакансии
    :param pages_count: число страниц (число запросов)
    :return: список ответов на каждый запрос
    """
    url = 'https://hh.ru'
    suffix = '/search/vacancy'
    params = {'text': job_name}
    headers = {'User-Agent': USER_AGENT}

    responses = []
    for page in range(pages_count):
        params['page'] = page + 1
        response = requests.get(url + suffix, params=params, headers=headers)
        responses.append(response)
        time.sleep(1)

    return responses


def parse_responses(responses):
    """
    Возвращает список с данными о вакансиях - список словарей
    :param responses: список ответов на запросы
    :return: список словарей с данными о вакансиях
    """
    jobs_list_total = []
    for response in responses:
        jobs_list = parse_response(response)
        jobs_list_total.extend(jobs_list)

    return jobs_list_total


def parse_response(response):
    """
    Возвращает список с данными о вакансиях - список словарей
    :param response: ответ на запрос
    :return: список словарей с данными о вакансиях
    """
    dom = BS(response.text, 'html.parser')
    jobs = dom.find_all('div', {'class': 'vacancy-serp-item vacancy-serp-item_redesigned'})
    jobs_list = []
    for job in jobs:
        job_name_tag = job.find('a', {'class': 'bloko-link'})
        salary_tag = job.find('span', {'class': 'bloko-header-section-3'})
        company_name_tag = job.find('a', {'class': 'bloko-link bloko-link_kind-tertiary'})
        location_tag = job.find('div', {'class': 'bloko-text bloko-text_no-top-indent'})
        date_tag = job.find('span', {'class': 'bloko-text bloko-text_tertiary'})

        salary_min, salary_max, salary_currency = get_salary_data(salary_tag)

        job_data = {
            'job_name': job_name_tag.text if job_name_tag else None,
            'salary_min': salary_min,
            'salary_max': salary_max,
            'salary_currency': salary_currency,
            'company_name': company_name_tag.text if company_name_tag else None,
            'location': location_tag.text if location_tag else None,
            'date': date_tag.text if date_tag else None,
            'job_link': job_name_tag.get('href'),
            'source': 'https://hh.ru',
        }

        jobs_list.append(job_data)

    return jobs_list


def get_salary_data(salary_tag):
    """
    Возвращает список, состоящий из min, max значений зарплаты и валюты
    :param salary_tag: Тэг, содержащий информацию о зарплате
    :return: Список [min, max, валюта] - данные о зарплате
    """
    if salary_tag is None:
        return [None] * 3

    salary_text = salary_tag.text
    salary_data = []
    str_list = [clean_spaces(el).lower() for el in salary_text.split(' ')]
    for el in str_list:
        number = try_parse(el)
        if number is not None:
            salary_data.append(number)

    if 'до' in str_list:
        salary_data.insert(0, None)
    elif 'от' in str_list:
        salary_data.append(None)

    salary_data.append(clean_punctuation(str_list[-1]).upper())
    return salary_data


def main():
    job_name = 'data scientist'
    pages_count = 1

    # Запрашивание у пользователя названия вакансии и числа страниц
    job_name = prompt_job_name()
    if job_name is None:
        return

    pages_count = prompt_pages_count()
    if pages_count is None:
        return

    # Выполнение всех запросов и получение ответов
    responses = execute_requests(job_name, pages_count)

    # Получение списка с данными о вакансиях
    jobs_list = parse_responses(responses)

    # Запись полученного списка в файлы
    write_list_to_json(jobs_list, 'jobs.json')
    write_list_to_csv(jobs_list, 'jobs.csv')


main()
