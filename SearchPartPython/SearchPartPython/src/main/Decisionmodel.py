#!/usr/bin/env python

from matplotlib import pyplot as plt
import Featureextractor as FE
import Featureselector as FS
import SVMclassification as SVMCL
import SearchPartModules as SPM
from scipy import ndimage
import random
import numpy as np
import math
import time

class Decisionmodel(object):
    Correlationmodel=None
    Featureextractor=None
    Featureselector=None
    Classifier=None
    Ipos=list()
    Ineg=list()
    
    numHist=None
    numSeg=None
    path_pca=None
    MAX_COMPONENTS=None
    ks_pca=None
    numFreq=None
    p_pca=None
    seg_threshold=None
    
    
    def __init__(self,Comp,numHist,numSeg,seg_threshold,path_pca,MAX_COMPONENTS,ks_pca,p_pca,numFreq,p_train):
        #numHist=20;numSeg=5;MAX_COMPONENTS=50;ks_pca=11;numFreq=5;seg_threshold=30;
        #path_pca='/home/bernifoellmer/Studium/SearchPartPython/SearchPartPython/SearchPartPython/SearchPartPython/data/savedata/'
        self.numHist=numHist
        self.numSeg=numSeg
        self.seg_threshold=seg_threshold
        self.path_pca=path_pca
        self.MAX_COMPONENTS=MAX_COMPONENTS
        self.ks_pca=ks_pca
        self.p_pca=p_pca
        self.numFreq=numFreq
        self.p_train=p_train
        
        # extract component images
        ImageMask=list()
        for Im in Comp.Imagelist:
            image_mask=np.ones([Im.image.shape[0],Im.image.shape[1]],dtype=np.uint8)
            Top=Im.Top
            for b in Top:
                b = [int(round(n, 0)) for n in b]
                Isub=Im.image[b[1]:b[1]+b[3],b[0]:b[0]+b[2],:]
                self.Ipos.append(Isub) 
                image_mask[b[1]:b[1]+b[3],b[0]:b[0]+b[2]]=np.zeros([b[2],b[3]],dtype=np.uint8)
            Right=Im.Right
            for b in Right:
                b = [int(round(n, 0)) for n in b]
                Isub=Im.image[b[1]:b[1]+b[3],b[0]:b[0]+b[2],:]
                Isub = ndimage.rotate(Isub, 90)
                self.Ipos.append(Isub) 
                image_mask[b[1]:b[1]+b[3],b[0]:b[0]+b[2]]=np.zeros([b[3],b[2]],dtype=np.uint8)
                
                #plt.imshow(Isub, interpolation='nearest')
                #plt.show()
            Bottom=Im.Bottom
            for b in Bottom:
                b = [int(round(n, 0)) for n in b]
                Isub=Im.image[b[1]:b[1]+b[3],b[0]:b[0]+b[2]]
                Isub = ndimage.rotate(Isub, 180)
                self.Ipos.append(Isub) 
                image_mask[b[1]:b[1]+b[3],b[0]:b[0]+b[2]]=np.zeros([b[2],b[3]],dtype=np.uint8)
            Left=Im.Left
            for b in Left:
                b = [int(round(n, 0)) for n in b]
                Isub=Im.image[b[1]:b[1]+b[3],b[0]:b[0]+b[2]]
                Isub = ndimage.rotate(Isub, -90)
                self.Ipos.append(Isub) 
                image_mask[b[0]:b[0]+b[2],b[1]:b[1]+b[3]]=np.zeros([b[3],b[2]],dtype=np.uint8)
            ImageMask.append(image_mask) 
          
        # extract non-component images
        l1=len(self.Ipos)
        l2=len(Comp.Imagelist)
        num_comp_image=math.ceil(float(l1)/float(l2))
        
        im=0
        for Im in Comp.Imagelist:
            if not Im.scale_factor==False:
                image_mask=ImageMask[im]
                im=im+1
                n=0
                S=np.sum(image_mask)
                while (S>0) and (n<num_comp_image):
                    x=random.randrange(1,Im.image.shape[1])
                    y=random.randrange(1,Im.image.shape[0])
                    ROIout=False
                    x1=x-b[3]/2+1
                    if x1<1:
                        x1=1
                        ROIout=True
                    x2=x+b[3]/2+1
                    if x2>Im.image.shape[1]:
                        x2=Im.image.shape[1]
                        ROIout=True
                    y1=y-b[2]/2+1
                    if y1<1:
                        y1=1
                        ROIout=True
                    y2=y+b[3]/2+1
                    if y2>Im.image.shape[0]:
                        y2=Im.image.shape[0]
                        ROIout=True
                    image_mask[y1:y2,x1:x2]=np.zeros((y2-y1,x2-x1),dtype=np.uint8)
                    if not ROIout:
                        Isub=Im.image[y1:y2, x1:x2]
                        self.Ineg.append(Isub)
                        n=n+1
                    S=np.sum(image_mask)
                    
                
    def extract_all(self):   
        FEx=FE.Featureextractor(self.numHist,self.numSeg,self.MAX_COMPONENTS,self.ks_pca,self.numFreq,self.seg_threshold,self.path_pca)
        # create histrogam features
        start = time.time()
        F_hist_pos=FEx.generate_histogram("predict",self.Ipos,None)
        F_hist_neg=FEx.generate_histogram("predict",self.Ineg,None)
        end = time.time()
        print end-start
        # create segment features
        
        #F_seg_pos=FEx.generate_segment("predict",self.Ipos,None)
        #F_seg_neg=FEx.generate_segment("predict",self.Ineg,None)
        
        # create pca featuresN1 = [x / num_pix for x in N1]
        num_pos=int(round(self.p_pca*len(self.Ipos)))
        num_neg=int(round(self.p_pca*len(self.Ineg)))
        images_pos=self.Ipos[0:num_pos]
        images_neg=self.Ineg[0:num_neg]
        FEx.generate_pca("apriori",None,images_pos,images_neg)
        F_pca_pos=FEx.generate_pca("predict",self.Ipos[num_pos+1:],self.Ineg[num_neg+1:],None)
        F_pca_neg=FEx.generate_pca("predict",self.Ineg[num_neg+1:],None)
        # create frequency features
        F_freq_pos=FEx.generate_frequency(self,"predict",self.Ipos,None)
        F_freq_neg=FEx.generate_frequency(self,"predict",self.Ineg,None)
        
        num_train_pos=self.p_train*F_hist_pos.shape[0]
        num_train_neg=self.p_train*F_hist_neg.shape[0]
        # select histrogam features
        FSel=FS.Featureselector()
        X_hist=np.concatenate((F_hist_pos[1:num_train_pos], F_hist_neg[1:num_train_neg]), axis=0)
        Y_hist=np.concatenate(np.zeros(F_hist_neg.shape[0],dtype=np.uint8),np.ones(F_hist_pos.shape[0],dtype=np.uint8), axis=0)
        num_trees=100;num_Features=3;
        F_hist_sel=FSel.RFimportance(X_hist,Y_hist,num_trees,num_Features);  
        # select segment features
        X_seg=np.concatenate((F_seg_pos, F_seg_neg), axis=0)
        Y_seg=np.concatenate(np.zeros(F_seg_neg.shape[0],dtype=np.uint8),np.ones(F_seg_pos.shape[0],dtype=np.uint8), axis=0)
        num_trees=100;num_Features=10;
        F_seg_sel=FSel.RFimportance(X_seg,Y_seg,num_trees,num_Features);  
        # select pca features
        F_pca_sel=np.concatenate(F_pca_pos,F_pca_neg,axis=0)
        # select frequency features
        X_freq=np.concatenate((F_freq_pos, F_freq_neg), axis=0)
        Y_freq=np.concatenate(np.zeros(F_freq_neg.shape[0],dtype=np.uint8),np.ones(F_freq_pos.shape[0],dtype=np.uint8), axis=0)
        num_trees=100;num_Features=10;
        F_freq_sel=FSel.RFimportance(X_freq,Y_freq,num_trees,num_Features);          
        # select all features
        # !!! pca feature are missing !!!
        X_sel=np.concatenate((F_hist_sel, F_seg_sel,F_freq_sel), axis=0)
        Y_sel=np.concatenate((Y_hist,Y_seg,Y_freq), axis=0)
        num_trees=100;num_Features=20;
        F_sel=FSel.RFimportance(X_sel,Y_sel,num_trees,num_Features);
        
        # train component
        SVM=SVMCL.SVMclassifier(F_sel,Y_sel)
        SVM.train()
        
    def predict(self):     
        
        return True

Comp=SPM.Component(None,"/home/bernifoellmer/Studium/SearchPartPython/SearchPartPython/SearchPartPython/SearchPartPython/data/SOT223_test.zip")

numHist=10;numSeg=3;MAX_COMPONENTS=50;ks_pca=11;numFreq=5;seg_threshold=30;p_pca=0.3;p_train=0.5
path_pca='/home/bernifoellmer/Studium/SearchPartPython/SearchPartPython/SearchPartPython/SearchPartPython/data/savedata/'
DM=Decisionmodel(Comp,numHist,numSeg,seg_threshold,path_pca,MAX_COMPONENTS,ks_pca,p_pca,numFreq,p_train)
DM.extract_all()

   