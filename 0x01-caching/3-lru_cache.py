#!/usr/bin/python3
"""
LRU Caching
"""
from base_caching import BaseCaching


class LRUCache(BaseCaching):
    """
    LRU Caching system
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

        self.cache_data[key] = item

        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            lru_key = next(iter(self.cache_data))
            del self.cache_data[lru_key]
            print(f"DISCARD: {lru_key}\n")

    def get(self, key):
        """
        returns the value linked to key
        """
        if key is None or key not in self.cache_data:
            return None

        return self.cache_data[key]
