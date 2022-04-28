import scrapy
from scrapy.http import HtmlResponse
from citilinkparser.items import CitilinkparserItem
from scrapy.loader import ItemLoader


class CitilinkSpider(scrapy.Spider):
    name = 'citilink'
    allowed_domains = ['citilink.ru']
    start_urls = [
        'https://www.citilink.ru/catalog/smartfony/',
    ]

    def parse(self, response: HtmlResponse):
        links = response.xpath('//a[contains(@class, "ProductCardHorizontal__title")]//@href').getall()
        for link in links:
            yield response.follow(link, callback=self.parse_card)

    def parse_card(self, response: HtmlResponse):
        loader = ItemLoader(item=CitilinkparserItem(), response=response)
        loader.add_xpath('name', '//h1/text()')
        loader.add_xpath('price', '//span[contains(@class, "ProductHeader__price-default_current-price")]/text()')
        loader.add_xpath('display_size', '//div[text()[contains(., "Дисплей")]]/following-sibling::div/text()')
        loader.add_xpath('display_tech', '//div[text()[contains(., "Дисплей")]]/following-sibling::div/text()')
        loader.add_xpath('cpu', '//div[text()[contains(., "Процессор")]]/following-sibling::div/text()')
        loader.add_xpath('clock_rate', '//div[text()[contains(., "Процессор")]]/following-sibling::div/text()')
        loader.add_xpath('cores', '//div[text()[contains(., "Процессор")]]/following-sibling::div/text()')
        loader.add_xpath('ram', '//div[text()[contains(., "Объем оперативной памяти")]]/following-sibling::div/text()')
        loader.add_xpath('rom', '//div[text()[contains(., "Объем встроенной памяти")]]/following-sibling::div/text()')
        loader.add_xpath('os', '//div[text()[contains(., "Операционная система")]]/following-sibling::div/text()')
        loader.add_value('link', response.url)
        loader.add_xpath('photos', '//img[contains(@class, "PreviewList__image")]/@src')
        yield loader.load_item()
