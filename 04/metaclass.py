class CustomMeta(type):

    def __call__(cls):
        prefix = "custom_"
        new_obj = super(CustomMeta, cls).__call__()  # call new + init
        for attr in dir(new_obj):
            if not attr.startswith("__") and not attr.startswith(prefix):
                new_obj.__setattr__(prefix + attr, getattr(new_obj, attr))
                if attr in cls.__dict__:
                    delattr(cls, attr)
                else:
                    delattr(new_obj, attr)
        return new_obj

    def __new__(cls, name, bases, dct):
        prefix = "custom_"
        inst = super(CustomMeta, cls).__new__(cls, name, bases, dct)
        def meta_setattr(inst, name, value):
            if name not in inst.__dict__ and \
                    not (name.startswith("__") or name.endswith("__")):
                inst.__dict__[prefix+name] = value
        inst.__setattr__ = meta_setattr
        return inst

    # def __setattr__(self, name, val):
    #     prefix = "custom_"
    #     if name not in self.__dict__:
    #         if not name.startswith(prefix):
    #             name = prefix + name
    #     super().__setattr__(name, val)
# идея переопределить метод setattr в создаваемом экземпляре

class CustomClass(metaclass=CustomMeta):
    x = 50

    def __init__(self, val=99):
        self.val = val

    def line(self):
        return 100

    def __str__(self):
        return "Custom_by_metaclass"

    # def __setattr__(self, name, val):
    #     prefix = "custom_"
    #     if name not in self.__dict__:
    #         if not name.startswith(prefix):
    #             name = prefix + name
    #     super().__setattr__(name, val)


if __name__ == "__main__":
    inst = CustomClass()
    CustomClass.y = 40
    print(inst.custom_x == 50)
    print(inst.custom_val == 99)
    print(inst.custom_line() == 100)
    print(str(inst) == "Custom_by_metaclass")
    print(CustomClass.custom_y == 40)
    inst.dynamic = "added later"
    print(inst.custom_dynamic == "added later")
