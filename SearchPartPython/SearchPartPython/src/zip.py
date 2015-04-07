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
import time
import zipfile


filepath="/home/bernifoellmer/Studium/SearchPartPython/SearchPartPython/SearchPartPython/SearchPartPython/data/compsa.zip"
path="/home/bernifoellmer/Studium/SearchPartPython/SearchPartPython/SearchPartPython/SearchPartPython/data/GTKfile/"

di, base_filename = os.path.split(filepath)

str1=base_filename.split('.')
xmlname=str1[0] + '.xml'
zipf = zipfile.ZipFile(filepath, 'r')
zipf.extract(xmlname,di)

str1=base_filename.split('.')

xmlpath=di + '/'+ xmlname
print xmlpath
dom = parse(xmlpath)

st=dom.toprettyxml()
#print st


#Creation_date=dom.getElementsByTagName('Creation_date').item(0).firstChild.nodeValue

#print Creation_date

#Images=dom.getElementsByTagName('Images')

#for n in Images:
#                print n.childNodes[0].nodeValue


#print dom.childNodes.item(0).childNodes[13].childNodes[1].childNodes[1]

images=dom.getElementsByTagName('Image')
for image in images:
    imagename=image.getElementsByTagName('Imagename')
    print imagename[0].childNodes[0].nodeValue
    
    n1=image.getElementsByTagName('Top')
    for n2 in n1:
        it=n2.getElementsByTagName('item')
        for i in it:
            print i.childNodes[0].nodeValue
    #print n1.childNodes[1].childNodes[0].nodeValue
    #for n2 in n1.childNodes:
    #    print n2





"""
node=dom.getElementsByTagName('Top')
for n in node:
    for n1 in n.childNodes:
        if(n1.hasChildNodes()==True):
            print n1.childNodes[0].nodeValue


node=dom.getElementsByTagName('Left')
for n in node:
    for n1 in n.childNodes:
        if(n1.hasChildNodes()==True):
            print n1.childNodes[0].nodeValue
            
"""