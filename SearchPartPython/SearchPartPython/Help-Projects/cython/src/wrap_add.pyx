from libcpp.list cimport list

cdef extern from "add.h":
    int addfunc(int x0, int x1)

def addPy(x0,x1):
    s=addfunc(x0,x1)
    print s