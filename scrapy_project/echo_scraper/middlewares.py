import random
import time
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from scrapy.downloadermiddlewares.retry import RetryMiddleware

class RandomUserAgentMiddleware(UserAgentMiddleware):
    """
    Middleware to assign a random User-Agent header to each outgoing request.
    """
    def __init__(self, user_agent="Scrapy"):
        super().__init__(user_agent)
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2.1 Safari/605.1.15",
            "Mozilla/5.0 (X11; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0"
        ]

    def process_request(self, request, spider):
        user_agent = random.choice(self.user_agents)
        request.headers["User-Agent"] = user_agent

class RetryWithDelayMiddleware(RetryMiddleware):
    """
    Middleware to handle rate limiting and HTTP 429/503 errors with exponential backoff.
    """
    def process_response(self, request, response, spider):
        if response.status in [429, 503]:
            reason = f"HTTP status {response.status} rate limited"
            spider.logger.warning(f"Rate limited on {request.url}. Sleeping before retrying...")
            time.sleep(2.0)
            return self._retry(request, reason, spider) or response
        return response
