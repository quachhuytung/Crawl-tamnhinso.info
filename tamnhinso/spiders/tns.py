# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
from scrapy.loader import ItemLoader
from scrapy.selector import Selector
from scrapy.shell import inspect_response
import pdb


class Film(scrapy.Item):
  img = scrapy.Field()
  name = scrapy.Field()
  alter_name = scrapy.Field()
  genre = scrapy.Field()
  description = scrapy.Field()
  origin = scrapy.Field()
  duration = scrapy.Field()
  copyright_year = scrapy.Field()
  medium = scrapy.Field()
  low = scrapy.Field()
  high = scrapy.Field()


class TnsSpider(scrapy.Spider):
  name = 'tns'
  allowed_domains = ['tamnhinso.info']
  start_urls = [
    'http://tamnhinso.info/phim/phim-le/viewbycategory?page=1',
  ]

  def start_requests(self):
    for url in self.start_urls:
      yield SplashRequest(url, self.parse)

  def parse(self, response):
    movie_items = response.xpath('//div[@class="col-md-2 col-xs-6 movie-item"]/a[@class="Tooltip"]/@href').extract()
    for item in movie_items:
      yield SplashRequest(response.urljoin(item), callback = self.parse_film)
    
    next_page = response.meta.get('next_page')
    num_next_page = 2 if next_page is None else next_page
    next_page_link = "phim/phim-le/viewbycategory?page="

    if num_next_page <= 88:
      yield response.follow(next_page_link + str(num_next_page), 
                    callback=self.parse, meta = {'next_page' : num_next_page + 1})
    
  def parse_film(self, response):
    item = ItemLoader(item=Film(), response=response)
    item.add_xpath('img', "//div[@class='movie-detail']//img[@itemprop='image']/@src")
    item.add_xpath('name', "//div[@class='movie-detail']//h1[@itemprop='name']/text()")
    item.add_xpath('alter_name', "//div[@class='movie-detail']//h2[@itemprop='alternateName']/text()")
    item.add_xpath('genre', "//div[@class='movie-detail']//p[@class='genre']/a/text()")
    item.add_xpath('description', "//div[@class='movie-detail']//div[@itemprop='description']/text()")
    item.add_xpath('origin', "//table//a[@class='Tooltip']/text()")
    item.add_xpath('duration', "//table//div[@itemprop='duration']/text()")
    item.add_xpath('copyright_year', "//table//div[@itemprop='copyrightYear']/text()")
    link_film_url = response.xpath("//div[@class='movie-detail']//div[@class='mt-10']/a/@href").extract_first()
    yield SplashRequest(response.urljoin(link_film_url), callback=self.parse_link_film, meta = {'film' : item } , args={'wait': 2})

  def parse_link_film(self, response):
    item = response.meta.get('film')
    item.selector = Selector(response)
    item.add_xpath('high', "//source[@label='1080']/@src")
    item.add_xpath('low', "//source[@label='360']/@src")
    item.add_xpath('medium', "//source[@label='720']/@src")
    return item.load_item()


