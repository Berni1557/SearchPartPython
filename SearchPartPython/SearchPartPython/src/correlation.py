import numpy as np
import cv2
from scipy import signal
from scipy import misc
import matplotlib.pyplot as plt
import time
path1='/home/bernifoellmer/Studium/SearchPartPython/SearchPartPython/SearchPartPython/SearchPartPython/data/I1.JPG'
#path2='/home/bernifoellmer/Studium/SearchPartPython/SearchPartPython/SearchPartPython/SearchPartPython/data/T1.png'
image=cv2.imread(path1,0)
dst=cv2.imread(path1,0)
#template=cv2.imread(path2,0)

#image = cv2.resize(image, (200,150))
#template = cv2.resize(template, (400,300)) 
newx,newy = image.shape[1]/8,image.shape[0]/8
image1 = cv2.resize(image,(newx,newy))
image2 = image1[280:340, 330:390]
#cv2.resize(template, template, 0, 0.5, 0.5, cv2.INTER_NEAREST);

#image = cv2.cv.fromarray(image)
#meanI=cv2.mean(image)
#image1 = image - meanI[0]

#cv2.namedWindow('display')
#cv2.imshow('display', image1)
#cv2.waitKey(0)
#meanT=cv2.mean(image)
#template1 = template-meanT[0]
#lena = lena + np.random.randn(*lena.shape) * 50 # add noise
print 'start'
start = time.time()
#corr = signal.correlate2d(image1, template1, boundary='symm', mode='same')
end = time.time()
print end - start
print 'end'

#dst = cv2.cv.fromarray(corr)

#cv2.normalize(corr,dst,0,255,cv2.NORM_MINMAX, cv2.CV_8UC1)
#cv2.CV_8UC1
#corr1=corr+minv
cv2.imshow('display',image2)
cv2.waitKey(0)
#y, x = np.unravel_index(np.argmax(corr), corr.shape) # find the match