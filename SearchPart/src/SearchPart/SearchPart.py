#!/usr/bin/python3
import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QCheckBox, QApplication, QMainWindow, QFileDialog
from PyQt5.uic import loadUi
import time
import string
import cv2
import numpy as np
import SearchPartModules as SPM

from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtGui import QPainter, QColor, QBrush
from PyQt5.QtGui import QPen, QPainter, QColor, QBrush, QPainterPath, QFont
from PyQt5.QtWidgets import QWidget, QGraphicsObject, QStyleOptionGraphicsItem
from PyQt5.QtCore import Qt, QTimer, QRectF

from PyQt5.QtCore import pyqtSignal, Qt, QDir, QFile, QFileInfo, QPoint, QTextStream, QTimer, QUrl, QRect

class SearchPartGUI(QMainWindow):
    
    # Events
    keyPressed = QtCore.pyqtSignal(QtCore.QEvent)
    
    # Member variables
    component = SPM.Component(None,None);
    counter = SPM.imagecounter();
    showBBox = True;
    #scaleVisualization = 1.0;
    scaleVisualization = [800,600]
    scaleVisualizationFactor = [1.0, 1.0]
    bboxrot = [True,False,False,False]
    pixmap = None
    
    def __init__(self):
        
        # Init GUI      
        super(SearchPartGUI,self).__init__()
        loadUi('../qt/SearchPartGUI_V13.ui',self)
        self.setWindowTitle('SearchPart')

        # Set callbacks
        self.CreateCompDataset.clicked.connect(self.on_button_CreateCompDataset);
        self.LoadCompDataset.clicked.connect(self.on_button_LoadCompDataset);
        self.SaveCompDataset.clicked.connect(self.on_button_SaveCompDataset);
        
        self.ComponentName.editingFinished.connect(self.on_ComponentName);
        self.ComponentDatasetPath.editingFinished.connect(self.on_ComponentDatasetPath)
        self.ComponentWidth.editingFinished.connect(self.on_ComponentWidth)
        self.ComponentHeight.editingFinished.connect(self.on_ComponentHeight)
        self.BorderSize.editingFinished.connect(self.on_BorderSize)
        self.ComponentID.editingFinished.connect(self.on_ComponentID)
        
        self.OCRText.editingFinished.connect(self.on_OCRText)
        self.OCRAxialSymmetricHorizontal.stateChanged.connect(self.on_OCRAxialSymmetricHorizontal)
        self.OCRAxialSymmetricVertical.stateChanged.connect(self.on_OCRAxialSymmetricVertical)
        
        self.OnlineDataBase.editingFinished.connect(self.on_OnlineDataBase)
        self.AxialSymmetricHorizontal.stateChanged.connect(self.on_AxialSymmetricHorizontal)
        self.AxialSymmetricVertical.stateChanged.connect(self.on_AxialSymmetricVertical)
        self.ComponentDescription.textChanged.connect(self.on_ComponentDescription)
        
        self.Back.clicked.connect(self.on_button_Back);
        self.Next.clicked.connect(self.on_button_Next);
        
        self.BBox.stateChanged.connect(self.on_BBox)
        #self.DeleteBBox.clicked.connect(self.on_DeleteBBox);
        self.ComponentMean.clicked.connect(self.on_ComponentMean)
        self.AddImage.clicked.connect(self.on_AddImage)
        self.DeleteImage.clicked.connect(self.on_DeleteImage)
        
        
        self.ImageNumber.setText(self.counter.tostring())
        self.ImageScale.setText(self.scale())
        
        self.Image.mousePressEvent = self.getPosition
        
        
        self.component=SPM.Component(self,None)
        
        self.counter=SPM.imagecounter();
        
        self.reset()
        self.draw()
    
    def getPosition(self , event):
        x = event.pos().x()
        y = event.pos().y()
        #print('x: ' + str(x))
        #print('y: ' + str(y))
        self.appendBBox(x, y)
        
    def scale(self):
        if (self.counter.imagenumber > -1):
            s = str(self.component.Imagelist[self.counter.imagenumber].scale_factor) + ' [p/mm]'
        else:
            s = 'Image scale [p/mm]'
        return s
    
    @pyqtSlot()
    def on_DeleteImage(self):
        del self.component.Imagelist[self.counter.imagenumber]
        #self.counter.imagenumber = self.counter.imagenumber - 1;
        self.update_componentdata()
        
    @pyqtSlot()
    def on_AddImage(self):
        #ImFilter = "PNG (*.png)"
        #filenames = QFileDialog.getOpenFileNamesAndFilter(self, "Open files", "C:\\Desktop", ImFilter)
        names = QFileDialog.getOpenFileNames(self,  'Open file','H:/Projects/SearchPartPython/SearchPartPython/SearchPart/data/images/',"Images (*.png *.tiff *.jpg)")
        filenames = names[0];
        print('filenames: ' + str(filenames))
        k=0
        for f in filenames:
            k=k+1
            print('Loading: ' + f + '; Image ' + str(k) + '/' + str(len(filenames)))
            Imname=os.path.basename(f)
            Im=SPM.Imagedata(f)
            if not Im.scale_factor==False:
                self.component.Imagename.append(Imname)
                self.component.Imagelist.append(Im)                          
        time.sleep(0.2)
        self.update_componentdata()
        
    @pyqtSlot()
    def on_ComponentMean(self):
        self.component.corr()
        self.BBox.setChecked(True)
        self.update_componentdata()
        
    #@pyqtSlot()
    #def on_DeleteBBox(self):
    #    print('on_DeleteBBox')
        
    @pyqtSlot()
    def on_BBox(self):
        self.showBBox = self.BBox.isChecked()
        
    @pyqtSlot()
    def on_button_Back(self):
        if(self.counter.imagenumber>0):
            self.counter.imagenumber=self.counter.imagenumber-1;
        self.update_componentdata()
        self.draw()
        
    @pyqtSlot()
    def on_button_Next(self):
        if(self.counter.imagenumber<self.counter.imagenumber_max):
            self.counter.imagenumber=self.counter.imagenumber+1;
        self.update_componentdata()
        self.draw()
    
    @pyqtSlot()
    def on_OCRAxialSymmetricHorizontal(self):
        self.component.CompOCRdata.AxialSymmetricHorizontal = self.OCRAxialSymmetricHorizontal.isChecked()
    
    @pyqtSlot()
    def on_OCRAxialSymmetricVertical(self):
        self.component.CompOCRdata.AxialSymmetricVertical = self.OCRAxialSymmetricVertical.isChecked()
        
    @pyqtSlot()
    def on_ComponentDescription(self):
        self.component.Componentdescription = self.ComponentDescription.toPlainText()
        
    @pyqtSlot()
    def on_AxialSymmetricHorizontal(self):
        self.component.AxialSymmetricHorizontal = self.AxialSymmetricHorizontal.isChecked()
    
    @pyqtSlot()
    def on_AxialSymmetricVertical(self):
        self.component.AxialSymmetricVertical = self.AxialSymmetricVertical.isChecked()
        
    @pyqtSlot()
    def on_OnlineDataBase(self):
        self.component.OnlineDataBase = self.OnlineDataBase.text()
        
    @pyqtSlot()
    def on_OCRText(self):
        self.component.CompOCRdata.OCRText = self.OCRText.text()
            
    @pyqtSlot()
    def on_BorderSize(self):
        if isfloat(self.BorderSize.text()):
            self.component.Componentborder = float(self.BorderSize.text())

    @pyqtSlot()
    def on_ComponentID(self):
        if isint(self.ComponentID.text()):
            self.component.ComponentID = int(self.ComponentID.text())
            
    @pyqtSlot()
    def on_ComponentWidth(self):
        if isfloat(self.ComponentWidth.text()):
            self.component.Componentwidth = float(self.ComponentWidth.text())
        
    @pyqtSlot()
    def on_ComponentHeight(self):
        if isfloat(self.ComponentHeight.text()):
            self.component.Componentheight = float(self.ComponentHeight.text())
        
    @pyqtSlot()
    def on_ComponentDatasetPath(self):
        self.component.ComponentDatasetPath = self.ComponentDatasetPath.text()
        
    @pyqtSlot()
    def on_ComponentName(self):
        self.component.Componentname = self.ComponentName.text()
        
    @pyqtSlot()
    def on_button_SelectDataset(self):
        txt = self.ComponentName.text()
        print(txt)

    @pyqtSlot()
    def on_button_CreateCompDataset(self):
        print("Create new dataset!")
        self.reset()

    @pyqtSlot()
    def on_button_SaveCompDataset(self):
        filedialog = QFileDialog.getSaveFileName(self, "Select component file", '', '*.zip')
        filepath = filedialog[0]
        self.ComponentDatasetPath.setText(filepath)
        #filepath = 'H:/Projects/SearchPartPython/SearchPartPython1/SearchPart/data/file.zip'
        creatable = SPM.is_path_exists_or_creatable(filepath)
        if creatable:
            SPM.write_zipdb(self.component, filepath)
        else:
            self.StatusLine.setText('Can not create file: ' + filepath)
        
    @pyqtSlot()
    def on_button_LoadCompDataset(self):
        filedialog = QFileDialog.getOpenFileName(self, "Select component file", '', '*.zip')
        filepath = filedialog[0]
        self.ComponentDatasetPath.setText(filepath)
        self.component = SPM.read_zipdb(self.component, filepath)
        self.update_componentdata();
        self.draw()
        
    def on_key(self):
        self.on_button_search()
        
    def reset(self):
        self.ComponentHeight.setText('0')
        self.ComponentWidth.setText('0')
        self.ComponentID.setText('0')
        self.BorderSize.setText('0')
        self.ComponentName.setText('')
        self.ComponentDatasetPath.setText('')
        self.ComponentDescription.setText('')
        
        self.BBox.setChecked(False)
        self.ImageScale.setText('Image scale [px/mm]: 0')
        self.ImageNumber.setText('ImageNumber: 0 / 0')
        
        self.DSComponent=SPM.Component(self.parent, '')
        
        
        
