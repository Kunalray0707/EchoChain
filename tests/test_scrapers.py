from scrapy_project.echo_scraper.pipelines import DataCleaningPipeline, CurrencyNormalizerPipeline

def test_data_cleaning_pipeline(sample_listing_item):
    pipeline = DataCleaningPipeline()
    cleaned = pipeline.process_item(sample_listing_item.copy(), None)
    
    assert cleaned["product_title"] == "Apple iPhone 14 Pro 256GB Space Black"
    assert "scraped_at" in cleaned
    assert isinstance(cleaned["price"], float)

def test_currency_normalizer_pipeline(sample_listing_item):
    pipeline = CurrencyNormalizerPipeline()
    item = sample_listing_item.copy()
    item["price"] = 100.0
    item["currency"] = "EUR"
    
    processed = pipeline.process_item(item, None)
    assert processed["price_usd"] == 109.0 # 100 EUR * 1.09
