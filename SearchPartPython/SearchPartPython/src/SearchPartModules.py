# Searchpart library

from gi.repository import Gtk
from gi.repository import GdkPixbuf
import cv2
import numpy as np
from xml.dom.minidom import *
import sys
import time
import os
import zipfile
import shutil
#from mlabwrap import mlab


class Imagedata(object):
    improbabilitymap=list()
    image=np.zeros((3000,4000,3), np.uint8)
    def __init__(self,path):
        self.Imagepath=path
        self.Imagename=os.path.basename(path)
        self.image=cv2.imread(path)    
        self.Top=list()
        self.Right=list()
        self.Bottom=list()
        self.Left=list()
        
        self.Topcorr=list()
        self.Rightcorr=list()
        self.Bottomcorr=list()
        self.Leftcorr=list()
        print 'Start scaling'
        #sc=mlab.evalmat('scaleCircle',self.image)
        
        sc=60.0
        self.scale_factor=sc
        
        #self.scale_factor=sc[0][0]
        print 'End scaling'
    def corr(self,Compscale):
        sc=Compscale/self.scale_factor;
        dst=self.image.copy()
        cv2.resize(self.image, dst, 0, 0.5, 0.5, cv2.INTER_NEAREST);
        
        #Icorr=cv2.resize(self.image)
        
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

def create_dom(Component):
    
    dom = Document();
    base = dom.createElement('datasetstruct')
    dom.appendChild(base)
    
    node1 = dom.createElement('Creation_date')
    text1 = dom.createTextNode(str(Component.Creation_date))
    node1.appendChild(text1)
    dom.childNodes[0].appendChild(node1)
    
    node1 = dom.createElement('Componentname')
    text1 = dom.createTextNode(str(Component.Componentname))
    node1.appendChild(text1)
    dom.childNodes[0].appendChild(node1)    

    node1 = dom.createElement('ComponentID')
    text1 = dom.createTextNode(str(Component.ComponentID))
    node1.appendChild(text1)
    dom.childNodes[0].appendChild(node1)    
        
    node1 = dom.createElement('Componenthight')
    text1 = dom.createTextNode(str(Component.Componenthight))
    node1.appendChild(text1)
    dom.childNodes[0].appendChild(node1)
    
    node1 = dom.createElement('Componentwidth')
    text1 = dom.createTextNode(str(Component.Componentwidth))
    node1.appendChild(text1)
    dom.childNodes[0].appendChild(node1)  
    
    node1 = dom.createElement('Componentborder')
    text1 = dom.createTextNode(str(Component.Componentborder))
    node1.appendChild(text1)
    dom.childNodes[0].appendChild(node1)       
    
    node1 = dom.createElement('Componentrotation')
    text1 = dom.createTextNode(str(Component.Componentrotation))
    node1.appendChild(text1)
    dom.childNodes[0].appendChild(node1)           

    node1 = dom.createElement('Componentdescription')
    text1 = dom.createTextNode(str(Component.Componentdescription))
    node1.appendChild(text1)
    dom.childNodes[0].appendChild(node1)  

    node1 = dom.createElement('CompOCRdata')
    
    node2 = dom.createElement("OCRrotation")
    text2 = dom.createTextNode(str(Component.CompOCRdata.OCRrotation))
    node2.appendChild(text2)
    node1.appendChild(node2)
    node2 = dom.createElement("OCR")
    text2 = dom.createTextNode(str(Component.CompOCRdata.OCR))
    node2.appendChild(text2)
    node1.appendChild(node2)
    node2 = dom.createElement("OCRlib")
    text2 = dom.createTextNode(str(Component.CompOCRdata.OCRlib))
    node2.appendChild(text2)
    node1.appendChild(node2)
    node2 = dom.createElement("charsubset")
    text2 = dom.createTextNode(str(Component.CompOCRdata.charsubset))
    node2.appendChild(text2)
    node1.appendChild(node2)
            
    dom.childNodes[0].appendChild(node1)      
        
    for Im in Component.Imagelist:
        node1 = dom.createElement('Image')
        
        node2 = dom.createElement("Imagename")
        text2 = dom.createTextNode(Im.Imagename)
        node2.appendChild(text2)
        node1.appendChild(node2)

        node2 = dom.createElement("Imagepath")
        text2 = dom.createTextNode(Im.Imagepath)
        node2.appendChild(text2)
        node1.appendChild(node2)
                
        node2 = dom.createElement("Top")
        for c in Im.Top:
            node3 = dom.createElement("item")
            text3 = dom.createTextNode(str(c))
            node3.appendChild(text3)
            node2.appendChild(node3)
            node1.appendChild(node2)
            
        node2 = dom.createElement("Right")
        for c in Im.Right:
            node3 = dom.createElement("item")
            text3 = dom.createTextNode(str(c))
            node3.appendChild(text3)
            node2.appendChild(node3)
            node1.appendChild(node2)

        node2 = dom.createElement("Bottom")
        for c in Im.Bottom:
            node3 = dom.createElement("item")
            text3 = dom.createTextNode(str(c))
            node3.appendChild(text3)
            node2.appendChild(node3)
            node1.appendChild(node2)

        node2 = dom.createElement("Left")
        for c in Im.Left:
            node3 = dom.createElement("item")
            text3 = dom.createTextNode(str(c))
            node3.appendChild(text3)
            node2.appendChild(node3)
            node1.appendChild(node2)   
        dom.childNodes[0].appendChild(node1)                                   
        
               
    return dom

