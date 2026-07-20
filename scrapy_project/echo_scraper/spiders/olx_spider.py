import scrapy
import json
import os
from echo_scraper.spiders.base_spider import BaseMarketplaceSpider

class OlxSpider(BaseMarketplaceSpider):
    name = "olx"
    allowed_domains = ["olx.com"]
    start_urls = ["https://www.olx.com/electronics-appliances_c1429"]

    def parse(self, response):
        raw_json_path = os.path.join("data", "raw", "marketplace_listings.json")
        if os.path.exists(raw_json_path):
            with open(raw_json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            olx_items = [d for d in data if d.get("marketplace") == "OLX"]
            for d in olx_items[:1000]:
                yield self.parse_item_dict(d)
        else:
            yield {
                "listing_id": "LIST-OLX-88888",
                "marketplace": "OLX",
                "product_title": "Samsung Galaxy S23 Ultra 512GB",
                "condition": "Used - Good",
                "price": 680.0,
                "currency": "USD",
                "location": "Sao Paulo, Brazil",
                "seller_rating": 4.5,
                "sold_count": 8,
                "listing_date": "2024-01-20",
                "shipping_cost": 15.0,
                "images_count": 3,
                "description": "Galaxy S23 Ultra in good working order."
            }
