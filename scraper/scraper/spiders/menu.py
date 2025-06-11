import scrapy


class MenuSpider(scrapy.Spider):
    name = "menu"
    allowed_domains = ["www.mcdonalds.com"]
    start_urls = ["https://www.mcdonalds.com/ua/uk-ua/eat/fullmenu.html"]

    def parse(self, response):
        pass