#        height=self.builder.get_object('height')
#        height.set_text('0')
#        width=self.builder.get_object('width')
#        width.set_text('0')            
#        CompID=self.builder.get_object('CompID')
#        CompID.set_text('0')        
#        Compborder=self.builder.get_object('Compborder')
#        Compborder.set_text('0') 
#        Compname=self.builder.get_object('Compname')
#        Compname.set_text('')        
#        #Comppath=self.builder.get_object('Comppath')
#        #Comppath.set_text('') 
#                
#        Comp_top=self.builder.get_object('Comp_top')
#        Comp_top.set_active(False)        
#        Comp_right=self.builder.get_object('Comp_right')
#        Comp_right.set_active(False)  
#        Comp_bottom=self.builder.get_object('Comp_bottom')
#        Comp_bottom.set_active(False)  
#        Comp_left=self.builder.get_object('Comp_left')
#        Comp_left.set_active(False)   
#
#        OCRborder_Top=self.builder.get_object('OCRborder_Top')
#        OCRborder_Top.set_text('Top')  
#        OCRborder_Right=self.builder.get_object('OCRborder_Right')
#        OCRborder_Right.set_text('Right')  
#        OCRborder_Bottom=self.builder.get_object('OCRborder_Bottom')
#        OCRborder_Bottom.set_text('Bottom')  
#        OCRborder_Left=self.builder.get_object('OCRborder_Left')
#        OCRborder_Left.set_text('Left')     
#
#        OCR_top=self.builder.get_object('OCR_top')
#        OCR_top.set_active(False)        
#        OCR_right=self.builder.get_object('OCR_right')
#        OCR_right.set_active(False)  
#        OCR_bottom=self.builder.get_object('OCR_bottom')
#        OCR_bottom.set_active(False)  
#        OCR_left=self.builder.get_object('OCR_left')
#        OCR_left.set_active(False)      
#        charsubset=self.builder.get_object('charsubset')
#        charsubset.set_text('ABCDEFGHIJKLMONOPQRSTUVWXYZ123456789/')   
#
#        Compdescription=self.builder.get_object('Compdescription')
#        Compdescription.set_text('')  
#        
#        selectbbox=self.builder.get_object('selectbbox')
#        selectbbox.set_active(False) 
#        
#        selectOCRborder=self.builder.get_object('selectOCRborder')
#        selectOCRborder.set_active(False) 
#        
#        Imscale=self.builder.get_object('Imscale')
#        Imscale.set_label('0.0 [p/mm]')   
#        
#        Imnumber=self.builder.get_object('Imnumber')
#        Imnumber.set_label(self.imagecounter.tostring()) 
        
