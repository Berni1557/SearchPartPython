from gi.repository import Gtk
#from gi.repository.GdkPixbuf import Pixbuf
from gi.repository import GdkPixbuf
#!/usr/bin/env python

# example drawingarea.py
#import PIL
#import pygtk
#pygtk.require('2.0')
#import gtk
#import operator
#import time
#import string

#from numpy import *

#import cv
import cv2
import numpy as np
from cv2.cv import *

#import Image

class Handler:
    def onDeleteWindow(self, *args):
        Gtk.main_quit(*args)

    def onButtonPressed(self, CheckButton):
        print("Hello World!")
        
    def new_component_select_cb(self, item):
        print("Hello new!")
        
    def open_component_select_cb(self, item):
        print("Hello new!")

    def save_component_select_cb(self, item):
        print("Hello save!")

    def resize(self, item):
        print("Hello resize!")

    def resize1(self, item):
        print("Hello resize1!")

"""
def image2pixbuf(im): 
    #convert image from BRG to RGB (pnm uses RGB)
    im2 = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
     # get image dimensions (depth is not used)
    height, width, depth = im2.shape
    #pixl = GdkPixbuf.PixbufLoader.new_with_type('pnm')
    #GdkPixbuf.PixbufLoaderClass.
    # P6 is the magic number of PNM format, 
    # and 255 is the max color allowed, see [2]
    pixl.write("P6 %d %d 255 " % (width, height) + im2.tostring())
    pix = pixl.get_pixbuf()
    pixl.close()
    return pix
"""  
      
def convertCV2GTK(image,image_gtk):
    
    height, width, depth = image.shape
    #height=image.size[0]
    #width=image.size[1]
    #depth=3
    
    #source = image # source is numpy array 
    #bitmap = cv.CreateImageHeader((source.shape[1], source.shape[0]), cv.IPL_DEPTH_8U, 3)
    #cv.SetData(bitmap, source.tostring(), source.dtype.itemsize * 3 * source.shape[1])
    #imtemp = np.zeros((height, width, depth), np.uint8) 
    imtemp=np.copy(image)
    
    src = cv2.cv.fromarray(image)
    dst = cv2.cv.fromarray(imtemp)
    
    
    cv2.cv.CvtColor(src, dst, cv2.cv.CV_BGR2RGB)
    #dst=src;
    
    #image_gtk = Gtk.Image()
    
    
    str1=dst.tostring()  
    img_pixbuf = GdkPixbuf.Pixbuf.new_from_data(str1,GdkPixbuf.Colorspace.RGB,False,8,width,height,width*depth) 
    image_gtk.set_from_pixbuf(img_pixbuf)
    return image_gtk

 
builder = Gtk.Builder()

builder.add_from_file("/home/bernifoellmer/Studium/SearchPartPython/SearchPartPython/SearchPartPython/SearchPartPython/glade/SearchPartGlade.glade")

listb=builder.get_objects()
print(listb)
builder.connect_signals(Handler())

window = builder.get_object("window1")
image_gtk = builder.get_object("image")

#image.set_from_file("apple-red.png")
source=cv2.imread('/home/bernifoellmer/workspace/SearchPartPython_V01/lena.jpeg')
#image_file = Image.open('/home/bernifoellmer/workspace/SearchPartPython_V01/lena.jpeg')

im=convertCV2GTK(source,image_gtk)


im.show()
window.maximize()
window.show_all()
Gtk.main()




