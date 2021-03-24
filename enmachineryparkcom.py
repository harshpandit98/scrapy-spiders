from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class MachineParkSpider(CrawlSpider):
    name = 'en.machinerypark.com'
    custom_settings = {
        'DOWNLOAD_DELAY': 1.5,
        'CONCURRENT_REQUESTS': 3
    }

    allowed_domains = [ name ]

    start_urls = [ 'https://en.machinerypark.com/search?limit=48' ]

    rules = (
        Rule(LinkExtractor( allow=(), 
                            restrict_xpaths=('//a[contains(@class,"page-link mpXhrlink" ) and @aria-label="Skip"]')
                        ), 
        callback="parse_listings", follow=True
        ),
    )

    def parse_start_url(self,response):
        return self.parse_listings(response)

    def parse_listings(self, response):
        listings = response.css(
            'div.card-body div[class="row mb-3 border-bottom pb-3 mpOfferItem mpOfferLonglist"]')
        for listing in listings:
            item = {}
            url_tag = listing.css('div.row > div[class="col-12 col-sm-8 order-1"] > p.mb-3 a')
            url = url_tag.css('::attr(href)').get()
            item['url'] = response.urljoin(url.strip()).strip() if url else ''
            item['title'] = (url_tag.css('strong::text').get() or '').strip()
            item['price'] = (listing.css(
                'div[class="d-none d-sm-flex col-sm-4 order-sm-2"] > a > strong.mpPrice::text').get() or '').strip()
            item['location'] = (listing.css(
                '[class="col-12 order-2 order-sm-3"] > p > a > small::text').get() or '').strip()
            item['year'] = (url_tag.xpath('text()[preceding-sibling::br]').get() or '').strip()
            item['image'] = (listing.css(
                'div[class="mpImgBg mpLazy "]::attr(data-background-image)').get() or '').strip()
            yield item