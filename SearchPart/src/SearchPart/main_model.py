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
    BGGenerator = BGDataGenerator('BGDataGenerator01')
    BGGenerator.loadBGModel('H:/Projects/SearchPartPython/SearchPartPython/SearchPart/data/background/BG14.zip')
    N_train = 500
    N_test = 1
    N_valid = 1
    nx = 572 
    ny = 572 
    nimg = 12
    BGGenerator.createData(N_train, N_test, N_valid, nx, ny, nimg)
    
    model = DLModel()
    nx = 572
    ny = 572
    model.init(nx, ny)
    model.train()
    model.test()
        
    start = timeit.default_timer()
    for i in range(10):
        model.test()
        imagedata = model.prediction
        image=imagedata[0,:,:,1]*255
        image8 = image.astype(np.uint8)
        cv2.namedWindow("Prediction", cv2.WINDOW_NORMAL)
        cv2.imshow('Prediction', image8) 
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    stop = timeit.default_timer()
    print('Time: ', stop - start)  
