# 3) Написать декоратор, который считает и выводит среднее время выполнения последних k вызовов исходной функции.
# k задается через параметр декоратора.
# После каждого вызова задекорированной функции должно выводиться среднее по k последним вызовам.
import time
from collections import deque


def mean_deco(arg):
    times = deque(maxlen=arg)

    def mean_time(func):
        def _mean_time(*args, **kwargs):
            st_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            times.append(end_time - st_time)
            if len(times) == arg:
                print(
                    f"For func {func.__name__} time for last {arg} calls is {sum(times)/len(times)}"
                )
            return result

        return _mean_time

    return mean_time


if __name__ == "__main__":

    @mean_deco(100)
    def foo(string):
        return 10

    @mean_deco(100)
    def boo(a, b):
        a = a**6
        b = b**6
        return a + b

    for _ in range(1000):
        foo("Walter")  # при каждом вызове выводится среднее по k=10 последним вызовам

    for _ in range(1000):
        boo(10, 20)
