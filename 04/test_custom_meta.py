import unittest
from custom_meta import CustomMeta


class TestCustomMeta(unittest.TestCase):
    def setUp(self):
        class TestClass(metaclass=CustomMeta):
            x = 50
            val = 99

            def line(self):
                return 100

            def __str__(self):
                return "Custom_by_metaclass"

        self.inst = TestClass()

    def test_custom(self):
        self.assertEqual(self.inst.custom_x, 50)

        self.assertEqual(self.inst.custom_val, 99)

        self.assertEqual(self.inst.custom_line(), 100)

        self.inst.dynamic = "added later"
        self.assertEqual(self.inst.custom_dynamic, "added later")

    def test_error_dynamic(self):
        with self.assertRaises(AttributeError):
            self.inst.dynamic

        with self.assertRaises(AttributeError):
            self.inst.x

        with self.assertRaises(AttributeError):
            self.inst.val

        with self.assertRaises(AttributeError):
            self.inst.line()

        with self.assertRaises(AttributeError):
            self.inst.yyy

        with self.assertRaises(AttributeError):
            self.inst.x

    def test_method(self):
        self.assertEqual(self.inst.__str__(), "Custom_by_metaclass")
        with self.assertRaises(AttributeError):
            self.inst.custom__str__()


if __name__ == "__main__":
    unittest.main()
