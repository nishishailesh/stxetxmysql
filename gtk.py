#!/usr/bin/python3.7
import gi
from gi.repository import Gtk
import subprocess
from gi.repository import glib
import glib

print(dir(Gtk.Button))

def me_clicked(myself):
  print('clicked' + myself.get_label())
  proc = subprocess.Popen("/root/micros-connect/stxetxcut_tty.py", shell = True)
  glib.io_add_watch(proc.stdout, # file descriptor
						glib.IO_IN,  # condition
                        self.write_to_buffer ) # callback

win = Gtk.Window()
bbox=Gtk.HButtonBox()

button1 = Gtk.Button.new_with_label("Start Micros-60 (1)")
button2 = Gtk.Button.new_with_label("Start Micros-60 (2)")
button3 = Gtk.Button.new_with_label("Start Micros-60 (3)")

#button1.connect("clicked", start_one())

bbox.add(button1)
bbox.add(button2)
bbox.add(button3)
win.add(bbox)

button1.connect("clicked", me_clicked)
button2.connect("clicked", me_clicked)
button3.connect("clicked", me_clicked)
win.show_all()
Gtk.main()
