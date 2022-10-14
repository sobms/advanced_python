import unittest
from metaclass import CustomClass


class MetaClassTest(unittest.TestCase):
    def test_meta_class(self):
        inst = CustomClass()
        CustomClass.y = 3
        print(inst)
        self.assertEqual(inst.custom_val, 99)
        self.assertEqual(inst.custom_x, 50)
        self.assertEqual(inst.custom_line(), 100)
        self.assertEqual(CustomClass.custom_y, 3)
        self.assertEqual(str(inst), "Custom_by_metaclass")
        with self.assertRaises(AttributeError):
            x = inst.x
        with self.assertRaises(AttributeError):
            val = inst.val
        with self.assertRaises(AttributeError):
            inst.line()
        with self.assertRaises(AttributeError):
            val = CustomClass.y
        with self.assertRaises(AttributeError):
            yyy = inst.yyy
        inst.dynamic = "added later"
        self.assertEqual(inst.custom_dynamic, "added later")
        with self.assertRaises(AttributeError):
            dynamic = inst.dynamic


if __name__ == "__main__":
    unittest.main()
