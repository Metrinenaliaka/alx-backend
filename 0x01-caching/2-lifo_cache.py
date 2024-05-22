#!/usr/bin/python3
""""
LIFO caching implementation
"""
from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """
    class implementing LIFO cache system
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
            last_key = list(self.cache_data.keys())[-1]
            del self.cache_data[last_key]
            print("DISCARD:", last_key)

        self.cache_data[key] = item

    def get(self, key):
        """
        returns the value linked to key
        """
        if key is None or key not in self.cache_data:
            return None

        return self.cache_data[key]
