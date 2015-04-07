#!/usr/bin/env python
"""
import cv2
import numpy as np
import time


class Featuregenerator(object):
    images=list()
    def __init__(self,images):
        self.images=images
        
    def generate_histogram(self,featurenum):
        Nimages=list()
        for Im in self.images:
            h,s,v = cv2.split(Im)
            if featurenum is None:
                bins = np.arange(0,261,20)
                N1,bins1 = np.histogram(h,bins)
                N2,bins2 = np.histogram(s,bins)
                N3,bins3 = np.histogram(v,bins)
                N=[N1,N2,N3]
                return N
            else:
                bins = np.arange(0,261,20)
                N=list()
                for fn in featurenum:
                    if fn<13:
                        binsind=[bins[fn],bins[fn+1]-1]
                        Ni,bi = np.histogram(h,binsind)
                        N.append(Ni[0])
                    elif fn>=13 and fn<26:
                        binsind=[bins[fn-13],bins[fn-12]-1]
                        Ni,bi = np.histogram(s,binsind)     
                        N.append(Ni[0])  
                    elif fn>=26 and fn<=38:
                        binsind=[bins[fn-26],bins[fn-25]-1]
                        Ni,bi = np.histogram(v,binsind)
                        N.append(Ni[0])
                    else:
                        N.append(None)
            Nimages.append(N)
        return Nimages
 
Im=cv2.imread('/home/bernifoellmer/Studium/SearchPartPython/SearchPartPython/SearchPartPython/SearchPartPython/data/Iq.JPG')
Im1=cv2.imread('/home/bernifoellmer/Studium/SearchPartPython/SearchPartPython/SearchPartPython/SearchPartPython/data/Iq1.JPG')
images=list()
images.append(Im)
#images.append(Im1)
FG=Featuregenerator(images) 
bins=FG.generate_histogram(None)
print bins
print 'feature'
#bins=FG.generate_histogram([3,4,40])
#print bins

start = time.time()
for x in xrange(0, 100):
    bins=FG.generate_histogram([3,4,23])
    print bins
end = time.time()
print end - start
"""


print "asd"