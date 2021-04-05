from unicodedata import normalize
from scrapy import Spider, Request

class LinkGmbhSpider(Spider):
    name = "link-gmbh.de"
    download_delay = 1.5

    start_urls = [ 'https://shop.link-gmbh.de/steckergehaeuse/' ]

    # def start_requests(self):
    #   page_no = 355
    #   urls = ['https://shop.link-gmbh.de/steckergehaeuse/?p=%s' % p for p in range(1, page_no+1)]
    #   for url in urls:
    #       yield scrapy.Request(url=url, callback=self.parse_page)

    def parse(self, response):
        total_pages = response.xpath('//div[@class="listing"]/@data-pages').get()
        for page_no in range(1, int(total_pages) + 1):
            yield Request(
                    url=f'https://shop.link-gmbh.de/steckergehaeuse/?p={page_no}',
                    callback=self.parse_page,
                )
            
    def parse_page(self, response):
        product_title = response.css('a.product--title ::text').extract() 
        product_description = response.css('div.product--description ::text').extract() 
        link_idnr = response.css('span.entry--content ::text').extract()
        info = response.css('ul.product--base-info.list--unstyled').xpath('./following-sibling::text()[1]').extract() 
        vpe = response.css('div.price--unit').xpath('span[@class="is--nowrap"]/text()').extract()    
        product_price = response.css('span.price--default.is--nowrap ::text').extract() 

        for item in zip(product_title,product_description,link_idnr,info,vpe,product_price):
            scraped_info = {
                'product_title' : item[0].strip(),
                'product_description' : item[1].strip() ,
                'link_idnr' : item[2].strip(),
                'info' : item[3].strip(),
                'vpe' : item[4].strip(),
                'product_price': normalize('NFKD', item[5]).replace('\n*','').strip()
            }

            yield scraped_info
