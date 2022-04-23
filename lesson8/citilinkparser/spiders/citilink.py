import scrapy


class CitilinkSpider(scrapy.Spider):
    name = 'citilink'
    allowed_domains = ['citilink.ru']
    start_urls = ['http://citilink.ru/']

    def parse(self, response):
        pass
