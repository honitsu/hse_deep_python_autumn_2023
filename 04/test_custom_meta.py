import unittest
from custom_meta import CustomMeta


class CustomClass(metaclass=CustomMeta):
    class_attr = 3

    def __init__(self, val, **kwargs):
        self.instance_attr = val
        self.__dict__.update(kwargs)

    @staticmethod
    def solve():
        return 100

    def __str__(self):
        return "Custom by metaclass"


# pylint: disable=E1101
class TestCustomMetaclass(unittest.TestCase):
    def test_cls_attributes(self):
        with self.assertRaises(AttributeError):
            print(CustomClass.class_attr)

        with self.assertRaises(AttributeError):
            print(CustomClass.solve())

        self.assertTrue(CustomClass.custom_class_attr == 3)
        self.assertTrue(CustomClass.custom_solve() == 100)

        self.assertTrue("__str__" in CustomClass.__dict__)
        self.assertFalse("custom___str__" in CustomClass.__dict__)

    def test_adding_class_attributes(self):
        CustomClass.new_cls_attr = "added"
        CustomClass.new_cls_method = lambda x: x

        with self.assertRaises(AttributeError):
            print(CustomClass.new_cls_attr)

        with self.assertRaises(AttributeError):
            print(CustomClass.new_cls_method(1))

        self.assertTrue(CustomClass.custom_new_cls_attr == "added")
        self.assertTrue(CustomClass.custom_new_cls_method(1) == 1)

    def test_inst_attributes(self):
        inst = CustomClass(1, a=20, b="thirty")

        with self.assertRaises(AttributeError):
            print(inst.instance_attr)

        with self.assertRaises(AttributeError):
            print(inst.class_attr)

        with self.assertRaises(AttributeError):
            print(inst.solve())

        self.assertTrue(inst.custom_instance_attr == 1)
        self.assertTrue(inst.a == 20)
        self.assertTrue(inst.b == "thirty")
        self.assertTrue(inst.custom_class_attr == 3)
        self.assertTrue(inst.custom_solve() == 100)
        self.assertEqual(str(inst), "Custom by metaclass")

    def test_adding_inst_attributes(self):
        inst = CustomClass(1, a=20, b="thirty")

        inst.new_attr = "added" # pylint: disable=attribute-defined-outside-init
        inst.new_method = lambda x: x # pylint: disable=attribute-defined-outside-init

        with self.assertRaises(AttributeError):
            print(inst.new_attr)

        with self.assertRaises(AttributeError):
            print(inst.new_method(1))

        self.assertTrue(inst.custom_new_attr == "added")
        self.assertTrue(inst.custom_new_method(1) == 1)

        inst.__some_magic_method__ = lambda x: x # pylint: disable=attribute-defined-outside-init

        with self.assertRaises(AttributeError):
            print(inst.custom___some_magic_method__(1))

        self.assertEqual(inst.__some_magic_method__(2), 2)


def main():
    unittest.main()


if __name__ == "__main__":
    main()
