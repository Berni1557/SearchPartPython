#!/usr/bin/env python
from gi.repository import Gtk
from gi.repository import Gdk
import cv2
import SearchPartModules as SPM
from gi.repository import GdkPixbuf
from xml.dom.minidom import parse
import numpy as np
import cairo


class Imagedata(object):
    improbabilitymap=list()
    imagepath=''
    image=np.zeros((3000,4000,3), np.uint8)
    def __init__(self,path):
        self.imagepath=path
        print(path)
        self.image=cv2.imread(path)    
        self.bbox=list()
        self.Top=list()
        self.Right=list()
        self.Bottom=list()
        self.Left=list()

class OCRdata(object):
    OCRrotation=[False,False,False,False]
    OCR=False
    OCRlib=False
    charsubset=''
        
class Component(object):
    Creation_date=''
    Componentname=''
    ComponentID=0
    path=''
    Top=list()
    Bottom=list()
    Left=list()
    Right=list()
    scale_factor=list()
    Componenthight=0
    Componentwidth=0
    Componentborder=0
    Componentrotation=[True,False,False,False]
    Componentdescription=''
    CompOCRdata=OCRdata()
    Imagename=list()
    Imagelist=list()
    
    def __init__(self, parent, filename,):
        if isinstance (filename, basestring):
            self.parent=parent
            dom = parse(filename)
            self.Creation_date=dom.getElementsByTagName('Creation_date').item(0).firstChild.nodeValue
            self.Componentname=dom.getElementsByTagName('Componentname').item(0).firstChild.nodeValue
            self.ComponentID=int(dom.getElementsByTagName('ComponentID').item(0).firstChild.nodeValue)
            self.path=dom.getElementsByTagName('path').item(0).firstChild.nodeValue
            self.Componenthight=float(dom.getElementsByTagName('Componenthight').item(0).firstChild.nodeValue)
            self.Componentwidth=float(dom.getElementsByTagName('Componentwidth').item(0).firstChild.nodeValue)
            self.Componentborder=float(dom.getElementsByTagName('Componentborder').item(0).firstChild.nodeValue)
            
            print 'now'
            for node in dom.childNodes.item(0).childNodes[15].childNodes:
                print 'now'
                if(node.hasChildNodes()==True):
                    self.Imagename.append(node.childNodes[0].nodeValue)
                    print(node.childNodes[0].nodeValue)
            for node in dom.childNodes.item(0).childNodes[17].childNodes:
                if(node.hasChildNodes()==True):
                    self.Top.append(node.childNodes[0].nodeValue)
            for node in dom.childNodes.item(0).childNodes[19].childNodes:
                if(node.hasChildNodes()==True):
                    self.Bottom.append(node.childNodes[0].nodeValue)
            for node in dom.childNodes.item(0).childNodes[21].childNodes:
                if(node.hasChildNodes()==True):
                    self.Left.append(node.childNodes[0].nodeValue)                    
            for node in dom.childNodes.item(0).childNodes[23].childNodes:
                if(node.hasChildNodes()==True):
                    self.Right.append(node.childNodes[0].nodeValue)   
            for node in dom.childNodes.item(0).childNodes[25].childNodes:
                if(node.hasChildNodes()==True):
                    self.scale_factor.append(float(node.childNodes[0].nodeValue))      
            self.Componentrotation=[False,False,False,False]
            self.load_images() 
            self.parent.imagecounter.imagenumber=0;
            self.parent.imagecounter.imagenumber_max=len(self.Imagelist)-1;

                                                                     
        else:
            self.Creation_date=''
            self.Componentname=''
            self.ComponentID=0
            self.path=''
            self.Imagename=list()
            self.Top=list()
            self.Bottom=list()
            self.Left=list()
            self.Right=list()
            self.scale_factor=list() 
            
    def load_images(self):  
        #imsize=self.parent.imsize
        #k=0
        for s in self.Imagename:
            impath=self.path + s
            Im=Imagedata(impath)
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
        fcd.destroy()
        self.parent.DSComponent=Component(self.parent,filename)
        self.parent.update_componentdata()
        
    def save_component_select_cb(self, item):
        print("Hello save!")
        print(self.parent.DSComponent.Componentname)
        
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
        self.parent.selectbbox=item.get_active() 
        
    def deletebbox_changed_cb(self,item):
        print('deletebbox')  
        #self.parent.deletebbox=item.get_active()      
        
    def compmean_changed_cb(self,item):
        print('compmean')  
        #self.parent.deletebbox=item.get_active() import Image
        
    def addimages_changed_cb(self,item):
        print('addimages')  
        #self.parent.addimages=item.get_active() 
        
    def deleteimage_changed_cb(self,item):
        print('deleteimage')  
        
    def NEXT_clicked_cb(self,item):
        #print self.parent.imagecounter.imagenumber_max
        #print self.parent.imagecounter.imagenumber
        if(self.parent.imagecounter.imagenumber<self.parent.imagecounter.imagenumber_max):
            self.parent.imagecounter.imagenumber=self.parent.imagecounter.imagenumber+1;
        self.parent.update_componentdata()
        self.parent.darea.queue_draw()  

    def BACK_clicked_cb(self,item):
        if(self.parent.imagecounter.imagenumber>0):
            self.parent.imagecounter.imagenumber=self.parent.imagecounter.imagenumber-1;
        self.parent.update_componentdata()
    
    def drawingarea_motion_notify_event_cb(self,item,event):
        print event.x
        print 'motion' 
        #if(len(self.parent.DSComponent.Imagelist)>0):
            #hight=self.parent.DSComponent.Componenthight * self.parent.scale * self.parent.DSComponent.scale_factor[self.parent.imagecounter.imagenumber]
            #width=self.parent.DSComponent.Componentwidth * self.parent.scale * self.parent.DSComponent.scale_factor[self.parent.imagecounter.imagenumber]
            #b=[event.x,event.y,hight,width]
            #event.set_source_rgb(255, 0, 0)
            #print b
            #event.rectangle(b[0], b[1], b[2], b[3]);
            #event.stroke()
        
        
    def drawingarea_button_press_event_cb(self,item,event):
        print 'click'
        """
        print event.button
        if(len(self.parent.DSComponent.Imagelist)>0):
            
            if(self.parent.bboxrot[0] or self.parent.bboxrot[2]):
                hight=self.parent.DSComponent.Componenthight * self.parent.scale * self.parent.DSComponent.scale_factor[self.parent.imagecounter.imagenumber]
                width=self.parent.DSComponent.Componentwidth * self.parent.scale * self.parent.DSComponent.scale_factor[self.parent.imagecounter.imagenumber]
            elif(self.parent.bboxrot[1] or self.parent.bboxrot[3]):
                width=self.parent.DSComponent.Componenthight * self.parent.scale * self.parent.DSComponent.scale_factor[self.parent.imagecounter.imagenumber]
                hight=self.parent.DSComponent.Componentwidth * self.parent.scale * self.parent.DSComponent.scale_factor[self.parent.imagecounter.imagenumber]

            h2=int(hight/2)
            w2=int(width/2)

                
            if(len(self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].bbox)==0):
                b=[event.x-h2,event.y-w2,hight,width]
                if self.parent.bboxrot[0]:
                    self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].Top.append(b)
                elif self.parent.bboxrot[1]:
                    self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].Left.append(b)
                elif self.parent.bboxrot[2]:
                    self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].Bottom.append(b)                    
                elif self.parent.bboxrot[3]:
                    self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].right.append(b)        
                self.parent.darea.queue_draw()  
                  
            else:     
                bboxfound=False       
                for b in self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].bbox:
                    print (event.x>b[0] and event.x<b[0]+hight)
                    if (event.x>b[0] and event.x<b[0]+hight and event.y>b[1] and event.y<b[1]+width):
                        self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].bbox.remove(b)
                        bboxfound=True
                if bboxfound==False:
                    b=[event.x-h2,event.y-w2,hight,width]
                    brot=self.parent.bboxrot
                    self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].bbox.append(b)
                    self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].bboxrot.append(brot)
                    
            self.parent.darea.queue_draw()
         """   
        

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
        
            for b in self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].bbox:
                cr.set_source_rgb(255, 0, 0)
                cr.rectangle(b[0], b[1], b[2], b[3]);
                cr.stroke()
            #cr.set_source_rgb(255, 0, 0)
            #cr.rectangle(20, 20, 120, 80);
            #cr.stroke()
    
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
        imstr=str(self.imagenumber+1) + " / " + str(self.imagenumber_max+1)
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
        self.height = self.builder.get_object("height")
        self.width = self.builder.get_object("width")
        self.CompID = self.builder.get_object("CompID")
        self.Compborder = self.builder.get_object("Compborder")
        
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
        self.darea= self.builder.get_object("drawingarea")
        #Gtk.Widget.set_events(self.darea, Gdk.Event.motion)
        #self.darea.set_eve
        
        #self.darea.set_events(Gdk.POINTER_MOTION_MASK| Gdk.POINTER_MOTION_HINT_MASK)
        
        
        self.imagecounter=imagecounter();

        self.window.show_all()
        self.reset()
        
        #self.motion=GDk.Event.MotionEvent()
        
    #def motion_notify_event_cb (self.image,GdkEventMotion *event,gpointer        data)    
        #print 'motion'
        #cr.set_source_rgb(0, 0, 0)
        #cr.set_line_width(0.5)
        
         
    def update_componentdata(self):
        print self.DSComponent.Componenthight
        #self.height.set_text('Hight: ' + str(self.DSComponent.Componenthight) + ' mm')
        #self.width.set_text('Width: ' + str(self.DSComponent.Componentwidth) + ' mm')
        #self.CompID.set_text('ID: ' + str(self.DSComponent.ComponentID))
        #self.Compborder.set_text('Border: ' + str(self.DSComponent.Componentborder) + ' mm')
        
        self.height.set_text(str(self.DSComponent.Componenthight))
        self.width.set_text(str(self.DSComponent.Componentwidth))
        self.CompID.set_text(str(self.DSComponent.ComponentID))
        self.Compborder.set_text(str(self.DSComponent.Componentborder))
        
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
        
        self.imagecounter.imagenumber_max=len(self.DSComponent.Imagelist)-1
        self.Imnumber.set_label(self.imagecounter.tostring()) 
        self.Imscale.set_label(str(self.DSComponent.scale_factor[self.imagecounter.imagenumber]) + ' [p/mm]') 
        self.darea.queue_draw()

            

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
        Compdescription.set_text('ABCDEFGHIJKLMONOPQRSTUVWXYZ123456789/')  
        
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


