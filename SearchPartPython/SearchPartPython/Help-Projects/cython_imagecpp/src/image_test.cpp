#include <cv.h>
#include <highgui.h>

#include <stdlib.h>
#include <stdio.h>

#include <opencv/cv.h>
#include <opencv/highgui.h>
#include "image_test.h"

using namespace cv;

void image_show() {
	IplImage *source = NULL;
	const char *infile ="/home/bernifoellmer/Studium/SearchPartPython/SearchPartPython/SearchPartPython/SearchPartPython/data/K1.JPG";
	source = cvLoadImage(infile, CV_LOAD_IMAGE_COLOR);
	namedWindow( "Display Image", CV_WINDOW_AUTOSIZE );
	Mat Im(source);
	imshow( "Display Image", Im);
	waitKey(0);
}
/*
int main( int argc, char** argv )
{
	image_show();
}
*/
