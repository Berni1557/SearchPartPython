#!/usr/bin/env python

# example drawingarea.py

import pygtk
pygtk.require('2.0')
import gtk
import operator
import time
import string

from numpy import *

import cv
import cv2
import numpy as np
from cv2.cv import *



def convertCV2GTK(image):
    
    height, width, depth = image.shape
    imtemp = np.zeros((height, width, depth), np.uint8) 
    
    src = cv2.cv.fromarray(image)
    dst = cv2.cv.fromarray(imtemp)
    
    cv2.cv.CvtColor(src, dst, cv2.cv.CV_BGR2RGB)
    
    image_gtk = gtk.Image()
    img_pixbuf = gtk.gdk.pixbuf_new_from_data(dst.tostring(),gtk.gdk.COLORSPACE_RGB,False,8,width,height,width*depth) 
    image_gtk.set_from_pixbuf(img_pixbuf)
    return image_gtk

source=cv2.imread('/home/bernifoellmer/workspace/SearchPartPython_V01/lena.jpeg')



image=convertCV2GTK(source)
image.show()
window = gtk.Window(gtk.WINDOW_TOPLEVEL)
window.add(image)
window.show()

gtk.main()
