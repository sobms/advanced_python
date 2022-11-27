import unittest
from metaclass import CustomClass


class MetaClassTest(unittest.TestCase):
    def test_meta_class(self):
        inst = CustomClass()
        CustomClass.y = 3
        print(inst)
        self.assertFalse(hasattr(inst, "val"))
        self.assertTrue(hasattr(inst, "custom_val"))
        self.assertEqual(inst.custom_val, 99)

        self.assertFalse(hasattr(inst, "x"))
        self.assertTrue(hasattr(inst, "custom_x"))
        self.assertEqual(inst.custom_x, 50)

        self.assertFalse(hasattr(inst, "line"))
        self.assertTrue(hasattr(inst, "custom_line"))
        self.assertEqual(inst.custom_line(), 100)

        self.assertTrue(hasattr(CustomClass, "custom_y"))
        self.assertTrue(hasattr(CustomClass, "custom_x"))
        self.assertEqual(CustomClass.custom_y, 3)
        self.assertEqual(CustomClass.custom_x, 50)

        self.assertEqual(str(inst), "Custom_by_metaclass")
        self.assertFalse(hasattr(CustomClass, "y"))
        self.assertFalse(hasattr(inst, "yyy"))
        inst.dynamic = "added later"
        self.assertEqual(inst.custom_dynamic, "added later")
        self.assertFalse(hasattr(inst, "dynamic"))


if __name__ == "__main__":
    unittest.main()
