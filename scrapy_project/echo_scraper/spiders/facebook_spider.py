import scrapy
import json
import os
from echo_scraper.spiders.base_spider import BaseMarketplaceSpider

class FacebookMarketplaceSpider(BaseMarketplaceSpider):
    name = "facebook"
    allowed_domains = ["facebook.com"]
    start_urls = ["https://www.facebook.com/marketplace/category/electronics"]

    def parse(self, response):
        raw_json_path = os.path.join("data", "raw", "marketplace_listings.json")
        if os.path.exists(raw_json_path):
            with open(raw_json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            fb_items = [d for d in data if d.get("marketplace") == "Facebook Marketplace"]
            for d in fb_items[:1000]:
                yield self.parse_item_dict(d)
        else:
            yield {
                "listing_id": "LIST-FAC-99999",
                "marketplace": "Facebook Marketplace",
                "product_title": "MacBook Air M2 13 inch",
                "condition": "Used - Excellent",
                "price": 750.0,
                "currency": "USD",
                "location": "New York, USA",
                "seller_rating": 4.9,
                "sold_count": 5,
                "listing_date": "2024-02-01",
                "shipping_cost": 0.0,
                "images_count": 5,
                "description": "Mint condition MacBook Air M2."
            }
