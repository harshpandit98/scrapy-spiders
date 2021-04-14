import json
from scrapy import Request, FormRequest
from scrapy.spiders import CrawlSpider
from manual_scraper_ext.items import Manual

class KawasakiSpider(CrawlSpider):
        name = 'kawasaki.com'
        download_delay = 2.0

        headers = { 'X-Requested-With': 'XMLHttpRequest',
                  'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
            }
        target_page = 'https://www.kawasaki.com/en-us/owner-center/service-manuals/{}/{}'
        product_cat_track = { '1' : 'MOTORCYCLE', '2' : 'ATV', '3' : 'SIDE X SIDE', '4' : 'WATERCRAFT'}
        
        def start_requests(self):
            get_years_url = 'https://www.kawasaki.com/en-us/ServiceManuals/ServiceAjaxModelYears'
            for product_cat_id in ['1','2','3','4']:
                yield FormRequest(get_years_url,
                    callback=self.get_vehicles_id,
                    method='POST',
                    formdata = dict( ProductCategoryId = product_cat_id, ModelYear = ''),
                    headers = self.headers,
                    meta = {
                        'product_cat': product_cat_id
                    }
                )

        def get_vehicles_id(self, response):
            get_vehicles_url ='https://www.kawasaki.com/en-us/ServiceManuals/ServiceAjaxVehicles'
            for cat_year in json.loads(response.text):
                yield FormRequest(
                    url = get_vehicles_url,
                    callback=self.form_target_url,
                    method='POST',
                    formdata = dict(ProductCategoryId = response.meta.get('product_cat'), ModelYear= cat_year['Id']),
                    headers = self.headers,
                    meta = {
                        'product_cat_key' : response.meta.get('product_cat'), 
                        'product_cat_year': cat_year['Id']
                    }
                )


        def form_target_url(self, response):
            for pid in json.loads(response.text):
                yield Request(
                    url = self.target_page.format(response.meta.get('product_cat_year'), pid['Id']),
                    meta = {
                        'model' : pid['Value'],
                        'model_year' : response.meta.get('product_cat_year'),
                        'product' : response.meta.get('product_cat_key')
                    },
                    callback = self.parse_products
                )

        def parse_products(self, response):
            manual_link = response.css('a[id="manualLink"] ::attr(href)').get()
            if manual_link is not None:
                manual = Manual()

                manual['product'] = self.product_cat_track[response.meta.get('product')]
                manual['brand'] = 'Kawasaki'
                manual['source'] = self.name
                manual['type'] = response.css('h3.headTwo.pb-2.pt-5 ::text').get()

                manual['model'] = '{} ({})'.format(response.meta.get('model'), response.meta.get('model_year'))
                manual['file_urls'] = [manual_link.replace(' ','%20')]
                manual['url'] = response.urljoin('')

                yield manual