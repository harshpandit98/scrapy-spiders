from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup

class esCoSpider(CrawlSpider):
    name = "es.co.th"
    download_delay = 1.5

    domain_url = 'https://www.es.co.th/'

    start_urls = [
        domain_url + 'tabs.asp?keyword=&catc=024', 
        domain_url + 'tabs.asp?keyword=&catc=034', 
        domain_url + 'tabs.asp?keyword=&catc=043', 
        domain_url + 'tabs.asp?keyword=&catc=018',
        domain_url + 'tabs.asp?keyword=&catc=006', 
        domain_url + 'tabs.asp?keyword=&catc=019',
        domain_url + 'tabs.asp?keyword=&catc=002', 
        domain_url + 'tabs.asp?keyword=&catc=015', 
        domain_url + 'tabs.asp?keyword=&catc=020', 
        domain_url + 'tabs.asp?keyword=&catc=013'
    ]

    rules = (Rule(LinkExtractor(
                    allow=(), 
                    restrict_xpaths=('//a[@class="next_paginator_lnk"]',)),
            callback="parse_page", follow= True),
    )

    def parse_start_url(self,response):
        return self.parse_page(response)

    def parse_page(self, response):
        cat_name = response.css('div.catselected_right ::text').extract_first()
        trs = response.xpath(
            '//div[contains(@style, "float:left;width:100%;min-height:100px;height:auto;margin-top:-1px;padding:20px 0 10px 0px;background-color:#fff;border:solid 1px #cccccc;")]').extract()
        
        prodData = []
        for tr in trs:
            soup = BeautifulSoup(tr,features="lxml")
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

        for item in prodData:
            scraped_info = {
            'Product P/N' : item[0],
            'Manufacturer' : item[1] ,
            'ES-P/N' : item[2],
            'Product Desc' : item[3],
            'Stock in hand': item[4],
            'Product Category' : cat_name
            }

            yield scraped_info
