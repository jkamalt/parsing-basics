# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient

from helpers.str_processing_helper import extract_and_try_parse, extract_letters, clean_spaces
from config.config import DB_HOST, DB_PORT


class JobparserPipeline:

    def __init__(self):
        client = MongoClient(DB_HOST, DB_PORT)
        self.db_mongo = client.vacancy_db

    def process_item(self, item, spider):
        process_salary = self.process_hh_salary
        if spider.name == 'superjobru':
            process_salary = self.process_superjob_salary
            item['name'] = ''.join(item['name'])

        item['salary_min'], item['salary_max'], item['salary_currency'] = process_salary(item['salary'])
        del item['salary']

        collection = self.db_mongo[spider.name]
        collection.insert_one(item)
        return item

    def process_hh_salary(self, salary):
        if not salary:
            return [None] * 3

        salary_clean = [clean_spaces(el).lower() for el in salary if el.split()]
        salary_data = []
        max_idx = 0
        for idx, el in enumerate(salary_clean):
            number = extract_and_try_parse(el)
            if number is not None:
                max_idx = idx
                salary_data.append(number)

        if not salary_data:
            return [None] * 3

        if len(salary_data) == 1:
            if 'до' in salary_clean:
                salary_data.insert(0, None)
            elif 'от' in salary_clean:
                salary_data.append(None)

        salary_data.append(extract_letters(salary_clean[max_idx + 1]).upper())
        return salary_data

    def process_superjob_salary(self, salary):
        if not salary:
            return [None] * 3

        salary_clean = [clean_spaces(el).lower() for el in salary if el.split()]
        salary_data = []
        max_idx = 0
        for idx, el in enumerate(salary_clean):
            number = extract_and_try_parse(el)
            if number is not None:
                max_idx = idx
                salary_data.append(number)

        if not salary_data:
            return [None] * 3

        if len(salary_data) == 1:
            if 'до' in salary_clean:
                salary_data.insert(0, None)
            elif 'от' in salary_clean:
                salary_data.append(None)
            else:
                salary_data.insert(0, None)
                max_idx += 1
        else:
            max_idx += 1

        salary_data.append(extract_letters(salary_clean[max_idx]).upper())
        return salary_data
