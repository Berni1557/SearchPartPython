from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [Extension("rgrowmod", 
                         sources=["wrap_rgrow.pyx", "rgrow.cpp"], 
                         include_dirs=[".","/usr/include/opencv","/usr/include/opencv/opencv_core.h","/usr/include/opencv/opencv_imgproc.h","/usr/include/opencv/opencv_highgui.h","/usr/local/include/opencv","/usr/local/lib"],
                         language='c++',
                         library_dirs=['/opt/local/lib', 'source'],
                         libraries=['opencv_core', 'opencv_imgproc', 'opencv_highgui']) 
]                

setup(cmdclass = {'build_ext': build_ext}, ext_modules = ext_modules)


