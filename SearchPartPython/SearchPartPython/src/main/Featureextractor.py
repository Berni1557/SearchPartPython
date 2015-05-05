#!/usr/bin/env python
# Featureextracor
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
    path_pca=None
    
    # init Featureextracor
    def __init__(self,numHist,numSeg,MAX_COMPONENTS,ks_pca,numFreq,seg_threshold,path_pca):
        self.numHist=numHist    # Number of histogram features
        self.numSeg=numSeg      # Number of segment features
        self.MAX_COMPONENTS=MAX_COMPONENTS  # Number of PCs
        self.ks_pca=ks_pca      # Kernel size of LOG kernel for edge detection in PCA featureextraction
        self.numFreq=numFreq    # Number of frequency features
        self.seg_threshold=seg_threshold;   # segmentation threshold of region growing approach
        self.path_pca=path_pca;     # path of PCs from apriori PCA feature extraction
    
    # Histogram features
    def generate_histogram(self,mode,images,featurenum):
        if mode=='predict':
            if featurenum is None:
                featuresAll=list()
                for Im in images:
                    Ihsv = cv2.cvtColor(Im,cv2.COLOR_BGR2HSV)   # rgb to hsv
                    h,s,v = cv2.split(Ihsv)   # split hsv in channels
                    bins = np.linspace(0, 256, self.numHist+1)  # create bins (bin-edges)
                    N1,_ = np.histogram(h,bins)     # create histogram of h channel
                    N2,_ = np.histogram(s,bins)     # create histogram of s channel
                    N3,_ = np.histogram(v,bins)     # create histogram of v channel
                    N=np.concatenate((N1,N2,N3),axis=0)     # concatenate histogram features
                    featuresAll.append(N)
                return featuresAll
            else:
                featuresAll=list()
                for Im in images:
                    Ihsv = cv2.cvtColor(Im,cv2.COLOR_BGR2HSV)   # rgb to hsv
                    h,s,v = cv2.split(Ihsv)   # split hsv in channels
                    bins = np.linspace(0, 256, self.numHist+1)  # create bins (bin-edges)
                    N=[];
                    b=len(bins)-1
                    for fn in featurenum:
                        if fn<b:                            # create histogram of h channel
                            binsind=[bins[fn],bins[fn+1]]
                            Ni,_ = np.histogram(h,binsind)
                            #N.append(Ni[0])
                            #N=[N,Ni[0]]
                            N=np.concatenate((N,Ni),axis=0)
                        elif fn>=b and fn<b*2:              # create histogram of s channel
                            binsind=[bins[fn-b],bins[fn-b+1]]
                            Ni,_ = np.histogram(s,binsind)   
                            #N=[N,Ni[0]]
                            N=np.concatenate((N,Ni),axis=0)  
                            #N.append(Ni[0])  
                        elif fn>=b*2 and fn<3*b:            # create histogram of v channel
                            binsind=[bins[fn-2*b],bins[fn-2*b+1]]
                            Ni,_ = np.histogram(v,binsind)
                            #N=[N,Ni[0]]
                            N=np.concatenate((N,Ni),axis=0) # concatenate histogram features
                    featuresAll.append(N)
                return featuresAll              
        else:
            return False
    # Segment features    
    def generate_segment(self,mode,images,featurenum):
        if mode=='predict':
            if featurenum is None:
                featuresAll=list()
                num_x=self.numSeg   # number of x coordinats
                num_y=self.numSeg   # number of y coordinats
                for Iin in images:
                    featuresIm=list()
                    I1=Iin.astype(double)
                    height, width, _ = Iin.shape
                    step_x=round((width/num_x)-0.5)     # step in x direction
                    step_y=round((height/num_y)-0.5)    # step in y direction
                    x_vec = np.linspace(round(step_x/2), width-round(step_x/2), num_x)      # vector in x direction
                    y_vec = np.linspace(round(step_y/2), height-round(step_y/2), num_y)     # vector in y direction
                    
                    featuresIm=[]
                    # create segment with region growing in each coordinat sx,sy
                    for sx in x_vec:
                        for sy in y_vec:
                                            
                            G=np.zeros((height,width),dtype=np.uint8)
                            I2=G.astype(double)
            
                            rgrowmod.rgrow_func(I1,I2,sx,sy,self.seg_threshold) # region growing in c++
                            
                            I1o = I1.astype(np.uint8)
                            I2o = I2.astype(np.uint8)
            
                            _,thr = cv2.threshold(I2o, 127, 1, cv2.THRESH_BINARY)   # binarize image
                # load component
    
    # create mean image
    
    # convert from rgb to hsv
    
    # convert image from rgb to hsv
    
    # correlation
    
    # filter position by threshold
    
    # compute correlation positions
    

                            contours, _ = cv2.findContours(thr, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)  # find segment contour
                            # compute segment features
                            c=contours[0]
                            rect = cv2.boundingRect(c)
                            mean_val = cv2.mean(I1o,mask = thr)
                            featuresSeg=[rect[0]+(rect[2]/2),rect[1]+(rect[3]/2),rect[2],rect[3],mean_val[0],mean_val[1],mean_val[2]];  # 7 segment features (centroid x, centroid y, height, width, mean h channel, mean s channel, mean v channel
                            featuresIm=np.concatenate((featuresIm,featuresSeg),axis=0)  # concatenate histogram features
                            
                    featuresAll.append(featuresIm)
                return featuresAll
            else:
                featuresAll=list()
                num_x=self.numSeg   # number of x coordinats
                num_y=self.numSeg   # number of y coordinats
                for Iin in images:
                    featuresIm=list()
                    I1=Iin.astype(double)
                    height, width, _ = Iin.shape
                    step_x=round((width/num_x)-0.5)     # step in x direction
                    step_y=round((height/num_y)-0.5)    # step in y direction
                    x_vec = np.linspace(round(step_x/2), width-round(step_x/2), num_x)  # vector in x direction
                    y_vec = np.linspace(round(step_y/2), height-round(step_y/2), num_y) # vector in y direction
                    k=0
                    for sx in x_vec:
                        for sy in y_vec:
                            if (k in featurenum):   # check if feature in included in featurenum
                                                
                                G=np.zeros((height,width),dtype=np.uint8)
                                I2=G.astype(double)
                                
                                rgrowmod.rgrow_func(I1,I2,sx,sy,self.seg_threshold)     # region growing in c++
                                
                                I1o = I1.astype(np.uint8)
                                I2o = I2.astype(np.uint8)
                
                                _,thr = cv2.threshold(I2o, 127, 1, cv2.THRESH_BINARY)   # binarize image
                
                                contours, _ = cv2.findContours(thr, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)  # find segment contour
                
                                c=contours[0]
                                rect = cv2.boundingRect(c)
                                mean_val = cv2.mean(I1o,mask = thr)
                                
                                featuresSeg=[rect[0]+(rect[2]/2),rect[1]+(rect[3]/2),rect[2],rect[3],mean_val[0],mean_val[1],mean_val[2]];  # 7 segment features (centroid x, centroid y, height, width, mean h channel, mean s channel, mean v channel
                                featuresIm=np.concatenate((featuresIm,featuresSeg),axis=0)  # concatenate histogram features
                            k=k+1 
                    featuresAll.append(featuresIm)
                return featuresAll
        else:
            return False
    # PCA features    
    def generate_pca(self,mode,images,featurenum):
        if mode=='predict':
            eigenvectors=np.load(self.path_pca+'eigenvectors.npy')  # load eigenvectors
            eigenmean=np.load(self.path_pca+'eigenmean.npy')        # load eigenmean
            (s1,s2,_)=images[0].shape
            matrix_train=np.zeros((s1*s2,1),np.float32)
            err=None
            if (featurenum is None or featurenum[0]==0):
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

                    # reshape data
                    imgvector = Ilog.reshape(s1*s2,1)
                    #imgvector=np.transpose(data)
                    matrix_train = np.hstack((matrix_train, imgvector))
                
                matrix_train=matrix_train[:,1:]    
                # compute reconstruction error
                matrix_train=np.transpose(matrix_train)
                proj=cv2.PCAProject(matrix_train, eigenmean, eigenvectors)
                back=cv2.PCABackProject(proj, eigenmean, eigenvectors)
                # compute reconstruction error as feature
                err=np.sum(abs(matrix_train-back),axis=1)
                featuresAll=err      
                return featuresAll
            else:
                return False
            
        elif mode=='apriori':
            (s1,s2,_)=images[0].shape
            matrix_train=np.zeros((s1*s2,1),np.float32) # create matrix with a zero line  
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
                    # LoG filter
                    Igauss = cv2.GaussianBlur(Igray,(self.ks_pca,self.ks_pca),0.5)
                    Ilog = cv2.Laplacian(Igauss, cv2.CV_32F, ksize = self.ks_pca)
                    # normalize Ilog
                    minval=np.percentile(Ilog,1)
                    maxval=np.percentile(Ilog,99)
                    if minval != maxval:
                        Ilog -= minval
                        Ilog *= (255.0/(maxval-minval))
                    # reshape data
                    imgvector = Ilog.reshape(s1*s2,1)
                    #imgvector=np.transpose(data)
                    matrix_train = np.hstack((matrix_train, imgvector))
                
                matrix_train=matrix_train[:,1:]     # delete  zero line from matrix
                mean=np.mean(matrix_train, axis=1).reshape(1,-1)    # compute image mean
                matrix_train=np.transpose(matrix_train)
                
                (_, eigenvectors)=cv2.PCACompute(matrix_train, mean, maxComponents=self.MAX_COMPONENTS)  
                np.save(self.path_pca+'eigenvectors.npy', eigenvectors) # save eigenvectors
                np.save(self.path_pca+'eigenmean.npy', mean)    # save eigenmean
                return True
            else:
                return False
        else:
            return False
        
    # Frequency features    
    def generate_frequency(self,mode,images,featurenum):
        if mode=='predict':
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
                    fvr=np.real(fv[0])  # select real part
                    fvi=np.real(fv[0])  # select imaginary part
                    featuresIm=np.concatenate((fvr,fvi),axis=1)
                    featuresAll.append(featuresIm)
                return featuresAll
            else:
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
                    fvr=np.real(fv[0])  # select real part
                    fvi=np.real(fv[0])  # select imaginary part
                    featuresIm=np.concatenate((fvr,fvi),axis=1)
                    featuresAll.append(featuresIm[featurenum])
                return featuresAll
        else:
            return False


"""
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
#images.append(Im5)
#images.append(Im6)
s1=100
s2=50
#s1=50
#s2=25
k=0
for Iin in images:
    images[k]=cv2.resize(Iin, (s1, s2));
    k=k+1

imagest=list()
#imagest.append(Im1)
imagest.append(Im2)
imagest.append(Imn)
imagest.append(Im4)
#imagest.append(Im5)
imagest.append(Im6)
k=0
for Iin in imagest:
    imagest[k]=cv2.resize(Iin, (s1, s2));
    k=k+1
    
numHist=20;numSeg=5;MAX_COMPONENTS=50;ks_pca=11;numFreq=5;seg_threshold=30;
path_pca='/home/bernifoellmer/Studium/SearchPartPython/SearchPartPython/SearchPartPython/SearchPartPython/data/savedata/'
FG=Featureextracor(numHist,numSeg,MAX_COMPONENTS,ks_pca,numFreq,seg_threshold,path_pca)
#F=FG.generate_frequency(None, images,None)
F=FG.generate_frequency('predict', images, None)
F1=FG.generate_frequency('predict', images, [2,5])
#F1=FG.generate_histogram('predict', images, [0])
#F2=FG.generate_histogram('predict', images, [0,20])
print(F)
print(F1)
"""

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


