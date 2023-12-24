#!/usr/bin/env python3

import unittest
from hash_table import HashTable


CAPACITY = 20


class TestHashTable(unittest.TestCase):
    def test_init(self):
        ht = HashTable()
        self.assertEqual(ht.capacity, CAPACITY)
        self.assertEqual(ht.size, 0)
        self.assertEqual(ht.buckets, [None] * CAPACITY)

    def test_hash(self):
        ht = HashTable()
        key = "apple"
        hash_value = ht.hash(key)
        self.assertIsInstance(hash_value, int)

    def test_rehash(self):
        ht = HashTable()
        ht["apple"] = 1
        ht["pear"] = 2
        ht["peach"] = 3
        ht["peach"] = 4
        ht.rehash()
        self.assertEqual(ht.get_capacity(), CAPACITY * 2)

    def test_setitem_and_getitem(self):
        ht = HashTable()
        ht["apple"] = 10
        self.assertEqual(ht.get("apple"), 10)

    def test_getitem_default_value(self):
        ht = HashTable()
        self.assertIsNone(ht.get("pear", default=None))

    def test_clear(self):
        ht = HashTable()
        ht["apple"] = 10
        ht.clear()
        self.assertIsNone(ht.get("apple", default=None))

    def test_copy(self):
        ht = HashTable()
        ht["apple"] = 10
        ht_copy = ht.copy()
        self.assertEqual(ht.items(), ht_copy.items())

    def test_fromkeys(self):
        ht = HashTable()
        ht_fromkeys = ht.fromkeys(["mango", "peach"], 50)
        self.assertEqual(ht_fromkeys.get("mango"), 50)
        self.assertEqual(ht_fromkeys.get("peach"), 50)

    def test_keys(self):
        ht = HashTable()
        ht["apple"] = 10
        ht["banana"] = 20
        keys = ht.keys()
        self.assertListEqual(sorted(keys), ["apple", "banana"])

    def test_expand(self):
        ht = HashTable(initial_capacity=2)
        print(ht.size)
        ht["apple"] = 10
        ht["banana"] = 20
        ht["orange"] = 30
        self.assertEqual(len(ht.items()), 3)
        self.assertEqual(ht.capacity, 4)
        self.assertEqual(ht["apple"], 10)
        self.assertEqual(ht["banana"], 20)
        self.assertEqual(ht["orange"], 30)

    def test_no_such_key(self):
        ht = HashTable(initial_capacity=2)
        with self.assertRaises(ValueError):
            ht["melon"]  # pylint: disable=pointless-statement


if __name__ == "__main__":
    unittest.main()
