class Integer:
    def __set_name__(self, owner, name):
        self.name = name
        self._protected_name = f"_{name}"

    def __set__(self, obj, val):
        if not isinstance(val, int):
            raise TypeError("Inconsistent type")
        setattr(obj, self._protected_name, val)

    def __get__(self, obj, val):
        return getattr(obj, self._protected_name)


class String:
    def __set_name__(self, owner, name):
        self.name = name
        self._protected_name = f"_{name}"

    def __set__(self, obj, val):
        if not isinstance(val, str):
            raise TypeError("Inconsistent type")
        setattr(obj, self._protected_name, val)

    def __get__(self, obj, val):
        return getattr(obj, self._protected_name)


class PositiveInteger:
    def __set_name__(self, owner, name):
        self.name = name
        self._protected_name = f"_{name}"

    def __set__(self, obj, val):
        if not isinstance(val, int):
            raise TypeError("Inconsistent type")
        if val <= 0:
            raise ValueError("Incorrect value")
        setattr(obj, self._protected_name, val)

    def __get__(self, obj, val):
        return getattr(obj, self._protected_name)


class Data:

    num = Integer()
    name = String()
    price = PositiveInteger()

    def __init__(self):
        self.num = -11
        self.name = "Integer"
        self.price = 990


if __name__ == "__main__":
    data = Data()
    print(data.num, data.name, data.price)
