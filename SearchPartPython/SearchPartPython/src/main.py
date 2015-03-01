#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
import os
import numpy as np
import cv2
from matplotlib import pyplot as plt
import matlab_wrapper


# SP_gui

def xpm_label_box(parent, xpm_filename, label_text):
    # Create box for xpm and label
    box1 = gtk.HBox(False, 0)
    box1.set_border_width(2)

    # Now on to the image stuff
    image = gtk.Image()
    image.set_from_file(xpm_filename)

    # Create a label for the button
    label = gtk.Label(label_text)

    # Pack the pixmap and label into the box
    box1.pack_start(image, False, False, 3)
    box1.pack_start(label, False, False, 3)

    image.show()
    label.show()
    return box1
 

class Buttons:
    # Our usual callback method
    def callback(self, widget, data=None):
        print "Hello again - %s was pressed" % data

    def __init__(self):
        # Create a new window
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)

        self.window.set_title("Image'd Buttons!")

        # It's a good idea to do this for all windows.
        self.window.connect("destroy", lambda wid: gtk.main_quit())
        self.window.connect("delete_event", lambda a1,a2:gtk.main_quit())

        # Sets the border width of the window.
        self.window.set_border_width(10)

        # Create a new button
        button = gtk.Button()

        # Connect the "clicked" signal of the button to our callback
        button.connect("clicked", self.callback, "cool button")

        # This calls our box creating function
        box1 = xpm_label_box(self.window, "info.xpm", "cool button")

        # Pack and show all our widgets
        button.add(box1)

        box1.show()
        button.show()

        self.window.add(button)
        self.window.show()


# matlab stuff
"""
os.environ["MATLABROOT"] = "/usr/local/MATLAB/R2011a"
matlab = matlab_wrapper.MatlabSession()

img = cv2.imread('/home/bernifoellmer/workspace/project1/lena.bmp')


cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()

matlab.put('I', img)
matlab.eval('I1=I+100')
I1 = matlab.get('I1')

cv2.imshow('image',I1)
cv2.waitKey(0)
cv2.destroyAllWindows()
"""
def main():
    gtk.main()
    return 0   

if __name__ == "__main__":
    Buttons()
    main()