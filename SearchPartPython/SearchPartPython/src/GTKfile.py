#!/usr/bin/env python
from gi.repository import Gtk
from gi.repository import Gdk
import cv2
import SearchPartModules as SPM
from gi.repository import GdkPixbuf
from xml.dom.minidom import *
import numpy as np
import cairo
from StringIO import StringIO
import os
#from mlabwrap import mlab
import time
import zipfile
import math
from scipy import signal
from scipy import ndimage

class OCRdata(object):
    OCRrotation=[False,False,False,False]
    OCR=False
    OCRlib=False
    charsubset=''
        
class Component(object):
    Creation_date=''
    Componentname=''
    ComponentID=0
    Componenthight=0
    Componentwidth=0
    Componentborder=0
    Componentrotation=[False,False,False,False]
    Componentdescription=''
    CompOCRdata=OCRdata()
    Imagename=list()
    Imagelist=list()
    dom=''
    Componentmean=0
    
    def __init__(self, parent, filename,):
        if isinstance (filename, basestring):
            self.parent=parent
            self=SPM.read_zipdb(self, filename)
            self.parent.imagecounter.imagenumber=0;
            self.parent.imagecounter.imagenumber_max=len(self.Imagelist)-1;                                                 
        else:
            self.parent=parent
            self.Creation_date=time.strftime("%c")
            self.Componentname=''
            self.ComponentID=0
            #self.path=''
            self.Imagename=list()
            self.Top=list()
            self.Bottom=list()
            self.Left=list()
            self.Right=list()
            self.Componentrotation=[False,False,False,False]
    
    def create_mean(self):
        #self.Componentmean=0
        sz=self.scale_corr()
        size=[sz[0],sz[1],3]
        print 'size'
        print size
        k=0
        Componentmean=np.zeros(size, dtype=np.uint8)
        for Im in self.Imagelist:
            #imagesc = cv2.resize(Im.image, (self.parent.imsize[0], self.parent.imsize[1])) 
            for b in Im.Top:
                Imcomp = Im.image[int(b[1]):int(b[1]+b[3]), int(b[0]):int(b[0]+b[2])]
                Compcorr = cv2.resize(Imcomp,(size[0],size[1]))
                Componentmean=Componentmean+Compcorr
                k+=1
        self.Componentmean=Componentmean/k
        return Componentmean 
              
    def corr(self):
        Componentmean=self.create_mean()
        sc=self.scale_corr()
        sc_corr=sc[2]
        for Im in self.Imagelist:
            del Im.Topcorr[:]
            del Im.Rightcorr[:]
            del Im.Bottomcorr[:]
            del Im.Leftcorr[:]
            scale=sc_corr/Im.scale_factor
            imagesc = cv2.resize(Im.image, (int(Im.image.shape[0]*scale), int(Im.image.shape[1]*scale))) 
            thr = 0.2
            
                        
            # Top correlation
            Compcorr=Componentmean
            h=sc[1];hl=int(h/2);hr=h-hl;w=sc[0];wl=int(w/2);wr=w-wl
            corr = cv2.matchTemplate(imagesc,Compcorr,cv2.TM_CCOEFF_NORMED)
            (minVal,maxVal,minLoc,maxLoc) = cv2.minMaxLoc(corr)
            roi=np.zeros([h,w],np.uint8)
            while maxVal>thr:
                if (maxLoc[1]-hl>0 and maxLoc[0]-wr>0 and maxLoc[1]+hr<corr.shape[0] and maxLoc[0]+wr<corr.shape[1]):
                    corr[maxLoc[1]-hl:maxLoc[1]+hr,maxLoc[0]-wl:maxLoc[0]+wr]=roi
                    b=[maxLoc[1],maxLoc[0],h,w]
                    borg = [x / scale for x in b]
                    Im.Topcorr.append(borg)
                    (minVal,maxVal,minLoc,maxLoc) = cv2.minMaxLoc(corr)
                else:
                    corr[maxLoc[1],maxLoc[0]]=0
                    (minVal,maxVal,minLoc,maxLoc) = cv2.minMaxLoc(corr)
                    
            # Right correlation
            Compcorr = ndimage.rotate(Componentmean, 45)
            h=sc[0];hl=int(h/2);hr=h-hl;w=sc[1];wl=int(w/2);wr=w-wl
            corr = cv2.matchTemplate(imagesc,Compcorr,cv2.TM_CCOEFF_NORMED)
            (minVal,maxVal,minLoc,maxLoc) = cv2.minMaxLoc(corr)
            roi=np.zeros([h,w],np.uint8)
            while maxVal>thr:
                if (maxLoc[1]-hl>0 and maxLoc[0]-wr>0 and maxLoc[1]+hr<corr.shape[0] and maxLoc[0]+wr<corr.shape[1]):
                    corr[maxLoc[1]-hl:maxLoc[1]+hr,maxLoc[0]-wl:maxLoc[0]+wr]=roi
                    b=[maxLoc[1],maxLoc[0],h,w]
                    borg = [x / scale for x in b]
                    Im.Rightcorr.append(borg)
                    (minVal,maxVal,minLoc,maxLoc) = cv2.minMaxLoc(corr)
                else:
                    corr[maxLoc[1],maxLoc[0]]=0
                    (minVal,maxVal,minLoc,maxLoc) = cv2.minMaxLoc(corr)
                                        
        print 'corr done'
        self.parent.update_componentdata()
        
    def scale_corr(self):
        x=self.Componentwidth*self.Componenthight
        res=15*math.exp( -( x -1)*0.05 )+5;
        return [int(self.Componenthight*res),int(self.Componentwidth*res),res]

    def load_images(self):  
        #imsize=self.parent.imsize
        #k=0
        for s in self.Imagename:
            impath=self.path + s
            Im=SPM.Imagedata(impath)
            self.Imagelist.append(Im)
            #self.Imagelist.insert(k, Im)
            #k=k+1
            #imagecv = cv2.resize(imagecv, (imsize[0], imsize[1]))
                     
