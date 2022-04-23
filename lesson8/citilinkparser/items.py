# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst
from helpers.str_processing_helper import extract_and_try_parse, extract_and_try_parse_float, \
    extract_letters, clean_controls_and_strip


def get_clock_rate(cpu_str):
    cpu_data = cpu_str.split(',')
    if len(cpu_data) < 2:
        return None
    return extract_and_try_parse(cpu_data[1])


def get_cores_count(cpu_str):
    cpu_data = cpu_str.split(',')
    if len(cpu_data) < 3:
        return None
    return extract_and_try_parse(cpu_data[2])


class CitilinkparserItem(scrapy.Item):
    name = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(clean_controls_and_strip))
    price = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(extract_and_try_parse))
    display_size = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(extract_and_try_parse_float))
    display_tech = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(extract_letters))
    cpu = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(clean_controls_and_strip))
    clock_rate = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(get_clock_rate))
    cores = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(get_cores_count))
    ram = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(extract_and_try_parse))
    rom = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(extract_and_try_parse))
    os = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(clean_controls_and_strip))
    link = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field()
    _id = scrapy.Field()
