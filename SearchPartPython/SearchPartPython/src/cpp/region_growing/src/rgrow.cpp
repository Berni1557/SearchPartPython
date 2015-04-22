
#include <cv.h>
#include <highgui.h>

#include <stdlib.h>
#include <stdio.h>

#include <opencv/cv.h>
#include <opencv/highgui.h>

#include "rgrow.h"

#include <iostream>
#include <list>

#include <opencv2/core/core.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>

using namespace cv;

typedef struct {
    unsigned char r;
    unsigned char g;
    unsigned char b;
} Color;


typedef struct PosList {
    int x;
    int y;
    struct PosList *next;
} PosList;


int
colordiff(Color a, Color b)
{
    int dr, dg, db;

    dr = (int) ((a.r < b.r) ? (b.r - a.r) : (a.r - b.r));
    dg = (int) ((a.g < b.g) ? (b.g - a.g) : (a.g - b.g));
    db = (int) ((a.b < b.b) ? (b.b - a.b) : (a.b - b.b));
    return dr + dg + db;
}

PosList *
newnode(int x, int y)
{
    PosList *pos;

    pos = (PosList *) malloc(sizeof(PosList));
    pos->x = x;
    pos->y = y;
    pos->next = NULL;
    return pos;
}

void
delnode(PosList **pos)
{
    free(*pos);
    *pos = NULL;
}

void
pl_push(PosList **list, PosList *pos)
{
    pos->next = *list;
    *list = pos;
}


int pl_mean(PosList *list_r, IplImage * source, Color *color, int num_r)
{
	PosList *a;
	//int k=0;
	a=list_r;
	int sx; int sy;
	sy=a->y;
	sx=a->x;
	CvScalar s=cvGet2D(source,sy,sx);
	float v1=((float)num_r/((float)num_r+1))*(float)(uint8_t)(color->b)+(1/((float)num_r+1))*(float)s.val[0];
	float v2=((float)num_r/((float)num_r+1))*(float)(uint8_t)(color->g)+(1/((float)num_r+1))*(float)s.val[1];
	float v3=((float)num_r/((float)num_r+1))*(float)(uint8_t)(color->r)+(1/((float)num_r+1))*(float)s.val[2];
	color->b=(uchar)round(v1);
	color->g=(uchar)round(v2);
	color->r=(uchar)round(v3);

return 1;

}

PosList *
pl_pop(PosList **list)
{
    PosList *pos;

    pos = *list;
    *list = (*list)->next;
    return pos;
}

void
dellist(PosList **list)
{
    PosList *a, *b;

    a = *list;
    while (a != NULL) {
        b = a->next;
        delnode(&a);
        a = b;
    }
}

int
contains(PosList *list, int x, int y)
{
    while (list != NULL) {
        if (list->x == x && list->y == y)
            return 1;
        list = list->next;
    }
    return 0;
}



