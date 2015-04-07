/* rgrow.i */
%module rgrow
%{
/* Put header files here or function declarations like below */
extern void rgrow(IplImage *source, IplImage *dest, int sx, int sy, int threshold);
%}

extern void rgrow(IplImage *source, IplImage *dest, int sx, int sy, int threshold);

