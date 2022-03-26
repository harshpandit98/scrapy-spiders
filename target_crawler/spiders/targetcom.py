import re
from scrapy import Spider, Request
from target_crawler.items import Product


class TargetSpider(Spider):
    name = "target"
    custom_settings = {
        'ROBOTSTXT_OBEY': False
    }
    allowed_domains = ["www.target.com"]

    def start_requests(self):
        try:
            url = self.url
            if url.startswith("https"):
                yield Request(url, self.parse_product)
            else:
                self.logger.warning(f"Please pass a valid url. Passed url: {url}")
        except:
            self.logger.warning('Pass the url with option -a url="https://example.com"')

    def parse_product(self, response):
        product = Product()
        product["url"] = response.url
        product["tcin"] = response.css("::attr(data-tcin)").get()
        product["upc"] = response.xpath('//div[contains(.,"UPC")]/text()').re_first(
            "\d+"
        )
        script_tag = response.css("script::text")
        product["price"] = script_tag.re_first('price":"(.*?)"')
        product["currency"] = script_tag.re_first('rency":"(.*?)"')
        product["title"] = response.css(
            '[data-test="product-title"] > span::text'
        ).get()
        product["description"] = response.css(
            '[property*="description"]::attr(content)'
        ).get()
        try:
            product["specs"] = [
                re.sub(r"<.*?>", "", spec)
                for spec in eval(
                    response.css("script::text")
                    .re_first(r'bullet_descriptions\\":(\[.*?\])')
                    .encode("ascii")
                    .decode("unicode-escape")
                )
            ]

        except:
            product["specs"] = None
        ingredient_list = (
            script_tag.re_first(r'ingredients\\":\\"(.*?)\\"').strip().split(", ")
        )
        last_elem = ingredient_list.pop()
        last_fs_idx = last_elem.rfind(". ")
        if last_fs_idx > 0:
            ingredient_list.extend(last_elem.split(". "))
        else:
            ingredient_list.append(last_elem)
        product["ingredient"] = ingredient_list
        yield product
