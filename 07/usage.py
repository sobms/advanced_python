import cffi

def test_work():
    ffi = cffi.FFI()
    lib = ffi.dlopen('./lib_test.so')
    ffi.cdef('''
    int sum_of_elements(long** matrix);
    ''')
    matrix = [[1,2,3], [4,5,6], [7,8,9]]
    matrix_a = ffi.new(f"long [{len(matrix)}][{len(matrix[0])}]", matrix)
    res = lib.sum_of_elements(matrix_a)
    print(res)

if __name__ == '__main__':
    print(test_work())
