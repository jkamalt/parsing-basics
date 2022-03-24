import hashlib
import json
import pymongo

from config import DB_HOST, DB_PORT
from pymongo.errors import DuplicateKeyError
from pprint import pprint


def write_list_to_db(input_list, print_result=False):
    """
    Записывает список словарей в БД MongoDB.
    :param input_list: список словарей, который будет записан в БД
    :param print_result: если True, то после записи в БД полученная колекция выводится на экран
    """
    if input_list is None:
        return

    with pymongo.MongoClient(DB_HOST, DB_PORT) as client:
        jobs = client.jobs_db.jobs

        for item in input_list:
            item_hash = calc_dict_hash(item)
            item_to_insert = {'_id': item_hash, **item}

            try:
                jobs.insert_one(item_to_insert)
            except DuplicateKeyError as e:
                print(e)
                print(f'Попытка добавить объект с существующим id. Объект не будет добавлен в БД.')
            except Exception as e:
                print(e)
                print(f'Ошибка при добавлении нового объекта. Объект не будет добавлен в БД.')

        if print_result:
            print_collection(jobs)


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
