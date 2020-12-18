import scrapy
# from scrapy.spiders import CrawlSpider, Rule
# from scrapy.linkextractors import LinkExtractor


class LinkGmbhSpider(scrapy.Spider):
	name = "link_gmbh"
	# domain_url = 'https://shop.link-gmbh.de/kontakte/?p=1'
	# start_urls =[domain_url+'kontakte/?p=1']
	
	# rules = (Rule(LinkExtractor(allow=(), restrict_css=('a.btn.is--primary.is--icon-right.js--load-more',)), callback="parse_page", follow= True),)
	def start_requests(self):
		page_no = 355

		urls = ['https://shop.link-gmbh.de/steckergehaeuse/?p=%s' % p for p in range(1, page_no+1)]
		# start_urls = ['https://shop.link-gmbh.de/steckergehaeuse/?p=%s' % page for page in range(100,176)]
		try:
			for url in urls:
			    yield scrapy.Request(url=url, callback=self.parse_page)
		except Exception as e:
			raise e
	# def start_requests(self):
		
	# 	# start_urls = ['https://www.blue-tomato.com/de-AT/products/categories/Snowboard+Shop-00000000/?page=%s' % page for page in range(1,PAGES+1)]
	# 	try:
	# 		for url in start_urls:
	# 		    yield scrapy.Request(url=url, callback=self.parse)
	# 	except Exception as e:
	# 		raise e
	def parse_page(self, response):
		product_title = response.css('a.product--title ::text').extract() 
		product_description = response.css('div.product--description ::text').extract() 
		link_idnr = response.css('span.entry--content ::text').extract()
		info = response.css('ul.product--base-info.list--unstyled').xpath('./following-sibling::text()[1]').extract() 
		vpe = response.css('div.price--unit').xpath('span[@class="is--nowrap"]/text()').extract()    
		product_price = response.css('span.price--default.is--nowrap ::text').extract() 

		for item in zip(product_title,product_description,link_idnr,info,vpe,product_price):
		#create a dictionary to store the scraped info
			scraped_info = {
			'product_title' : item[0].strip(),
			'product_description' : item[1].strip() ,
			'link_idnr' : item[2].strip(),
			'info' : item[3].strip(),
			'vpe' : item[4].strip(),
			'product_price': item[5].strip()
			}

			#yield or give the scraped info to scrapy
			yield scraped_info