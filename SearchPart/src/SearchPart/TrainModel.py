# TrainModel.py
import cv2
import numpy as np
from BGDataGenerator import BGDataProvider
import image_gen
import unet
import util

class DLModel(object): 
    
    modelname = 'CNN'     
    
    def init(nx, ny):
        #nx = 572
        #ny = 572
        
        #generator = image_gen.GrayScaleDataProvider(nx, ny, cnt=20)
        generator = BGDataProvider(nx, ny, cnt=20)       
        x_test, y_test = generator(1)
        
        fig, ax = plt.subplots(1,2, sharey=True, figsize=(8,4))
        ax[0].imshow(x_test[0,...,0], aspect="auto")
        ax[1].imshow(y_test[0,...,1], aspect="auto")
        
    
    def train():
        net = unet.Unet(channels=generator.channels, n_class=generator.n_class, layers=3, features_root=16)       
        trainer = unet.Trainer(net, optimizer="momentum", opt_kwargs=dict(momentum=0.2))       
        path = trainer.train(generator, "./unet_trained", training_iters=20, epochs=10, display_step=2)
        
    def test():
        x_test, y_test = generator(1)        
        prediction = net.predict("./unet_trained/model.cpkt", x_test)