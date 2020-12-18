import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup
# const proxies = [ 'socks5://72.195.114.184', 'socks5://195.144.21.185','socks5://5.189.130.21'
#           ]
# const ports = [44527,1080,1080]
class esCoSpider(CrawlSpider):
	name = "esco"
	domain_url = 'https://www.es.co.th/'
	# [('Semiconductors - Discrete', 'tabs.asp?keyword=&catc=024'), 
	# ('Semiconductors - Integrated Circuit', 'tabs.asp?keyword=&catc=034'), 
	# ('Semiconductors - Power Modules', 'tabs.asp?keyword=&catc=043'), 
	# ('Boards and Modules', 'tabs.asp?keyword=&catc=018'),
	#  ('Connectors & Sockets', 'tabs.asp?keyword=&catc=006'), 
	#  ('Electromechanical', 'tabs.asp?keyword=&catc=019'),
	#   ('Industrial Automation', 'tabs.asp?keyword=&catc=002'), 
	#   ('Optoelectronics', 'tabs.asp?keyword=&catc=015'), 
	#   ('Passive Components', 'tabs.asp?keyword=&catc=020'), 
	#   ('Power, Circuit Protection', 'tabs.asp?keyword=&catc=013'),
	# 	]

	# {'Semiconductors - Discrete': 'https://www.es.co.th/tabs.asp?keyword=&catc=024',
	 # 'Semiconductors - Integrated Circuit': 'https://www.es.co.th/tabs.asp?keyword=&catc=034',
	 # 'Semiconductors - Power Modules': 'https://www.es.co.th/tabs.asp?keyword=&catc=043',
	 # 'Boards and Modules': 'https://www.es.co.th/tabs.asp?keyword=&catc=018',
	 # 'Connectors': 'https://www.es.co.th/tabs.asp?keyword=&catc=004',
	 # 'Sockets': 'https://www.es.co.th/tabs.asp?keyword=&catc=067',
	 # 'Audio Products': 'https://www.es.co.th/tabs.asp?keyword=&catc=039',
	 # 'Touch Panel': 'https://www.es.co.th/tabs.asp?keyword=&catc=041',
	 # 'Motors,Solenoids': 'https://www.es.co.th/tabs.asp?keyword=&catc=059',
	 # 'Switches, Keypads': 'https://www.es.co.th/tabs.asp?keyword=&catc=028',
	 # 'Thermal Printer & Accessories': 'https://www.es.co.th/tabs.asp?keyword=&catc=036',
	 # 'Relays': 'https://www.es.co.th/tabs.asp?keyword=&catc=021',
	 # 'Validators': 'https://www.es.co.th/tabs.asp?keyword=&catc=068',
	 # 'Industrial Automation': 'https://www.es.co.th/tabs.asp?keyword=&catc=002',
	 # 'Optoelectronics': 'https://www.es.co.th/tabs.asp?keyword=&catc=015',
	 # 'Filters': 'https://www.es.co.th/tabs.asp?keyword=&catc=008',
	 # 'Capacitors': 'https://www.es.co.th/tabs.asp?keyword=&catc=003',
	 # 'Crystals / Oscillators / Resonators': 'https://www.es.co.th/tabs.asp?keyword=&catc=035',
	 # 'Resistors': 'https://www.es.co.th/tabs.asp?keyword=&catc=022',
	 # 'Potentiometers / Variable Resistors': 'https://www.es.co.th/tabs.asp?keyword=&catc=029',
	 # 'Inductors/Coils/Chokes': 'https://www.es.co.th/tabs.asp?keyword=&catc=055',
	 # 'Thermistors': 'https://www.es.co.th/tabs.asp?keyword=&catc=017',
	 # 'Power, Circuit Protection': 'https://www.es.co.th/tabs.asp?keyword=&catc=013'}

	start_urls = [domain_url +'tabs.asp?keyword=&catc=024', 
				 domain_url +'tabs.asp?keyword=&catc=034', 
				 domain_url + 'tabs.asp?keyword=&catc=043', 
				domain_url +'tabs.asp?keyword=&catc=018',
				 domain_url +'tabs.asp?keyword=&catc=006', 
				 domain_url +'tabs.asp?keyword=&catc=019',
				domain_url + 'tabs.asp?keyword=&catc=002', 
				domain_url +  'tabs.asp?keyword=&catc=015', 
				domain_url +  'tabs.asp?keyword=&catc=020', 
				domain_url + 'tabs.asp?keyword=&catc=013'
				]

	rules = (Rule(LinkExtractor(allow=(), restrict_xpaths=('//a[@class="next_paginator_lnk"]',)), callback="parse_page", follow= True),)
	# def start_requests(self):
	# 	urls = [('Semiconductors - Discrete', 'tabs.asp?keyword=&catc=024'), 
	# 			('Semiconductors - Integrated Circuit', 'tabs.asp?keyword=&catc=034'), 
	# 			('Semiconductors - Power Modules', 'tabs.asp?keyword=&catc=043'), 
	# 			('Boards and Modules', 'tabs.asp?keyword=&catc=018'),
	# 			 ('Connectors & Sockets', 'tabs.asp?keyword=&catc=006'), 
	# 			 ('Electromechanical', 'tabs.asp?keyword=&catc=019'),
	# 			  ('Industrial Automation', 'tabs.asp?keyword=&catc=002'), 
	# 			  ('Optoelectronics', 'tabs.asp?keyword=&catc=015'), 
	# 			  ('Passive Components', 'tabs.asp?keyword=&catc=020'), 
	# 			  ('Power, Circuit Protection', 'tabs.asp?keyword=&catc=013')
	# 			]
	# 	for _,u in urls:
	# 		yield scrapy.Request(self.domain_url+u, callback=self.parse_page)

	def parse_page(self, response):
		# dt_mfrpn = response.css("div.dt_mfrpn *::text").extract()
		# dt_mfrpnname = response.css("div.dt_mfrpnname ::text").extract()  
		# mfrbox = response.css("div.mfrbox *::text").extract()  
		# dt_espntopic = response.css("div.dt_espntopic ::text").extract()
		cat_name = response.css('div.catselected_right ::text').extract_first()
		trs = response.xpath('//div[contains(@style, "float:left;width:100%;min-height:100px;height:auto;margin-top:-1px;padding:20px 0 10px 0px;background-color:#fff;border:solid 1px #cccccc;")]').extract()
		
		prodData = []
		for d in (trs):
			soup = BeautifulSoup(d,features="lxml")
			dt_mfrpn = soup.find("div", class_='dt_mfrpn').text
			dt_mfrpnname = soup.find("div", class_='dt_mfrpnname').text
			dt_espn = soup.find("div", class_='dt_espn').text
			desc = (soup.find_all("div", class_='dt_desc'))
			stockamount = soup.find("div", class_='stockamount').text
			desc_text = ' '.join(de.text for de in desc)
			prodData.append( tuple(
	                                (
	                                 dt_mfrpn, dt_mfrpnname, dt_espn, desc_text, stockamount
	                                )
	                        )
	                      )
		# dt_espn = response.css("div.dt_espn ::text").extract()
		# dt_desc =  response.css("div.dt_desc ::text").extract()
		# qty_lv = response.css("div.qty_lv ::text").extract()
		# price_lv = response.css("div.price_lv ::text").extract()  
		# stockamount = response.css("div.stockamount ::text").extract()  
		for item in prodData:
		#create a dictionary to store the scraped info
			scraped_info = {
			'Product P/N' : item[0],
			'Manufacturer' : item[1] ,
			'ES-P/N' : item[2],
			'Product Desc' : item[3],
			'Stock in hand': item[4],
			'Product Category' : cat_name
			}

			#yield or give the scraped info to scrapy
			yield scraped_info