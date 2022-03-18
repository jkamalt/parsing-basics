import hashlib
import json
import pymongo

from config import DB_HOST, DB_PORT
from pymongo.errors import DuplicateKeyError
from pprint import pprint


def write_jobs_to_db(jobs_list, print_result=False):
    """
    Записывает список вакансий в БД MongoDB.
    :param jobs_list: список вакансий - список словарей, который будет записан в БД
    :param print_result: если True, то после записи в БД полученная колекция выводится на экран
    """
    if jobs_list is None:
        return

    with pymongo.MongoClient(DB_HOST, DB_PORT) as client:
        jobs = client.jobs_db.jobs
        add_items_to_collection(jobs_list, jobs)

        if print_result:
            print_collection(jobs)


def write_news_to_db(news_list, print_result=False):
    """
    Записывает список новостей в БД MongoDB
    :param news_list: список новостей - список словарей, который будет записан в БД
    :param print_result: если True, то после записи в БД полученная колекция выводится на экран
    """
    if news_list is None:
        return

    with pymongo.MongoClient(DB_HOST, DB_PORT) as client:
        news = client.news_db.news
        add_items_to_collection(news_list, news)

        if print_result:
            print_collection(news)


def add_items_to_collection(items, collection):
    """
    Записывает список словарей items в коллекцию collection БД MongoDB
    :param items: список словарей для записи в БД
    :param collection: коллекция БД, куда будут добавлены новые элементы
    """
    for item in items:
        item_hash = calc_dict_hash(item)
        item_to_insert = {'_id': item_hash, **item}

        try:
            collection.insert_one(item_to_insert)
        except DuplicateKeyError as e:
            print(e)
            print(f'Попытка добавить объект с существующим id. Объект не будет добавлен в БД.')
        except Exception as e:
            print(e)
            print(f'Ошибка при добавлении нового объекта. Объект не будет добавлен в БД.')


def calc_dict_hash(input_dict):
    """
    Вычисляет MD5 хэш словаря
    :param input_dict: словарь, для которого будет вычислен хэш
    :return: хэш словаря
    """
    dict_str = json.dumps(input_dict, sort_keys=True).encode()
    method = hashlib.md5(dict_str)
    return method.hexdigest()


def print_jobs_with_salary_greater_than(salary_min):
    """
    Выводит на экран список вакансий из БД с зарплатой больше заданного значения
    :param salary_min: минимальное значение зарплаты
    """
    with pymongo.MongoClient(DB_HOST, DB_PORT) as client:
        jobs = client.jobs_db.jobs

        print(f'Список вакансий с зарплатой больше {salary_min} руб:')
        for job in jobs.find({'$or': [{'salary_min': {'$gt': salary_min}}, {'salary_max': {'$gt': salary_min}}]}):
            pprint(job)


def print_collection(collection):
    """
    Выводит на экран все элементы коллекции в БД
    :param collection: коллекция в БД
    """
    for doc in collection.find({}):
        pprint(doc)
