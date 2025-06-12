import scrapy
from scraper.items import ProductItem
from scrapy.http import Response


class MenuSpider(scrapy.Spider):
    name = "menu"
    allowed_domains = ["www.mcdonalds.com"]
    start_urls = ["https://www.mcdonalds.com/ua/uk-ua/eat/fullmenu.html"]

    def parse(self, response: Response, **kwargs):
        for product in response.css(".cmp-category__item"):
            product_id = product.attrib.get("data-product-id")
            if product_id:
                url = f"https://www.mcdonalds.com/dnaapp/itemDetails?country=UA&language=uk&showLiveData=true&item={product_id}"
                yield scrapy.Request(url, callback=self.parse_product_detail)

    def parse_product_detail(self, response: Response):
        try:
            data = response.json()
        except Exception as e:
            self.logger.error(f"Failed to parse JSON from {response.url}: {e}")
            return

        item = data.get("item")
        if not item:
            self.logger.warning(f"No 'item' key in JSON response from {response.url}")
            return

        product = ProductItem()

        if item.get("item_name") is None:
            product["name"] = None
        else:
            product["name"] = item.get("item_name").replace('"', "")

        if item.get("description") is None or type(item.get("description")) is dict:
            product["description"] = None
        else:
            product["description"] = item.get("description").replace("\r\n", " ")

        nutrient_facts = item.get("nutrient_facts")

        product["calories"] = None
        product["fats"] = None
        product["carbs"] = None
        product["proteins"] = None
        product["unsaturated_fats"] = None
        product["sugar"] = None
        product["salt"] = None
        product["portion"] = None

        if nutrient_facts and nutrient_facts.get("nutrient"):
            nutrient_map = {
                "Калорійність": "calories",
                "Жири": "fats",
                "НЖК": "unsaturated_fats",
                "Вуглеводи": "carbs",
                "Цукор": "sugar",
                "Білки": "proteins",
                "Вага порції": "portion",
                "Сіль": "salt",
            }
            for nutrient_fact in nutrient_facts.get("nutrient"):
                nutrient_name = nutrient_fact.get("name")
                value = nutrient_fact.get("value")
                if nutrient_name in nutrient_map and value is not None:
                    product[nutrient_map[nutrient_name]] = value
        else:
            self.logger.warning(
                f"Nutrient facts not found or empty for {product.get('name')} at {response.url}"
            )

        yield product
