#!/usr/bin/python3.4
__author__ = 'muratov'

from gi.repository import Gtk
from gi.repository import Gdk


class Handler:
    counter = 0

    def searchBoxChanged(self, sBox):
        print(sBox.get_text())


    def deleteMain(self, *args):
        Gtk.main_quit(*args)


    def keyPressEvnt(self, sBox, event):
        """
        Умеет перехватывать клик по таб
        :param sBox:
        :param event:
        :return:
        """
        keyname = Gdk.keyval_name(event.keyval)
        print("Key %s (%d) was pressed" % (keyname, event.keyval))


builder = Gtk.Builder()
builder.add_from_file("gui_glade_2.glade")
builder.connect_signals(Handler())

window = builder.get_object("mainWindow")
answerBox = builder.get_object("answerBox")

window.show_all()

Gtk.main()