int rgrow(double* array1, double* array2, int m, int n, int sx, int sy, int threshold)
{

	unsigned char array1d[m][n][3];
	unsigned char array2d[m][n];
	//convert_array(array1,array2,array1d,array2d, int m, int n);

	int k=0;
	for(int i=0; i<m; ++i){
		for(int j=0; j<n; ++j){
			for(int p=0; p<3; ++p){
				array1d[i][j][p]=(uchar)(array1[k]+50);
				k++;
			}
		}
	}
	k=0;
	for(int i=0; i<m; ++i){
		for(int j=0; j<n; ++j){
			array2d[i][j]=(uchar)array2[k];
			k++;
		}
	}

	Mat source1 =  Mat(n,m, CV_8UC3, array1d);
	Mat dest1 =  Mat(n,m, CV_8UC1, array2d);



	//Mat source1;
	//Mat dest1;


	IplImage source;
	IplImage dest;
	source = source1.operator IplImage();
	dest = dest1.operator IplImage();

    PosList *list_n;
    PosList *node_r;
    PosList *list_r;
    Color curcolor;
    int dx, dy;

#ifdef REC
    CvVideoWriter *writer;
    CvSize size;
    IplImage *frame;
    int i;
#endif

#ifdef REC
    size = cvSize(dest->width, dest->height);
    frame = cvCreateImage(size, IPL_DEPTH_8U, 3);
    writer = cvCreateVideoWriter("rgrow.avi", CV_FOURCC('M', 'J', 'P', 'G'), 15.0, size, 1);
#endif

    cvSet(&dest, cvScalar(10,10,10));
    list_n = newnode(sx, sy);
    list_r = NULL;

    Color color;
    CvScalar s=cvGet2D(&source,sy,sx);
    color.b = s.val[0];
    color.g = s.val[1];
    color.r = s.val[2];
    int curdiff;
    int num_r=0;
    while (list_n != NULL) {
        sx = list_n->x;
        sy = list_n->y;
        pl_push(&list_r, pl_pop(&list_n));
        num_r++;
        for (dy = -1; dy <= 1; dy++) {
            for (dx = -1; dx <= 1; dx++) {
                if (dx == 0 && dy == 0)
                    continue;
                if (dx != 0 && dy != 0)
                    continue;
                if (sx + dx == -1 || sx + dx == (&source)->width || sy + dy == -1 || sy + dy == (&source)->height)
                    break;
                if (contains(list_n, sx + dx, sy + dy))
                    continue;
                if (contains(list_r, sx + dx, sy + dy))
                    continue;
                s=cvGet2D(&source,(sy + dy),(sx + dx));
                curcolor.b = s.val[0];
                curcolor.g = s.val[1];
                curcolor.r = s.val[2];
                curdiff = colordiff(color, curcolor);
                if (curdiff <= threshold)
                    pl_push(&list_n, newnode(sx + dx, sy + dy));
            }
        }
        pl_mean(list_r,&source,&color,num_r);
    }

#ifdef REC
    cvCvtColor(dest, frame, CV_GRAY2BGR);
    cvWriteFrame(writer, frame);
    i = 0;
#endif
    node_r = list_r;
    CvScalar s1;
    s1.val[0]=255;
    while (node_r != NULL) {
    	cvSet2D(&dest,node_r->y,node_r->x,s1);

#ifdef REC
        if (i % 100 == 0) {
            cvCvtColor(dest, frame, CV_GRAY2BGR);
            cvWriteFrame(writer, frame);
        }
        i++;
#endif

        node_r = node_r->next;
    }
    dellist(&list_r);

#ifdef REC
    cvReleargrow(source, dest, color, threshold);seVideoWriter(&writer);
#endif
/*
*/
//imshow( "Display Image", dest1);
//waitKey(0);

k=0;
for(int i=0; i<m; ++i){
	for(int j=0; j<n; ++j){
		array2[k]=(double)array2d[i][j];
		k++;
	}
}

return 3;


}

/*

int main( int argc, char** argv )
{
  Mat image;

  // region growing
  //IplImage source;
  //IplImage dest;
  int64 t0, t1;
  double tps, deltatime;

  int threshold=30;

  //const char *infile ="/home/bernifoellmer/Studium/SearchPartPython/SearchPartPython/SearchPartPython/SearchPartPython/data/K1.JPG";

  //source = cvLoadImage(infile, CV_LOAD_IMAGE_COLOR);
  //dest = cvCreateImage(cvSize(source->width, source->height),IPL_DEPTH_8U, 1);

  int sx=25;
  int sy=60;

  t0 = cvGetTickCount();

  Mat source1 = imread("/home/bernifoellmer/Studium/SearchPartPython/SearchPartPython/SearchPartPython/SearchPartPython/data/K1.JPG", CV_LOAD_IMAGE_COLOR);
  Mat dest1 = Mat::zeros(source1.rows,source1.cols, CV_8UC1);


  //source = source1.operator IplImage();
  //source = cvCreateImage(cvSize(source1.cols,source1.rows), 8, 3);
  //source->imageData = (char *) source1.data;

  //Mat Im1(&source);
  //imshow( "Display Image1", Im1);
  //waitKey(0);

  //dest = cvCreateImage(cvSize(dest1.cols,dest1.rows), 8, 1);
  //dest->imageData = (char *) dest1.data;
  //dest = dest1.operator IplImage();


  //IplImage source=cvCloneImage(&(IplImage)source1);
  //IplImage dest=cvCloneImage(&(IplImage)dest1);

  //IplImage* source=cvCloneImage(&(IplImage)source1);
  //IplImage* dest=cvCloneImage(&(IplImage)dest1);

  rgrow(source1, dest1, sx, sy , threshold);
  t1 = cvGetTickCount();
  tps = cvGetTickFrequency() * 1.0e6;
  deltatime = (double) (t1 - t0) / tps;
  std::cout << deltatime;

  namedWindow( "Display Image", CV_WINDOW_AUTOSIZE );
  //Mat Im(&dest);
  imshow( "Display Image", dest1);
  waitKey(0);

  return 0;


}
*/


