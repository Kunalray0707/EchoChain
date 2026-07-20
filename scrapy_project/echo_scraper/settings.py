BOT_NAME = "echo_scraper"

SPIDER_MODULES = ["echo_scraper.spiders"]
NEWSPIDER_MODULE = "echo_scraper.spiders"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Concurrent requests & throttling
CONCURRENT_REQUESTS = 16
DOWNLOAD_DELAY = 0.5

# AutoThrottle settings
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1.0
AUTOTHROTTLE_MAX_DELAY = 10.0
AUTOTHROTTLE_TARGET_CONCURRENCY = 2.0

# Middlewares
DOWNLOADER_MIDDLEWARES = {
    "echo_scraper.middlewares.RandomUserAgentMiddleware": 400,
    "echo_scraper.middlewares.RetryWithDelayMiddleware": 550,
}

# Item Pipelines
ITEM_PIPELINES = {
    "echo_scraper.pipelines.DataCleaningPipeline": 100,
    "echo_scraper.pipelines.CurrencyNormalizerPipeline": 200,
    "echo_scraper.pipelines.JsonExportPipeline": 300,
}

# User agents pool
USER_AGENT_LIST = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0",
]

LOG_LEVEL = "INFO"
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
