from collections import deque


class LRUCache:
    def __init__(self, limit=42):
        self.cache = {}
        self.key_order = deque(maxlen=limit)
        self.limit = limit

    def get(self, key):
        if key in self.cache:
            self.key_order.remove(key)  # O(n)
            self.key_order.append(key)
            return self.cache[key]
        return None

    def set(self, key, value):
        if len(self.key_order) == self.limit and key not in self.cache:
            self.cache.pop(self.key_order[0])
        elif key in self.cache:
            self.key_order.remove(key)  # O(n)
        self.cache[key] = value
        self.key_order.append(key)

    def __setitem__(self, key, value):
        if len(self.key_order) == self.limit and key not in self.cache:
            self.cache.pop(self.key_order[0])
        elif key in self.cache:
            self.key_order.remove(key)  # O(n)
        self.cache[key] = value
        self.key_order.append(key)

    def __getitem__(self, key):
        if key in self.cache:
            self.key_order.remove(key)  # O(n)
            self.key_order.append(key)
            return self.cache[key]
        return None


cache = LRUCache(2)

cache.set("k1", "val1")
cache.set("k2", "val2")

print(cache.get("k3"))  # None
print(cache.get("k2"))  # "val2"
print(cache.get("k1"))  # "val1"

cache.set("k3", "val3")

print(cache.get("k3"))  # "val3"
print(cache.get("k2"))  # None
print(cache.get("k1"))  # "val1"

cache["k1"] = "val1"
print(cache["k3"])  # "val3"
