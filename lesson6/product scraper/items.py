# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import Compose, MapCompose, TakeFirst


def process_price(values):

    return {
        'amount': int(values[0].replace(' ', '')),
        'currency': 'RUR' if values[1] == '₽' else values[1],
        'units': values[2],
    }


def process_images(values):
    return values


class ProductItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    url = scrapy.Field(output_processor=TakeFirst())

    title = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(output_processor=Compose(process_price))
    description = scrapy.Field(output_processor=TakeFirst())
    images = scrapy.Field(input_processor=Compose())
