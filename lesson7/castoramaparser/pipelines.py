# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

import scrapy
import json
import hashlib

from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from os.path import join
from pymongo import MongoClient
from config.config import DB_HOST, DB_PORT


class CastoramaparserPipeline:
    def __init__(self):
        self.result = []
        self.db_client = MongoClient(DB_HOST, DB_PORT)
        self.mongo_db = self.db_client.shops_db

    def close_spider(self, spider):
        self.db_client.close()
        with open('result.json', 'w', encoding='utf-8') as f:
            json.dump(self.result, f, ensure_ascii=False, indent=4)

    def process_item(self, item, spider):
        self.result.append(ItemAdapter(item).asdict())

        collection = self.mongo_db[spider.name]
        try:
            collection.insert_one(item)
        except Exception as e:
            print(f'Error occurred by insert item: {e}')

        return item


class CastoramaPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        item['photos'] = [el[1] for el in results if el[0]]
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        image_url_hash = hashlib.shake_256(request.url.encode()).hexdigest(5)
        item_url_hash = hashlib.shake_256(item['link'].encode()).hexdigest(5)
        return join(item_url_hash, f'{image_url_hash}.jpg')
