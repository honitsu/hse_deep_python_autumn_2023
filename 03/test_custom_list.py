import unittest
from custom_list import CustomList


class TestCustomList(unittest.TestCase):
    def setUp(self):
        self.cl1 = CustomList([5, 1, 3, 7])
        self.cl2 = CustomList([1, 2, 7])
        self.cl3 = CustomList([4, 4, 4, 4])
        self.cl4 = CustomList()
        self.list1 = [2, 2]

    def compare(self, list1, list2):
        self.assertEqual(len(list1), len(list2))
        for num1, num2 in zip(list1, list2):
            self.assertEqual(num1, num2)

    def test__str__(self):
        self.assertEqual(self.cl4.__str__(), "[] 0")
        self.assertEqual(self.cl1.__str__(), "[5, 1, 3, 7] 16")

    def test_same_size(self):
        cl1, cl2 = CustomList.same_size([1, 2], [1, 2, 3, 4])
        self.compare(cl1, [1, 2, 0, 0])
        self.compare(cl2, [1, 2, 3, 4])

        cl1, cl2 = CustomList.same_size([], [1, 2])
        self.compare(cl1, [0, 0])
        self.compare(cl2, [1, 2])

        cl1, cl2 = CustomList.same_size([1, 2], [3, 4])
        self.compare(cl1, [1, 2])
        self.compare(cl2, [3, 4])

    def test__add__(self):

        self.compare(self.cl1 + self.cl2, CustomList([6, 3, 10, 7]))
        self.compare(self.cl2 + self.cl1, CustomList([6, 3, 10, 7]))
        self.compare(self.cl2 + CustomList(self.list1), CustomList([3, 4, 7]))
        self.compare(self.cl1 + self.list1, CustomList([7, 3, 3, 7]))
        self.compare(self.cl2 + self.list1, CustomList([3, 4, 7]))

        self.assertIsInstance(self.cl1 + self.cl2, CustomList)
        self.assertIsInstance(self.cl1 + self.list1, CustomList)

        self.compare(self.cl1, CustomList([5, 1, 3, 7]))
        self.compare(self.cl2, CustomList([1, 2, 7]))
        self.compare(self.list1, [2, 2])

    def test__radd__(self):

        self.compare(self.list1 + self.cl1, CustomList([7, 3, 3, 7]))
        self.compare(self.list1 + self.cl2, CustomList([3, 4, 7]))

        self.assertIsInstance(self.list1 + self.cl1, CustomList)
        self.assertIsInstance(self.list1 + self.cl2, CustomList)

        self.compare(self.cl1, CustomList([5, 1, 3, 7]))
        self.compare(self.cl2, CustomList([1, 2, 7]))
        self.compare(self.list1, [2, 2])

    def test__sub__(self):

        self.compare(self.cl1 - self.cl2, CustomList([4, -1, -4, 7]))
        self.compare(self.cl2 - self.cl1, CustomList([-4, 1, 4, -7]))
        self.compare(self.cl2 - CustomList(self.list1), CustomList([-1, 0, 7]))
        self.compare(self.cl1 - self.list1, CustomList([3, -1, 3, 7]))
        self.compare(self.cl2 - self.list1, CustomList([-1, 0, 7]))
        self.compare(CustomList() - self.list1, CustomList([-2, -2]))

        self.assertIsInstance(self.cl1 - self.cl2, CustomList)
        self.assertIsInstance(CustomList() - self.list1, CustomList)

        self.compare(self.cl1, CustomList([5, 1, 3, 7]))
        self.compare(self.cl2, CustomList([1, 2, 7]))
        self.compare(self.list1, [2, 2])

    def test__rsub__(self):
        self.compare(self.list1 - self.cl1, CustomList([-3, 1, -3, -7]))
        self.compare(self.list1 - self.cl2, CustomList([1, 0, -7]))

        self.assertIsInstance(self.list1 - self.cl1, CustomList)
        self.assertIsInstance(self.list1 - self.cl2, CustomList)

        self.compare(self.cl1, CustomList([5, 1, 3, 7]))
        self.compare(self.cl2, CustomList([1, 2, 7]))
        self.compare(self.list1, [2, 2])

    def test__iadd__(self):
        self.cl1 += self.cl2
        self.compare(self.cl1, CustomList([6, 3, 10, 7]))
        self.cl2 += CustomList(self.list1)
        self.compare(self.cl2, CustomList([3, 4, 7]))
        self.cl2 += self.list1
        self.compare(self.cl2, CustomList([5, 6, 7]))

        self.assertIsInstance(self.cl2, CustomList)

    def test__isub__(self):
        self.cl1 -= self.cl2
        self.compare(self.cl1, CustomList([4, -1, -4, 7]))
        self.cl2 -= CustomList(self.list1)
        self.compare(self.cl2, CustomList([-1, 0, 7]))
        self.cl2 -= self.list1
        self.compare(self.cl2, CustomList([-3, -2, 7]))

        self.assertIsInstance(self.cl2, CustomList)

    def test__lt__(self):
        self.cl2.append(4)

        self.assertFalse(self.cl1 < self.cl2)
        self.assertFalse(self.cl3 < self.cl1)
        self.assertFalse(self.cl1 < self.cl4)

    def test__le__(self):
        self.cl2.append(4)

        self.assertFalse(self.cl1 <= self.cl2)
        self.assertTrue(self.cl3 <= self.cl1)
        self.assertFalse(self.cl1 <= self.cl4)

    def test__eq__(self):
        self.cl2.append(4)

        self.assertFalse(self.cl1 == self.cl2)
        self.assertTrue(self.cl3 == self.cl1)
        self.assertTrue(self.cl4 == CustomList())

    def test__ne__(self):
        self.cl2.append(4)

        self.assertTrue(self.cl1 != self.cl2)
        self.assertFalse(self.cl3 != self.cl1)
        self.assertTrue(self.cl4 != self.cl2)

    def test__gt__(self):
        self.cl2.append(4)

        self.assertTrue(self.cl1 > self.cl2)
        self.assertFalse(self.cl3 > self.cl1)
        self.assertTrue(self.cl1 > self.cl4)
        self.assertTrue(self.cl2 > self.cl4)

    def test__ge__(self):
        self.cl2.append(4)

        self.assertTrue(self.cl1 >= self.cl2)
        self.assertTrue(self.cl3 >= self.cl1)
        self.assertTrue(self.cl1 >= self.cl4)
        self.assertTrue(self.cl2 >= self.cl4)


def main():
    unittest.main()


if __name__ == "__main__":
    main()
