#!/usr/bin/env python
from gi.repository.GdkPixbuf import Pixbuf
# example drawingarea.py
from gi.repository import Gtk
#from gi.repository import Gdk
from gi.repository import GdkPixbuf
#from gi.repository import GObject

import pygtk
import SearchPartModules as SPM
pygtk.require('2.0')


import cv
import cv2
import numpy as np
from cv2.cv import *

from PIL import Image

image_gtk = Gtk.Image()

source=cv2.imread('/home/bernifoellmer/workspace/SearchPartPython_V01/lena.jpeg')
image_gtk=SPM.convertCV2GTK(source)

image_gtk.show()
window = Gtk.Window()
window.add(image_gtk)
window.show()


Gtk.main()
