#!/usr/bin/env python3
# test_lru_cache.py

import unittest
from lru_cache import LRUCache


class LRUCacheTests(unittest.TestCase):
    def test_as_in_homework(self):
        cache = LRUCache(2)
    
        cache.set("k1", "val1")
        cache.set("k2", "val2")
    
        assert cache.get("k3") is None
        assert cache.get("k2") == "val2"
        assert cache.get("k1") == "val1"
    
        cache.set("k3", "val3")
    
        assert cache.get("k3") == "val3"  # Typo with extra ')' in homework.md fixed
        assert cache.get("k2") is None
        assert cache.get("k1") == "val1"

    def test_size_0(self):
        cache = LRUCache(0)
        self.assertEqual(cache.get(1), None)
        cache.set(1, "one")
        self.assertEqual(cache.get(1), None)

    def test_size_1(self):
        cache = LRUCache(1)
        cache.set(1, "one")
        cache.set(2, "two")
        self.assertEqual(cache.get(1), None)
        self.assertEqual(cache.get(2), "two")
        self.assertEqual(cache.get(3), None)
        cache.set(3, "three")
        self.assertEqual(cache.get(1), None)
        self.assertEqual(cache.get(2), None)
        self.assertEqual(cache.get(3), "three")

    def test_size_2(self):
        cache = LRUCache(2)
        cache.set(1, "one")
        cache.set(2, "two")
        self.assertEqual(cache.get(1), "one")
        self.assertEqual(cache.get(2), "two")
        self.assertEqual(cache.get(3), None)
        cache.set(1, "one again")
        cache.set(3, "three")
        self.assertEqual(cache.get(1), "one again")
        self.assertEqual(cache.get(2), None)
        self.assertEqual(cache.get(3), "three")
        cache.set(4, "four")
        self.assertEqual(cache.get(1), None)
        self.assertEqual(cache.get(3), "three")
        self.assertEqual(cache.get(4), "four")

    def test_get_key_and_next(self):
        cache = LRUCache()  # default limit=42
        cache.set(1, "one")
        cache.set(2, "two")
        self.assertEqual(cache.get(1), "one")
        self.assertEqual(cache.get(2), "two")
        self.assertEqual(cache.get(3), None)
        cache.set(1, "updated")
        self.assertEqual(cache.get(1), "updated")

        cache.__init__()  # Reset all cache
        cache.set(1, "one")
        cache.set(2, "two")
        cache.set(3, "three")
        self.assertEqual(cache.get(3), "three")
        self.assertEqual(cache.head.key, None)
        self.assertEqual(cache.head.next.key, 3)
        self.assertEqual(cache.head.next.next.key, 2)
        self.assertEqual(cache.head.next.next.next.key, 1)

    def test_red_update_prolongs_life(self):
        cache = LRUCache(limit=3)
        cache.set(1, "one")
        cache.set(2, "two")
        cache.set(3, "three")
        cache.set(4, "four")
        self.assertEqual(cache.get(1), None)
        self.assertEqual(cache.get(2), "two")
        self.assertEqual(cache.get(3), "three")
        cache.set(1, "one")
        cache.set(2, "two")
        cache.set(3, "three")
        cache.get(1)  # Read value to prolong its life
        cache.set(4, "four")
        self.assertEqual(cache.get(1), "one")
        self.assertEqual(cache.get(2), None)
        self.assertEqual(cache.get(3), "three")
        self.assertEqual(cache.get(4), "four")
        cache.set(1, "one")
        cache.set(2, "two")
        cache.set(3, "three")
        cache.set(1, "It's alive!")
        cache.set(2, "It's alive too!")
        cache.set(4, "four")
        self.assertEqual(cache.get(1), "It's alive!")
        self.assertEqual(cache.get(2), "It's alive too!")
        self.assertEqual(cache.get(3), None)
        self.assertEqual(cache.get(4), "four")


if __name__ == "__main__":
    unittest.main(verbosity=2)