class Handler(object):
    
    def __init__(self, parent):
        self.parent = parent    # <= garbage-collector safe!
        
    def onDeleteWindow(self, *args):
        Gtk.main_quit(*args)
        
    def new_component_select_cb(self, item):
        self.parent.reset()
        
    def open_component_select_cb(self, item):
        fcd=Gtk.FileChooserDialog('Open...', None, Gtk.FileChooserAction.OPEN, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        response=fcd.run()
        if response == Gtk.ResponseType.OK:
            filename=fcd.get_filename()
            self.parent.DSComponent=Component(self.parent,filename)
            #SPM.read_zipdb(Component,filename)
            self.parent.update_componentdata()
        fcd.destroy()
        
        
    def save_component_select_cb(self, item):
        print("Hello save!")
        #dom=SPM.create_dom2(self.parent.DSComponent)
        #st=dom.toprettyxml()
        #print st
        fcd=Gtk.FileChooserDialog('Save as...', None, Gtk.FileChooserAction.SAVE, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_SAVE_AS, Gtk.ResponseType.OK))
        response=fcd.run()
        if response == Gtk.ResponseType.OK:
            filename=fcd.get_filename()
            SPM.write_zipdb(self.parent.DSComponent, filename)
        fcd.destroy()
        
    def height_changed_cb(self,item):
        if isfloat(item.get_text()):
            self.parent.DSComponent.Componenthight=float(item.get_text())
        
    def width_changed_cb(self,item):
        if isfloat(item.get_text()):
            self.parent.DSComponent.Componentwidth=float(item.get_text())
        
    def CompID_changed_cb(self,item):
        if isfloat(item.get_text()):
            self.parent.DSComponent.ComponentID=int(item.get_text())
        
    def Compborder_changed_cb(self,item):
        if isfloat(item.get_text()):
            self.parent.DSComponent.Componentborder=float(item.get_text())       
 
    def Compname_changed_cb(self,item):
        self.parent.DSComponent.Componentname=item.get_text()  
            
    def Comp_top_changed_cb(self,item):
        self.parent.DSComponent.Componentrotation[0]=item.get_active()       

    def Comp_right_changed_cb(self,item):
        self.parent.DSComponent.Componentrotation[1]=item.get_active() 

    def Comp_bottom_changed_cb(self,item):
        self.parent.DSComponent.Componentrotation[2]=item.get_active() 

    def Comp_left_changed_cb(self,item):
        self.parent.DSComponent.Componentrotation[3]=item.get_active() 

    def OCR_top_changed_cb(self,item):
        self.parent.DSComponent.CompOCRdata.OCRrotation[0]=item.get_active()       

    def OCR_right_changed_cb(self,item):
        self.parent.DSComponent.CompOCRdata.OCRrotation[1]=item.get_active() 

    def OCR_bottom_changed_cb(self,item):
        self.parent.DSComponent.CompOCRdata.OCRrotation[2]=item.get_active() 

    def OCR_left_changed_cb(self,item):
        self.parent.DSComponent.CompOCRdata.OCRrotation[3]=item.get_active()
         
    def OCR_changed_cb(self,item):
        self.parent.DSComponent.CompOCRdata.OCR=item.get_active() 

    def Octopart_changed_cb(self,item):
        self.parent.DSComponent.CompOCRdata.Octopart=item.get_active() 

    def charsubset_changed_cb(self,item):
        self.parent.DSComponent.CompOCRdata.charsubset=item.get_text()
                  
    def Compdescription_changed_cb(self,item):
        self.parent.DSComponent.Componentdescription=item.get_text()  
                        
    def selectbbox_changed_cb(self,item):
        print "cursor"
        #self.parent.selectbbox=item.get_active() 
        #self.parent.Cursor=Gdk.Cursor(Gdk.CursorType.CIRCLE)
        win = self.parent.drawarea.get_window()
        if item.get_active():
            cursor = Gdk.Cursor(Gdk.CursorType.HAND1)
            win.set_cursor(cursor)
        else:
            cursor = Gdk.Cursor(Gdk.CursorType.LEFT_PTR)
            win.set_cursor(cursor)
        self.parent.update_componentdata()
        #self.parent.windowbox.window.set_cursor(cursor)
        
    def deletebbox_changed_cb(self,item):
        print('deletebbox')  
        #self.parent.deletebbox=item.get_active()      
        
    def compmean_changed_cb(self,item):
        self.parent.selectbbox.set_active(True) 
        self.parent.DSComponent.corr()
        #self.parent.deletebbox=item.get_active() import Image
        
    def addimages_changed_cb(self,item):
        print('addimages')  
        fcd=Gtk.FileChooserDialog('Open...', None, Gtk.FileChooserAction.OPEN, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        fcd.set_select_multiple(True)
        #filenames = fcd.get_filenames()
        #print filenames
        response=fcd.run()
        if response == Gtk.ResponseType.OK:
            filenames=fcd.get_filenames()
            fcd.destroy()
            k=0
            for f in filenames:
                k=k+1
                Imname=os.path.basename(f)
                self.parent.DSComponent.Imagename.append(Imname)
                self.parent.DSComponent.Imagelist.append(SPM.Imagedata(f))
            self.parent.update_componentdata()
        
        
    def deleteimage_changed_cb(self,item):
        del self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber]
        self.parent.update_componentdata()
        
    def NEXT_clicked_cb(self,item):
        #print self.parent.imagecounter.imagenumber_max
        print self.parent.imagecounter.imagenumber
        if(self.parent.imagecounter.imagenumber<self.parent.imagecounter.imagenumber_max):
            self.parent.imagecounter.imagenumber=self.parent.imagecounter.imagenumber+1;
        print self.parent.imagecounter.imagenumber
        self.parent.update_componentdata()
        self.parent.drawarea.queue_draw()  

    def BACK_clicked_cb(self,item):
        if(self.parent.imagecounter.imagenumber>0):
            self.parent.imagecounter.imagenumber=self.parent.imagecounter.imagenumber-1;
        self.parent.update_componentdata()
    
    def drawingarea_motion_notify_event_cb(self,item,event):
        print event.x
        print 'motion' 
        
    def drawingarea_button_press_event_cb(self,item,event):
        print 'click'
        if(len(self.parent.DSComponent.Imagelist)>0):
            if self.parent.bboxrot[0]:  # Top
                hight=self.parent.DSComponent.Componenthight * self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].scale_factor
                width=self.parent.DSComponent.Componentwidth * self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].scale_factor
                h2=int(hight/2)
                w2=int(width/2)
                x=event.x/self.parent.scale
                y=event.y/self.parent.scale
                bbox=[x-h2,y-w2,hight,width]
                if(len(self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].Top)==0):
                    self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].Top.append(bbox)
                else:
                    bboxfound=False 
                    for b in self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].Top:
                        if (event.x>b[0] and event.x<b[0]+hight and event.y>b[1] and event.y<b[1]+width):
                            self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].Top.remove(b)
                            bboxfound=True
                    if bboxfound==False:
                        print 'bboxfound-false'
                        self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].Top.append(bbox)
                self.parent.drawarea.queue_draw()
            if self.parent.bboxrot[1]:  # Right
                width=self.parent.DSComponent.Componenthight * self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].scale_factor
                hight=self.parent.DSComponent.Componentwidth * self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].scale_factor
                h2=int(hight/2)
                w2=int(width/2)
                x=event.x/self.parent.scale
                y=event.y/self.parent.scale
                bbox=[x-h2,y-w2,hight,width]
                if(len(self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].Right)==0):
                    self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].Right.append(bbox)
                else:
                    bboxfound=False 
                    for b in self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].Right:
                        if (event.x>b[0] and event.x<b[0]+hight and event.y>b[1] and event.y<b[1]+width):
                            print
                            self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].Right.remove(b)
                            bboxfound=True
                    if bboxfound==False:
                        print 'bboxfound-false'
                        self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].Right.append(bbox)
                self.parent.drawarea.queue_draw()                    
            if self.parent.bboxrot[2]:  # Bottom
                hight=self.parent.DSComponent.Componenthight * self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].scale_factor
                width=self.parent.DSComponent.Componentwidth * self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].scale_factor
                h2=int(hight/2)
                w2=int(width/2)
                x=event.x/self.parent.scale
                y=event.y/self.parent.scale
                bbox=[x-h2,y-w2,hight,width]
                if(len(self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].Bottom)==0):
                    self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].Bottom.append(bbox)
                else:
                    bboxfound=False 
                    for b in self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].Bottom:
                        if (event.x>b[0] and event.x<b[0]+hight and event.y>b[1] and event.y<b[1]+width):
                            print
                            self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].Bottom.remove(b)
                            bboxfound=True
                    if bboxfound==False:
                        print 'bboxfound-false'
                        self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].Bottom.append(bbox)
                self.parent.drawarea.queue_draw()              
            if self.parent.bboxrot[3]:  # Left
                width=self.parent.DSComponent.Componenthight * self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].scale_factor
                hight=self.parent.DSComponent.Componentwidth * self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].scale_factor
                h2=int(hight/2)
                w2=int(width/2)
                x=event.x/self.parent.scale
                y=event.y/self.parent.scale
                bbox=[x-h2,y-w2,hight,width]
                if(len(self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].Left)==0):
                    self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].Left.append(bbox)
                else:
                    bboxfound=False 
                    for b in self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].Left:
                        if (event.x>b[0] and event.x<b[0]+hight and event.y>b[1] and event.y<b[1]+width):
                            print
                            self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].Left.remove(b)
                            bboxfound=True
                    if bboxfound==False:
                        print 'bboxfound-false'
                        self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].Left.append(bbox)
                self.parent.drawarea.queue_draw()                  

    def draw_callback (self, wid, cr):
        print len(self.parent.DSComponent.Imagelist)
        if len(self.parent.DSComponent.Imagelist)>0:
            print self.parent.imagecounter.imagenumber
            imagecv=self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].image
            imagecv = cv2.resize(imagecv, (self.parent.imsize[0], self.parent.imsize[1])) 
            imagegtk=SPM.convertCV2GTK(imagecv)
            p=imagegtk.get_pixbuf()
            Gdk.cairo_set_source_pixbuf(cr, p, 0, 0)
            cr.rectangle(0, 0, self.parent.imsize[0], self.parent.imsize[1])
            cr.fill()
        
            for borg in self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].Top:
                b = [x * self.parent.scale for x in borg]
                cr.set_source_rgb(255, 0, 0)
                cr.rectangle(b[0], b[1], b[2], b[3]);
                cr.stroke()

            for borg in self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].Right:
                b = [x * self.parent.scale for x in borg]
                cr.set_source_rgb(255, 255, 0)
                cr.rectangle(b[0], b[1], b[2], b[3]);
                cr.stroke()
                
            for borg in self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].Bottom:
                b = [x * self.parent.scale for x in borg]
                cr.set_source_rgb(0, 255, 0)
                cr.rectangle(b[0], b[1], b[2], b[3]);
                cr.stroke()
            for borg in self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].Left:
                b = [x * self.parent.scale for x in borg]
                cr.set_source_rgb(0, 0, 255)
                cr.rectangle(b[0], b[1], b[2], b[3]);
                cr.stroke()
                
            if self.parent.selectbbox.get_active():  
                for borg in self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].Topcorr:
                    b = [x * self.parent.scale for x in borg]
                    cr.set_source_rgb(255, 255, 255)
                    cr.rectangle(b[0], b[1], b[2], b[3]);
                    cr.stroke()                          
                for borg in self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].Rightcorr:
                    b = [x * self.parent.scale for x in borg]
                    cr.set_source_rgb(255, 255, 255)
                    cr.rectangle(b[0], b[1], b[2], b[3]);
                    cr.stroke()
                    
    
    def window1_key_press_event_cb(self,item,event):
        if(event.keyval==65362):
            print('top')
            self.parent.bboxrot=[True,False,False,False]
        elif(event.keyval==65363):
            print('right')
            self.parent.bboxrot=[False,True,False,False]
        elif(event.keyval==65364):
            print('bottom')
            self.parent.bboxrot=[False,False,True,False]
        elif(event.keyval==65361):
            print('left')
            self.parent.bboxrot=[False,False,False,True]
                                            
