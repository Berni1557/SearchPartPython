#!/usr/bin/python3
from RegionGrowing import RegionGrowing
import os
from xml.dom.minidom import Document, parse
import zipfile
from SearchPartModules import Imagedata
import numpy as np
from enum import Enum
import cv2
               
class BGClass(Enum): 
    UNKNOWN = 0
    BACKGROUND = 1
    PART = 2
    
class BackgroundDetector(object):
    Imagename = []
    Imagelist = []
    RegionsList = []
    RegionsMap = []
    RegionsClass = []   # 0-unknown, 1-background, 2-part
    ContourImagelist = []
    RegionGrower = None
    Detected = False

    def __init__(self):
        threshold = 10
        reg_size_min=100
        show = True
        scale = 0.03
        self.RegionGrower = RegionGrowing(threshold, reg_size_min, show, scale)

    def setBGClass(self, x, y, imagenumber, classBG, sc):
        
        if self.Detected:
            scalereg = self.RegionGrower.m_scale / sc;
            print('scalereg', scalereg)
            x_image = round(x * scalereg)
            y_image = round(y * scalereg)
            print('x', x_image)
            print('y', y_image)
            regions = self.RegionsList[imagenumber]
            for i, reg in enumerate(regions):
                #print('reg shape: ', reg.shape)
                if reg[y_image, x_image]==255:
                    self.RegionsClass[imagenumber][i] = classBG
                    print('Region found: ', x, y, classBG)
        else:
            print('Region growning was not applyed!')
        
    def regionGrowing(self):
        
        for im in self.Imagelist:
            regions, regionsMap = self.RegionGrower.region_growing(im.image)
            
            print('regionsMap max', np.amax(regionsMap))
            print('regions len', len(regions))
        
            self.RegionsList.append(regions)
            show = False
            ContourImage = self.RegionGrower.drawContours(regions, show)
            self.ContourImagelist.append(ContourImage)
            self.RegionsMap.append(regionsMap)
            
            classlist = []
            for i in range(len(regions)):
                classlist.append(BGClass.UNKNOWN)
                
            self.RegionsClass.append(classlist)
        self.Detected = True
            
    def getRegion(self, index, x, y):
        k = 0
        for im in self.regions[index]:
            if im[x][y] > 0:
                return k
            k = k + 1
        return -1
    
    def create_dom(self):
        
        dom = Document();
        base = dom.createElement('datasetstruct')
        dom.appendChild(base)    
            
        for i, Im in enumerate(self.Imagelist):
            node1 = dom.createElement('Image')
            
            node2 = dom.createElement("Imagename")
            text2 = dom.createTextNode(Im.Imagename)
            node2.appendChild(text2)
            node1.appendChild(node2)
    
            node2 = dom.createElement("Imagepath_relative")
            text2 = dom.createTextNode(Im.Imagepath_relative)      
            node2.appendChild(text2)
            node1.appendChild(node2)
            
            node2 = dom.createElement("RegionsMap")
            directory, base_filename = os.path.split(self.Imagelist[i].Imagepath)
            filename = os.path.splitext(base_filename)[0]
            filepathImageRelative = filename + '_RegionsMap.png'
            text2 = dom.createTextNode(filepathImageRelative)      
            node2.appendChild(text2)
            node1.appendChild(node2)
            
            node2 = dom.createElement("RegionsClass")
            
            c_str='';
            for c in self.RegionsClass[i]:
                c_str = c_str + str(c.value) + ', '
            text2 = dom.createTextNode(c_str)
            node2.appendChild(text2)
            node1.appendChild(node2)
            
            node2 = dom.createElement("Scale_factor")
            text2 = dom.createTextNode(str(Im.scale_factor))
            node2.appendChild(text2)
            node1.appendChild(node2)
          
            dom.childNodes[0].appendChild(node1)                                   
           
        return dom
    
    def write_zipdb(self, filepath_ext):
        
        filepath, file_extension = os.path.splitext(filepath_ext)    
        print('filepath: ' + filepath)
        
        # Create  dom
        dom = self.create_dom()
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
        for Im in self.Imagelist:
            di, base_filename = os.path.split(Im.Imagepath)
            os.chdir(di)
            zipf.write(base_filename) 
        
        # Add RegionsMap
        #folder = os.path.basename(filepath_ext)
        for i, im in enumerate(self.RegionsMap):
            directory, base_filename = os.path.split(self.Imagelist[i].Imagepath)
            filename = os.path.splitext(base_filename)[0]
            filepathImage = directory + '/' + filename + '_RegionsMap.png'
            #print('path: ', directory, base_filename, filepathImage)
            cv2.imwrite(filepathImage, im)
            di, base_filename = os.path.split(filepathImage)
            os.chdir(di)
            zipf.write(base_filename) 
            os.remove(filepathImage)
        zipf.close()
        
        print('RegionsMap max', np.amax(self.RegionsMap[0]))
        print('RegionsClass', len(self.RegionsClass[0]))
    
    def read_zipdb(self, filepath, StatusLine):
        
        #print('filepath1: ' + filepath)
        
        base_folder, base_filename = os.path.split(filepath)
        
        
        str1=base_filename.split('.')
        filename = str1[0]
        xmlname=str1[0] + '.xml'
        zipf = zipfile.ZipFile(filepath, 'r')
        zipf.extract(xmlname,base_folder)
        zipf.extractall(base_folder + '/' + filename)
        
        str1=base_filename.split('.')
        
        xmlpath=base_folder + '/'+ xmlname
        dom = parse(xmlpath)
        os.remove(xmlpath)
        
        images=dom.getElementsByTagName('Image')
        for image in images:

            # Read image
            node=image.getElementsByTagName('Imagepath_relative')
            Imagepath_relative=node[0].childNodes[0].nodeValue
            Imagepath = base_folder + '/' + filename + '/' + Imagepath_relative
            Im=Imagedata(Imagepath)
            node=image.getElementsByTagName('Imagename')
            Im.Imagename=node[0].childNodes[0].nodeValue
            
            # Read RegionsMap
            node=image.getElementsByTagName('RegionsMap')
            RegionsMapPath=node[0].childNodes[0].nodeValue
            Imagepath = base_folder + '/' + filename + '/' + RegionsMapPath
            print('RegionsMapPath', Imagepath)
            imageCV=cv2.imread(Imagepath, cv2.IMREAD_ANYDEPTH)
            self.RegionsMap.append(imageCV) 
                        
            StatusLine.append('reading image: ' + Im.Imagename)

            self.Imagelist.append(Im)
            self.Imagename.append(Im.Imagename)
            
            # Read RegionsClass
            node=image.getElementsByTagName('RegionsClass')
            map_str=node[0].childNodes[0].nodeValue
            map_list = map_str.split(',')
            map_list=map_list[:-1]
            print('map_list', map_list)
            map_list_img = []
            for i in map_list:
                map_list_img.append(BGClass(int(i)))
            self.RegionsClass.append(map_list_img)
            print('map_list_img len', len(map_list_img))
            
            
        self.RegionsList = self.createRegions(self.RegionsMap)
        print('RegionsList len', len(self.RegionsList[0]))
        
        for reg in self.RegionsList:
            ContourImage = self.RegionGrower.drawContours(reg, False)
            self.ContourImagelist.append(ContourImage)
            
        
            
    def createRegions(self, RegionsMap):
        RegionsList = []
        for im in self.RegionsMap:
            m = np.amax(im)
            dims = im.shape
            rlist=[]
            for i in range(m):
                reg = np.zeros((dims[0], dims[1], 1), np.uint8)
                reg[np.where(np.equal(im, i))] = 255
                rlist.append(reg)           
            RegionsList.append(rlist)   
        return RegionsList


   