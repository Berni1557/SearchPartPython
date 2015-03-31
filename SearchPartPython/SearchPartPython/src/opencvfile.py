
from numpy import *
import cv2


img=cv2.imread('/home/bernifoellmer/workspace/SearchPartPython_V01/lena.jpeg')
cv2.imshow('ImageWindow',img)
cv2.waitKey()

a = array([[-4,2,3,4],[5,6,7,8]])
print (a)
print abs(a)