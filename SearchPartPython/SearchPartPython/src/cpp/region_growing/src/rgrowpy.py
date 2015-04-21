import rgrowmod
import cython
# import both numpy and the Cython declarations for numpy
import numpy as np
import cv2
from numpy import double

import time

#Iin = cv2.imread("/home/bernifoellmer/workspace/cython_image/I1.png")
Iin = cv2.imread("/home/bernifoellmer/Studium/SearchPartPython/SearchPartPython/SearchPartPython/SearchPartPython/data/T.JPG")
#G = cv2.cvtColor(Iin, cv2.COLOR_BGR2GRAY)

height, width, depth = Iin.shape
G=np.zeros((height,width),dtype=np.uint8)

#height, width, depth = Iin.shape
#G=np.zeros((height,width),dtype=np.uint8)
#G = cv2.cvtColor(G, cv2.COLOR_GRAY2BGR)


I1=Iin.astype(double)
I2=G.astype(double)

start = time.time()
for x in range(0, 1000):
    out=rgrowmod.rgrow_func(I1,I2)
end = time.time()
print end - start

I1o = I1.astype(np.uint8)
I2o = I2.astype(np.uint8)
cv2.imshow('gray_image',I2o) 
cv2.waitKey(0) 




