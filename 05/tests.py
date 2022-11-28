import unittest
import io
from LRUCache import LRUCache
from filter_file_gen import filter_file


class LRUCacheTest(unittest.TestCase):
    def setUp(self):
        self.cache = LRUCache(2)

    def test1(self):
        self.cache.set("k1", "val1")
        self.cache.set("k2", "val2")
        self.assertEqual(self.cache.get("k3"), None)
        self.cache.set("k3", "val3")
        self.assertEqual(self.cache.get("k1"), None)
        self.assertEqual(self.cache.get("k2"), "val2")

    def test2(self):
        self.cache.set("k1", "val1")
        self.cache.set("k2", "val2")
        self.assertEqual(self.cache.get("k1"), "val1")
        self.cache.set("k3", "val3")
        self.assertEqual(self.cache.get("k2"), None)
        self.assertEqual(self.cache.get("k1"), "val1")
        self.cache.set("k4", "val4")
        self.assertEqual(self.cache.get("k3"), None)

    def test3(self):
        self.cache["k1"] = "val1"
        self.cache["k2"] = "val2"
        print(self.cache["k1"])
        self.cache["k3"] = "val3"
        self.assertEqual(self.cache["k1"], "val1")
        self.assertEqual(self.cache["k2"], None)

    def test4(self):
        # capacity = 1
        self.cache = LRUCache(1)
        self.cache.set("k1", "val1")
        self.cache["k2"] = "val2"
        self.assertEqual(self.cache["k1"], None)
        self.assertEqual(self.cache["k2"], "val2")
        self.cache["k3"] = "val3"
        print(self.cache["k2"])
        self.assertEqual(self.cache["k3"], "val3")
        self.assertEqual(self.cache["k2"], None)

    def test5(self):
        # from task
        self.cache.set("k1", "val1")
        self.cache.set("k2", "val2")

        self.assertEqual(self.cache.get("k3"), None)
        self.assertEqual(self.cache.get("k2"), "val2")
        self.assertEqual(self.cache.get("k1"), "val1")

        self.cache.set("k3", "val3")

        self.assertEqual(self.cache.get("k3"), "val3")
        self.assertEqual(self.cache.get("k2"), None)
        self.assertEqual(self.cache.get("k1"), "val1")

    def test6(self):
        # inserting of new element after changing value by existing key
        # lead to deletion unchanged element
        self.cache.set("k1", "val1")
        self.cache.set("k2", "val2")
        # change existing value
        self.cache.set("k1", "new_val1")
        # add new value
        self.cache.set("k3", "val3")
        self.assertEqual(self.cache.get("k3"), "val3")
        self.assertEqual(self.cache.get("k2"), None)
        self.assertEqual(self.cache.get("k1"), "new_val1")


class FilterFileTest(unittest.TestCase):
    def test_filter_file(self):
        file_obj = io.StringIO("abc\ndef ghi jkl\nmno pqr stu\nvw xyz\n")
        self.assertEqual(
            "".join(filter_file(file_obj, ["abc", "sTu", "DEF"])),
            "abc\ndef ghi jkl\nmno pqr stu\n",
        )
        file_obj2 = io.StringIO("abc\ndef ghi jkl\n")
        self.assertEqual("".join(filter_file(file_obj2, ["mro", "sTu"])), "")
        file_obj3 = io.StringIO("ABX\nDEFine ghi jkl\nMNO pQr\nVw xyz\n")
        self.assertEqual(
            "".join(filter_file(file_obj3, ["ABC", "DEF", "mno", "vW"])),
            "MNO pQr\nVw xyz\n",
        )
        with open("input", "w") as file_obj4:
            file_obj4.write("aBC de\ndefense mn\nvw XyZ\n")
        self.assertEqual(
            "".join(filter_file("input", ["ABC", "DEF", "mno", "vW"])),
            "aBC de\nvw XyZ\n",
        )

    def test_multiple_string_return(self):
        # check if one line is output multiple times
        file_obj5 = io.StringIO("abc\ndef ghi jkl\nmno pqr stu\nvw xyz")
        self.assertEqual(
            "".join(filter_file(file_obj5,
                                ["abc", "sTu", "DEF", "ghi", "jkl"])),
            "abc\ndef ghi jkl\nmno pqr stu\n",
        )


if __name__ == "__main__":
    unittest.main()
