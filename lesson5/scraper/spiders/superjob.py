# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from items import ScraperItem

class SuperjobSpider(scrapy.Spider):
    key = 'python'
    name = 'superjob'
    allowed_domains = ['superjob.ru']
    start_urls = [f'https://russia.superjob.ru/vacancy/search/?keywords={key}']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath(
            '//a[@rel="next"]/@href').extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        vacancies = response.xpath('//div[@class="_3syPg _3P0J7 _9_FPy"]/div/a/@href').extract()

        for link in vacancies:
            yield response.follow(link, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):

        title = response.xpath('//h1[@class="_3mfro rFbjy s1nFK _2JVkc"]//text()').extract_first()
        url = response.url
        salary = response.xpath('//span[@class="_3mfro _2Wp8I ZON4b PlM3e _2JVkc"]//text()').extract()
        location = response.xpath('//span[@class="_3mfro _1hP6a _2JVkc"]/text()').extract_first()
        employer = response.xpath('//h2[@class="_3mfro PlM3e _2JVkc _2VHxz _3LJqf _15msI"]/text()').extract()

        yield ScraperItem(title=title, url=url, salary=salary, location=location, employer=employer)