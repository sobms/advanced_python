#! /usr/bin/env python

import time
import cutils


def matrix_multiplication(*args):
    matrix_a = args[0]
    result = []
    for i in range(1, len(args)):
        matrix_b = args[i]
        result = []
        for j in range(len(matrix_a)):
            row = []
            for k in range(len(matrix_b[0])):
                row.append(
                    sum(
                        [
                            matrix_a[j][t] * matrix_b[t][k]
                            for t in range(len(matrix_a[j]))
                        ]
                    )
                )
            result.append(row)
        matrix_a = result
    return result


def main():
    args = (
        [[(3 * i + j) / 10 for i in range(100)] for j in range(50)],
        [[(2 * i + j) / 20 for i in range(100)] for j in range(100)],
        *[
            [[(i + 2 * j) / 20 for i in range(100)] for j in range(100)]
            for _ in range(100)
        ],
    )
    print("+---------- python ----------+")
    start_time = time.time()
    result = matrix_multiplication(*args)
    end_time = time.time()
    print(
        f"Time of execution of python matrix multiplication is {end_time-start_time} seconds"
    )
    print("+---------- capi ----------+")
    start_time = time.time()
    result_capi = cutils.matrix_multiplication(*args)
    end_time = time.time()
    print(
        f"Time of execution of capi matrix multiplication is {end_time-start_time} seconds"
    )
    assert result == result_capi


if __name__ == "__main__":
    main()
