#!/usr/bin/python3
"""
FIFO caching implementation
"""
from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """
    class implementing FIFO cache system
    """
    def __init__(self):
        """
        constructor method
        """
        super().__init__()

    def put(self, key, item):
        """
        puts key and item in cache_data
        """
        if key is None or item is None:
            return

        if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            first_item = next(iter(self.cache_data))
            del self.cache_data[first_item]
            print(f"DISCARD: {first_item}")

        self.cache_data[key] = item

    def get(self, key):
        """
        returns the value linked to key
        """
        if key is None or key not in self.cache_data:
            return None

        return self.cache_data[key]
