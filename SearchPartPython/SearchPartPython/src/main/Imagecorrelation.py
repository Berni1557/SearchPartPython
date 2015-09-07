#!/usr/bin/env python
# Imagecorrelation

import cv2
import SearchPartModules as SPM
import ScaleCircle as SC
import numpy as np

def corrcomponent(Comp,images):
    thr = 0.4
    n_max=5
    sc=Comp.scale_corr()
    sc_corr=sc[2]
    for Im in images:
        # scale circle
        Circle=SC.ScaleCircle(Im)
        sc_circle=Circle.scale()
        #scale image
        scale=sc_corr/sc_circle
        imagesc = cv2.resize(Im, (int(Im.shape[1]*scale), int(Im.shape[0]*scale)))
        # create mean image
        Componentmean=Comp.create_mean()
        
        
        # Top correlation
        h=sc[0];hl=int(h/2);hr=h-hl
        w=sc[1];wl=int(w/2);wr=w-wl
        # create template
        Compcorr = Componentmean
        n=0
        maxVal=1000
        
        # RGB to HSV
        imagehsv=cv2.cvtColor(imagesc, cv2.cv.CV_BGR2HSV);
        Compcorrhsv=cv2.cvtColor(Compcorr, cv2.cv.CV_BGR2HSV);
        # correlation
        corr = cv2.matchTemplate(imagesc,Compcorr,cv2.TM_CCOEFF_NORMED)
        
        #cv2.imshow('display',corr*255)
        #cv2.waitKey(0)

        while maxVal>thr and n<n_max:
            # determine maximum
            (minVal,maxVal,minLoc,maxLoc) = cv2.minMaxLoc(corr)
            x=maxLoc[0];y=maxLoc[1]
            if (x-wl>0 and y-hl>0 and x+wr<corr.shape[1] and y+hr<corr.shape[0]):
                # remove correlation maximum
                roi=np.zeros([h,w],np.uint8)
                corr[y-hl:y+hr,x-wl:x+wr]=roi
                #create rectangle
                b=[x,y,w,h]
                borg = [i / scale for i in b]
                Im.Topcorr.append(borg)  
            else:
                corr[y,x]=0
            n=n+1  
                
Im1=cv2.imread('/home/bernifoellmer/Studium/SearchPartPython/SearchPartPython/SearchPartPython/SearchPartPython/data/SOT223_images/SAM_0593.JPG')
Im2=cv2.imread('/home/bernifoellmer/Studium/SearchPartPython/SearchPartPython/SearchPartPython/SearchPartPython/data/SOT223_images/SAM_0594.JPG')
Im3=cv2.imread('/home/bernifoellmer/Studium/SearchPartPython/SearchPartPython/SearchPartPython/SearchPartPython/data/SOT223_images/SAM_0613.JPG')
Im4=cv2.imread('/home/bernifoellmer/Studium/SearchPartPython/SearchPartPython/SearchPartPython/SearchPartPython/data/SOT223_images/SAM_0636.JPG')
Im5=cv2.imread('/home/bernifoellmer/Studium/SearchPartPython/SearchPartPython/SearchPartPython/SearchPartPython/data/SOT223_images/SAM_0665.JPG')
Im6=cv2.imread('/home/bernifoellmer/Studium/SearchPartPython/SearchPartPython/SearchPartPython/SearchPartPython/data/SOT223_images/SAM_0698.JPG')
images=list()
images.append(Im1)
images.append(Im2)
images.append(Im3)
images.append(Im4)
images.append(Im5)
images.append(Im6)

filename="/home/bernifoellmer/Studium/SearchPartPython/SearchPartPython/SearchPartPython/SearchPartPython/data/SOT223.zip"
Comp=SPM.Component(None,filename)

corrcomponent(Comp,images)

