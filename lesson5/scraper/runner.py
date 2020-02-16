from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

import settings
from spiders.headhunter import HeadhunterSpider
from spiders.superjob import SuperjobSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(HeadhunterSpider, keyword='python')
    process.crawl(SuperjobSpider, keyword='python')
    process.start()
