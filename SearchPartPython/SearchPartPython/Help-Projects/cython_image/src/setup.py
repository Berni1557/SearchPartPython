from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [Extension("imagemod", ["wrap_add.pyx", "image_test.cpp"], include_dirs=["/usr/include/opencv","/usr/local/include/opencv","/usr/local/lib"], language='c++',)]

setup(cmdclass = {'build_ext': build_ext}, ext_modules = ext_modules)