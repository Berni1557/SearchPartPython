#!/usr/bin/env python

import cv2
import numpy as np
#import time
from numpy import double
import rgrowmod

class Featureextracor(object):
    numHist=None
    numSeg=None
    ks_pca=None
    numFreq=None
    seg_threshold=None
    
    def __init__(self,numHist,numSeg,MAX_COMPONENTS,ks_pca,numFreq,seg_threshold):
        self.numHist=numHist
        self.numSeg=numSeg
        self.MAX_COMPONENTS=MAX_COMPONENTS
        self.ks_pca=ks_pca
        self.numFreq=numFreq
        self.seg_threshold=seg_threshold;
        
    def generate_histogram(self,mode,images,featurenum):
        if mode=='predict':
            if featurenum is None:
                featuresAll=list()
                for Im in images:
                    h,s,v = cv2.split(Im)
                    bins = np.linspace(0, 256, self.numHist+1)
                    N1,_ = np.histogram(h,bins)
                    N2,_ = np.histogram(s,bins)
                    N3,_ = np.histogram(v,bins)
                    N=np.concatenate((N1,N2,N3),axis=0)
                    featuresAll.append(N)
                return featuresAll
            else:
                featuresAll=list()
                for Im in images:
                    h,s,v = cv2.split(Im)
                    bins = np.linspace(0, 256, self.numHist+1)
                    N=[];
                    b=len(bins)-1
                    for fn in featurenum:
                        if fn<b:
                            binsind=[bins[fn],bins[fn+1]]
                            Ni,_ = np.histogram(h,binsind)
                            #N.append(Ni[0])
                            #N=[N,Ni[0]]
                            N=np.concatenate((N,Ni),axis=0)
                        elif fn>=b and fn<b*2:
                            binsind=[bins[fn-b],bins[fn-b+1]]
                            Ni,_ = np.histogram(s,binsind)   
                            #N=[N,Ni[0]]
                            N=np.concatenate((N,Ni),axis=0)  
                            #N.append(Ni[0])  
                        elif fn>=b*2 and fn<3*b:
                            binsind=[bins[fn-2*b],bins[fn-2*b+1]]
                            Ni,_ = np.histogram(v,binsind)
                            #N=[N,Ni[0]]
                            N=np.concatenate((N,Ni),axis=0)
                    featuresAll.append(N)
                return featuresAll              

    def generate_segment(self,mode,images,featurenum):
        if mode=='predict':
            if featurenum is None:
                featuresAll=list()
                num_x=self.numSeg 
                num_y=self.numSeg
                for Iin in images:
                    featuresIm=list()
                    I1=Iin.astype(double)
                    height, width, _ = Iin.shape
                    step_x=round((width/num_x)-0.5)
                    step_y=round((height/num_y)-0.5)
                    x_vec = np.linspace(round(step_x/2), width-round(step_x/2), num_x)
                    y_vec = np.linspace(round(step_y/2), height-round(step_y/2), num_y)
                    
                    #Iin = cv2.imread("/home/bernifoellmer/Studium/SearchPartPython/SearchPartPython/SearchPartPython/SearchPartPython/data/T.JPG")
                    featuresIm=[]
                    for sx in x_vec:
                        for sy in y_vec:
                                            
                            G=np.zeros((height,width),dtype=np.uint8)
                            I2=G.astype(double)
            
                            rgrowmod.rgrow_func(I1,I2,sx,sy,self.seg_threshold)
                            
                            I1o = I1.astype(np.uint8)
                            I2o = I2.astype(np.uint8)
            
                            _,thr = cv2.threshold(I2o, 127, 1, cv2.THRESH_BINARY)
            
                            contours, _ = cv2.findContours(thr, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            
                            c=contours[0]
                            rect = cv2.boundingRect(c)
                            mean_val = cv2.mean(I1o,mask = thr)
                            featuresSeg=[rect[0]+(rect[2]/2),rect[1]+(rect[3]/2),rect[2],rect[3],mean_val[0],mean_val[1],mean_val[2]];
                            featuresIm=np.concatenate((featuresIm,featuresSeg),axis=0)
                            
                    featuresAll.append(featuresIm)
                return featuresAll
            else:
                featuresAll=list()
                num_x=self.numSeg 
                num_y=self.numSeg
                for Iin in images:
                    featuresIm=list()
                    I1=Iin.astype(double)
                    height, width, _ = Iin.shape
                    step_x=round((width/num_x)-0.5)
                    step_y=round((height/num_y)-0.5)
                    x_vec = np.linspace(round(step_x/2), width-round(step_x/2), num_x)
                    y_vec = np.linspace(round(step_y/2), height-round(step_y/2), num_y)
                    k=0
                    for sx in x_vec:
                        for sy in y_vec:
                            if (next((i for i in featurenum if i==k), None)):
                                                
                                G=np.zeros((height,width),dtype=np.uint8)
                                I2=G.astype(double)
                                
                                rgrowmod.rgrow_func(I1,I2,sx,sy,self.seg_threshold)
                                
                                I1o = I1.astype(np.uint8)
                                I2o = I2.astype(np.uint8)
                
                                _,thr = cv2.threshold(I2o, 127, 1, cv2.THRESH_BINARY)
                
                                contours, _ = cv2.findContours(thr, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
                
                                c=contours[0]
                                rect = cv2.boundingRect(c)
                                mean_val = cv2.mean(I1o,mask = thr)
                                
                                featuresSeg=[rect[0],rect[1],rect[2],rect[3],mean_val[0],mean_val[1],mean_val[2]];
                                featuresIm=np.concatenate((featuresIm,featuresSeg),axis=0)
                            k=k+1 
                    featuresAll.append(featuresIm)
                return featuresAll

    def generate_pca(self,mode,images):
        
        path='/home/bernifoellmer/Studium/SearchPartPython/SearchPartPython/SearchPartPython/SearchPartPython/data/savedata/'
        if mode=='predict':
            eigenvectors=np.load(path+'eigenvectors.npy') 
            eigenmean=np.load(path+'eigenmean.npy') 
            (s1,s2,_)=images[0].shape
            matrix_train=np.zeros((s1*s2,1),np.float32)
            err=None
            for Iin in images:
                # rgb to gray
                Igray = cv2.cvtColor(Iin, cv2.COLOR_RGB2GRAY )
                Igray = Igray.astype(np.float)
                # normalize image
                minval=np.percentile(Igray,1)
                maxval=np.percentile(Igray,99)
                if minval != maxval:
                    Igray -= minval
                    Igray *= (255.0/(maxval-minval))
                # LoG filter
                Igauss = cv2.GaussianBlur(Igray,(self.ks_pca,self.ks_pca),0.5)
                Ilog = cv2.Laplacian(Igauss, cv2.CV_64F, ksize = self.ks_pca)
                
                
                # normalize Ilog
                minval=np.percentile(Ilog,1)
                maxval=np.percentile(Ilog,99)
                if minval != maxval:
                    Ilog -= minval
                    Ilog *= (255.0/(maxval-minval))
                #Ishow = Ilog.astype(np.uint8)
                #cv2.imshow('win1',Ishow)
                #cv2.waitKey()
                
                
                # reshape data
                imgvector = Ilog.reshape(s1*s2,1)
                #imgvector=np.transpose(data)
                matrix_train = np.hstack((matrix_train, imgvector))
            
            matrix_train=matrix_train[:,1:]    
            # compute reconstruction error
            matrix_train=np.transpose(matrix_train)
            proj=cv2.PCAProject(matrix_train, eigenmean, eigenvectors)
            back=cv2.PCABackProject(proj, eigenmean, eigenvectors)

            err=np.sum(abs(matrix_train-back),axis=1)
            featuresAll=err      
            return featuresAll
        elif mode=='apriori':
            (s1,s2,_)=images[0].shape
            matrix_train=np.zeros((s1*s2,1),np.float32)  
            for Iin in images:
                # rgb to gray
                Igray = cv2.cvtColor( Iin, cv2.COLOR_RGB2GRAY)
                Igray = Igray.astype(np.float)
                # normalize image
                minval=np.percentile(Igray,1)
                maxval=np.percentile(Igray,99)
                if minval != maxval:
                    Igray -= minval
                    Igray *= (255.0/(maxval-minval))
                
                # LoG filter
                Igauss = cv2.GaussianBlur(Igray,(self.ks_pca,self.ks_pca),0.5)
                Ilog = cv2.Laplacian(Igauss, cv2.CV_32F, ksize = self.ks_pca)
                
                # normalize Ilog
                minval=np.percentile(Ilog,1)
                maxval=np.percentile(Ilog,99)
                if minval != maxval:
                    Ilog -= minval
                    Ilog *= (255.0/(maxval-minval))
                #Ishow = Ilog.astype(np.uint8)
                #cv2.imshow('win1',Ishow)
                #cv2.waitKey()  
                 
                # reshape data
                imgvector = Ilog.reshape(s1*s2,1)
                #imgvector=np.transpose(data)
                matrix_train = np.hstack((matrix_train, imgvector))
            
            matrix_train=matrix_train[:,1:]    
                     
            mean=np.mean(matrix_train, axis=1).reshape(1,-1)
            matrix_train=np.transpose(matrix_train)
            
            (_, eigenvectors)=cv2.PCACompute(matrix_train, mean, maxComponents=self.MAX_COMPONENTS)  
            np.save(path+'eigenvectors.npy', eigenvectors)
            np.save(path+'eigenmean.npy', mean)
            return 1
        else:
            return 0
        
        
    def generate_frequency(self,mode,images,featurenum):
        featuresAll=list()
        if featurenum is None:
            for Iin in images:
                # rgb to gray
                Igray = cv2.cvtColor( Iin, cv2.COLOR_RGB2GRAY)
                Igray = Igray.astype(np.float)
                # normalize image
                minval=np.percentile(Igray,1)
                maxval=np.percentile(Igray,99)
                if minval != maxval:
                    Igray -= minval
                    Igray *= (255.0/(maxval-minval))
                # compute fft
                f=np.fft.fft2(Igray)
                fn=f[0:self.numFreq,0:self.numFreq]
                fv = fn.reshape(1,self.numFreq*self.numFreq)
                fvr=np.real(fv)
                fvi=np.real(fv)
                featuresIm=np.concatenate((fvr,fvi),axis=1)
                featuresAll.append(featuresIm)
            return featuresAll
        else:
            for Iin in images:
                # rgb to gray
                Igray = cv2.cvtColor( Iin, cv2.COLOR_RGB2GRAY)
                Igray = Igray.astype(np.float)
                f=np.fft.fft2(Igray)
                fn=f[0:self.numFreq,0:self.numFreq]
                fv = fn.reshape(1,self.numFreq*self.numFreq)
                fvr=np.real(fv)
                fvi=np.real(fv)
                featuresIm=np.concatenate((fvr,fvi),axis=1)
                featuresAll.append(featuresIm[0,featurenum])
            return featuresAll


 
Im1=cv2.imread('/home/bernifoellmer/Studium/SearchPartPython/SearchPartPython/SearchPartPython/SearchPartPython/data/Widerstand/W1.png')
Im2=cv2.imread('/home/bernifoellmer/Studium/SearchPartPython/SearchPartPython/SearchPartPython/SearchPartPython/data/Widerstand/W2.png')
Im3=cv2.imread('/home/bernifoellmer/Studium/SearchPartPython/SearchPartPython/SearchPartPython/SearchPartPython/data/Widerstand/W3.png')
Im4=cv2.imread('/home/bernifoellmer/Studium/SearchPartPython/SearchPartPython/SearchPartPython/SearchPartPython/data/Widerstand/W4.png')
Im5=cv2.imread('/home/bernifoellmer/Studium/SearchPartPython/SearchPartPython/SearchPartPython/SearchPartPython/data/Widerstand/W5.png')
Im6=cv2.imread('/home/bernifoellmer/Studium/SearchPartPython/SearchPartPython/SearchPartPython/SearchPartPython/data/Widerstand/W6.png')

Imn=cv2.imread('/home/bernifoellmer/Studium/SearchPartPython/SearchPartPython/SearchPartPython/SearchPartPython/data/Widerstand/Wn.png')

#Im=cv2.resize(Im, (70, 35));

#Im1=cv2.imread('/home/bernifoellmer/Studium/SearchPartPython/SearchPartPython/SearchPartPython/SearchPartPython/data/T.JPG')
images=list()
images.append(Im1)
#images.append(Im2)
#images.append(Im3)
#images.append(Im4)
#images.append(Im6)
s1=100
s2=50
k=0
for Iin in images:
    images[k]=cv2.resize(Iin, (s1, s2));
    k=k+1

numHist=20;numSeg=5;MAX_COMPONENTS=50;ks_pca=11;numFreq=5;seg_threshold=30;
FG=Featureextracor(numHist,numSeg,MAX_COMPONENTS,ks_pca,numFreq,seg_threshold)
#F=FG.generate_frequency(None, images,None)
#F=FG.generate_segment('predict', images, None)
F1=FG.generate_segment('predict', images, [0])
#F1=FG.generate_histogram('predict', images, [0])
#F2=FG.generate_histogram('predict', images, [0,20])
#print(F)
print(F1)
#print(F1)
#print(F2)
"""
start = time.time()
for i in range(1):
    FG.generate_frequency(None, images)
end = time.time()
print end - start
"""


"""
s1=70
s2=40
k=0
for Iin in images:
    images[k]=cv2.resize(Iin, (s1, s2));
    k=k+1

FG=Featureextracor(None)    
err=feateures=FG.generate_pca(None,images)
print err



images1=list()
images1.append(Imn)
k=0
for Iin in images1:
    images1[k]=cv2.resize(Iin, (s1, s2));
    k=k+1
err1=feateures=FG.generate_pca('predict',images1)
print err1

images2=list()
images2.append(Im5)
#images2.append(Im6)
k=0
for Iin in images2:
    images2[k]=cv2.resize(Iin, (s1, s2));
    k=k+1
err2=feateures=FG.generate_pca('predict',images2)
print err2

images3=list()
images3.append(Im3)
k=0
for Iin in images3:
    images3[k]=cv2.resize(Iin, (s1, s2));
    k=k+1
err3=feateures=FG.generate_pca('predict',images3)
print err3

start = time.time()
for i in range(1000):
    err4=feateures=FG.generate_pca('predict',images2)
end = time.time()
print end - start
"""

"""
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


