#include <iostream>
#include <cstdarg>
#include <vector>

extern "C" {
	struct PyList_Matrix {
		long* arr;
		int shape_w;
		int shape_h;
		std::vector<std::vector<long>> get_matrix() {
			std::vector<std::vector<long>> matrix(shape_h, std::vector<long>(shape_w));
			for (int i = 0; i < shape_h; i++) {
				for (int j = 0; j < shape_w; j++) {
					matrix[i][j] = arr[i*shape_w+j];
				}
			}
			return matrix;
		}
	};
	int sum_of_elements(struct PyList_Matrix* matrix) {
		std::vector<std::vector<long>> m_a = matrix->get_matrix();
		/*std::cout << m_a[0][0] << std::endl;
		return m_a[0][0];*/
		return 0;
	}

}
