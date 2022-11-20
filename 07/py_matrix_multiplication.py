def is_matrix(matrix):
    if not all([isinstance(matrix[i], list) and len(matrix[i]) == len(matrix[0])
                for i in range(len(matrix))]):
        return False
    return True

def check_shapes(matrix_a, matrix_b):
    if len(matrix_a[0]) == len(matrix_b):
        return True
    else:
        return False

def matrix_multiplication(*args):
    if len(args) < 2:
        print("Incorrect count of arguments!")
        return None
    matrix_a = args[0]
    result = []
    for i in range(1, len(args)):
        matrix_b = args[i]
        if not (is_matrix(matrix_a) and is_matrix(matrix_b)):
            print("Error! At least one of the argument is not a matrix!")
            return None
        if not check_shapes(matrix_a, matrix_b):
            print("Inconsistent matrix shapes. Count of columns A don't match with count of rows B")
            return None
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