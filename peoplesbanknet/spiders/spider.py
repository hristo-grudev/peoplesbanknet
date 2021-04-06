import scrapy

from scrapy.loader import ItemLoader

from ..items import PeoplesbanknetItem
from itemloaders.processors import TakeFirst


class PeoplesbanknetSpider(scrapy.Spider):
	name = 'peoplesbanknet'
	start_urls = ['https://www.peoplesbanknet.com/blog/']

	def parse(self, response):
		post_links = response.xpath('//div[@class="blog-info"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//a[@rel="next"]/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//article//p//text()[normalize-space()] | //div[@class="content"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()
		date = response.xpath('//span[@class="date"]/text()').get()

		item = ItemLoader(item=PeoplesbanknetItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
