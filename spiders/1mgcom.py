import scrapy
from json import loads

class AyurdataItem(scrapy.Item):
    sku = scrapy.Field()
    price = scrapy.Field()
    availability = scrapy.Field()
    rating = scrapy.Field()
    brand = scrapy.Field()
    manufacturer = scrapy.Field()
    image = scrapy.Field()
    desc = scrapy.Field()
    url = scrapy.Field()

class OneMgSpider(scrapy.Spider):
    name = '1mg.com'

    custom_settings = custom_settings = dict(
        CONCURRENT_REQUESTS = 3,
        DOWNLOAD_DELAY = 3,
        AUTOTHROTTLE_ENABLED= True,
        # ROTATING_PROXY_LIST = [
        #     # 'https://address:port',
        #     # 'http://address:port'
        # ],
        # DOWNLOADER_MIDDLEWARES = {
        #     'rotating_proxies.middlewares.RotatingProxyMiddleware': 800,
        #     'rotating_proxies.middlewares.BanDetectionMiddleware': 800,
        # }
    )

    allowed_domains = ['1mg.com']

    with open("./web.txt",'r') as f:
        start_urls = [url.strip() for url in f.readlines()]
        
    def parse(self, response):
        item = AyurdataItem()
        ld_json = loads(response.css('script[type="application/ld+json"]::text').get())
        item['sku'] = ld_json.get('sku')
        item['price'] = '{} {}'.format(
            ld_json.get('offers',{}).get('price'),
            ld_json.get('offers',{}).get('priceCurrency')
        )
        item['availability'] = ld_json.get('offers',{}).get('availability')
        item['rating'] = 'value: {} count: {}'.format(
            ld_json.get('aggregateRating').get('ratingValue'),
            ld_json.get('aggregateRating').get('ratingCount')
        )
        item['brand'] = ld_json.get('brand')
        item['manufacturer'] = ld_json.get('manufacturer',{}).get('name')
        item['desc'] = ld_json.get('description')
        item['image'] = ld_json.get('image')
        item['url'] = response.url
        yield item