#! /usr/bin/env python

import time
import cutils
from py_matrix_multiplication import matrix_multiplication


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
        f"Time of execution of python matrix multiplication is "
        f"{end_time-start_time} seconds"
    )
    print("+---------- capi ----------+")
    start_time = time.time()
    result_capi = cutils.matrix_multiplication(*args)
    end_time = time.time()
    print(
        f"Time of execution of capi matrix multiplication is "
        f"{end_time-start_time} seconds"
    )
    assert result == result_capi


if __name__ == "__main__":
    main()
