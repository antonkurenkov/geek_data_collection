# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from items import ProductItem
from scrapy.loader import ItemLoader


class LeroiSpider(scrapy.Spider):

    def __init__(self, keyword):
        self.allowed_domains = ['leroymerlin.ru']
        # self.name = f'leroi-{keyword}'
        self.name = f'leroi'
        self.start_urls = [f'https://leroymerlin.ru/search/?q={keyword}']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath('//div[@class="next-paginator-button-wrapper"]/a/@href').extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        products = response.xpath('//div[@class="product-name"]/a/@href').extract()

        for link in products:
            yield response.follow(link, callback=self.product_parse)

    def product_parse(self, response: HtmlResponse):
        loader = ItemLoader(item=ProductItem(), response=response)
        loader.add_xpath('title', '//h1[@slot="title"]/text()')
        loader.add_xpath('price', '//uc-pdp-price-view[@slot="primary-price"]/span/text()')
        loader.add_xpath('description', '//uc-pdp-section-vlimited/div/p/text()')
        loader.add_xpath('images', '//img[@alt="product image"]/@src')
        loader.add_value('url', response.url)
        yield loader.load_item()
        # title = response.xpath('//h1[@slot="title"]/text()').extract_first()
        # url = response.url
        # price = response.xpath('//uc-pdp-price-view[@slot="primary-price"]/span/text()').extract()
        # description = response.xpath('//uc-pdp-section-vlimited/div/p/text()').extract_first()
        # images = response.xpath('//img[@alt="product image"]/@src').extract()
        # yield ProductItem(title=title, url=url, price=price, description=description, images=images)
