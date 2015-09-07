#!/usr/bin/env python
# Featureselector class
import cv2
import numpy as np
#import time
from numpy import double
import rgrowmod
from sklearn.ensemble import RandomForestClassifier

class Featureselector(object):
    
    def __init__(self,num_Features):
        return None
    
    def RFimportance(self,X,Y,num_trees,num_Features):    
        # compute RF importance
        forest = RandomForestClassifier(n_estimators=num_trees,criterion='gini')
        forest.fit(X, Y)
        importances = forest.feature_importances_
        indices=np.argsort(importances)
        FeaturesOut=X[:, indices[1:num_Features]]
        return FeaturesOut
    
    def Fscore(self,labels,samples):
        data_num=float(len(samples))
        p_num = {} #key: label;  value: data num
        sum_f = [] #index: feat_idx;  value: sum
        sum_l_f = {} #dict of lists.  key1: label; index2: feat_idx; value: sum
        sumq_l_f = {} #dict of lists.  key1: label; index2: feat_idx; value: sum of square
        F={} #key: feat_idx;  valud: fscore
        max_idx = -1
    
        ### pass 1: check number of each class and max index of features
        for p in range(len(samples)): # for every data point
            label=labels[p]
            point=samples[p]
    
            if label in p_num: p_num[label] += 1
            else: p_num[label] = 1
    
            for f in point.keys(): # for every feature
                if f>max_idx: max_idx=f
        ### now p_num and max_idx are set
    
        ### initialize variables
        sum_f = [0 for i in range(max_idx)]
        for la in p_num.keys():
            sum_l_f[la] = [0 for i in range(max_idx)]
            sumq_l_f[la] = [0 for i in range(max_idx)]
    
        ### pass 2: calculate some stats of data
        for p in range(len(samples)): # for every data point
            point=samples[p]
            label=labels[p]
            for tuple in point.items(): # for every feature
                f = tuple[0]-1 # feat index
                v = tuple[1] # feat value
                sum_f[f] += v
                sum_l_f[label][f] += v
                sumq_l_f[label][f] += v**2
        ### now sum_f, sum_l_f, sumq_l_f are done
    
        ### for each feature, calculate f-score
        eps = 1e-12
        for f in range(max_idx):
            SB = 0
            for la in p_num.keys():
                SB += (p_num[la] * (sum_l_f[la][f]/p_num[la] - sum_f[f]/data_num)**2 )
    
            SW = eps
            for la in p_num.keys():
                SW += (sumq_l_f[la][f] - (sum_l_f[la][f]**2)/p_num[la]) 
    
            F[f+1] = SB / SW
    
        return F


FS=Featureselector(3)
samples=np.array([[10,10],[100,100],[150,106],[11,9]])
labels=np.array([1,0,1,0])
labels=np.transpose(labels)
 
#FS.Fscore(labels, samples)        
ind=FS.RFimportance(samples,labels,100,10)
print(ind)