#        self.DSComponent=SPM.Component(self,None)

    def update_componentdata(self):
        self.counter.imagenumber_max=len(self.component.Imagelist)-1
        
        if(self.counter.imagenumber==-1):
            self.counter.imagenumber=0
            
        #self.counter.imagenumber = 1
        if(self.counter.imagenumber>self.counter.imagenumber_max):
            self.counter.imagenumber=self.counter.imagenumber_max
        
        self.ComponentHeight.setText(str(self.component.Componentheight))
        self.ComponentWidth.setText(str(self.component.Componentwidth))
        self.ComponentID.setText(str(self.component.ComponentID))
        self.BorderSize.setText(str(self.component.Componentborder))
        self.ComponentName.setText(self.component.Componentname)
        
        self.AxialSymmetricHorizontal.setChecked(self.component.AxialSymmetricHorizontal)
        self.AxialSymmetricVertical.setChecked(self.component.AxialSymmetricVertical)
        
        self.OCRAxialSymmetricHorizontal.setChecked(self.component.CompOCRdata.AxialSymmetricHorizontal)
        self.OCRAxialSymmetricVertical.setChecked(self.component.CompOCRdata.AxialSymmetricVertical)
        
        self.OnlineDataBase.setText(self.component.OnlineDataBase)
        self.OCRText.setText(self.component.CompOCRdata.OCRText)
        self.ComponentDescription.setText(self.component.Componentdescription);
        
        self.BBox.setChecked(self.showBBox)
        
        self.ImageNumber.setText(self.counter.tostring()) 
        self.ImageScale.setText(self.scale()) 
        self.draw()
