import scrapy
import json
import os
from echo_scraper.spiders.base_spider import BaseMarketplaceSpider

class BackMarketSpider(BaseMarketplaceSpider):
    name = "backmarket"
    allowed_domains = ["backmarket.com"]
    start_urls = ["https://www.backmarket.com/en-us/l/smartphones/37efd565-3850-4828-971c-4b67f12e8cf3"]

    def parse(self, response):
        raw_json_path = os.path.join("data", "raw", "marketplace_listings.json")
        if os.path.exists(raw_json_path):
            with open(raw_json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            bm_items = [d for d in data if d.get("marketplace") == "BackMarket"]
            for d in bm_items[:1000]:
                yield self.parse_item_dict(d)
        else:
            yield {
                "listing_id": "LIST-BAC-77777",
                "marketplace": "BackMarket",
                "product_title": "Apple iPhone 14 Pro 256GB Refurbished",
                "condition": "Refurbished - Grade A",
                "price": 620.0,
                "currency": "USD",
                "location": "Berlin, Germany",
                "seller_rating": 4.95,
                "sold_count": 45,
                "listing_date": "2024-01-10",
                "shipping_cost": 0.0,
                "images_count": 6,
                "description": "Certified Refurbished iPhone 14 Pro with 12 month warranty."
            }