class imagecounter(object): 
    imagenumber=0     
    imagenumber_max=0;
    def tostring(self):
        if self.imagenumber_max>0:
            imstr=str(self.imagenumber+1) + " / " + str(self.imagenumber_max+1)
        else:
            imstr="0 / 0"
        return imstr
        
class DSclass(object):
    
    selectbbox=False
    deletebbox=False
    compmean=False
    addimages=False
    deleteimage=False
    DSComponent=Component(None,None)
    scale=0.2;
    imsize=[int(4000*scale),int(3000*scale)]
    bboxrot=[True,False,False,False]
    
    def __init__(self):
        print("Start")
        self.builder = Gtk.Builder()
        self.builder.add_from_file("/home/bernifoellmer/Studium/SearchPartPython/SearchPartPython/SearchPartPython/SearchPartPython/glade/SearchPartGlade.glade")
        self.builder.connect_signals(Handler(self))

        self.window = self.builder.get_object("window1")
        self.windowbox = self.builder.get_object("windowbox")
        self.height = self.builder.get_object("height")
        self.width = self.builder.get_object("width")
        self.CompID = self.builder.get_object("CompID")
        self.Compborder = self.builder.get_object("Compborder")
        self.Compname = self.builder.get_object("Compname")
        self.Comppath = self.builder.get_object("Comppath")
        
        self.Comp_top = self.builder.get_object("Comp_top")
        self.Comp_right = self.builder.get_object("Comp_right")
        self.Comp_bottom = self.builder.get_object("Comp_bottom")
        self.Comp_left = self.builder.get_object("Comp_left")
        
        self.OCR_top = self.builder.get_object("OCR_top")
        self.OCR_right = self.builder.get_object("OCR_right")
        self.OCR_bottom = self.builder.get_object("OCR_bottom")
        self.OCR_left = self.builder.get_object("OCR_left")
        
        self.charsubset = self.builder.get_object("charsubset")
        self.Compdescription = self.builder.get_object("Compdescription")
        self.selectbbox = self.builder.get_object("selectbbox")
        
        self.Imscale = self.builder.get_object("Imscale")
        self.Imnumber = self.builder.get_object("Imnumber")
        
        self.Imageback = self.builder.get_object("Imageback")
        self.Imagenext = self.builder.get_object("Imagenext")
        
        #self.image = self.builder.get_object("image_main")
        self.drawarea=self.builder.get_object("drawingarea")
        
        self.progressbar=self.builder.get_object("progressbar")
        self.progressbar.set_fraction(0.5)
        #Gtk.Widget.set_events(self.drawarea, Gdk.Event.motion)
        #self.drawarea.set_eve
        
        #self.drawarea.set_events(Gdk.POINTER_MOTION_MASK| Gdk.POINTER_MOTION_HINT_MASK)
        
        
        self.imagecounter=imagecounter();

        self.window.show_all()
        self.reset()
        
        #self.motion=GDk.Event.MotionEvent()
        
    #def motion_notify_event_cb (self.image,GdkEventMotion *event,gpointer        data)    
        #print 'motion'
        #cr.set_source_rgb(0, 0, 0)
        #cr.set_line_width(0.5)
        
         
    def update_componentdata(self):
        #print self.DSComponent.Componenthight
        #self.height.set_text('Hight: ' + str(self.DSComponent.Componenthight) + ' mm')
        #self.width.set_text('Width: ' + str(self.DSComponent.Componentwidth) + ' mm')
        #self.CompComponent.ComponentnameID.set_text('ID: ' + str(self.DSComponent.ComponentID))
        #self.Compborder.set_text('Border: ' + str(self.DSComponent.Componentborder) + ' mm')
        
        self.imagecounter.imagenumber_max=len(self.DSComponent.Imagelist)-1
        
        if(self.imagecounter.imagenumber>self.imagecounter.imagenumber_max):
            self.imagecounter.imagenumber=self.imagecounter.imagenumber_max
            
        if(self.imagecounter.imagenumber<0):
            self.imagecounter.imagenumber=0
        
        self.height.set_text(str(self.DSComponent.Componenthight))
        self.width.set_text(str(self.DSComponent.Componentwidth))
        self.CompID.set_text(str(self.DSComponent.ComponentID))
        self.Compborder.set_text(str(self.DSComponent.Componentborder))
        self.Compname.set_text(str(self.DSComponent.Componentname))
        
        self.Comp_top.set_active(self.DSComponent.Componentrotation[0])
        self.Comp_right.set_active(self.DSComponent.Componentrotation[1])
        self.Comp_bottom.set_active(self.DSComponent.Componentrotation[2])
        self.Comp_left.set_active(self.DSComponent.Componentrotation[3])

        self.OCR_top.set_active(self.DSComponent.CompOCRdata.OCRrotation[0])
        self.OCR_right.set_active(self.DSComponent.CompOCRdata.OCRrotation[1])
        self.OCR_bottom.set_active(self.DSComponent.CompOCRdata.OCRrotation[2])
        self.OCR_left.set_active(self.DSComponent.CompOCRdata.OCRrotation[3])
        
        self.charsubset.set_text(self.DSComponent.CompOCRdata.charsubset)
        self.Compdescription.set_text(self.DSComponent.Componentdescription)
        
        
        self.Imnumber.set_label(self.imagecounter.tostring()) 
        if self.imagecounter.imagenumber_max>0:
            self.Imscale.set_label(str(self.DSComponent.Imagelist[self.imagecounter.imagenumber].scale_factor) + ' [p/mm]') 
        self.drawarea.queue_draw()

    def reset(self):
        print("Reset")
        
        height=self.builder.get_object('height')
        height.set_text('0')
        width=self.builder.get_object('width')
        width.set_text('0')            
        CompID=self.builder.get_object('CompID')
        CompID.set_text('0')        
        Compborder=self.builder.get_object('Compborder')
        Compborder.set_text('0') 
        Compname=self.builder.get_object('Compname')
        Compname.set_text('')        
        #Comppath=self.builder.get_object('Comppath')
        #Comppath.set_text('') 
                
        Comp_top=self.builder.get_object('Comp_top')
        Comp_top.set_active(False)        
        Comp_right=self.builder.get_object('Comp_right')
        Comp_right.set_active(False)  
        Comp_bottom=self.builder.get_object('Comp_bottom')
        Comp_bottom.set_active(False)  
        Comp_left=self.builder.get_object('Comp_left')
        Comp_left.set_active(False)   

        OCR_top=self.builder.get_object('OCR_top')
        OCR_top.set_active(False)        
        OCR_right=self.builder.get_object('OCR_right')
        OCR_right.set_active(False)  
        OCR_bottom=self.builder.get_object('OCR_bottom')
        OCR_bottom.set_active(False)  
        OCR_left=self.builder.get_object('OCR_left')
        OCR_left.set_active(False)          

        charsubset=self.builder.get_object('charsubset')
        charsubset.set_text('ABCDEFGHIJKLMONOPQRSTUVWXYZ123456789/')   

        Compdescription=self.builder.get_object('Compdescription')
        Compdescription.set_text('')  
        
        selectbbox=self.builder.get_object('selectbbox')
        selectbbox.set_active(False) 
        
        Imscale=self.builder.get_object('Imscale')
        Imscale.set_label('0.0 [p/mm]')   
        
        Imnumber=self.builder.get_object('Imnumber')
        Imnumber.set_label(self.imagecounter.tostring()) 
        
def isfloat(x):
    try:
        float(x)
    except ValueError:
        return False
    else:
        return True
             
def main():
    Gtk.main()
    return 0

if __name__ == "__main__":
    DSclass()
    main()    


