#!/usr/bin/env python3
"""
 5. Implementing an expiring web
cache and tracker
"""
import redis
import requests
from typing import Callable

r = redis.Redis()


def get_page(url: str) -> str:
    """Fetch a URL and cache its content for 10 seconds."""
    # Check if the page is cached
    cached_page = r.get(f"cached:{url}")
    if cached_page:
        return cached_page.decode('utf-8')

    # Fetch the page content
    response = requests.get(url)
    page_content = response.text

    # Cache the content and
    # set expiration time of 10 seconds
    r.setex(f"cached:{url}", 10, page_content)

    # Track how many times the page is accessed
    r.incr(f"count:{url}")

    return page_content


# We can create a decorator
# to apply caching logic for any URL
def cache_page(func: Callable) -> Callable:
    """Decorator to cache the page content with expiration."""
    def wrapper(url: str):
        return get_page(url)
    return wrapper
