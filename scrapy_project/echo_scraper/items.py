import scrapy

class ListingItem(scrapy.Item):
    """
    Data model for scraped secondary marketplace product listings.
    """
    listing_id = scrapy.Field()
    marketplace = scrapy.Field()
    product_title = scrapy.Field()
    condition = scrapy.Field()
    price = scrapy.Field()
    currency = scrapy.Field()
    location = scrapy.Field()
    seller_rating = scrapy.Field()
    sold_count = scrapy.Field()
    listing_date = scrapy.Field()
    shipping_cost = scrapy.Field()
    images_count = scrapy.Field()
    description = scrapy.Field()
    scraped_at = scrapy.Field()
