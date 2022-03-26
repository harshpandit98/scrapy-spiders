from scrapy import Item, Field


class Product(Item):
    url = Field()
    tcin = Field()
    upc = Field()
    price = Field()
    currency = Field()
    title = Field()
    description = Field()
    specs = Field()
    ingredient = Field()
