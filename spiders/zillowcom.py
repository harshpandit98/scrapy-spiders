from scrapy import Spider, Request

class ZillowSpider(Spider):
    name = 'zillow.com'
    
    custom_settings = {
        'DOWNLOAD_DELAY': 3,
        'CONCURRENT_REQUESTS': 2,
        'AUTOTHROTTLE_ENABLED': True
    }

    base_url = 'https://www.zillow.com/'
    
    suggetion_endpoint = 'https://www.zillowstatic.com/autocomplete/v2/suggestions?q={}'
    user_agent = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0'}
    
    def start_requests(self):
        yield Request(
                url=self.suggetion_endpoint.format(self.region),
                headers=self.user_agent,
                callback=self.locate_region
            )

    def locate_region(self, response):
        regions = response.json().get('resultGroups',[{}])[0].get('results',[])
        for region_json in regions:
            display_tag = region_json.get('display')
            yield Request(
                    url=self.base_url + display_tag.replace(',','').replace(' ','-').lower(),
                    callback=self.parse_listings,
                    headers=self.user_agent,
                    meta={
                        'region': display_tag
                    }
                )

    def parse_listings(self, response):
        for article in response.xpath('//article[@role="presentation"]'):
            item = {}
            item['region'] = response.meta['region']
            item['price'] = article.css('div.list-card-price::text').get()
            item['address'] = article.css('address::text').get()
            item['bds'] = article.xpath('.//ul[@class="list-card-details"]/li[*[contains(.,"bds")]]/text()').get()
            item['ba'] = article.xpath('.//ul[@class="list-card-details"]/li[*[contains(.,"ba")]]/text()').get()
            item['sqft'] = article.xpath('.//ul[@class="list-card-details"]/li[*[contains(.,"sqft")]]/text()').get()
            item['status'] = article.css('li.list-card-statusText::text').get()
            item['listing_url'] = article.css('div.list-card-info > a::attr(href)').get()
            yield item