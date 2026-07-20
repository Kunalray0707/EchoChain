import scrapy
import random
from echo_scraper.items import ListingItem

class BaseMarketplaceSpider(scrapy.Spider):
    """
    Base Spider providing reusable item generation for offline testing & online scraping.
    """
    name = "base_spider"
    
    def parse_item_dict(self, d):
        item = ListingItem()
        for k, v in d.items():
            item[k] = v
        return item
