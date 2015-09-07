#!/usr/bin/env python

# Create Searchpart dataset

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
#import ScaleCircle as SC
        

class Handler(object):
    
    def __init__(self, parent):
        self.parent = parent    
        
    def onDeleteWindow(self, *args):
        print "Quit!"
        Gtk.main_quit()
        
    def exit(self, *args):
        print "Quit!"
        Gtk.main_quit()
        
    def new_component_select_cb(self, item):
        self.parent.reset()
        
    def open_component_select_cb(self, item):
        fcd=Gtk.FileChooserDialog('Open...', None, Gtk.FileChooserAction.OPEN, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        response=fcd.run()
        if response == Gtk.ResponseType.OK:
            filename=fcd.get_filename()
            self.parent.DSComponent=SPM.Component(self.parent,filename)
            #SPM.read_zipdb(Component,filename)
            self.parent.update_componentdata()
        fcd.destroy()
        
        
    def save_component_select_cb(self, item):
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
        
    def OCRborder_Top_changed_cb(self,item):
        if isfloat(item.get_text()):
            self.parent.DSComponent.CompOCRdata.OCRborder_Top=float(item.get_text())      
            self.parent.update_componentdata()
            self.parent.drawarea.queue_draw()  
            
    def OCRborder_Right_changed_cb(self,item):
        if isfloat(item.get_text()):
            self.parent.DSComponent.CompOCRdata.OCRborder_Right=float(item.get_text())  
            self.parent.update_componentdata()
            self.parent.drawarea.queue_draw()  
            
    def OCRborder_Bottom_changed_cb(self,item):
        if isfloat(item.get_text()):
            self.parent.DSComponent.CompOCRdata.OCRborder_Bottom=float(item.get_text())  
            self.parent.update_componentdata()
            self.parent.drawarea.queue_draw()  
            
    def OCRborder_Left_changed_cb(self,item):
        if isfloat(item.get_text()):
            self.parent.DSComponent.CompOCRdata.OCRborder_Left=float(item.get_text())  
            self.parent.update_componentdata()
            self.parent.drawarea.queue_draw()  
                   
    def OCR_changed_cb(self,item):
        self.parent.DSComponent.CompOCRdata.OCR=item.get_active() 

    def Octopart_changed_cb(self,item):
        self.parent.DSComponent.CompOCRdata.Octopart=item.get_active() 

    def charsubset_changed_cb(self,item):
        self.parent.DSComponent.CompOCRdata.charsubset=item.get_text()
                  
    def Compdescription_changed_cb(self,item):
        self.parent.DSComponent.Componentdescription=item.get_text()  
                        
    def selectbbox_changed_cb(self,item):
        win = self.parent.drawarea.get_window()
        if item.get_active():
            cursor = Gdk.Cursor(Gdk.CursorType.HAND1)
            win.set_cursor(cursor)
        else:
            cursor = Gdk.Cursor(Gdk.CursorType.LEFT_PTR)
            win.set_cursor(cursor)
        self.parent.update_componentdata()
    
    def selectOCRborder_toggled_cb(self,item):
        self.parent.update_componentdata()
    
    def compmean_changed_cb(self,item):
        self.parent.DSComponent.corr()
        self.parent.selectbbox.set_active(True)
        self.parent.update_componentdata()
        
        
    def addimages_changed_cb(self,item):
        fcd=Gtk.FileChooserDialog('Open...', None, Gtk.FileChooserAction.OPEN, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        fcd.set_select_multiple(True)
        response=fcd.run()
        if response == Gtk.ResponseType.OK:
            filenames=fcd.get_filenames()
            fcd.destroy()
            k=0
            for f in filenames:
                k=k+1
                print 'Image ' + str(k) + '/' + str(len(filenames))
                Imname=os.path.basename(f)
                Im=SPM.Imagedata(f)
                if not Im.scale_factor==False:
                    self.parent.DSComponent.Imagename.append(Imname)
                    self.parent.DSComponent.Imagelist.append(Im)
            time.sleep(0.2)
            self.parent.update_componentdata()
        
        
    def deleteimage_changed_cb(self,item):
        del self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber]
        self.parent.update_componentdata()
        
    def NEXT_clicked_cb(self,item):
        if(self.parent.imagecounter.imagenumber<self.parent.imagecounter.imagenumber_max):
            self.parent.imagecounter.imagenumber=self.parent.imagecounter.imagenumber+1;
        self.parent.update_componentdata()
        self.parent.drawarea.queue_draw()  

    def BACK_clicked_cb(self,item):
        if(self.parent.imagecounter.imagenumber>0):
            self.parent.imagecounter.imagenumber=self.parent.imagecounter.imagenumber-1;
        self.parent.update_componentdata()
        
    def drawingarea_button_press_event_cb(self,item,event):
        x=event.x/self.parent.scale
        y=event.y/self.parent.scale
        if(len(self.parent.DSComponent.Imagelist)>0):
            if not self.parent.selectbbox.get_active():
                if self.parent.bboxrot[0]:  # Top
                    hight=self.parent.DSComponent.Componenthight * self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].scale_factor
                    width=self.parent.DSComponent.Componentwidth * self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].scale_factor
                    h2=int(hight/2)
                    w2=int(width/2)
                    bbox=[x-w2,y-h2,width,hight]
                    if(len(self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].Top)==0):
                        self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].Top.append(bbox)
                    else:
                        bboxfound=False 
                        for b in self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].Top:
                            if (x>b[0] and x<b[0]+width and y>b[1] and y<b[1]+hight):
                                self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].Top.remove(b)
                                bboxfound=True
                        if bboxfound==False:
                            self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].Top.append(bbox)
                    self.parent.drawarea.queue_draw()
                if self.parent.bboxrot[1]:  # Right
                    width=self.parent.DSComponent.Componenthight * self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].scale_factor
                    hight=self.parent.DSComponent.Componentwidth * self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].scale_factor
                    h2=int(hight/2)
                    w2=int(width/2)
                    bbox=[x-w2,y-h2,width,hight]
                    if(len(self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].Right)==0):
                        self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].Right.append(bbox)
                    else:
                        bboxfound=False 
                        for b in self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].Right:
                            if (x>b[0] and x<b[0]+width and y>b[1] and y<b[1]+hight):
                                self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].Right.remove(b)
                                bboxfound=True
                        if bboxfound==False:
                            self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].Right.append(bbox)
                    self.parent.drawarea.queue_draw()                    
                if self.parent.bboxrot[2]:  # Bottom
                    hight=self.parent.DSComponent.Componenthight * self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].scale_factor
                    width=self.parent.DSComponent.Componentwidth * self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].scale_factor
                    h2=int(hight/2)
                    w2=int(width/2)
                    bbox=[x-w2,y-h2,width,hight]
                    if(len(self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].Bottom)==0):
                        self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].Bottom.append(bbox)
                    else:
                        bboxfound=False 
                        for b in self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].Bottom:
                            if (x>b[0] and x<b[0]+width and y>b[1] and y<b[1]+hight):
                                self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].Bottom.remove(b)
                                bboxfound=True
                        if bboxfound==False:
                            self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].Bottom.append(bbox)
                    self.parent.drawarea.queue_draw()              
                if self.parent.bboxrot[3]:  # Left
                    width=self.parent.DSComponent.Componenthight * self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].scale_factor
                    hight=self.parent.DSComponent.Componentwidth * self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].scale_factor
                    h2=int(hight/2)
                    w2=int(width/2)
                    bbox=[x-w2,y-h2,width,hight]
                    if(len(self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].Left)==0):
                        self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].Left.append(bbox)
                    else:
                        bboxfound=False 
                        for b in self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].Left:
                            if (x>b[0] and x<b[0]+width and y>b[1] and y<b[1]+hight):
                                self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].Left.remove(b)
                                bboxfound=True
                        if bboxfound==False:
                            self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].Left.append(bbox)                  
            else:
                hight=self.parent.DSComponent.Componenthight * self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].scale_factor
                width=self.parent.DSComponent.Componentwidth * self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].scale_factor
                bboxfound=False 
                for b in self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].Topcorr:
                    if (x>b[0] and x<b[0]+hight and y>b[1] and y<b[1]+width):
                        self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].Topcorr.remove(b)
                        self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].Top.append(b)
                        
                for b in self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].Rightcorr:
                    if (x>b[0] and x<b[0]+hight and y>b[1] and y<b[1]+width):
                        self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].Rightcorr.remove(b)
                        self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].Right.append(b)
                        
                for b in self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].Bottomcorr:
                    if (x>b[0] and x<b[0]+hight and y>b[1] and y<b[1]+width):
                        self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].Bottomcorr.remove(b)
                        self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].Bottom.append(b)
                        
                for b in self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].Leftcorr:
                    if (x>b[0] and x<b[0]+hight and y>b[1] and y<b[1]+width):
                        self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].Leftcorr.remove(b)
                        self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].Left.append(b)
            self.parent.drawarea.queue_draw()        
                
                
    def draw_callback (self, wid, cr):
        if len(self.parent.DSComponent.Imagelist)>0:
            imagecv=self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].image
            imagecv = cv2.resize(imagecv, (self.parent.imsize[0], self.parent.imsize[1])) 
            imagegtk=SPM.convertCV2GTK(imagecv)
            p=imagegtk.get_pixbuf()
            Gdk.cairo_set_source_pixbuf(cr, p, 0, 0)
            cr.rectangle(0, 0, self.parent.imsize[0], self.parent.imsize[1])
            cr.fill()
            # draw component bbox
            scale=self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].scale_factor;
            scaleOCR=self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].scale_factor*self.parent.scale;
            for borg in self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].Top:
                b = [x * self.parent.scale for x in borg]
                cr.set_source_rgb(255, 0, 0)
                cr.rectangle(b[0], b[1], b[2], b[3]);
                cr.stroke()
                if self.parent.selectOCRborder.get_active():  
                    cr.set_source_rgb(125, 125, 125)
                    bOCR=[b[0]+self.parent.DSComponent.CompOCRdata.OCRborder_Left*scaleOCR, b[1]+self.parent.DSComponent.CompOCRdata.OCRborder_Top*scaleOCR, b[2]-self.parent.DSComponent.CompOCRdata.OCRborder_Left*scaleOCR-self.parent.DSComponent.CompOCRdata.OCRborder_Right*scaleOCR, b[3]-self.parent.DSComponent.CompOCRdata.OCRborder_Top*scaleOCR-self.parent.DSComponent.CompOCRdata.OCRborder_Bottom*scaleOCR]
                    cr.rectangle(bOCR[0], bOCR[1], bOCR[2], bOCR[3])
                    cr.stroke()

            for borg in self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].Right:
                b = [x * self.parent.scale for x in borg]
                cr.set_source_rgb(255, 255, 0)
                cr.rectangle(b[0], b[1], b[2], b[3]);
                cr.stroke()
                if self.parent.selectOCRborder.get_active():  
                    cr.set_source_rgb(125, 125, 125)
                    bOCR=[b[0]+self.parent.DSComponent.CompOCRdata.OCRborder_Bottom*scaleOCR, b[1]+self.parent.DSComponent.CompOCRdata.OCRborder_Left*scaleOCR, b[2]-self.parent.DSComponent.CompOCRdata.OCRborder_Bottom*scaleOCR-self.parent.DSComponent.CompOCRdata.OCRborder_Top*scaleOCR, b[3]-self.parent.DSComponent.CompOCRdata.OCRborder_Left*scaleOCR-self.parent.DSComponent.CompOCRdata.OCRborder_Right*scaleOCR]
                    cr.rectangle(bOCR[0], bOCR[1], bOCR[2], bOCR[3])
                    cr.stroke()
                                    
            for borg in self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].Bottom:
                b = [x * self.parent.scale for x in borg]
                cr.set_source_rgb(0, 255, 0)
                cr.rectangle(b[0], b[1], b[2], b[3]);
                cr.stroke()
                if self.parent.selectOCRborder.get_active():  
                    cr.set_source_rgb(125, 125, 125)
                    bOCR=[b[0]+self.parent.DSComponent.CompOCRdata.OCRborder_Right*scaleOCR, b[1]+self.parent.DSComponent.CompOCRdata.OCRborder_Bottom*scaleOCR, b[2]-self.parent.DSComponent.CompOCRdata.OCRborder_Right*scaleOCR-self.parent.DSComponent.CompOCRdata.OCRborder_Left*scaleOCR, b[3]-self.parent.DSComponent.CompOCRdata.OCRborder_Bottom*scaleOCR-self.parent.DSComponent.CompOCRdata.OCRborder_Top*scaleOCR]
                    cr.rectangle(bOCR[0], bOCR[1], bOCR[2], bOCR[3])
                    cr.stroke()
                    
            for borg in self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].Left:
                b = [x * self.parent.scale for x in borg]
                cr.set_source_rgb(0, 0, 255)
                cr.rectangle(b[0], b[1], b[2], b[3]);
                cr.stroke()
                if self.parent.selectOCRborder.get_active():  
                    cr.set_source_rgb(125, 125, 125)
                    bOCR=[b[0]+self.parent.DSComponent.CompOCRdata.OCRborder_Top*scale, b[1]+self.parent.DSComponent.CompOCRdata.OCRborder_Right*scale, b[2]-self.parent.DSComponent.CompOCRdata.OCRborder_Top*scale-self.parent.DSComponent.CompOCRdata.OCRborder_Bottom*scale, b[3]-self.parent.DSComponent.CompOCRdata.OCRborder_Right*scale-self.parent.DSComponent.CompOCRdata.OCRborder_Left*scale]
                    cr.rectangle(bOCR[0], bOCR[1], bOCR[2], bOCR[3])
                    cr.stroke()
            # draw component bbox expected components    
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
                for borg in self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].Bottomcorr:
                    b = [x * self.parent.scale for x in borg]
                    cr.set_source_rgb(255, 255, 255)
                    cr.rectangle(b[0], b[1], b[2], b[3]);
                    cr.stroke()                          
                for borg in self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].Leftcorr:
                    b = [x * self.parent.scale for x in borg]
                    cr.set_source_rgb(255, 255, 255)
                    cr.rectangle(b[0], b[1], b[2], b[3]);
                    cr.stroke()                    
    
    def window1_key_press_event_cb(self,item,event):
        if(event.keyval==65362):
            self.parent.bboxrot=[True,False,False,False]
        elif(event.keyval==65363):
            self.parent.bboxrot=[False,True,False,False]
        elif(event.keyval==65364):
            self.parent.bboxrot=[False,False,True,False]
        elif(event.keyval==65361):
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
    selectOCRborder=False
    deletebbox=False
    compmean=False
    addimages=False
    deleteimage=False
    #DSComponent=Component(None,None)
    scale=0.2;
    imsize=[int(4000*scale),int(3000*scale)]
    bboxrot=[True,False,False,False]
    
    def __init__(self):
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
        
        self.OCR = self.builder.get_object("OCR")
        self.Octopart = self.builder.get_object("Octopart")
        
        self.OCR_top = self.builder.get_object("OCR_top")
        self.OCR_right = self.builder.get_object("OCR_right")
        self.OCR_bottom = self.builder.get_object("OCR_bottom")
        self.OCR_left = self.builder.get_object("OCR_left")
        
        self.OCRborder_Top = self.builder.get_object("OCRborder_Top")
        self.OCRborder_Right = self.builder.get_object("OCRborder_Right")
        self.OCRborder_Bottom = self.builder.get_object("OCRborder_Bottom")
        self.OCRborder_Left = self.builder.get_object("OCRborder_Left")
        
        self.charsubset = self.builder.get_object("charsubset")
        self.Compdescription = self.builder.get_object("Compdescription")
        self.selectbbox = self.builder.get_object("selectbbox")
        self.selectOCRborder = self.builder.get_object("selectOCRborder")
        
        self.Imscale = self.builder.get_object("Imscale")
        self.Imnumber = self.builder.get_object("Imnumber")
        
        self.Imageback = self.builder.get_object("Imageback")
        self.Imagenext = self.builder.get_object("Imagenext")
        
        self.drawarea=self.builder.get_object("drawingarea")
        
        self.progressbar=self.builder.get_object("progressbar")
        self.progressbar.set_fraction(0.5)
        
        self.DSComponent=SPM.Component(self,None)

        self.imagecounter=imagecounter();

        self.window.show_all()
        self.reset()

    def update_componentdata(self):
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
        
        self.Octopart.set_active(self.DSComponent.CompOCRdata.OCRlib)
        self.OCR.set_active(self.DSComponent.CompOCRdata.OCR)
        self.Octopart.set_active(self.DSComponent.CompOCRdata.OCRlib)

        self.OCRborder_Top.set_text(str(self.DSComponent.CompOCRdata.OCRborder_Top))
        self.OCRborder_Right.set_text(str(self.DSComponent.CompOCRdata.OCRborder_Right))
        self.OCRborder_Bottom.set_text(str(self.DSComponent.CompOCRdata.OCRborder_Bottom))
        self.OCRborder_Left.set_text(str(self.DSComponent.CompOCRdata.OCRborder_Left))
                
        self.charsubset.set_text(self.DSComponent.CompOCRdata.charsubset)
        self.Compdescription.set_text(self.DSComponent.Componentdescription)
        
        
        self.Imnumber.set_label(self.imagecounter.tostring()) 

        if len(self.DSComponent.Imagelist)>0:
            self.Imscale.set_label(str(self.DSComponent.Imagelist[self.imagecounter.imagenumber].scale_factor) + ' [p/mm]') 
        self.drawarea.queue_draw()

    def reset(self):
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

        OCRborder_Top=self.builder.get_object('OCRborder_Top')
        OCRborder_Top.set_text('Top')  
        OCRborder_Right=self.builder.get_object('OCRborder_Right')
        OCRborder_Right.set_text('Right')  
        OCRborder_Bottom=self.builder.get_object('OCRborder_Bottom')
        OCRborder_Bottom.set_text('Bottom')  
        OCRborder_Left=self.builder.get_object('OCRborder_Left')
        OCRborder_Left.set_text('Left')     

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
        
        selectOCRborder=self.builder.get_object('selectOCRborder')
        selectOCRborder.set_active(False) 
        
        Imscale=self.builder.get_object('Imscale')
        Imscale.set_label('0.0 [p/mm]')   
        
        Imnumber=self.builder.get_object('Imnumber')
        Imnumber.set_label(self.imagecounter.tostring()) 
        
        self.DSComponent=SPM.Component(self,None)
        
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

