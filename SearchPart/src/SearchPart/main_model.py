# TrainModel.py
from __future__ import print_function, division, absolute_import, unicode_literals

import sys
sys.path.append('H:\\Projects\\SearchPartPython\\SearchPartPython\\SearchPart\\src\\SearchPart\\unet')

import cv2
import numpy as np
from enum import Enum
from BackgroundDetector import BackgroundDetector, BGClass

import numpy as np
import cv2
import scipy.misc
import math

from scipy.misc import imresize
from random import randint
from TrainModel import DLModel
from BGDataGenerator import BGDataGenerator
from unet.image_util import BaseDataProvider

import image_gen
from unet import unet
import util
import timeit


if __name__ == '__main__':
    
        
    model = DLModel()
    nx = 572
    ny = 572
    filepath = 'H:/Projects/SearchPartPython/SearchPartPython/SearchPart/data/background/BG12.zip'
    model.init(nx, ny, filepath)
    model.train()
    model.test()
    
    image = cv2.imread('H:/Projects/SearchPartPython/SearchPartPython/SearchPart/data/background/SAM_0595.JPG')
    image_pred = model.predict(image, 572, 572, 532, 532)
    
    cv2.imwrite('tmp1.png', image_pred)
    
    #cv2.namedWindow("Predict", cv2.WINDOW_NORMAL)
    #cv2.imshow('Predict', image_pred) 
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    
    cv2.namedWindow("Prediction", cv2.WINDOW_NORMAL)
    cv2.imshow('Prediction', image_pred) 
    cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
    cv2.imshow('Image', image) 
    cv2.waitKey(0)
    cv2.destroyAllWindows()
        
        
    start = timeit.default_timer()
    for i in range(10):
        model.test()
        imagedata = model.prediction
        image=imagedata[0,:,:,1]*255
        image8 = image.astype(np.uint8)
        cv2.namedWindow("Prediction", cv2.WINDOW_NORMAL)
        cv2.imshow('Prediction', image8) 
        cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
        cv2.imshow('Image', model.prediction_img) 
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    stop = timeit.default_timer()
    print('Time: ', stop - start)  
