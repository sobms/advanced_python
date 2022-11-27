class CustomList(list):
    def __add__(self, x: list):
        # checking if incorrect types
        if not isinstance(x, list):
            raise TypeError(
                f"can only add one list "
                f"(not {str(type(x))}) to another list"
            )
        # create instance to return
        result_list = CustomList()
        result_list.extend(self)
        # extend first list if it's shorter
        dif = self.__len__() - x.__len__()
        if dif < 0:
            result_list.extend([0 for i in range(0, -dif)])
        # get sum
        for i in range(0, x.__len__()):
            result_list[i] = result_list[i] + x[i]
        return result_list

    def __radd__(self, x: list):
        return self + x

    def __sub__(self, x: list):
        if not isinstance(x, list):
            raise TypeError(
                f"can only subtract one list "
                f"(not {str(type(x))}) from another list"
            )
        result_list = CustomList()
        result_list.extend(self)
        dif = result_list.__len__() - x.__len__()
        if dif < 0:
            result_list.extend([0 for i in range(0, -dif)])
        for i in range(0, x.__len__()):
            result_list[i] = result_list[i] - x[i]
        return result_list

    def __rsub__(self, x: list):
        res = self - x
        for i in range(len(res)):
            res[i] *= -1
        return res

    def __ge__(self, x: list) -> bool:
        if not isinstance(x, list):
            raise TypeError(
                f"can only compare one list (not "
                f"{str(type(x))}) with another list"
            )
        return sum(self) >= sum(x)

    def __le__(self, x: list) -> bool:
        if not isinstance(x, list):
            raise TypeError(
                f"can only compare one list (not "
                f"{str(type(x))}) with another list"
            )
        return sum(self) <= sum(x)

    def __lt__(self, x: list) -> bool:
        if not isinstance(x, list):
            raise TypeError(
                f"can only compare one list (not "
                f"{str(type(x))}) with another list"
            )
        return sum(self) < sum(x)

    def __gt__(self, x: list) -> bool:
        if not isinstance(x, list):
            raise TypeError(
                f"can only compare one list (not "
                f"{str(type(x))}) with another list"
            )
        return sum(self) > sum(x)

    def __eq__(self, x: list):
        if not isinstance(x, list):
            raise TypeError(
                f"can only compare one list (not "
                f"{str(type(x))}) with another list"
            )
        return sum(self) == sum(x)

    def __ne__(self, x: list):
        if not isinstance(x, list):
            raise TypeError(
                f"can only compare one list (not "
                f"{str(type(x))}) with another list"
            )
        return sum(self) != sum(x)

    def __str__(self):
        return f"{super().__str__()} sum: {str(sum(self))}"
