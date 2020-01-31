#!/usr/bin/python3.7
import gi
from gi.repository import Gtk
import subprocess
from gi.repository import GLib
#print(dir(Gtk.Button))

proc=None

def me_clicked0(myself):
  global proc
  print('clicked' + myself.get_label())
  #proc = subprocess.Popen("/root/micros-connect/stxetxcut_tty.py", shell = True, stdout = subprocess.PIPE)
  #proc = subprocess.Popen("/usr/bin/inotifywait -m /root/inbox0 -e create -e moved_from", shell = False, stdout = subprocess.PIPE)
  proc = subprocess.Popen("/bin/ls", shell = False, stdout = subprocess.PIPE)
  print ("Process ID" , proc.pid)


def mp(self):
  print(self)
  
def get_micros0_buffer(myself):
  print ("Process ID" , proc.pid)
  print ("Process Buffer" , proc.stdout,flush=True)

  
win = Gtk.Window()
bbox=Gtk.HButtonBox()

button0 = Gtk.Button.new_with_label("Start Micros-60 (0)")
button00 = Gtk.Button.new_with_label("Get Micros-60 (0) buffer")

#button1.connect("clicked", start_one())

bbox.add(button0)
bbox.add(button00)
win.add(bbox)

button0.connect("clicked", me_clicked0)
button00.connect("clicked", get_micros0_buffer)

win.show_all()
Gtk.main()
