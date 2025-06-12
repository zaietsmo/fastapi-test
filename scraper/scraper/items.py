import scrapy


class ProductItem(scrapy.Item):
    name = scrapy.Field()
    description = scrapy.Field()
    calories = scrapy.Field()
    fats = scrapy.Field()
    carbs = scrapy.Field()
    proteins = scrapy.Field()
    unsaturated_fats = scrapy.Field()
    sugar = scrapy.Field()
    salt = scrapy.Field()
    portion = scrapy.Field()
