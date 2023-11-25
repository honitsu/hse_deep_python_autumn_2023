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
    def test_integer_descriptor(self):
        data = Data()
        data.num = 10
        self.assertEqual(data.num, 10)

    def test_string_descriptor(self):
        data = Data()
        data.name = "Test"
        self.assertEqual(data.name, "Test")

    def test_positive_integer_descriptor(self):
        data = Data()
        data.price = 100
        self.assertEqual(data.price, 100)

    def test_positive_integer_descriptor_negative_value(self):
        data = Data()
        with self.assertRaises(ValueError):
            data.price = -100

    def test_positive_integer_descriptor_non_integer_value(self):
        data = Data()
        with self.assertRaises(ValueError):
            data.price = "Not an integer"


if __name__ == "__main__":
    unittest.main()
