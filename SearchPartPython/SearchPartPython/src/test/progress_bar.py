from gi.repository import Gtk, GObject
import time
class ProgressBarWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="ProgressBar Demo")
        self.set_border_width(20)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        self.progressbar = Gtk.ProgressBar()
        vbox.pack_start(self.progressbar, True, True, 0)
        self.activity_mode = False

    def set_value(self, new_value):
        self.progressbar.set_fraction(new_value)
        
    def add_value(self, value):
        new_value=value + self.progressbar.get_fraction()
        self.progressbar.set_fraction(new_value)

win = ProgressBarWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
