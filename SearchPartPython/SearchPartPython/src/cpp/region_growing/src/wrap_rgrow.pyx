from libcpp.list cimport list
import cython

# import both numpy and the Cython declarations for numpy
import numpy as np
cimport numpy as np

cdef extern from "rgrow.h":
    int rgrow(double* source1, double* dest1, int m, int n, int sx, int sy, int threshold);

def rgrow_func(np.ndarray[double, ndim=3, mode="c"] source1, np.ndarray[double, ndim=2, mode="c"] dest1):
    cdef int m, n, sx, sy, threshold
    m, n = source1.shape[1], source1.shape[0]
    sx=31
    sy=22
    threshold=30
    a=rgrow(&source1[0,0,0], &dest1[0,0],m,n,sx,sy,threshold)
    return a