class ProgressBarWindow(Gtk.Window):

    def __init__(self):
        #Gtk.Window.__init__(self, title="ProgressBar Demo")
        self.set_window(Gtk.WindowType.POPUP)
        self.set_border_width(20)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        self.progressbar = Gtk.ProgressBar()
        vbox.pack_start(self.progressbar, True, True, 0)
        self.activity_mode = False

    def set_value(self, new_value):
        self.progressbar.set_fraction(new_value)
        
    def add_value(self, value):
        new_value=value + self.progressbar.get_fraction()
        self.progressbar.set_fraction(new_value)
        



def write_zipdb(Component, filepath):
    
    # Create  dom
    dom=create_dom(Component)
    st=dom.toprettyxml()
    
    #Create xml file
    filepathxml=filepath + '.xml'

    f = open(filepathxml, 'w')
    f.write(st)
    f.close()

    # Create zip path
    zipname=filepath + '.zip'
    zipf = zipfile.ZipFile(zipname, 'w')

    # Change to filepathxml folder and add xml-file to zip-file
    di, base_filename = os.path.split(filepathxml)
    os.chdir(di)
    zipf.write(base_filename)
    
    # Remove zip-file
    os.remove(filepathxml)
    
    # Add imagefiles to zipImagepath
    for Im in Component.Imagelist:
        di, base_filename = os.path.split(Im.Imagepath)
        os.chdir(di)
        zipf.write(base_filename) 
    zipf.close()
    
