# -*- coding: utf-8 -*-
import scrapy
from scrapy.shell import inspect_response
from scrapy import Request
from scrapy.loader import ItemLoader
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from tamnhinso.items import PhimBoItem, Episode, Link
from scrapy_splash import SplashRequest
import pdb

class PhimleSpider(scrapy.Spider):
    name = 'phimbo'
    allowed_domains = ['tamnhinso.info']
    start_urls = [
      'http://tamnhinso.info/phim/phim-bo/viewbycategory',
    ]
    
    def start_requests(self):
      for url in self.start_urls:
        yield Request(url=url, callback=self.parse_list_movie)

    def parse_list_movie(self, response):
      movie_urls = LinkExtractor(restrict_xpaths="//div[@class='col-md-2 col-xs-6 movie-item']").extract_links(response)
      for item in movie_urls:
        yield Request(url=item.url, callback=self.parse_movie_info)
      
      next_page = response.meta.get('next_page')
      num_next_page = 2 if next_page is None else next_page
      next_page_link = "phim/phim-bo/viewbycategory?page="

      if num_next_page <= 40:
        yield response.follow(next_page_link + str(num_next_page), 
                      callback=self.parse_list_movie, meta = {'next_page' : num_next_page + 1})
    
    def parse_movie_info(self, response):
      l = ItemLoader(item=PhimBoItem(), response=response)
      l.add_value('id', response.url, re = r'\.(\d+)\/')
      l.add_xpath('title_en', '//h1[@class="movie-title-en"]/text()')
      l.add_xpath('title_vi', '//h2[@class="movie-title-vi"]/text()')
      l.add_xpath('description', '//div[@class="movie-desc"]/text()')
      l.add_xpath('genres', '//p[@class="genre"]/a/text()')
      l.add_xpath('imdb', '//span[@class="imdb-mark"]/text()')
      l.add_xpath('poster', '//img[@itemprop="image"]/@src')
      l.add_xpath('origins', "//table//a[@class='Tooltip']/text()")
      l.add_xpath('release_year', '//div[@itemprop="copyrightYear"]/text()')
      l.add_xpath('duration', '//div[@itemprop="duration"]/text()')

      link_film_url = response.xpath("//div[@class='movie-detail']//div[@class='mt-10']/a/@href").extract_first()
      yield scrapy.Request(url=response.urljoin(link_film_url), callback=self.parse_list_episode, meta={"item": l})
      

    def parse_list_episode(self, response):
        loader = response.meta.get('item')
        script = """
                function main(splash)
                    splash.html5_media_enabled = true
                    splash.private_mode_enabled = false
                    assert(splash:go(splash.args.url))
                    assert(splash:wait(3))
                    return splash:html()
                end
            """
        for episode in LinkExtractor(restrict_xpaths="//div[@class='col-md-6 mt-20 watch-chap']").extract_links(response):
            yield SplashRequest(url=response.urljoin(episode.url), callback=self.parse_link_episode, meta={'item': loader}, endpoint='execute',
                                    args={'lua_source': script,'wait': 5, 'timeout': 3600})
    
    def parse_link_episode(self, response):
      loader = response.meta.get('item')
      loader.replace_value('episode', self.get_episode(response))
      return loader.load_item()

    def get_episode(self, response):
        l = ItemLoader(item=Episode(), response=response)
<<<<<<< HEAD
        l.add_value('ep_num', response.url, re = r'tap\-(\d+)')
=======
        l.add_value('ep_num', response.url, re = r'\-(\d+)')
>>>>>>> eaf6d477aa6c754c86deb985bc47d456e57e424f
        l.add_value('link', self.get_link(response))
        return dict(l.load_item())
            

    def get_link(self, response):
      l = ItemLoader(item=Link(), response=response)
      l.add_xpath('link_360', "//source[@label='360']/@src")
      l.add_xpath('link_720', "//source[@label='720']/@src")
      l.add_xpath('link_1080',  "//source[@label='1080']/@src")
      
      return dict(l.load_item())

<<<<<<< HEAD
  
=======
  
>>>>>>> eaf6d477aa6c754c86deb985bc47d456e57e424f
