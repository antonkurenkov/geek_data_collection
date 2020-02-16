# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient


from scrapy.utils.python import to_bytes
import hashlib


class DataBasePipeline(object):

    def __init__(self):
        # brew services start mongodb-community@4.2
        client = MongoClient('mongodb://127.0.0.1:27017')
        self.db = client.products

    def process_item(self, item, spider):
        collection = self.db[spider.name][spider.keyword]
        collection.update_one({'url': item['url']}, {'$set': item}, upsert=True)
        return item


class ProductImagePipeline(ImagesPipeline):

    def file_path(self, request, response=None, info=None):
        spider = info.spider.name
        keyword = info.spider.start_urls[0].split('/?q=')[-1]
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        return f'full/{spider}/{keyword}/{image_guid}.jpg'

    def get_media_requests(self, item, info):
        if item['images']:
            for img in item['images']:
                try:

                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        if results:
            item['images'] = [itm[1] for itm in results if itm[0]]
        return item
