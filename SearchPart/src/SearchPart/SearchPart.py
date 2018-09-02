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
from BackgroundDetector import BackgroundDetector, BGClass

from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtGui import QPainter, QColor, QBrush
from PyQt5.QtGui import QPen, QPainter, QColor, QBrush, QPainterPath, QFont
from PyQt5.QtWidgets import QWidget, QGraphicsObject, QStyleOptionGraphicsItem
from PyQt5.QtCore import Qt, QTimer, QRectF

from PyQt5.QtCore import pyqtSignal, Qt, QDir, QFile, QFileInfo, QPoint, QTextStream, QTimer, QUrl, QRect
import timeit

    
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
    scaleVisualizationBG = [800,600]
    scaleVisualizationFactorBG = [1.0, 1.0]
    bboxrot = [True,False,False,False]
    pixmap = None
    pixmapBG = None
    backgroundDetector = BackgroundDetector()
    showContoursClass = True
    
    def __init__(self):
        # Init GUI      
        super(SearchPartGUI,self).__init__()
        loadUi('../qt/SearchPartGUI_V17.ui',self)
        self.setWindowTitle('SearchPart')
        
        self.StatusLine.append("Initialization started")

        
        # Set callbacks
        self.CreateCompDataset.clicked.connect(self.on_button_CreateCompDataset)
        self.LoadCompDataset.clicked.connect(self.on_button_LoadCompDataset)
        self.SaveCompDataset.clicked.connect(self.on_button_SaveCompDataset)
        
        self.LoadBackgroundModel.clicked.connect(self.on_button_LoadBackgroundModel)
        self.SaveBackgroundModel.clicked.connect(self.on_button_SaveBackgroundModel)
        
        self.ComponentName.editingFinished.connect(self.on_ComponentName);
        self.ComponentDatasetPath.editingFinished.connect(self.on_ComponentDatasetPath)
        self.ComponentWidth.editingFinished.connect(self.on_ComponentWidth)
        self.ComponentHeight.editingFinished.connect(self.on_ComponentHeight)
        self.BorderSize.editingFinished.connect(self.on_BorderSize)
        self.ComponentID.editingFinished.connect(self.on_ComponentID)
        
        self.OCRText.editingFinished.connect(self.on_OCRText)
        self.OCRAxialSymmetricHorizontal.stateChanged.connect(self.on_OCRAxialSymmetricHorizontal)
        self.OCRAxialSymmetricVertical.stateChanged.connect(self.on_OCRAxialSymmetricVertical)
        
        self.OCROnlineDataBase.editingFinished.connect(self.on_OCROnlineDataBase)
        self.AxialSymmetricHorizontal.stateChanged.connect(self.on_AxialSymmetricHorizontal)
        self.AxialSymmetricVertical.stateChanged.connect(self.on_AxialSymmetricVertical)
        self.ComponentDescription.textChanged.connect(self.on_ComponentDescription)
        
        self.Back.clicked.connect(self.on_button_Back);
        self.Next.clicked.connect(self.on_button_Next);
        
        self.BackBG.clicked.connect(self.on_button_BackBG);
        self.NextBG.clicked.connect(self.on_button_NextBG);
        
        self.BBox.stateChanged.connect(self.on_BBox)
        #self.DeleteBBox.clicked.connect(self.on_DeleteBBox);
        self.ComponentMean.clicked.connect(self.on_ComponentMean)
        self.AddImage.clicked.connect(self.on_AddImage)
        self.DeleteImage.clicked.connect(self.on_DeleteImage)
        self.ImageNumber.setText(self.counter.tostring())
        self.ImageScale.setText(self.scale())
        
        self.Image.mousePressEvent = self.getPosition
        self.ImageBG.mousePressEvent = self.getPositionBG
        
        self.LoadBackgroundImages.clicked.connect(self.on_LoadBackgroundImages)
        
        
        self.component=SPM.Component(self,None)
        
        self.counter=SPM.imagecounter()
        self.counterBG=SPM.imagecounter()
        
        self.RegionGrowing.clicked.connect(self.on_button_RegionGrowing)
        self.ShowContours.stateChanged.connect(self.on_ShowContours)
        
        self.update_componentdata()
        self.update_backgrounddata()
        
        self.reset()
        self.draw()
        self.drawRectangle()
        
        self.StatusLine.append("Initialization finished")
    
    @pyqtSlot()
    def on_ShowContours(self):
        self.showContoursClass = self.ShowContours.isChecked()
        self.drawBG()
        
    @pyqtSlot()
    def on_button_RegionGrowing(self):
        self.StatusLine.append('Starting region growing')
        self.backgroundDetector.regionGrowing()
        self.update_backgrounddata()
        self.drawBG()
        self.StatusLine.append('Finished region growing')
        
    @pyqtSlot()
    def on_button_SaveBackgroundModel(self):
        self.StatusLine.append('Saving background model started')
        filedialog = QFileDialog.getSaveFileName(self, "Select background model file", '', '*.zip')
        filepath = filedialog[0]
        #self.ComponentDatasetPath.setText(filepath)
        #filepath = 'H:/Projects/SearchPartPython/SearchPartPython1/SearchPart/data/file.zip'
        creatable = SPM.is_path_exists_or_creatable(filepath)
        if creatable:
            #SPM.write_zipdb(self.component, filepath)
            self.backgroundDetector.write_zipdb(filepath)
        else:
            self.StatusLine.append('Can not create file: ' + filepath)
        self.StatusLine.append('Saving background model finished')
        
    @pyqtSlot()
    def on_button_LoadBackgroundModel(self):
        self.StatusLine.append("Loading background model started")
        filedialog = QFileDialog.getOpenFileName(self, "Select background model file", '', '*.zip')
        filepath = filedialog[0]
        #self.ComponentDatasetPath.setText(filepath)
        #self.component = SPM.read_zipdb(self.component, filepath, self.StatusLine)
        self.backgroundDetector.read_zipdb(filepath, self.StatusLine)
        
        self.update_backgrounddata();
        if self.backgroundDetector.RegionsDetected[self.counterBG.imagenumber] == True:
            print('test1')
            self.backgroundDetector.RegionsList[self.counterBG.imagenumber] = self.backgroundDetector.createRegions(self.backgroundDetector.RegionsMap, self.counterBG.imagenumber)
        self.drawBG()
        self.StatusLine.append("Loading background model finished")
        
    @pyqtSlot()
    def on_LoadBackgroundImages(self):
        names = QFileDialog.getOpenFileNames(self,  'Open file','H:/Projects/SearchPartPython/SearchPartPython/SearchPart/data/images/',"Images (*.png *.tiff *.jpg)")
        filenames = names[0];
        
        if len(filenames)>0:
            k=0
            for f in filenames:
                k=k+1
                #print('Loading: ' + f + '; Image ' + str(k) + '/' + str(len(filenames)))
                self.StatusLine.append('Loading: ' + f + '; Image ' + str(k) + '/' + str(len(filenames)))
                Imname=os.path.basename(f)
                Im=SPM.Imagedata(f)
                if not Im.scale_factor==False:
                    self.backgroundDetector.Imagelist.append(Im)
                    self.backgroundDetector.RegionsDetected.append(False)
                    self.backgroundDetector.RegionsClass.append([])
                    self.backgroundDetector.RegionsList.append([])
                    self.backgroundDetector.RegionsMap.append(None)
            time.sleep(0.2)
            self.counterBG = SPM.imagecounter(0, len(self.backgroundDetector.Imagelist)-1)
            self.update_backgrounddata()
            self.drawBG()
            
            self.StatusLine.append("Added image " + Imname)
        else:
            self.StatusLine.append("No image selected.")
        
    def getPosition(self , event):
        x = event.pos().x()
        y = event.pos().y()
        self.appendBBox(x, y)
        
    def getPositionBG(self , event):
        
        start = timeit.default_timer()

        x = event.pos().x()
        y = event.pos().y()
        idx = self.LabelBG.currentIndex()
        sc = self.scaleVisualizationFactorBG[0]
        self.backgroundDetector.setBGClass(x, y, self.counterBG.imagenumber, BGClass(idx), sc)
        self.drawBG()
        
        stop = timeit.default_timer()
        print('Time: ', stop - start)  

        
    def scale(self):
        if (self.counter.imagenumber > -1):
            s = str(round(self.component.Imagelist[self.counter.imagenumber].scale_factor,2)) + ' [p/mm]'
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
            #print('Loading: ' + f + '; Image ' + str(k) + '/' + str(len(filenames)))
            self.StatusLine.append('Loading: ' + f + '; Image ' + str(k) + '/' + str(len(filenames)))
            Imname=os.path.basename(f)
            Im=SPM.Imagedata(f)
            if not Im.scale_factor==False:
                self.component.Imagename.append(Imname)
                self.component.Imagelist.append(Im)                          
        time.sleep(0.2)
        self.update_componentdata()
        self.StatusLine.append("Added image " + Imname)
        
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
        self.drawRectangle()
        
    @pyqtSlot()
    def on_button_Next(self):
        if(self.counter.imagenumber<self.counter.imagenumber_max):
            self.counter.imagenumber=self.counter.imagenumber+1;
        self.update_componentdata()
        self.draw()
        self.drawRectangle()
        
    @pyqtSlot()
    def on_button_BackBG(self):
        self.backgroundDetector.RegionsList[self.counterBG.imagenumber]=None
        if(self.counterBG.imagenumber>0):
            self.counterBG.imagenumber=self.counterBG.imagenumber-1
        if self.backgroundDetector.RegionsDetected[self.counterBG.imagenumber] == True:
            self.backgroundDetector.RegionsList[self.counterBG.imagenumber] = self.backgroundDetector.createRegions(self.backgroundDetector.RegionsMap, self.counterBG.imagenumber)
        self.update_backgrounddata()
        self.drawBG()
        
    @pyqtSlot()
    def on_button_NextBG(self):
        self.backgroundDetector.RegionsList[self.counterBG.imagenumber]=None
        if(self.counterBG.imagenumber<self.counterBG.imagenumber_max):
            self.counterBG.imagenumber=self.counterBG.imagenumber+1;
        if self.backgroundDetector.RegionsDetected[self.counterBG.imagenumber] == True:
            self.backgroundDetector.RegionsList[self.counterBG.imagenumber] = self.backgroundDetector.createRegions(self.backgroundDetector.RegionsMap, self.counterBG.imagenumber)
        
        self.update_backgrounddata()
        self.drawBG()
        
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
    def on_OCROnlineDataBase(self):
        self.component.CompOCRdata.OCROnlineDataBase = self.OCROnlineDataBase.text()
        
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
        self.StatusLine.append('Saving component started')
        filedialog = QFileDialog.getSaveFileName(self, "Select component file", '', '*.zip')
        filepath = filedialog[0]
        self.ComponentDatasetPath.setText(filepath)
        #filepath = 'H:/Projects/SearchPartPython/SearchPartPython1/SearchPart/data/file.zip'
        creatable = SPM.is_path_exists_or_creatable(filepath)
        if creatable:
            SPM.write_zipdb(self.component, filepath)
        else:
            self.StatusLine.append('Can not create file: ' + filepath)
        self.StatusLine.append('Saving component finished')
        
    @pyqtSlot()
    def on_button_LoadCompDataset(self):
        self.StatusLine.append("Loading component started")
        filedialog = QFileDialog.getOpenFileName(self, "Select component file", '', '*.zip')
        filepath = filedialog[0]
        self.ComponentDatasetPath.setText(filepath)
        self.component = SPM.read_zipdb(self.component, filepath, self.StatusLine)
        self.update_componentdata();
        self.draw()
        self.StatusLine.append("Loading component finished")
        
    def on_key(self):
        self.on_button_search()
        
    def reset(self):
        self.StatusLine.append("Resetting component")
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
  
    def update_componentdata(self):
        self.counter.imagenumber_max=len(self.component.Imagelist)-1
        
        if(self.counter.imagenumber==-1):
            self.counter.imagenumber=0
            
        #self.counter.imagenumber = 1
        if(self.counter.imagenumber>self.counter.imagenumber_max):
            self.counter.imagenumber=self.counter.imagenumber_max
        
        self.ComponentName.setText(self.component.Componentname)
        self.ComponentHeight.setText(str(self.component.Componentheight))
        self.ComponentWidth.setText(str(self.component.Componentwidth))
        self.ComponentID.setText(str(self.component.ComponentID))
        self.BorderSize.setText(str(self.component.Componentborder))
        
        
        self.AxialSymmetricHorizontal.setChecked(self.component.AxialSymmetricHorizontal)
        self.AxialSymmetricVertical.setChecked(self.component.AxialSymmetricVertical)
        
        self.OCRAxialSymmetricHorizontal.setChecked(self.component.CompOCRdata.OCRAxialSymmetricHorizontal)
        self.OCRAxialSymmetricVertical.setChecked(self.component.CompOCRdata.OCRAxialSymmetricVertical)
        
        self.OCROnlineDataBase.setText(self.component.CompOCRdata.OCROnlineDataBase)
        self.OCRText.setText(self.component.CompOCRdata.OCRText)
        self.ComponentDescription.setText(self.component.Componentdescription);
        
        self.BBox.setChecked(self.showBBox)
        
        self.ImageNumber.setText(self.counter.tostring()) 
        self.ImageScale.setText(self.scale()) 
        self.draw()
        
    def update_backgrounddata(self):
        self.counterBG.imagenumber_max=len(self.backgroundDetector.Imagelist)-1
        if(self.counterBG.imagenumber==-1):
            self.counterBG.imagenumber=0
        if(self.counterBG.imagenumber>self.counterBG.imagenumber_max):
            self.counterBG.imagenumber=self.counterBG.imagenumber_max
        self.ImageNumberBG.setText(self.counterBG.tostring()) 
        
        self.ShowContours.setChecked(self.showContoursClass)
        
        self.drawBG()

    def drawBG(self):
        
        if self.counterBG.valid():
            imagecv = self.backgroundDetector.Imagelist[self.counterBG.imagenumber].image          
            self.scaleVisualizationFactorBG[0] = self.scaleVisualizationBG[0] / imagecv.shape[1]
            self.scaleVisualizationFactorBG[1] = self.scaleVisualizationBG[1] / imagecv.shape[0]
            imagecv = cv2.resize(imagecv, (self.scaleVisualizationBG[0], self.scaleVisualizationBG[1])) 
            
            if self.showContoursClass:
                if (len(self.backgroundDetector.RegionsList) > self.counterBG.imagenumber and (self.backgroundDetector.RegionsList[self.counterBG.imagenumber] is not None) and self.backgroundDetector.RegionsDetected[self.counterBG.imagenumber]):
                    regions = self.backgroundDetector.RegionsList[self.counterBG.imagenumber]                
                    ## Show contours
                    image_cont = np.zeros((self.scaleVisualizationBG[1], self.scaleVisualizationBG[0], 3), np.uint8)
                    for i, im in enumerate(regions):
                        im_res = cv2.resize(im, (self.scaleVisualizationBG[0], self.scaleVisualizationBG[1]))
                        _, contours, hierarchy = cv2.findContours(im_res.astype(np.uint8), cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)                  
                        cv2.drawContours(image_cont, contours, -1, [255,255,255], 1); 
                    imagecv[np.where((image_cont==[255,255,255]).all(axis=2))] = [255,255,255]
                
                    # Draw classes
                    for i, im in enumerate(regions):                 
                        if self.backgroundDetector.RegionsClass[self.counterBG.imagenumber][i]==BGClass.BACKGROUND:
                            im_res = cv2.resize(im, (self.scaleVisualizationBG[0], self.scaleVisualizationBG[1]))
                            mask = np.zeros((self.scaleVisualizationBG[1], self.scaleVisualizationBG[0], 3), np.uint8)
                            mask[:,:,0]=im_res
                            mask[:,:,1]=im_res
                            mask[:,:,2]=im_res
                            imagecv[np.where((mask==[255,255,255]).all(axis=2))] = [255,0,0]
                        if self.backgroundDetector.RegionsClass[self.counterBG.imagenumber][i]==BGClass.PART:
                            im_res = cv2.resize(im, (self.scaleVisualizationBG[0], self.scaleVisualizationBG[1]))
                            mask = np.zeros((self.scaleVisualizationBG[1], self.scaleVisualizationBG[0], 3), np.uint8)
                            mask[:,:,0]=im_res
                            mask[:,:,1]=im_res
                            mask[:,:,2]=im_res
                            imagecv[np.where((mask==[255,255,255]).all(axis=2))] = [0,0,250]    
                                   
            image = QtGui.QImage(imagecv.data, imagecv.shape[1], imagecv.shape[0], imagecv.strides[0], QtGui.QImage.Format_RGB888).rgbSwapped()
            self.pixmapBG = QtGui.QPixmap(image)
            self.ImageBG.setPixmap(self.pixmapBG)

        else:
            imagecv = np.zeros((self.scaleVisualizationBG[1], self.scaleVisualizationBG[0], 3), np.uint8)           
            self.scaleVisualizationFactorBG[0] = self.scaleVisualizationBG[0] / imagecv.shape[1]
            self.scaleVisualizationFactorBG[1] = self.scaleVisualizationBG[1] / imagecv.shape[0]
            imagecv = cv2.resize(imagecv, (self.scaleVisualizationBG[0], self.scaleVisualizationBG[1])) 
            image = QtGui.QImage(imagecv.data, imagecv.shape[1], imagecv.shape[0], imagecv.strides[0], QtGui.QImage.Format_RGB888)
            self.pixmapBG = QtGui.QPixmap(image)
            self.ImageBG.setPixmap(self.pixmapBG)

    def draw(self):

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
