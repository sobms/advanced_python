#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include "Python.h"
#include <utility>
#include <stdexcept>
#include <variant>

extern "C" 
{	
	std::pair<long, long> get_matrix_shape(PyObject* matrix) 
	{
		long rows_count = PyList_Size(matrix);
		long columns_count = 0;
		for (int i = 0; i < rows_count; i++) {
			PyObject* row = PyList_GetItem(matrix, i);
			if (columns_count == 0) 
			{
				columns_count = PyList_Size(row);
			}
			else if (PyList_Size(row) != columns_count) 
			{
				throw std::invalid_argument("At least one of the argument is not a matrix!");
			}
		}
		return std::make_pair(rows_count, columns_count);
	}

	enum DataType {long_ = 1, float_ = 2, other_ = 3}; 
	DataType get_type(PyObject* matrix) 
	{
		PyObject* row = PyList_GetItem(matrix, 0);
		PyObject* a = PyList_GetItem(row, 0);
		if (PyLong_Check(a)) 
		{
			return long_;
		}
		else if (PyFloat_Check(a))
		{
			return float_;
		}
		else
		{
			return other_;
		}
	}

	union rational 
	{
		long l;
		double d;
	};

	PyObject* cutils_matrix_multiplication(PyObject* self, PyObject* args)
	{

       		long matrix_count = PyTuple_Size(args);
		PyObject* matrix_a = PyTuple_GetItem(args, 0);
		PyObject* result = NULL;
		DataType type = get_type(matrix_a);
			
      		for (int i = 1; i < matrix_count; i++) 
    		{	
			PyObject* matrix_b = PyTuple_GetItem(args, i);
			std::pair<long, long> shape_a, shape_b;
			try 
			{
				shape_a = get_matrix_shape(matrix_a);
				shape_b = get_matrix_shape(matrix_b);
			}
			catch (std::invalid_argument& msg) 
			{
				std::cout << msg.what() << std::endl;
				return Py_BuildValue("O", Py_None);
			}
			if (shape_a.second != shape_b.first) 
			{
				std::cout << "Inconsistent matrix shapes. Count of columns A don't match with count of rows B" << std::endl;
				return Py_BuildValue("O", Py_None);
			}
			result = PyList_New(shape_a.first);
			for (int j = 0; j < shape_a.first; j++) 
			{
				PyObject* a_row = PyList_GetItem(matrix_a, j);
				PyObject* result_row = PyList_New(shape_b.second);
				for (int k = 0; k < shape_b.second; k++) 
				{
					rational res_elem;
					if (type == long_) 
					{
						res_elem.l = 0;
					}
					else 
					{
						res_elem.d = 0;
					}
					for (int t = 0; t < shape_a.second; t++) 
					{
						PyObject* a = PyList_GetItem(a_row, t);
						PyObject* b_row = PyList_GetItem(matrix_b, t);
						PyObject* b = PyList_GetItem(b_row, k);
						
						if (PyLong_Check(a) && PyLong_Check(b) && type == long_)
						{
							res_elem.l += PyLong_AsLong(a) * PyLong_AsLong(b);
						}
						else if (PyFloat_Check(a) && PyFloat_Check(b) && type == float_)
						{
							res_elem.d += PyFloat_AsDouble(a) * PyFloat_AsDouble(b);
						}
						else 
						{
							std::cout << "The types of matrix elements don't match" << std::endl;
							return Py_BuildValue("O", Py_None);
						}
					}
					if (type == long_) 
					{
						PyList_SetItem(result_row, k, Py_BuildValue("i", res_elem.l));
					}
					else 
					{
						PyList_SetItem(result_row, k, Py_BuildValue("f", res_elem.d));
					}
				}
				PyList_SetItem(result, j, result_row);
			}
			matrix_a = result;
    		}
		return result;
	}	
}
static PyMethodDef methods[] = {
	{"matrix_multiplication", cutils_matrix_multiplication, METH_VARARGS, "sum of elements of the list"},
	{NULL, NULL, 0, NULL}
};

static struct PyModuleDef cutils_module = {
	PyModuleDef_HEAD_INIT, "cutils",
	NULL, -1, methods
};

PyMODINIT_FUNC PyInit_cutils(void) {
	return PyModule_Create( &cutils_module );
}
