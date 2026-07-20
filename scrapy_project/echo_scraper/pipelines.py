import os
import json
from datetime import datetime
try:
    from scrapy.exceptions import DropItem
except ImportError:
    class DropItem(Exception):
        pass


class DataCleaningPipeline:
    """
    Cleans raw strings, validates required fields, and normalizes numbers.
    """
    def process_item(self, item, spider):
        if not item.get("product_title"):
            raise DropItem(f"Missing product_title in {item}")
            
        item["product_title"] = item["product_title"].strip()
        item["scraped_at"] = datetime.utcnow().isoformat()
        
        # Ensure numerical types
        try:
            item["price"] = float(item.get("price", 0.0))
            item["shipping_cost"] = float(item.get("shipping_cost", 0.0))
            item["seller_rating"] = float(item.get("seller_rating", 0.0))
            item["sold_count"] = int(item.get("sold_count", 0))
        except (ValueError, TypeError):
            item["price"] = 0.0

        return item

class CurrencyNormalizerPipeline:
    """
    Normalizes local currencies (EUR, GBP, BRL, INR) to standard USD estimate.
    """
    RATES = {"USD": 1.0, "EUR": 1.09, "GBP": 1.27, "BRL": 0.18, "INR": 0.012}

    def process_item(self, item, spider):
        currency = item.get("currency", "USD").upper()
        rate = self.RATES.get(currency, 1.0)
        item["price_usd"] = round(item["price"] * rate, 2)
        return item

class JsonExportPipeline:
    """
    Exports scraped items to a local JSON output file for Bronze ingestion.
    """
    def open_spider(self, spider):
        os.makedirs(os.path.join("data", "raw"), exist_ok=True)
        self.filename = os.path.join("data", "raw", f"scraped_{spider.name}.json")
        self.file = open(self.filename, "w", encoding="utf-8")
        self.items = []

    def close_spider(self, spider):
        json.dump(self.items, self.file, indent=2)
        self.file.close()

    def process_item(self, item, spider):
        self.items.append(dict(item))
        return item
