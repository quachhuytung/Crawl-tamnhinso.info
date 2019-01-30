import scrapy
from scrapy.loader.processors import TakeFirst

class PhimLeItem(scrapy.Item):
    id = scrapy.Field(output_processor=TakeFirst())
    title_en = scrapy.Field(output_processor=TakeFirst())
    title_vi = scrapy.Field(output_processor=TakeFirst())
    description = scrapy.Field()
    genres = scrapy.Field()
    imdb = scrapy.Field(output_processor=TakeFirst())
    poster = scrapy.Field(output_processor=TakeFirst())
    origins = scrapy.Field()
    release_year = scrapy.Field(output_processor=TakeFirst())
    duration = scrapy.Field(output_processor=TakeFirst())
    link = scrapy.Field(output_processor=TakeFirst())

class PhimBoItem(scrapy.Item):
    id = scrapy.Field(output_processor=TakeFirst())
    title_en = scrapy.Field(output_processor=TakeFirst())
    title_vi = scrapy.Field(output_processor=TakeFirst())
    description = scrapy.Field()
    genres = scrapy.Field()
    imdb = scrapy.Field(output_processor=TakeFirst())
    poster = scrapy.Field(output_processor=TakeFirst())
    origins = scrapy.Field()
    release_year = scrapy.Field(output_processor=TakeFirst())
    duration = scrapy.Field(output_processor=TakeFirst())
    episode = scrapy.Field(output_processor=TakeFirst())

class Episode(scrapy.Item):
    ep_num = scrapy.Field(output_processor=TakeFirst())
    link = scrapy.Field(output_processor=TakeFirst())

class Link(scrapy.Item):
    link_360 = scrapy.Field(output_processor=TakeFirst())
    link_720 = scrapy.Field(output_processor=TakeFirst())
    link_1080 = scrapy.Field(output_processor=TakeFirst())
