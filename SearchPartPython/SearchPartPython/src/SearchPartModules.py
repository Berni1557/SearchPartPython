# Searchpart library

from gi.repository import Gtk
from gi.repository import GdkPixbuf
import cv2
import numpy as np

def convertCV2GTK(image):
    image_gtk = Gtk.Image()
    src = cv2.cv.fromarray(image)
    cv2.cv.SaveImage('/home/bernifoellmer/workspace/SearchPartPython_V01/tempimage.png', src)
    image_gtk.set_from_file("/home/bernifoellmer/workspace/SearchPartPython_V01/tempimage.png")
    return image_gtk


def convertCV2GTK_v01(image,image_gtk):
    
    height, width, depth = image.shape
    imtemp = np.zeros((height, width, depth), np.uint8) 
    
    src = cv2.cv.fromarray(image)
    dst = cv2.cv.fromarray(imtemp)
    
    cv2.cv.CvtColor(src, dst, cv2.cv.CV_RGB2BGR)
    #dst=src;
    
    #image_gtk = Gtk.Image()
    img_pixbuf = GdkPixbuf.Pixbuf.new_from_data(dst.tostring(),GdkPixbuf.Colorspace.RGB,False,8,width,height,width*depth) 
    image_gtk.set_from_pixbuf(img_pixbuf)


def Imagecopy(imageorg,imagecopy):    
    p=imageorg.get_pixbuf()   
    imagecopy.set_from_pixbuf(p)
