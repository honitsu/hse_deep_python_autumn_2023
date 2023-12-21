#!/usr/bin/env python3
# test_descriptors.py

import unittest
from descriptors import Integer, String, PositiveInteger


class Data:  # pylint: disable=too-few-public-methods
    num = Integer("Int")
    name = String("Str")
    price = PositiveInteger("Positive")

    def __init__(self, num=1, name="name", price=1):
        self.dict = {}
        self.num = num
        self.name = name
        self.price = price


class TestDescriptors(unittest.TestCase):
    def setUp(self):
        self.data = Data()

    def test_integer_descriptor(self):
        self.data.num = 10
        self.assertEqual(self.data.num, 10)

    def test_string_descriptor(self):
        self.data.name = "Test"
        self.assertEqual(self.data.name, "Test")

    def test_positive_descriptor(self):
        self.data.price = 100
        self.assertEqual(self.data.price, 100)

    def test_positive_descriptor_negative_value(self):
        self.data.price = 22
        with self.assertRaises(ValueError):
            self.data.price = -100
        self.assertEqual(self.data.price, 22)
        with self.assertRaises(ValueError):
            object.__setattr__(self.data, "price", -200)
        self.assertEqual(self.data.price, 22)

    def test_positive_descriptor_non_integer_value(self):
        with self.assertRaises(ValueError):
            self.data.price = "Not an integer"

    def test_set_invalid_value(self):
        with self.assertRaises(TypeError):
            self.data.num = "20"
        self.assertEqual(self.data.num, 1)
        with self.assertRaises(TypeError):
            self.data.name = 12345
        self.assertEqual(self.data.name, "name")
        with self.assertRaises(ValueError):
            self.data.price = -100
        self.assertEqual(self.data.price, 1)
        with self.assertRaises(ValueError):
            object.__setattr__(self.data, "price", -20)
        self.assertEqual(self.data.price, 1)

    def test_set_new_valid_value(self):
        self.assertEqual(self.data.num, 1)
        self.data.num = 2
        self.assertEqual(self.data.num, 2)

        self.assertEqual(self.data.name, "name")
        self.data.name = "12345"
        self.assertEqual(self.data.name, "12345")

        self.assertEqual(self.data.price, 1)
        self.data.price = 100
        self.assertEqual(self.data.price, 100)


if __name__ == "__main__":
    unittest.main(verbosity=2)
