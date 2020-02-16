# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import Compose, MapCompose, TakeFirst


def process_price(price_raw):

    return {
        'amount': int(price_raw[0].replace(' ', '')),
        'currency': 'RUR' if price_raw[1] == '₽' else price_raw[1],
        'units': price_raw[2],
    }


def process_features(features_raw):

    keys = [item.strip() for item in features_raw if not features_raw.index(item) % 2]
    values = [item.strip() for item in features_raw if features_raw.index(item) % 2]
    values = [float(v) if v.replace('.', '').isdigit() else v for v in values]

    return {key: value for key, value in zip(keys, values)}


class ProductItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    url = scrapy.Field(output_processor=TakeFirst())

    title = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(output_processor=Compose(process_price))
    description = scrapy.Field(output_processor=TakeFirst())

    features = scrapy.Field(output_processor=Compose(process_features))
    images = scrapy.Field(input_processor=Compose())
