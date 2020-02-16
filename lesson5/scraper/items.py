# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import Compose, MapCompose, TakeFirst
import re


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


def location_process(location_raw):
    if location_raw:
        if location_raw[:int(len(location_raw) / 2)] == location_raw[int(len(location_raw) / 2):]:
            location_raw = location_raw[:int(len(location_raw) / 2)]
        return ''.join(location_raw).strip()


def employer_process(employer_raw):
    if employer_raw:
        if employer_raw[:int(len(employer_raw) / 2)] == employer_raw[int(len(employer_raw) / 2):]:
            employer_raw = employer_raw[:int(len(employer_raw) / 2)]
        return ''.join(employer_raw).replace('\xa0', ' ').strip()


class VacancyItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    title = scrapy.Field(output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    salary = scrapy.Field(output_processor=Compose(salary_process))
    location = scrapy.Field(output_processor=Compose(location_process))
    employer = scrapy.Field(output_processor=Compose(employer_process))