#
#        self.OCR_top.set_active(self.DSComponent.CompOCRdata.OCRrotation[0])
#        self.OCR_right.set_active(self.DSComponent.CompOCRdata.OCRrotation[1])
#        self.OCR_bottom.set_active(self.DSComponent.CompOCRdata.OCRrotation[2])
#        self.OCR_left.set_active(self.DSComponent.CompOCRdata.OCRrotation[3])
#        
#        self.Octopart.set_active(self.DSComponent.CompOCRdata.OCRlib)
#        self.OCR.set_active(self.DSComponent.CompOCRdata.OCR)
#        self.Octopart.set_active(self.DSComponent.CompOCRdata.OCRlib)
#
#        self.OCRborder_Top.set_text(str(self.DSComponent.CompOCRdata.OCRborder_Top))
#        self.OCRborder_Right.set_text(str(self.DSComponent.CompOCRdata.OCRborder_Right))
#        self.OCRborder_Bottom.set_text(str(self.DSComponent.CompOCRdata.OCRborder_Bottom))
#        self.OCRborder_Left.set_text(str(self.DSComponent.CompOCRdata.OCRborder_Left))
#                
#        self.charsubset.set_text(self.DSComponent.CompOCRdata.charsubset)
#        self.Compdescription.set_text(self.DSComponent.Componentdescription)
#        
#        
#        self.Imnumber.set_label(self.imagecounter.tostring()) 
#
#        if len(self.DSComponent.Imagelist)>0:
#            self.Imscale.set_label(str(self.DSComponent.Imagelist[self.imagecounter.imagenumber].scale_factor) + ' [p/mm]') 
#        self.drawarea.queue_draw()
    def draw(self):
        print('draw')
        #print('Image size:' + str(self.Image.size().width()))
        #print('Image size:' + str(self.Image.size().height()))
        
        print('Image size:' + str(len(self.component.Imagelist)))
        print('imagenumber:' + str(self.counter.imagenumber))
        print('imagenumber_max:' + str(self.counter.imagenumber_max))
        
        if self.counter.valid():
            imagecv = self.component.Imagelist[self.counter.imagenumber].image
            
            self.scaleVisualizationFactor[0] = self.scaleVisualization[0] / imagecv.shape[1]
            self.scaleVisualizationFactor[1] = self.scaleVisualization[1] / imagecv.shape[0]
            
            #print('scaleVisualizationFactor: ' + str(self.scaleVisualizationFactor))
            #print('scaleVisualization: ' + str(self.scaleVisualization))
            #print('imagecv: ' + str(imagecv.shape))
            
            #imagecv = scipy.misc.imresize(imagecv, 0.175)
            imagecv = cv2.resize(imagecv, (self.scaleVisualization[0], self.scaleVisualization[1])) 
            #print("shape0: " + str(imagecv.shape[0]))
            #print("shape1: " + str(imagecv.shape[1]))
            
            #image = QtGui.QImage(imagecv, imagecv.shape[1],imagecv.shape[0], imagecv.shape[1] * 3, QtGui.QImage.Format_Indexed8)
            image = QtGui.QImage(imagecv.data, imagecv.shape[1], imagecv.shape[0], imagecv.strides[0], QtGui.QImage.Format_RGB888)
            self.pixmap = QtGui.QPixmap(image)
            #self.pixmap = self.pixmap.scaledToWidth(self.scaleVisualizationWidth)
            #self.scaleVisualization = self.scaleVisualizationWidth / imagecv.shape[1]
            self.Image.setPixmap(self.pixmap)
            #self.Image.setPixmap(self.pixmap.scaled(self.Image.width(), self.Image.height(), QtCore.Qt.KeepAspectRatio))
        else:
            imagecv = np.zeros((self.scaleVisualization[1], self.scaleVisualization[0], 3), np.uint8)
            
            self.scaleVisualizationFactor[0] = self.scaleVisualization[0] / imagecv.shape[1]
            self.scaleVisualizationFactor[1] = self.scaleVisualization[1] / imagecv.shape[0]
            
            #print('scaleVisualizationFactor: ' + str(self.scaleVisualizationFactor))
            #print('scaleVisualization: ' + str(self.scaleVisualization))
            #print('imagecv: ' + str(imagecv.shape))
            
            #imagecv = scipy.misc.imresize(imagecv, 0.175)
            imagecv = cv2.resize(imagecv, (self.scaleVisualization[0], self.scaleVisualization[1])) 
            #print("shape0: " + str(imagecv.shape[0]))
            #print("shape1: " + str(imagecv.shape[1]))
            
            #image = QtGui.QImage(imagecv, imagecv.shape[1],imagecv.shape[0], imagecv.shape[1] * 3, QtGui.QImage.Format_Indexed8)
            image = QtGui.QImage(imagecv.data, imagecv.shape[1], imagecv.shape[0], imagecv.strides[0], QtGui.QImage.Format_RGB888)
            self.pixmap = QtGui.QPixmap(image)
            #self.pixmap = self.pixmap.scaledToWidth(self.scaleVisualizationWidth)
            #self.scaleVisualization = self.scaleVisualizationWidth / imagecv.shape[1]
            self.Image.setPixmap(self.pixmap)
            #self.Image.setPixmap(self.pixmap.scaled(self.Image.width(), self.Image.height(), QtCore.Qt.KeepAspectRatio))

    def drawRectangle(self):
        
        #print('Image width:' + str(self.Image.size().width()))
        #print('Image height:' + str(self.Image.size().height()))
        
        #self.draw()
        
        #print('drawRectangle')
        painter = QPainter(self.pixmap)
        painter.setBrush(Qt.NoBrush)
        painter.setPen(Qt.red)
                
        if len(self.component.Imagelist)>0:
            
            imagecv=self.component.Imagelist[self.counter.imagenumber].image
            #self.scaleVisualizationFactor[0] = self.scaleVisualization[0] / imagecv.shape[0]
            #self.scaleVisualizationFactor[1] = self.scaleVisualization[1] / imagecv.shape[1]
            #imagecv = cv2.resize(imagecv, None, fx=self.scaleVisualizationFactor[0], fy=self.scaleVisualizationFactor[1]);
            imagecv = cv2.resize(imagecv, (self.scaleVisualization[0], self.scaleVisualization[1])) 
            image = QtGui.QImage(imagecv, imagecv.shape[1], imagecv.shape[0], imagecv.shape[1] * 3, QtGui.QImage.Format_RGB888)
            self.pixma = QtGui.QPixmap(image)

            for borg in self.component.Imagelist[self.counter.imagenumber].Top:  
                painter.setPen(Qt.red)
                rect = QRect(borg[0]*self.scaleVisualizationFactor[0], borg[1]*self.scaleVisualizationFactor[1], borg[2]*self.scaleVisualizationFactor[0], borg[3]*self.scaleVisualizationFactor[1])
                painter.drawRect(rect)           

            for borg in self.component.Imagelist[self.counter.imagenumber].Right:
                painter.setPen(Qt.green)
                rect = QRect(borg[0]*self.scaleVisualizationFactor[0], borg[1]*self.scaleVisualizationFactor[1], borg[2]*self.scaleVisualizationFactor[0], borg[3]*self.scaleVisualizationFactor[1])
                painter.drawRect(rect)
                
            for borg in self.component.Imagelist[self.counter.imagenumber].Left:
                painter.setPen(Qt.yellow)
                rect = QRect(borg[0]*self.scaleVisualizationFactor[0], borg[1]*self.scaleVisualizationFactor[1], borg[2]*self.scaleVisualizationFactor[0], borg[3]*self.scaleVisualizationFactor[1])
                painter.drawRect(rect)
                
            for borg in self.component.Imagelist[self.counter.imagenumber].Bottom:
                painter.setPen(Qt.blue)
                rect = QRect(borg[0]*self.scaleVisualizationFactor[0], borg[1]*self.scaleVisualizationFactor[1], borg[2]*self.scaleVisualizationFactor[0], borg[3]*self.scaleVisualizationFactor[1])
                painter.drawRect(rect)

            self.Image.setPixmap(self.pixmap);    
            self.Image.repaint() 
            
