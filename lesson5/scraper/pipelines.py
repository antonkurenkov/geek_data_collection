# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
import re


class DataBasePipeline(object):

    def __init__(self):
        # brew services start mongodb-community@4.2
        client = MongoClient('mongodb://127.0.0.1:27017')
        self.db = client.vacancies

    def process_item(self, item, spider):
        collection = self.db[spider.name]
        collection.update_one({'url': item['url']}, {'$set': item}, upsert=True)
        return item