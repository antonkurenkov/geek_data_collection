# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from items import VacancyItem
from scrapy.loader import ItemLoader


class HeadhunterSpider(scrapy.Spider):

    def __init__(self, keyword):
        # super().__init__()
        self.allowed_domains = ['hh.ru']
        # self.name = f'headhunter-{keyword}'
        self.name = 'headhunter'
        self.start_urls = [f'https://hh.ru/search/vacancy?area=&st=searchVacancy&text={keyword}']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath(
            '//a[@class="bloko-button HH-Pager-Controls-Next HH-Pager-Control"]/@href').extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        vacancies = response.xpath('//a[@class="bloko-link HH-LinkModifier"]/@href').extract()

        for link in vacancies:
            yield response.follow(link, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):

        loader = ItemLoader(item=VacancyItem(), response=response)
        loader.add_xpath('title', '//h1[@class="header"]/text()')
        loader.add_xpath('salary', '//p[@class="vacancy-salary"]/text()')
        loader.add_xpath('salary', '//p[@class="vacancy-salary vacancy-salary_vacancyconstructor"]/text()')
        loader.add_xpath('location', '//p[@data-qa="vacancy-view-location"]//text()')
        loader.add_xpath('employer', '//a[@class="vacancy-company-name"]//text()')

        # loader.add_xpath('location',
        #                  '//div[@class="bloko-column bloko-column_xs-4 bloko-column_s-0 bloko-column_m-0 bloko-column_l-0"]/div/div/p[2]/span/text()')
        # loader.add_xpath('employer',
        #                  '//div[@class="bloko-column bloko-column_xs-4 bloko-column_s-0 bloko-column_m-0 bloko-column_l-0"]/div/div/p/a[1]/span/text()')

        loader.add_value('url', response.url)
        yield loader.load_item()

        # title = response.xpath('//h1[@class="header"]/text()').extract_first()
        # url = response.url
        # salary = response.xpath('//p[@class="vacancy-salary"]/text()').extract()
        # if not salary:
        #     salary = response.xpath('//p[@class="vacancy-salary vacancy-salary_vacancyconstructor"]/text()').extract()

        # location = response.xpath('//p[@data-qa="vacancy-view-location"]//text()').extract()
        # employer = response.xpath('//a[@class="vacancy-company-name"]//text()').extract()

        # yield ScraperItem(title=title, url=url, salary=salary, location=location, employer=employer)
