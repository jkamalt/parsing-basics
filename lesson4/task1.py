# Урок 4
# 1. Написать приложение, которое собирает основные новости с сайта на выбор news.mail.ru, lenta.ru, yandex-новости.
# Для парсинга использовать XPath. Структура данных должна содержать:
#   - название источника;
#   - наименование новости;
#   - ссылку на новость;
#   - дата публикации.
# 2. Сложить собранные новости в БД


import requests
import time
from lxml import html

from config import USER_AGENT
from mongo_helper import write_news_to_db
from export_helper import write_list_to_json
from str_processing_helper import clean_nb_spaces


def execute_request(url):
    """
    Выполняет запрос по заданному url-адресу
    :param url: url-адрес сайта
    :return: ответ на запрос
    """
    headers = {'User-Agent': USER_AGENT}
    return requests.get(url, headers=headers)


def parse_response(response):
    """
    Возвращает список с данными по новостям - список словарей
    :param response: ответ на запрос
    :return: список словарей с данными по новостям
    """
    dom = html.fromstring(response.text)
    news_cards = dom.xpath('//a[@class="list__text"]')
    news_list = []
    for card in news_cards:
        url = card.xpath('./@href')[0]
        source, publish_date = get_add_info(url)

        news = {
            'source': source,
            'title': clean_nb_spaces(card.xpath('./text()')[0]),
            'url': url,
            'publish_date': publish_date,
        }
        news_list.append(news)

        time.sleep(1)

    return news_list


def get_add_info(news_url):
    """
    Выполняет дополнительный запрос по адресу новости для получения источника и даты публикации новости
    :param news_url: url-адрес новости
    :return: кортеж (источник, дата публикации) новости
    """
    response = execute_request(news_url)
    dom = html.fromstring(response.text)

    source = dom.xpath('//a[@class="link color_gray breadcrumbs__link"]/@href')[0]
    publish_date = dom.xpath('//span[@class="note__text breadcrumbs__text js-ago"]/@datetime')[0]

    return source, publish_date


def main():
    url = 'https://news.mail.ru'

    response = execute_request(url)
    news_list = parse_response(response)

    write_list_to_json(news_list, 'news.json')
    write_news_to_db(news_list, print_result=True)


main()
