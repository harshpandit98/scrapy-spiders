import scrapy
class BlueTomatoSpider(scrapy.Spider):
	name = "bluetomato"
	def start_requests(self):
		PAGES = 34
		start_urls = ['https://www.blue-tomato.com/de-AT/products/categories/Snowboard+Shop-00000000/?page=%s' % page for page in range(1,PAGES+1)]
		try:
			for url in start_urls:
			    yield scrapy.Request(url=url, callback=self.parse)
		except Exception as e:
			raise e
	def parse(self, response):
		title = response.css("li.productcell ").css("span.productdesc").xpath('a/div/div/p/text()').extract()   
		# response.xpath("//div[@class='ellipsis']/div/p/text()").extract()  #r   
		price =  response.css("li.productcell ").css("span.productdesc").xpath('span[1]/text()').extract()  
		# response.xpath("//span[@class='productdesc']/span[1]/text()").extract() 
		price = [ p.strip() for p in price if len(p.strip()) > 0] #r              

		# img_url = response.xpath("//span[@class='productimage']/img/@data-src").extract()
		img_url = response.css("li.productcell ").css("span.productimage").xpath('img/@src').extract()[:6]   
		img_url += response.css("li.productcell ").css("span.productimage").xpath('img/@data-src').extract()    
		prod_url = response.css("li.productcell ").xpath('@data-href').extract()  
		# response.xpath("//span[@class='productdesc']/a/@href").extract()  #r
		# response.css("li.productcell ").xpath('@data-href').extract()  
		for item in zip(title,price,img_url,prod_url):
		#create a dictionary to store the scraped info
			scraped_info = {
			'Name' : item[0],
			'Price' : item[1] ,
			'ImageUrl' : "https:"+ item[2],
			'ProductUrl' : "https://www.blue-tomato.com"+item[3],
			}

			#yield or give the scraped info to scrapy
			yield scraped_info