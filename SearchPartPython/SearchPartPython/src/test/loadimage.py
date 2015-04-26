#!/usr/bin/env python

# example images.py

import pygtk
pygtk.require('2.0')
import gtk


window = gtk.Window()

window.show()


image = gtk.Image()
#window.add(image)
image.set_from_file("apple-red.png")
image.show()

#cm = image.get_colormap()
area = gtk.DrawingArea()
window.add(image)
"""
gc = area.style.fg_gc[gtk.STATE_NORMAL]
#gc=gtk.gdk.GC
gc = image.get_style().black_gc

image.window.draw_rectangle(gc, False, 2, 2, 20, 20)

gtk.gdk.draw_polygon()

"""
#p=Gtk.gdk.Pixbuf

gtk.main()
