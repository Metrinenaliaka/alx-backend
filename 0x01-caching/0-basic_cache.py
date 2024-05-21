#!/usr/bin/python3
"""
Basic dictionary caching
"""
BaseCaching = __import__('base_caching').BaseCaching


class BasicCache(BaseCaching):
    """
    Dictionary caching system that has no limit
    """
    def put(self, key, item):
        """
        puts key and item in cache_data
        """
        if key is None or item is None:
            return
        self.cache_data[key] = item

    def get(self, key):
        """
        returns the value linked to key
        """
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data[key]
