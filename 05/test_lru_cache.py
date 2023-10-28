import unittest
from lru_cache import LRUCache


class LRUCacheTests(unittest.TestCase):
    def test_get_existing_key_returns_correct_value(self):
        cache = LRUCache()
        cache.set(1, "one")
        cache.set(2, "two")

        result = cache.get(1)

        self.assertEqual(result, "one")

    def test_get_non_existing_key_returns_none(self):
        cache = LRUCache()
        cache.set(1, "one")
        cache.set(2, "two")

        result = cache.get(3)

        self.assertEqual(result, None)

    def test_set_new_key_updates_cache_correctly(self):
        cache = LRUCache()
        cache.set(1, "one")
        cache.set(2, "two")

        result = cache.get(2)

        self.assertEqual(result, "two")

    def test_set_existing_key_updates_cache_correctly(self):
        cache = LRUCache()
        cache.set(1, "one")
        cache.set(2, "two")

        cache.set(1, "updated")

        result = cache.get(1)

        self.assertEqual(result, "updated")

    def test_set_key_updates_head_of_cache(self):
        cache = LRUCache()
        cache.set(1, "one")
        cache.set(2, "two")
        cache.set(3, "three")

        result = cache.get(3)

        self.assertEqual(result, "three")
        self.assertEqual(cache.head.next.key, 3)

    def test_cache_limit_is_maintained(self):
        cache = LRUCache(limit=2)
        cache.set(1, "one")
        cache.set(2, "two")
        cache.set(3, "three")

        result = cache.get(1)

        self.assertEqual(result, None)

        result = cache.get(2)
        self.assertEqual(result, "two")

        result = cache.get(3)
        self.assertEqual(result, "three")

    def test_lru_items_are_removed_when_cache_limit_is_exceeded(self):
        cache = LRUCache(limit=3)
        cache.set(1, "one")
        cache.set(2, "two")
        cache.set(3, "three")
        cache.get(1)
        cache.set(4, "four")

        result = cache.get(1)
        self.assertEqual(result, "one")

        result = cache.get(2)
        self.assertEqual(result, None)

        result = cache.get(3)
        self.assertEqual(result, "three")

        result = cache.get(4)
        self.assertEqual(result, "four")


if __name__ == "__main__":
    unittest.main()
