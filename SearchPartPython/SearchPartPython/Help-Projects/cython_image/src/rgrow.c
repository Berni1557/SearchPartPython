//============================================================================

// Name        : gregion_grow.cpp
// Author      : Ich
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C++, Ansi-style
//============================================================================


#include <cv.h>
#include <highgui.h>

#include <stdlib.h>
#include <stdio.h>

#include <opencv/cv.h>
#include <opencv/highgui.h>

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
	int k=0;
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

void
rgrow(IplImage *source, IplImage *dest, int sx, int sy, int threshold)
{
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

    cvSet(dest, cvScalar(10,10,10));
    list_n = newnode(sx, sy);
    list_r = NULL;

    Color color;
    CvScalar s=cvGet2D(source,sy,sx);
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
                if (sx + dx == -1 || sx + dx == source->width ||
                    sy + dy == -1 || sy + dy == source->height)
                    break;
                if (contains(list_n, sx + dx, sy + dy))
                    continue;
                if (contains(list_r, sx + dx, sy + dy))
                    continue;
                s=cvGet2D(source,(sy + dy),(sx + dx));
                curcolor.b = s.val[0];
                curcolor.g = s.val[1];
                curcolor.r = s.val[2];
                curdiff = colordiff(color, curcolor);
                if (curdiff <= threshold)
                    pl_push(&list_n, newnode(sx + dx, sy + dy));
            }
        }
        pl_mean(list_r,source,&color,num_r);
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
    	cvSet2D(dest,node_r->y,node_r->x,s1);

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

}



int main( int argc, char** argv )
{
  Mat image;

  // region growing
  IplImage *source = NULL;
  IplImage *dest = NULL;
  int64 t0, t1;
  double tps, deltatime;

  int threshold=30;

  const char *infile ="/home/bernifoellmer/Studium/SearchPartPython/SearchPartPython/SearchPartPython/SearchPartPython/data/K1.JPG";

  source = cvLoadImage(infile, CV_LOAD_IMAGE_COLOR);
  dest = cvCreateImage(cvSize(source->width, source->height),IPL_DEPTH_8U, 1);

  int sx=30;
  int sy=60;

  t0 = cvGetTickCount();
  rgrow(source, dest, sx, sy , threshold);
  t1 = cvGetTickCount();
  tps = cvGetTickFrequency() * 1.0e6;
  deltatime = (double) (t1 - t0) / tps;
  std::cout << deltatime;

  namedWindow( "Display Image", CV_WINDOW_AUTOSIZE );
  Mat Im(dest);
  imshow( "Display Image", Im);
  waitKey(0);

  return 0;
}


