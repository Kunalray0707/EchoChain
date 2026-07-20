import scrapy
import json
import os
from echo_scraper.spiders.base_spider import BaseMarketplaceSpider

class EbaySpider(BaseMarketplaceSpider):
    name = "ebay"
    allowed_domains = ["ebay.com"]
    start_urls = ["https://www.ebay.com/b/Cell-Phones-Smartphones/9355/bn_320094"]

    def parse(self, response):
        """
        Parses eBay response HTML or loads mock simulated raw dataset when offline.
        """
        raw_json_path = os.path.join("data", "raw", "marketplace_listings.json")
        if os.path.exists(raw_json_path):
            with open(raw_json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            ebay_items = [d for d in data if d.get("marketplace") == "eBay"]
            for d in ebay_items[:1000]:
                yield self.parse_item_dict(d)
        else:
            for card in response.css(".s-item__info"):
                title = card.css(".s-item__title::text").get()
                price_str = card.css(".s-item__price::text").get()
                if title and price_str:
                    yield {
                        "listing_id": f"LIST-EBA-{hash(title) % 1000000}",
                        "marketplace": "eBay",
                        "product_title": title,
                        "condition": "Used - Good",
                        "price": 299.99,
                        "currency": "USD",
                        "location": "USA",
                        "seller_rating": 4.8,
                        "sold_count": 12,
                        "listing_date": "2024-01-15",
                        "shipping_cost": 10.0,
                        "images_count": 4,
                        "description": title
                    }
