import requests
import time
from lxml import html

from base.base_parser import BaseParser
from config.config import USER_AGENT
from helpers.str_processing_helper import clean_nb_spaces


class NewsMailParser(BaseParser):
    """ Парсер для новостей news.mail.ru """

    @property
    def url_to_parse(self):
        return 'https://news.mail.ru'

    @property
    def db_name(self):
        return 'news_db'

    @property
    def collection_name(self):
        return 'news_mail_ru'

    def _get_items(self):
        """
        Возвращает список элементов страницы, которые содержат новости.
        :return: список элементов страницы
        """
        response = self._execute_request(self.url_to_parse)
        dom = html.fromstring(response.text)

        items = dom.xpath('//a[@class="list__text"]')
        items.extend(dom.xpath('//a[contains(@class, "js-topnews__item")]'))
        items.extend(dom.xpath('//a[contains(@class, "newsitem__title")]'))
        items.extend(dom.xpath('//a[@class="link link_flex"]'))
        return items

    def _parse_items(self, items):
        """
        Парсит элементы страницы, которые содержат новости.
        :param items: список элементов страницы, которые содержат новости
        """
        for item in items:
            try:
                self._parse_item(item)
                time.sleep(1)
            except Exception as e:
                print(f'При парсинге новости произошла ошибка: {e}')

    def _parse_item(self, item):
        """
        Парсит элемент страницы с новостью.
        :param item: элемент страницы с новостью
        """
        url = item.xpath('./@href')[0]
        source, publish_date = self._get_add_info(url)

        news = {
            'source': source,
            'title': clean_nb_spaces(item.xpath('.//text()')[0]),
            'url': url,
            'publish_date': publish_date,
        }
        self._result.append(news)

    def parse(self):
        try:
            items = self._get_items()
            self._parse_items(items)
        except Exception as e:
            print(f'При парсинге сайта произошла ошибка: {e}')

    def _execute_request(self, url):
        """
        Выполняет запрос по заданному url-адресу
        :param url: url-адрес сайта
        :return: ответ на запрос
        """
        headers = {'User-Agent': USER_AGENT}
        return requests.get(url, headers=headers)

    def _get_add_info(self, news_url):
        """
        Выполняет дополнительный запрос по адресу новости для получения источника и даты публикации новости
        :param news_url: url-адрес новости
        :return: кортеж (источник, дата публикации) новости
        """
        response = self._execute_request(news_url)
        dom = html.fromstring(response.text)

        source = dom.xpath('//a[@class="link color_gray breadcrumbs__link"]/@href')[0]
        publish_date = dom.xpath('//span[@class="note__text breadcrumbs__text js-ago"]/@datetime')[0]

        return source, publish_date
