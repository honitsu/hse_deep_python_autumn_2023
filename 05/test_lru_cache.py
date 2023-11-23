import unittest
from lru_cache import LRUCache


class LRUCacheTests(unittest.TestCase):
    def test_size_012(self):
        cache = LRUCache(0)
        assert cache.get(1) is None
        cache.set(1, "one")
        assert cache.get(1) is None

        cache = LRUCache(1)
        cache.set(1, "one")
        cache.set(2, "two")
        assert cache.get(1) is None
        assert cache.get(2) == "two"
        assert cache.get(3) is None
        cache.set(3, "three")
        assert cache.get(1) is None
        assert cache.get(2) is None
        assert cache.get(3) == "three"

        cache = LRUCache(2)
        cache.set(1, "one")
        cache.set(2, "two")
        assert cache.get(1) == "one"
        assert cache.get(2) == "two"
        assert cache.get(3) is None
        cache.set(3, "three")
        assert cache.get(1) is None
        assert cache.get(2) == "two"
        assert cache.get(3) == "three"

    def test_get_key_returns_value(self):
        cache = LRUCache()  # default limit=42
        cache.set(1, "one")
        cache.set(2, "two")
        self.assertEqual(cache.get(1), "one")

        cache = LRUCache()
        cache.set(1, "one")
        cache.set(2, "two")
        self.assertEqual(cache.get(3), None)

    def test_updates_cache(self):
        cache = LRUCache()
        cache.set(1, "one")
        cache.set(2, "two")
        self.assertEqual(cache.get(2), "two")

        cache = LRUCache()
        cache.set(1, "one")
        cache.set(2, "two")
        cache.set(1, "updated")
        self.assertEqual(cache.get(1), "updated")

    def test_cache_next_key(self):
        cache = LRUCache()
        cache.set(1, "one")
        cache.set(2, "two")
        cache.set(3, "three")
        self.assertEqual(cache.get(3), "three")
        self.assertEqual(cache.head.key, None)
        self.assertEqual(cache.head.next.key, 3)
        self.assertEqual(cache.head.next.next.key, 2)
        self.assertEqual(cache.head.next.next.next.key, 1)

    def test_cache_limit_is_maintained(self):
        cache = LRUCache(limit=2)
        cache.set(1, "one")
        cache.set(2, "two")
        cache.set(3, "three")
        self.assertEqual(cache.get(1), None)
        self.assertEqual(cache.get(2), "two")
        self.assertEqual(cache.get(3), "three")

    def test_lru_items_are_removed_when_cache_limit_is_exceeded(self):
        cache = LRUCache(limit=3)
        cache.set(1, "one")
        cache.set(2, "two")
        cache.set(3, "three")
        cache.get(1)
        cache.set(4, "four")
        self.assertEqual(cache.get(1), "one")
        self.assertEqual(cache.get(2), None)
        self.assertEqual(cache.get(3), "three")
        self.assertEqual(cache.get(4), "four")


if __name__ == "__main__":
    unittest.main()
