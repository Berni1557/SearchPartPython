from gi.repository import Gtk
from numpy import *
import sys
sys.path.append("/usr/local/lib/python2.7/site-packages")
#a=array([1,2,3,4])
class Handler:
    def onDeleteWindow(self, *args):
        Gtk.main_quit(*args)

    def onButtonPressed(self, CheckButton):
        print("Hello World!")
        
    def new_component_select_cb(self, item):
        print("Hello new!")
        
    def open_component_select_cb(self, item):
        print("Hello new!")

    def save_component_select_cb(self, item):
        print("Hello save!")

    def resize(self, item):
        print("Hello resize!")

    def resize1(self, item):
        print("Hello resize1!")
        
        
builder = Gtk.Builder()
builder.add_from_file("/home/bernifoellmer/Studium/SearchPartPython/SearchPartPython/SearchPartPython/SearchPartPython/glade/SearchPartGlade.glade")

listb=builder.get_objects()
print(listb)
builder.connect_signals(Handler())



window = builder.get_object("window1")
window.maximize()
window.show_all()
a = array([[1,2,3,4],[5,6,7,8]])
Gtk.main()