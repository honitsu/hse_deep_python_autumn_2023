#!/usr/bin/env python3
# test_custom_meta.py

import unittest
from custom_meta import CustomMeta

# pylint: disable=no-member,attribute-defined-outside-init


class TestCustomMeta(unittest.TestCase):
    def setUp(self) -> None:
        class TestClass(metaclass=CustomMeta):
            x = 50

            def __init__(self, val=99):
                self.val = val

            def line(self):  # pylint: disable=no-self-use
                return 100

            def __str__(self):
                return "Custom_by_metaclass"

        self.inst = TestClass()

    def test_01_info(self):
        pass
        # print(dir(self.inst))

    def test_04_attribs(self):
        self.assertTrue(hasattr(self.inst, "custom_x"))
        self.assertFalse(hasattr(self.inst, "x"))
        self.assertTrue(hasattr(self.inst, "custom_val"))
        self.assertFalse(hasattr(self.inst, "val"))

    def test_05_methods(self):
        self.assertTrue(hasattr(self.inst, "__init__"))
        self.assertFalse(hasattr(self.inst, "custom___init__"))
        self.assertFalse(hasattr(self.inst, "line"))
        self.assertTrue(hasattr(self.inst, "custom_line"))
        self.assertTrue(hasattr(self.inst, "__str__"))
        self.assertFalse(hasattr(self.inst, "custom___str__"))

    def test_10_members(self):
        self.assertEqual(self.inst.__str__(), "Custom_by_metaclass")
        self.assertRaises(AttributeError, lambda: self.inst.custom__str__())  # pylint: disable=unnecessary-lambda
        self.inst.__init__(val="pi=3.14159265")
        self.assertEqual(self.inst.custom_val, "pi=3.14159265")
        self.assertFalse(hasattr(self.inst, "val"))

    def test_20_custom_members(self):
        self.assertEqual(self.inst.custom_x, 50)
        self.assertEqual(self.inst.custom_val, 99)
        self.assertEqual(self.inst.custom_line(), 100)

    def test_30_added_members(self):
        self.assertFalse(hasattr(self.inst, "dynamic"))
        self.assertFalse(hasattr(self.inst, "custom_dynamic"))
        self.inst.dynamic = "Added later"
        self.assertEqual(self.inst.custom_dynamic, "Added later")

        self.assertFalse(hasattr(self.inst, "__mymag__"))
        self.assertFalse(hasattr(self.inst, "custom___mymag__"))
        self.inst.__mymag__ = "My magic var"
        self.assertEqual(self.inst.__mymag__, "My magic var")

    def test_40_error_dynamic(self):
        self.assertFalse(hasattr(self.inst, "dynamic"))
        self.assertFalse(hasattr(self.inst, "custom_dynamic"))
        self.inst.dynamic = "Added later"
        self.assertFalse(hasattr(self.inst, "dynamic"))

        self.assertFalse(hasattr(self.inst, "__mymag__"))
        self.assertFalse(hasattr(self.inst, "custom___mymag__"))
        self.inst.__mymag__ = "My magic var"
        self.assertFalse(hasattr(self.inst, "custom___mymag__"))

    def test_50_new_custom_var(self):
        self.assertFalse(hasattr(self.inst, "custom_z"))
        self.assertFalse(hasattr(self.inst, "custom_custom_z"))
        self.inst.custom_z = "Double custom var"
        self.assertEqual(self.inst.custom_custom_z, "Double custom var")
        self.assertFalse(hasattr(self.inst, "custom_z"))

    def test_60_breaking_the_rules(self):
        object.__setattr__(self.inst, "custom_z", 66)
        self.assertEqual(self.inst.custom_z, 66)
        object.__setattr__(self.inst, "x", "123")
        self.assertEqual(self.inst.x, "123")


if __name__ == "__main__":
    unittest.main(verbosity=2)