def read_zipdb(Component, filepath):
    di, base_filename = os.path.split(filepath)
    
    str1=base_filename.split('.')
    xmlname=str1[0] + '.xml'
    zipf = zipfile.ZipFile(filepath, 'r')
    zipf.extract(xmlname,di)
    
    str1=base_filename.split('.')
    
    xmlpath=di + '/'+ xmlname
    print xmlpath
    dom = parse(xmlpath)
    Component.dom = dom
    os.remove(xmlpath)
    
    st=dom.toprettyxml()
    print st
    
    
    Component.Creation_date=Component.dom.getElementsByTagName('Creation_date').item(0).firstChild.nodeValue
    
    if Component.dom.getElementsByTagName('Componentname').item(0).childNodes:
        Component.Componentname=Component.dom.getElementsByTagName('Componentname').item(0).firstChild.nodeValue
    if Component.dom.getElementsByTagName('ComponentID').item(0).childNodes:
        Component.ComponentID=Component.dom.getElementsByTagName('ComponentID').item(0).firstChild.nodeValue
    if Component.dom.getElementsByTagName('Componenthight').item(0).childNodes:
        Component.Componenthight=Component.dom.getElementsByTagName('Componenthight').item(0).firstChild.nodeValue
    if Component.dom.getElementsByTagName('Componentwidth').item(0).childNodes:
        Component.Componentwidth=Component.dom.getElementsByTagName('Componentwidth').item(0).firstChild.nodeValue
    if Component.dom.getElementsByTagName('Componentborder').item(0).childNodes:
        Component.border=Component.dom.getElementsByTagName('Componentborder').item(0).firstChild.nodeValue
    
    s=Component.dom.getElementsByTagName('Componentrotation').item(0).firstChild.nodeValue
    s1=s.split('[')
    s2=s1[1].split(']')
    str1=s2[0].split(',')
    b=list()
    for i in str1:
        i=i.replace(" ", "")
        b.append(str_to_bool(i))
    Component.Componentrotation=b
    
    if Component.dom.getElementsByTagName('Componentdescription').item(0).childNodes:
        Component.Componentdescription=Component.dom.getElementsByTagName('Componentdescription').item(0).firstChild.nodeValue

    if Component.dom.getElementsByTagName('OCR').item(0).childNodes:
        s=Component.dom.getElementsByTagName('OCR').item(0).firstChild.nodeValue
        Component.CompOCRdata.OCR=str_to_bool(s)
    if Component.dom.getElementsByTagName('OCRlib').item(0).childNodes:
        s=Component.dom.getElementsByTagName('OCRlib').item(0).firstChild.nodeValue
        Component.CompOCRdata.OCRlib=str_to_bool(s)
    if Component.dom.getElementsByTagName('charsubset').item(0).childNodes:
        s=Component.dom.getElementsByTagName('charsubset').item(0).childNodes[0].nodeValue
        Component.CompOCRdata.charsubset=s
        
    s=Component.dom.getElementsByTagName('OCRrotation').item(0).firstChild.nodeValue
    s1=s.split('[')
    s2=s1[1].split(']')
    str1=s2[0].split(',')
    b=list()
    for i in str1:
        i=i.replace(" ", "")
        b.append(str_to_bool(i))
    Component.CompOCRdata.OCRrotation=b
    
    """
    OCRnode=Component.dom.getElementsByTagName('CompOCRdata')
    
    print 'OCRnode: '
    print OCRnode
    print OCRnode.item(0).childNodes[0].nodeValue
    print OCRnode.item(0).childNodes[1].nodeValue
    print OCRnode.item(0).childNodes[2].nodeValue
    print OCRnode.item(0).childNodes[3].nodeValue
    #print OCRnode[0].childNodes[3].nodeValue
    
    Component.CompOCRdata.OCR=str_to_bool(OCRnode.getElementsByTagName('OCR').item(0).firstChild.nodeValue)
    Component.CompOCRdata.OCRlib=str_to_bool(OCRnode.getElementsByTagName('OCRlib').item(0).firstChild.nodeValue)
    Component.CompOCRdata.charsubset=OCRnode.getElementsByTagName('charsubset').item(0).firstChild.nodeValue
    
    s=OCRnode.getElementsByTagName('OCRrotation').item(0).firstChild.nodeValue
    s1=s.split('[')
    s2=s1[1].split(']')
    str1=s2[0].split(',')
    b=list()
    for i in str1:
        b.append(str_to_bool(i))
    Component.CompOCRdata.OCRrotation=b
    """
        
    images=Component.dom.getElementsByTagName('Image')
    for image in images:
        node=image.getElementsByTagName('Imagepath')
        Imagepath=node[0].childNodes[0].nodeValue
        
        print Imagepath
        Im=Imagedata(Imagepath)
        
        node=image.getElementsByTagName('Imagename')
        Im.Imagename=node[0].childNodes[0].nodeValue
        
        n1=image.getElementsByTagName('Top')
        for n2 in n1:
            it=n2.getElementsByTagName('item')
            for i in it:
                s=i.childNodes[0].nodeValue
                s1=s.split('[')
                s2=s1[1].split(']')
                str1=s2[0].split(',')
                b=list()
                for i in str1:
                    b.append(float(i))
                Im.Top.append(b)


        n1=image.getElementsByTagName('Right')
        for n2 in n1:
            it=n2.getElementsByTagName('item')
            for i in it:
                s=i.childNodes[0].nodeValue
                s1=s.split('[')
                s2=s1[1].split(']')
                str1=s2[0].split(',')
                b=list()
                for i in str1:
                    b.append(float(i))
                Im.Right.append(b)

        n1=image.getElementsByTagName('Bottom')
        for n2 in n1:
            it=n2.getElementsByTagName('item')
            for i in it:
                s=i.childNodes[0].nodeValue
                s1=s.split('[')
                s2=s1[1].split(']')
                str1=s2[0].split(',')
                b=list()
                for i in str1:
                    b.append(float(i))
                Im.Bottom.append(b)   
    
        n1=image.getElementsByTagName('Left')
        for n2 in n1:
            it=n2.getElementsByTagName('item')
            for i in it:
                s=i.childNodes[0].nodeValue
                s1=s.split('[')
                s2=s1[1].split(']')
                str1=s2[0].split(',')
                b=list()
                for i in str1:
                    b.append(float(i))
                Im.Left.append(b)
                      
        Component.Imagelist.append(Im)
        Component.Imagename.append(Im.Imagename)
    return Component
    
def str_to_bool(s):
    if s == 'True':
        return True
    elif s == 'False':
        return False
    else:
        raise ValueError # evil ValueError that doesn't tell you what the wrong value was


