import scrapy

class FarFetchSpider(scrapy.Spider):
    name = "farfetch.com"
    def start_requests(self):
        start_urls = [
        'http://www.farfetch.com/de/shopping/men/shoes-2/items.aspx?page=%s&view=90&scale=282' % page for page in range(100,176)
        ]
        try:
            for url in start_urls:
                yield scrapy.Request(url=url, callback=self.parse)
        except Exception as e:
            raise e
            
    def parse(self, response):
        title = response.css("._5ce6f6").css("._bab25b._18fbc8").xpath("p/text()").extract()
        brand = response.css("._5ce6f6").css("._bab25b._18fbc8").xpath("h3/text()").extract() 
        price = response.css("._5ce6f6").css("._6356bb").xpath("span/text()").extract() 
        
        img_url = response.css("._5ce6f6").xpath("meta[1]/@content").extract()
        prod_url = response.css("._5ce6f6").xpath("@href").extract()  
        
        for item in zip(title,brand,price,img_url,prod_url):
            scraped_info = { 
                'Name' : item[0],   
                'Brand' : item[1],
                'Price' : item[2],
                'ImageUrl' : item[3],
                'ProductUrl' : "https://www.farfetch.com"+item[4],
            }
            yield scraped_info
