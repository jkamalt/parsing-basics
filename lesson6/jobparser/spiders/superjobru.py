import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class SuperjobruSpider(scrapy.Spider):
    name = 'superjobru'
    allowed_domains = ['superjob.ru']
    start_urls = [
        'https://www.superjob.ru/vacancy/search/?keywords=python&geo%5Br%5D%5B0%5D=3',
        'https://www.superjob.ru/vacancy/search/?keywords=python&geo%5Br%5D%5B0%5D=2',
    ]

    def parse(self, response: HtmlResponse):
        next_page = response.xpath('//a[contains(@class, "f-test-button-dalshe")]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath('//span[@class="_1BiPY _26ig7 _1d47O"]//@href').getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        name = response.xpath('//h1//text()').getall()
        link = response.url
        salary = response.xpath('//span[@class="_1OuF_ ZON4b"]//text()').getall()
        item = JobparserItem(name=name, link=link, salary=salary)
        yield item
