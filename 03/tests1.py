import unittest
from custom_list import CustomList


class CustomListTest(unittest.TestCase):
    def setUp(self):
        self.list1 = CustomList([1, 2, 3, 0, 6, 4])

    def compare_elements(self, list1, list2):
        self.assertIsInstance(list1, list)
        self.assertIsInstance(list2, list)
        self.assertEqual(len(list1), len(list2))
        for a, b in zip(list1, list2):
            self.assertEqual(a, b)

    def test_add(self):
        # CustomList + CustomList
        list2 = CustomList([9, 8, 7, 10])
        result = self.list1 + list2
        self.assertIsInstance(result, CustomList)
        self.compare_elements(result, [10, 10, 10, 10, 6, 4])
        # check if operands stay unchanged
        self.assertIsInstance(self.list1, CustomList)
        self.assertIsInstance(list2, CustomList)
        self.compare_elements(self.list1, [1, 2, 3, 0, 6, 4])
        self.compare_elements(list2, [9, 8, 7, 10])
        # CustomList + CustomList (left list have less length)
        result = list2 + self.list1
        self.assertIsInstance(result, CustomList)
        self.compare_elements(result, [10, 10, 10, 10, 6, 4])
        # check if operands stay unchanged
        self.assertIsInstance(self.list1, CustomList)
        self.assertIsInstance(list2, CustomList)
        self.compare_elements(self.list1, [1, 2, 3, 0, 6, 4])
        self.compare_elements(list2, [9, 8, 7, 10])
        # check if incompatible types
        with self.assertRaises(TypeError):
            lst = self.list1 + 3
        # CustomList + list (CustomList have more elements)
        list2 = [1, 1, 1]
        result = self.list1 + list2
        self.assertIsInstance(result, CustomList)
        self.compare_elements(result, [2, 3, 4, 0, 6, 4])
        # check if operands stay unchanged
        self.assertIsInstance(self.list1, CustomList)
        self.assertIsInstance(list2, list)
        self.compare_elements(self.list1, [1, 2, 3, 0, 6, 4])
        self.compare_elements(list2, [1, 1, 1])
        # list + CustomList (CustomList have more elements)
        result = list2 + self.list1
        self.assertIsInstance(result, CustomList)
        self.compare_elements(result, [2, 3, 4, 0, 6, 4])
        # check if operands stay unchanged
        self.assertIsInstance(self.list1, CustomList)
        self.assertIsInstance(list2, list)
        self.compare_elements(self.list1, [1, 2, 3, 0, 6, 4])
        self.compare_elements(list2, [1, 1, 1])
        # CustomList + list (CustomList have less elements)
        list2 = [1, 1, 1, 0, 9, 7, 3, 2]
        result = self.list1 + list2
        self.assertIsInstance(result, CustomList)
        self.compare_elements(result, [2, 3, 4, 0, 15, 11, 3, 2])
        # check if operands stay unchanged
        self.assertIsInstance(self.list1, CustomList)
        self.assertIsInstance(list2, list)
        self.compare_elements(self.list1, [1, 2, 3, 0, 6, 4])
        self.compare_elements(list2, [1, 1, 1, 0, 9, 7, 3, 2])
        # list + CustomList (CustomList have less elements)
        result = list2 + self.list1
        self.assertIsInstance(result, CustomList)
        self.compare_elements(result, [2, 3, 4, 0, 15, 11, 3, 2])
        # check if operands stay unchanged
        self.assertIsInstance(self.list1, CustomList)
        self.assertIsInstance(list2, list)
        self.compare_elements(self.list1, [1, 2, 3, 0, 6, 4])
        self.compare_elements(list2, [1, 1, 1, 0, 9, 7, 3, 2])

    def test_subtract(self):
        # CustomList - CustomList
        list2 = CustomList([-1, -3, -7, 10])
        result = self.list1 - list2
        self.assertIsInstance(result, CustomList)
        self.compare_elements(result, [2, 5, 10, -10, 6, 4])
        # check if operands stay unchanged
        self.assertIsInstance(self.list1, CustomList)
        self.assertIsInstance(list2, list)
        self.compare_elements(self.list1, [1, 2, 3, 0, 6, 4])
        self.compare_elements(list2, [-1, -3, -7, 10])
        # CustomList - CustomList (left list have less length)
        result = list2 - self.list1
        self.assertIsInstance(result, CustomList)
        self.compare_elements(result, [-2, -5, -10, 10, -6, -4])
        # check if operands stay unchanged
        self.assertIsInstance(self.list1, CustomList)
        self.assertIsInstance(list2, list)
        self.compare_elements(self.list1, [1, 2, 3, 0, 6, 4])
        self.compare_elements(list2, [-1, -3, -7, 10])
        # CustomList - list (CustomList have more elements)
        list2 = [1, 1, 1]
        result = self.list1 - list2
        self.assertIsInstance(result, CustomList)
        self.compare_elements(self.list1 - list2, [0, 1, 2, 0, 6, 4])
        # check if operands stay unchanged
        self.assertIsInstance(self.list1, CustomList)
        self.assertIsInstance(list2, list)
        self.compare_elements(self.list1, [1, 2, 3, 0, 6, 4])
        self.compare_elements(list2, [1, 1, 1])
        # list - CustomList (CustomList have more elements)
        result = list2 - self.list1
        self.assertIsInstance(result, CustomList)
        self.compare_elements(result, [0, -1, -2, 0, -6, -4])
        # check if operands stay unchanged
        self.assertIsInstance(self.list1, CustomList)
        self.assertIsInstance(list2, list)
        self.compare_elements(self.list1, [1, 2, 3, 0, 6, 4])
        self.compare_elements(list2, [1, 1, 1])
        # CustomList - list (CustomList have less length)
        list2 = [1, 1, 1, 0, 9, 7, 3, 2]
        result = self.list1 - list2
        self.assertIsInstance(result, CustomList)
        self.compare_elements(result, [0, 1, 2, 0, -3, -3, -3, -2])
        # check if operands stay unchanged
        self.assertIsInstance(self.list1, CustomList)
        self.assertIsInstance(list2, list)
        self.compare_elements(self.list1, [1, 2, 3, 0, 6, 4])
        self.compare_elements(list2, [1, 1, 1, 0, 9, 7, 3, 2])
        # list - CustomList (CustomList have less elements)
        result = list2 - self.list1
        self.assertIsInstance(result, CustomList)
        self.compare_elements(result, [0, -1, -2, 0, 3, 3, 3, 2])
        # check if operands stay unchanged
        self.assertIsInstance(self.list1, CustomList)
        self.assertIsInstance(list2, list)
        self.compare_elements(self.list1, [1, 2, 3, 0, 6, 4])
        self.compare_elements(list2, [1, 1, 1, 0, 9, 7, 3, 2])
        # check if incompatible types
        with self.assertRaises(TypeError):
            lst = self.list1 - 3

    def test_compare(self):
        list2 = CustomList([1, 3, 7, 10])
        self.assertTrue(self.list1 < list2)
        # check if operands stay unchanged
        self.assertIsInstance(self.list1, CustomList)
        self.assertIsInstance(list2, CustomList)
        self.compare_elements(self.list1, [1, 2, 3, 0, 6, 4])
        self.compare_elements(list2, [1, 3, 7, 10])

        list2 = CustomList([1, 3, 1, 10])
        self.assertTrue(self.list1 > list2)
        # check if operands stay unchanged
        self.assertIsInstance(self.list1, CustomList)
        self.assertIsInstance(list2, CustomList)
        self.compare_elements(self.list1, [1, 2, 3, 0, 6, 4])
        self.compare_elements(list2, [1, 3, 1, 10])

        list2 = CustomList([1, 3, 2, 10])
        self.assertTrue(self.list1 >= list2)
        # check if operands stay unchanged
        self.assertIsInstance(self.list1, CustomList)
        self.assertIsInstance(list2, CustomList)
        self.compare_elements(self.list1, [1, 2, 3, 0, 6, 4])
        self.compare_elements(list2, [1, 3, 2, 10])

        self.assertTrue(self.list1 <= list2)
        # check if operands stay unchanged
        self.assertIsInstance(self.list1, CustomList)
        self.assertIsInstance(list2, CustomList)
        self.compare_elements(self.list1, [1, 2, 3, 0, 6, 4])
        self.compare_elements(list2, [1, 3, 2, 10])

        list2 = [3, 3, 3]
        self.assertTrue(self.list1 > list2)
        # check if operands stay unchanged
        self.assertIsInstance(self.list1, CustomList)
        self.assertIsInstance(list2, list)
        self.compare_elements(self.list1, [1, 2, 3, 0, 6, 4])
        self.compare_elements(list2, [3, 3, 3])

        self.assertTrue(list2 < self.list1)
        # check if operands stay unchanged
        self.assertIsInstance(self.list1, CustomList)
        self.assertIsInstance(list2, list)
        self.compare_elements(self.list1, [1, 2, 3, 0, 6, 4])
        self.compare_elements(list2, [3, 3, 3])

        list2 = [6, 6, 6]
        self.assertTrue(self.list1 <= list2)
        # check if operands stay unchanged
        self.assertIsInstance(self.list1, CustomList)
        self.assertIsInstance(list2, list)
        self.compare_elements(self.list1, [1, 2, 3, 0, 6, 4])
        self.compare_elements(list2, [6, 6, 6])

        self.assertTrue(list2 >= self.list1)
        # check if operands stay unchanged
        self.assertIsInstance(self.list1, CustomList)
        self.assertIsInstance(list2, list)
        self.compare_elements(self.list1, [1, 2, 3, 0, 6, 4])
        self.compare_elements(list2, [6, 6, 6])

        list2 = CustomList([6, 7, 0, -3, 6])
        self.assertTrue(list2 == self.list1)
        # check if operands stay unchanged
        self.assertIsInstance(self.list1, CustomList)
        self.assertIsInstance(list2, CustomList)
        self.compare_elements(self.list1, [1, 2, 3, 0, 6, 4])
        self.compare_elements(list2, [6, 7, 0, -3, 6])

        list2 = CustomList([1, 2, 3, 3, -1])
        self.assertTrue(list2 != self.list1)
        # check if operands stay unchanged
        self.assertIsInstance(self.list1, CustomList)
        self.assertIsInstance(list2, CustomList)
        self.compare_elements(self.list1, [1, 2, 3, 0, 6, 4])
        self.compare_elements(list2, [1, 2, 3, 3, -1])

    def test_string(self):
        self.assertEqual(
            self.list1.__str__(), f"[1, 2, 3, 0, 6, 4] sum: {sum(self.list1)}"
        )
        self.list2 = CustomList([])
        self.assertEqual(self.list2.__str__(), f"[] sum: {sum(self.list2)}")


if __name__ == "__main__":
    unittest.main()
