class CustomMeta(type):
    def __init__(cls, name, bases, dct):
        print("CustomMeta, __init__")
        super().__init__(cls)

    def __call__(cls):
        print("CustomMeta, __call__")
        prefix = "custom_"
        new_obj = super().__call__()  # call new + init
        for attr in dir(cls):
            if not (
                attr.startswith("__") and attr.endswith("__")
            ) and not attr.startswith(prefix):
                setattr(cls, "custom_" + attr, getattr(cls, attr))
                if attr in cls.__dict__:
                    delattr(cls, attr)
        return new_obj

    def __new__(cls, name, bases, dct):
        print("CustomMeta, __new__")
        prefix = "custom_"
        instance = super(CustomMeta, cls).__new__(cls, name, bases, dct)

        def meta_setattr(inst, name, value):
            print("CustomClass", "meta_setattr", name)
            if (
                name not in inst.__dict__
                and not name.startswith(prefix)
                and not (name.startswith("__") and name.endswith("__"))
            ):
                inst.__dict__[prefix + name] = value

        instance.__setattr__ = meta_setattr
        return instance

    def __setattr__(cls, name, val):
        print("CustomMeta, __setattr__")
        prefix = "custom_"
        if name not in cls.__dict__:
            if not name.startswith(prefix) and not (
                name.startswith("__") and name.endswith("__")
            ):
                name = prefix + name
        super().__setattr__(name, val)


class CustomClass(metaclass=CustomMeta):
    x = 50

    def __init__(self, val=99):
        self.val = val

    def line(self):
        return 100

    def __str__(self):
        return "Custom_by_metaclass"


if __name__ == "__main__":
    inst = CustomClass()
    CustomClass.y = 40
    print(inst.custom_x == 50)

    print(inst.custom_val == 99)
    print(inst.custom_line() == 100)
    print(str(inst) == "Custom_by_metaclass")
    print(CustomClass.custom_y == 40)
    print(CustomClass.custom_x == 50)
    inst.dynamic = "added later"
    print(inst.custom_dynamic == "added later")
