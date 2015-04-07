from libcpp.list cimport list

cdef extern from "image_test.h":
    int image_show()

def show():
    a=image_show()
    b=2
    print a
    print 'Done3'