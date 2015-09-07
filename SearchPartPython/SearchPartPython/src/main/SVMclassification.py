#!/usr/bin/env python
# SVM classification
import numpy as np
#import time
from sklearn import svm

class SVMclassifier(object):
    traindata=None
    trainresults=None
    testdata=None
    testresults=None
    seg_threshold=None
    path_pca=None
    model=None
    
    # init Featureextracor
    def __init__(self,traindata,trainresults):
        self.traindata=traindata    # train samples
        self.trainresults=trainresults      # train sample results
        
    def train(self):
        SVM = svm.NuSVC()
        SVM.fit(self.traindata, self.trainresults)
        self.model=SVM
        return True
    
    def predict(self,X):
        Y=self.model.predict(X)
        return Y

X=np.array([[10,10],[100,100],[150,106],[11,9]])
Y=np.array([1,0,1,0])
Y=np.transpose(Y);
SVM=SVMclassifier(X,Y)
SVM.train()
Y=SVM.predict(X)
print(Y)
