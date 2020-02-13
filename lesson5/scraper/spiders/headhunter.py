# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from items import ScraperItem

class HeadhunterSpider(scrapy.Spider):
    key = 'python'
    name = 'headhunter'
    allowed_domains = ['hh.ru']
    start_urls = [f'https://hh.ru/search/vacancy?area=&st=searchVacancy&text={key}']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath(
            '//a[@class="bloko-button HH-Pager-Controls-Next HH-Pager-Control"]/@href').extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        vacancies = response.xpath('//a[@class="bloko-link HH-LinkModifier"]/@href').extract()

        for link in vacancies:
            yield response.follow(link, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):

        title = response.xpath('//h1[@class="header"]/text()').extract_first()
        url = response.url
        salary = response.xpath('//p[@class="vacancy-salary"]/text()').extract()
        if not salary:
            salary = response.xpath('//p[@class="vacancy-salary vacancy-salary_vacancyconstructor"]/text()').extract()

        location = response.xpath('//p[@data-qa="vacancy-view-location"]//text()').extract()
        employer = response.xpath('//a[@class="vacancy-company-name"]//text()').extract()

        yield ScraperItem(title=title, url=url, salary=salary, location=location, employer=employer)
