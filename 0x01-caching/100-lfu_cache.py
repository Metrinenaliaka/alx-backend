#!/usr/bin/python3
from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """
    LFU caching implementation
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

        if key in self.cache_data:
            self.cache_data[key]['value'] = item
            self.cache_data[key]['frequency'] += 1
        else:
            if len(self.cache_data) >= self.MAX_ITEMS:
                min_frequency = min(self.cache_data.values(), key=lambda x: x['frequency'])['frequency']
                least_frequent_items = [k for k, v in self.cache_data.items() if v['frequency'] == min_frequency]
                if len(least_frequent_items) > 1:
                    least_recently_used_item = min(least_frequent_items, key=lambda x: self.cache_data[x]['last_used'])
                    del self.cache_data[least_recently_used_item]
                    print(f"DISCARD: {least_recently_used_item}\n")
                else:
                    del self.cache_data[least_frequent_items[0]]
                    print(f"DISCARD: {least_frequent_items[0]}\n")

            self.cache_data[key] = {'value': item, 'frequency': 1, 'last_used': 0}

    def get(self, key):
        """
        returns the value linked to key
        """
        if key is None or key not in self.cache_data:
            return None

        self.cache_data[key]['frequency'] += 1
        self.cache_data[key]['last_used'] = max(self.cache_data.values(), key=lambda x: x['last_used'])['last_used'] + 1
        return self.cache_data[key]['value']