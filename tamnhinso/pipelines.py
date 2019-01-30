import codecs
import pdb
import json
from scrapy.exceptions import DropItem

class FilterNullLinkPipeline(object):
  def process_item(self, item, spider):
    if spider.name == 'phimle':
      if all(len(element) is 0 for element in item['link']):
        raise DropItem("Missing link")
    if spider.name == 'phimbo':
      if all(len(element) is 0 for element in item['episode']['link']):
        raise DropItem("Missing link")
    return item

class DescriptionProcessorPipeline(object):
  def process_item(self, item, spider):
    item['description'] = " ".join(item['description'][0].split())
    return item

class JsonWriterPipeline(object):
  def open_spider(self, spider):
    self.file = codecs.open('items.jl', 'w', encoding='utf-8')

  def close_spider(self, spider):
    self.file.close()

  def process_item(self, item, spider):
    line = json.dumps(dict(item), ensure_ascii=False) + "\n"
    self.file.write(line)
    return item