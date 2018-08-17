#!/usr/bin/python3
import sys
from PyQt5 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QCheckBox, QApplication, QMainWindow, QFileDialog
from PyQt5.uic import loadUi
import time
import string

class SearchPartGUI(QMainWindow):
    
    keyPressed = QtCore.pyqtSignal(QtCore.QEvent)
    
    def __init__(self):
        
        # Init GUI      
        super(SearchPartGUI,self).__init__()
        loadUi('../qt/SearchPartGUI_V06.ui',self)
        self.setWindowTitle('SearchPart')

        # Set callbacks
        self.SelectDataset.clicked.connect(self.on_button_SelectDataset);
        self.CreateDataset.clicked.connect(self.on_button_CreateDataset);
        self.SelectComponentPath.clicked.connect(self.on_button_SelectComponentPath);
        
        
    @pyqtSlot()
    def on_button_SelectDataset(self):
        print("test")
        txt = self.ComponentName.text()
        print(txt)
        print("test1")
    
    @pyqtSlot()
    def on_button_CreateDataset(self):
        print("Create new dataset!")
        self.reset()

    @pyqtSlot()
    def on_button_SelectComponentPath(self):
        print("file")
        file = str(QFileDialog.getOpenFileName(self, "Select Component Directory"))
        print(file)
        
    def on_key(self):
        self.on_button_search()
        
    def reset(self):
        self.ComponentHeight.setText('0')
        self.ComponentWidth.setText('0')
        self.ComponentID.setText('0')
        self.BorderSize.setText('0')
        self.ComponentName.setText('0')
        
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
