# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class JobparserPipeline:

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.db_mongo = client.vacancy_db

    def process_item(self, item, spider):
        # item['min'], item['max'], item['cur'] = self.process_salary(item['salary'])
        collection = self.db_mongo[spider.name]
        collection.insert_one(item)
        return item

    def process_salary(self, salary):
        return 1, 2, 3
