from re import compile
from scrapy import Spider, Request

rm_newline_or_space = compile(r'\s|\n')

class AgriAffairesSpider(Spider):
    name = 'agriaffaires.us'

    custom_settings = {
        'DOWNLOAD_DELAY': 1.5,
        'CONCURRENT_REQUESTS': 3,
        'AUTOTHROTTLE_ENABLED': True
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0',
    }

    def start_requests(self):
        yield Request(
                url='https://www.agriaffaires.us/',
                callback=self.category_navigator,
                headers=self.headers
            )

    def category_navigator(self, response):
        for category_url in response.css(
            'div.js-div-submenu1 > ul > li div.main-nav--title a[onclick*="menu_rubrique"]::attr(href)').getall():
            yield Request(
                    url=response.urljoin(category_url),
                    callback=self.paginator,
                    headers=self.headers
                )

    def paginator(self, response):
        page_count = response.css(
                'ul.pagination.unstyled.item-center li.pagination--simple'
            ).xpath('text()[preceding-sibling::span]').get()
        if page_count:
            tot_page = page_count[page_count.rfind(' ')+1:]
            if tot_page and int(tot_page) > 1:
                for page_no in range(2, int(tot_page)+1):
                    if page_no == 2:
                        yield Request(
                            url=response.url.replace('1',str(page_no)),
                            callback=self.listing_navigator,
                            headers=self.headers,
                            meta={
                                'page1_listings': response.css('div.listing--element a.link::attr(href)').getall()
                            }
                        )
                    else:
                        yield Request(
                            url=response.url.replace('1',str(page_no)),
                            callback=self.listing_navigator,
                            headers=self.headers
                        )

    def listing_navigator(self, response):
        for listing_url in (response.meta.get('page1_listings',[]) 
            + response.css('div.listing--element a.link::attr(href)').getall()):
            yield Request(
                    url=response.urljoin(listing_url),
                    callback=self.parse_item,
                    headers=self.headers
                )

    def parse_item(self, response):
        item = {}
        item['url'] = response.url
        thumbnail = (response.css('meta[property="og:image"]::attr(content)').get() 
                or response.css('img[itemprop="image"][data-index="0"]::attr(src)').get())
        item['thumbnail url'] = response.urljoin(thumbnail) if thumbnail else ''
        item['category'] = (response.xpath('//td[contains(.,"Category")]/following-sibling::td/*/text()').get()
            or response.xpath('//td[contains(.,"Category")]/following-sibling::td/text()').get()
            or '').strip()
        item['make'] = (response.css('span[itemprop="manufacturer"]::text').get()
            or response.xpath('//td[contains(.,"Make") or contains(.,"Title")]/following-sibling::td/*/text()').get() 
            or '').strip()
        item['model'] = (response.css('span[itemprop="model"]::text').get()
            or response.xpath('//td[contains(.,"Model")]/following-sibling::td/*/text()').get() 
            or '').strip()
        item['type of ads'] = (response.xpath('//td[contains(.,"Type of ad")]/following-sibling::td/*/text()').get() 
            or '').strip() 
        item['reference'] = (response.xpath('//td[contains(.,"Reference")]/following-sibling::td/*/text()').get() 
            or '').strip()
        item['status'] = (response.xpath('//td[contains(.,"Status")]/following-sibling::td/*/text()').get() 
            or '').strip()
        item['year'] = (response.css('span[itemprop="releaseDate"]::text').get()
            or response.xpath('//td[contains(.,"Year")]/following-sibling::td/*/text()').get() 
            or '').strip()
        item['hours'] = (response.css('span.js-hour-prop::text').get() 
            or response.xpath('//td[contains(.,"Hours")]/following-sibling::td/*/text()').get() or '').strip()
        power = response.xpath('//td[contains(.,"Power")]/following-sibling::td/*/text()').get() or ''
        item['power'] = rm_newline_or_space.sub('',power)

        address = ' '.join(
            response.css(f'span[data-info="{attr_val}"]::text').get() or '' 
            for attr_val in ['streetAddress','postalCode','addressLocality']
            )
        country = response.xpath('//span[@data-info="addressLocality"]/following-sibling::text()').get() or ''
        item['location'] = (address + country).strip()
        seller_name = (response.css('div.u-bold[itemprop="member"]::text').get() 
            or '').strip().replace('\n','').split()
        item['seller_name'] = ' '.join(seller_name)
        item['advertiser_name'] = (response.css('p[class="u-bold h3-like"]::text').get() or '').strip()
        item['advertiser_url'] = response.css('a[onclick*="detail_website"]::attr(href)').get() or ''
        
        yield item