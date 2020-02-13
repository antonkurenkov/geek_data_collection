# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
import re


class ScraperPipeline(object):

    def __init__(self):
        # brew services start mongodb-community@4.2
        client = MongoClient('mongodb://127.0.0.1:27017')
        self.db = client.vacancies

    def process_item(self, item, spider):
        collection = self.db[spider.name]

        salary = salary_process(item['salary'])

        data = {
            'title': item['title'],
            'employer': ''.join(item['employer']).strip().replace('\xa0', ' ') if item['employer'] else None,
            'location': ''.join(item['location']) if item['location'] else None,
            'url': item['url'],
            'salary_currency': salary['currency'],
            'salary_min': salary['min'],
            'salary_max': salary['max'],
        }
        collection.update_one({'url': data['url']}, {'$set': data}, upsert=True)
        return data


def salary_process(salary_raw):

    line = ''.join(salary_raw).strip()
    line = re.sub(r'\xa0', '', line)

    salary = {
        'currency': None,
        'min': None,
        'max': None
    }

    nums = re.findall(r'[0-9]{3,7}', line)
    if ' до вычета налогов' in line:
        line = line.replace(' до вычета налогов', '')
    elif ' на руки' in line:
        line = line.replace(' на руки', '')

    if nums:
        salary['currency'] = re.split('[0-9]', line)[-1].strip()
        if len(nums) == 2:
            salary['min'] = nums[0]
            salary['max'] = nums[1]
        else:
            if line[:2] == 'от':
                salary['min'] = nums[0]
            elif line[:2] == 'до':
                salary['max'] = nums[0]

    return salary
