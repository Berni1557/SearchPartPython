#include <time.h>

 int addfunc(int a, int b) {
	 return a+b;
 }

 // swig -python add.i
 // gcc -c add.c add_wrap.c -I/usr/include/python2.7 -lpython2.7 -fPIC
 // ld -shared add.o add_wrap.o -o _add.so

