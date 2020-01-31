#!/usr/bin/python3.7
import gi
from gi.repository import Gtk
import subprocess
from gi.repository import GLib
from gi.repository import Vte as vte
import os
#print(dir(Gtk.Button))

win = Gtk.Window()

v = vte.Terminal()
#v.fork_command('bash')
#v.feed_child('whoami\n')
#v.feed_child('echo test\n')

v.spawn_sync(
    vte.PtyFlags.DEFAULT,
    os.environ['HOME'],
    ["/bin/sh"],
    [],
    GLib.SpawnFlags.DO_NOT_REAP_CHILD,
    None,
    None,
    )
    
#v.show()

win.add(v)


win.show_all()
Gtk.main()
