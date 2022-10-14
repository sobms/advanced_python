import unittest
from descriptors import Data


class IntegerTest(unittest.TestCase):
    def setUp(self):
        self.data = Data()

    def test_integer(self):
        self.data.num = 100
        self.assertEqual(self.data.num, 100)
        self.data.num = -100
        self.assertEqual(self.data.num, -100)
        with self.assertRaises(TypeError):
            self.data.num = [1, 2, 2]
        with self.assertRaises(TypeError):
            self.data.num = "ok"


class StringTest(unittest.TestCase):
    def setUp(self):
        self.data = Data()

    def test_string(self):
        self.data.name = "masha"
        self.assertEqual(self.data.name, "masha")
        with self.assertRaises(TypeError):
            self.data.name = {"a": "b"}
        with self.assertRaises(TypeError):
            self.data.name = 4.2


class PositiveIntegerTest(unittest.TestCase):
    def setUp(self):
        self.data = Data()

    def test_positive_integer(self):
        self.data.price = 9900
        self.assertEqual(self.data.price, 9900)
        with self.assertRaises(TypeError):
            self.data.price = "paper"
        with self.assertRaises(TypeError):
            self.data.price = 4.2
        with self.assertRaises(ValueError):
            self.data.price = -100
        with self.assertRaises(ValueError):
            self.data.price = 0


if __name__ == "__main__":
    unittest.main()