#            painter = QPainter(self.pixmap)
#            painter.setBrush(Qt.NoBrush);
#            painter.setPen(Qt.red);              
#            painter.drawRect(QRect(100, 100, 200, 200))
#            self.Image.setPixmap(self.pixmap);
#            self.Image.repaint()    
#            

#            
#            imagecv=self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].image
#            imagecv = cv2.resize(imagecv, (self.parent.imsize[0], self.parent.imsize[1])) 
#            imagegtk=SPM.convertCV2GTK(imagecv)
#            p=imagegtk.get_pixbuf()
#            Gdk.cairo_set_source_pixbuf(cr, p, 0, 0)
#            cr.rectangle(0, 0, self.parent.imsize[0], self.parent.imsize[1])
#            cr.fill()
#            # draw component bbox
#            scale=self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].scale_factor;
#            scaleOCR=self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].scale_factor*self.parent.scale;
#            for borg in self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].Top:
#                b = [x * self.parent.scale for x in borg]
#                cr.set_source_rgb(255, 0, 0)
#                cr.rectangle(b[0], b[1], b[2], b[3]);
#                cr.stroke()
#                if self.parent.selectOCRborder.get_active():  
#                    cr.set_source_rgb(125, 125, 125)
#                    bOCR=[b[0]+self.parent.DSComponent.CompOCRdata.OCRborder_Left*scaleOCR, b[1]+self.parent.DSComponent.CompOCRdata.OCRborder_Top*scaleOCR, b[2]-self.parent.DSComponent.CompOCRdata.OCRborder_Left*scaleOCR-self.parent.DSComponent.CompOCRdata.OCRborder_Right*scaleOCR, b[3]-self.parent.DSComponent.CompOCRdata.OCRborder_Top*scaleOCR-self.parent.DSComponent.CompOCRdata.OCRborder_Bottom*scaleOCR]
#                    cr.rectangle(bOCR[0], bOCR[1], bOCR[2], bOCR[3])
#                    cr.stroke()
#
#            for borg in self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].Right:
#                b = [x * self.parent.scale for x in borg]
#                cr.set_source_rgb(255, 255, 0)
#                cr.rectangle(b[0], b[1], b[2], b[3]);
#                cr.stroke()
#                if self.parent.selectOCRborder.get_active():  
#                    cr.set_source_rgb(125, 125, 125)
#                    bOCR=[b[0]+self.parent.DSComponent.CompOCRdata.OCRborder_Bottom*scaleOCR, b[1]+self.parent.DSComponent.CompOCRdata.OCRborder_Left*scaleOCR, b[2]-self.parent.DSComponent.CompOCRdata.OCRborder_Bottom*scaleOCR-self.parent.DSComponent.CompOCRdata.OCRborder_Top*scaleOCR, b[3]-self.parent.DSComponent.CompOCRdata.OCRborder_Left*scaleOCR-self.parent.DSComponent.CompOCRdata.OCRborder_Right*scaleOCR]
#                    cr.rectangle(bOCR[0], bOCR[1], bOCR[2], bOCR[3])
#                    cr.stroke()
#                                    
#            for borg in self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].Bottom:
#                b = [x * self.parent.scale for x in borg]
#                cr.set_source_rgb(0, 255, 0)
#                cr.rectangle(b[0], b[1], b[2], b[3]);
#                cr.stroke()
#                if self.parent.selectOCRborder.get_active():  
#                    cr.set_source_rgb(125, 125, 125)
#                    bOCR=[b[0]+self.parent.DSComponent.CompOCRdata.OCRborder_Right*scaleOCR, b[1]+self.parent.DSComponent.CompOCRdata.OCRborder_Bottom*scaleOCR, b[2]-self.parent.DSComponent.CompOCRdata.OCRborder_Right*scaleOCR-self.parent.DSComponent.CompOCRdata.OCRborder_Left*scaleOCR, b[3]-self.parent.DSComponent.CompOCRdata.OCRborder_Bottom*scaleOCR-self.parent.DSComponent.CompOCRdata.OCRborder_Top*scaleOCR]
#                    cr.rectangle(bOCR[0], bOCR[1], bOCR[2], bOCR[3])
#                    cr.stroke()
#                    
#            for borg in self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].Left:
#                b = [x * self.parent.scale for x in borg]
#                cr.set_source_rgb(0, 0, 255)
#                cr.rectangle(b[0], b[1], b[2], b[3]);
#                cr.stroke()
#                if self.parent.selectOCRborder.get_active():  
#                    cr.set_source_rgb(125, 125, 125)
#                    bOCR=[b[0]+self.parent.DSComponent.CompOCRdata.OCRborder_Top*scale, b[1]+self.parent.DSComponent.CompOCRdata.OCRborder_Right*scale, b[2]-self.parent.DSComponent.CompOCRdata.OCRborder_Top*scale-self.parent.DSComponent.CompOCRdata.OCRborder_Bottom*scale, b[3]-self.parent.DSComponent.CompOCRdata.OCRborder_Right*scale-self.parent.DSComponent.CompOCRdata.OCRborder_Left*scale]
#                    cr.rectangle(bOCR[0], bOCR[1], bOCR[2], bOCR[3])
#                    cr.stroke()
#            # draw component bbox expected components    
#            if self.parent.selectbbox.get_active():  
#                for borg in self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].Topcorr:
#                    b = [x * self.parent.scale for x in borg]
#                    cr.set_source_rgb(255, 255, 255)
#                    cr.rectangle(b[0], b[1], b[2], b[3]);
#                    cr.stroke()                          
#                for borg in self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].Rightcorr:
#                    b = [x * self.parent.scale for x in borg]
#                    cr.set_source_rgb(255, 255, 255)
#                    cr.rectangle(b[0], b[1], b[2], b[3]);
#                    cr.stroke()
#                for borg in self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].Bottomcorr:
#                    b = [x * self.parent.scale for x in borg]
#                    cr.set_source_rgb(255, 255, 255)
#                    cr.rectangle(b[0], b[1], b[2], b[3]);
#                    cr.stroke()                          
#                for borg in self.parent.DSComponent.Imagelist[self.parent.imagecounter.imagenumber].Leftcorr:
#                    b = [x * self.parent.scale for x in borg]
#                    cr.set_source_rgb(255, 255, 255)
#                    cr.rectangle(b[0], b[1], b[2], b[3]);
#                    cr.stroke()         
        
    def appendBBox(self, x_image, y_image):
        #print('scaleVisualization' + str(self.scaleVisualization))
        x=x_image / self.scaleVisualizationFactor[0]
        y=y_image / self.scaleVisualizationFactor[1]
        
        #print('scale_factor appendBBox: ' + str(self.component.Imagelist[self.counter.imagenumber].scale_factor))
        #print('y1: ' + str(y))
        
        RotIndex = self.ComponentRotationSelect.currentIndex()
        print('RotIndex: ' + str(RotIndex))
        
        if(len(self.component.Imagelist)>0):
            #print('len: ' + str(len(self.component.Imagelist)))
            if self.BBox.isChecked():
                print('bboxrot')
                if RotIndex==0:  # Top
                    height=self.component.Componentheight * self.component.Imagelist[self.counter.imagenumber].scale_factor
                    width=self.component.Componentwidth * self.component.Imagelist[self.counter.imagenumber].scale_factor
                    h2=int(height/2)
                    w2=int(width/2)
                    bbox=[x-w2,y-h2,width,height]
                    #bbox=[x,y,width,height]
                    
                    #print('width: ' + str(self.component.Componentwidth))
                    #print('height: ' + str(self.component.Componentheight))
                    
                    if(len(self.component.Imagelist[self.counter.imagenumber].Top)==0):
                        self.component.Imagelist[self.counter.imagenumber].Top.append(bbox)
                    else:
                        bboxfound=False 
                        for b in self.component.Imagelist[self.counter.imagenumber].Top:
                            if (x>b[0] and x<b[0]+width and y>b[1] and y<b[1]+height):
                                self.component.Imagelist[self.counter.imagenumber].Top.remove(b)
                                bboxfound=True
                        if bboxfound==False:
                            self.component.Imagelist[self.counter.imagenumber].Top.append(bbox)
                    #self.drawRectangle()
                if RotIndex==1:  # Right
                    width=self.component.Componentheight * self.component.Imagelist[self.counter.imagenumber].scale_factor
                    height=self.component.Componentwidth * self.component.Imagelist[self.counter.imagenumber].scale_factor
                    h2=int(height/2)
                    w2=int(width/2)
                    bbox=[x-w2,y-h2,width,height]
                    if(len(self.component.Imagelist[self.counter.imagenumber].Right)==0):
                        self.component.Imagelist[self.counter.imagenumber].Right.append(bbox)
                    else:
                        bboxfound=False 
                        for b in self.component.Imagelist[self.counter.imagenumber].Right:
                            if (x>b[0] and x<b[0]+width and y>b[1] and y<b[1]+height):
                                self.component.Imagelist[self.counter.imagenumber].Right.remove(b)
                                bboxfound=True
                        if bboxfound==False:
                            self.component.Imagelist[self.counter.imagenumber].Right.append(bbox)
                    #self.drawRectangle()              
                if RotIndex==3:  # Bottom
                    height=self.component.Componentheight * self.component.Imagelist[self.counter.imagenumber].scale_factor
                    width=self.component.Componentwidth * self.component.Imagelist[self.counter.imagenumber].scale_factor
                    h2=int(height/2)
                    w2=int(width/2)
                    bbox=[x-w2,y-h2,width,height]
                    if(len(self.component.Imagelist[self.counter.imagenumber].Bottom)==0):
                        self.component.Imagelist[self.counter.imagenumber].Bottom.append(bbox)
                    else:
                        bboxfound=False 
                        for b in self.component.Imagelist[self.counter.imagenumber].Bottom:
                            if (x>b[0] and x<b[0]+width and y>b[1] and y<b[1]+height):
                                self.component.Imagelist[self.counter.imagenumber].Bottom.remove(b)
                                bboxfound=True
                        if bboxfound==False:
                            self.component.Imagelist[self.counter.imagenumber].Bottom.append(bbox)
                    #self.drawRectangle()         
                if RotIndex==2:  # Left
                    width=self.component.Componentheight * self.component.Imagelist[self.counter.imagenumber].scale_factor
                    height=self.component.Componentwidth * self.component.Imagelist[self.counter.imagenumber].scale_factor
                    h2=int(height/2)
                    w2=int(width/2)
                    bbox=[x-w2,y-h2,width,height]
                    if(len(self.component.Imagelist[self.counter.imagenumber].Left)==0):
                        self.component.Imagelist[self.counter.imagenumber].Left.append(bbox)
                    else:
                        bboxfound=False 
                        for b in self.component.Imagelist[self.counter.imagenumber].Left:
                            if (x>b[0] and x<b[0]+width and y>b[1] and y<b[1]+height):
                                self.component.Imagelist[self.counter.imagenumber].Left.remove(b)
                                bboxfound=True
                        if bboxfound==False:
                            self.component.Imagelist[self.counter.imagenumber].Left.append(bbox)                  
            else:
                print('no bboxrot')
                
                bboxfound=False 
                for b in self.component.Imagelist[self.counter.imagenumber].Top:
                    height=self.component.Componentheight * self.component.Imagelist[self.counter.imagenumber].scale_factor
                    width=self.component.Componentwidth * self.component.Imagelist[self.counter.imagenumber].scale_factor
                    if (x>b[0] and x<b[0]+width and y>b[1] and y<b[1]+height):
                        print('delete')
                        #self.component.Imagelist[self.counter.imagenumber].Topcorr.remove(b)
                        self.component.Imagelist[self.counter.imagenumber].Top.remove(b)
                        
                for b in self.component.Imagelist[self.counter.imagenumber].Rightcorr:
                    width=self.component.Componentheight * self.component.Imagelist[self.counter.imagenumber].scale_factor
                    height=self.component.Componentwidth * self.component.Imagelist[self.counter.imagenumber].scale_factor
                    if (x>b[0] and x<b[0]+height and y>b[1] and y<b[1]+width):
                        #self.component.Imagelist[self.counter.imagenumber].Rightcorr.remove(b)
                        self.component.Imagelist[self.counter.imagenumber].Right.remove(b)
                        
                for b in self.component.Imagelist[self.counter.imagenumber].Bottomcorr:
                    height=self.component.Componentheight * self.component.Imagelist[self.counter.imagenumber].scale_factor
                    width=self.component.Componentwidth * self.component.Imagelist[self.counter.imagenumber].scale_factor
                    if (x>b[0] and x<b[0]+width and y>b[1] and y<b[1]+height):
                        #self.component.Imagelist[self.counter.imagenumber].Bottomcorr.remove(b)
                        self.component.Imagelist[self.counter.imagenumber].Bottom.remove(b)
                        
                for b in self.component.Imagelist[self.counter.imagenumber].Leftcorr:
                    width=self.component.Componentheight * self.component.Imagelist[self.counter.imagenumber].scale_factor
                    height=self.component.Componentwidth * self.component.Imagelist[self.counter.imagenumber].scale_factor
                    if (x>b[0] and x<b[0]+height and y>b[1] and y<b[1]+width):
                        #self.component.Imagelist[self.counter.imagenumber].Leftcorr.remove(b)
                        self.component.Imagelist[self.counter.imagenumber].Left.remove(b)
            self.draw()
            self.drawRectangle()  
            
        
            
def isfloat(x):
    try:
        float(x)
    except ValueError:
        return False
    else:
        return True

def isint(x):
    try:
        int(x)
    except ValueError:
        return False
    else:
        return True
    
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    widget = SearchPartGUI()
    widget.show();
    sys.exit(app.exec_())
    
    #b = QWebView()
    #b.show()
    #app.exec_()
    #widget = PDMSGUI()
    #widget.show();
    #sys.exit(app.exec_())
