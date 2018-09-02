# TrainModel.py
import cv2
import numpy as np
from BGDataGenerator import BGDataProvider

#from unet import Unet, Trainer
#import sys
#sys.path.append('H:\\Projects\\SearchPartPython\\SearchPartPython\\SearchPart\\src\\SearchPart\\unet')

#import image_gen
from unet import unet
#import util

import matplotlib.pyplot as plt
import matplotlib

class DLModel(object): 
    
    modelname = 'CNN'     
    generator = None
    path = None
    net = None
    prediction = None
    
    def init(self, nx, ny):
        #nx = 572
        #ny = 572
        
        #generator = image_gen.GrayScaleDataProvider(nx, ny, cnt=20)
        self.generator = BGDataProvider(nx, ny, cnt=20)       
        x_test, y_test = self.generator(1)
        
        fig, ax = plt.subplots(1,2, sharey=True, figsize=(8,4))
        ax[0].imshow(x_test[0,...,0], aspect="auto")
        ax[1].imshow(y_test[0,...,1], aspect="auto")
        
    
    def train(self):
        self.net = unet.Unet(channels=self.generator.channels, n_class=self.generator.n_class, layers=3, features_root=16)       
        trainer = unet.Trainer(self.net, optimizer="momentum", opt_kwargs=dict(momentum=0.2))       
        self.path = trainer.train(self.generator, "./unet_trained", training_iters=20, epochs=10, display_step=2)
        
    def test(self):
        x_test, y_test = self.generator(1)        
        self.prediction = self.net.predict("./unet_trained/model.cpkt", x_test)
        
        