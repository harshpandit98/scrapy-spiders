import scrapy
import pandas as pd
from serp.serp_urls import generate_urls

class OneillSpider(scrapy.Spider):
	name = "oneill.com"
	def start_requests(self):
		# start_urls = generate_urls()
		start_urls = pd.read_csv('prod_urls.csv')
		
		for url in start_urls['Product Page URL']:
			if ('product url with' not in url) and ('No results' not in url):
			    yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		title = response.xpath("//span[@itemprop]/text()").extract_first()  
		price = response.xpath("//span[@class='sales']/span/text()").extract_first()

		scraped_info = {
		'Name' : title,
		'Price' : price.strip() ,
		'Product Url': response.url 
		}

		yield scraped_info
