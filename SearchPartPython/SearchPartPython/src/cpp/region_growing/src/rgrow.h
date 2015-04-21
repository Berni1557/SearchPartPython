#ifndef TESTLIB_H
#define TESTLIB_H

#include <cv.h>
#include <highgui.h>

#include <stdlib.h>
#include <stdio.h>

#include <opencv/cv.h>
#include <opencv/highgui.h>



#include <iostream>
#include <list>

#include <opencv2/core/core.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>

int rgrow(double* array1, double* array2, int m, int n, int sx, int sy, int threshold);
//int rgrow(double* array,int n, int m);
//void rgrow(IplImage *source, IplImage *dest, int sx, int sy, int threshold);

#endif
