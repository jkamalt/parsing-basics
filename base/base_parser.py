import pymongo

from config.config import DB_HOST, DB_PORT
from helpers.export_helper import write_list_to_json, write_list_to_csv
from helpers.mongo_helper import add_items_to_collection, print_collection


class BaseParser:
    """ Базовый парсер """

    def __init__(self):
        self._result = []

    @property
    def url_to_parse(self):
        """
        Адрес сайта в виде строки, который будет парситься.
        """
        return NotImplementedError('Свойство не реализовано!')

    @property
    def db_name(self):
        """
        Название БД в виде строки, куда будет записан результат работы парсера.
        """
        return NotImplementedError('Свойство не реализовано!')

    @property
    def collection_name(self):
        """
        Название коллекции в БД в виде строки, куда будет записан результат работы парсера.
        """
        return NotImplementedError('Свойство не реализовано!')

    def _get_items(self):
        """
        Возвращает список элементов страницы, которые содержат нужную информацию.
        :return: список элементов
        """
        return NotImplementedError('Метод не реализован!')

    def _parse_items(self, items):
        """
        Парсит список элементов страницы, которые содержат нужную информацию.
        :param items: список элементов
        """
        return NotImplementedError('Метод не реализован!')

    def _parse_item(self, item):
        """
        Парсит элемент страницы, который содержит нужную информацию.
        :param item: элемент страницы, который содержит нужную информацию
        """
        return NotImplementedError('Метод не реализован!')

    def parse(self):
        """
        Парсит сайт с адресом url_to_parse.
        """
        return NotImplementedError('Метод не реализован!')

    def write_result_to_db(self, print_db_collection=False):
        """
        Записывает результат работы парсера в БД Mongo.
        """
        if not self._result:
            return
        try:
            with pymongo.MongoClient(DB_HOST, DB_PORT) as client:
                db = client[self.db_name]
                collection = db[self.collection_name]

                add_items_to_collection(self._result, collection)

                if print_db_collection:
                    print_collection(collection)
        except Exception as e:
            print(f'При записи в БД Mongo произошла ошибка: {e}')

    def write_result_to_json(self, file_name, ensure_ascii=True):
        """
        Записывает результат работы парсера в json-файл с заданным именем.
        :param file_name: имя файла, куда будут записаны данные
        :param ensure_ascii: экранирование ASCII-символов
        """
        try:
            if self._result:
                write_list_to_json(self._result, file_name, ensure_ascii=ensure_ascii)
        except Exception as e:
            print(f'При записи в json-файл произошла ошибка: {e}')

    def write_result_to_csv(self, file_name):
        """
        Записывает результат работы парсера в csv-файл с заданным именем.
        :param file_name: имя файла, куда будут записаны данные
        """
        try:
            if self._result:
                write_list_to_csv(self._result, file_name)
        except Exception as e:
            print(f'При записи в csv-файл произошла ошибка: {e}')
