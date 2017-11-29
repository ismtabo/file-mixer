#! /usr/bin/python3

import os
import sys

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from .main_view import MainView

BASE_DIR = os.path.dirname(__file__)

builder = Gtk.Builder()
builder.add_from_file(os.path.join(BASE_DIR, 'file-mixer.gui.glade'))


win = MainView(builder, "window1")
win.show_all()
Gtk.main()
