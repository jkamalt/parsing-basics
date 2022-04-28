from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from citilinkparser import settings
from citilinkparser.spiders.citilink import CitilinkSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(CitilinkSpider)

    process.start()
