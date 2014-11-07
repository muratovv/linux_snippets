#! /usr/bin/env python3
__author__ = 'flire'

from gi.repository import Gtk

class EditorWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Snippets editor")
        self.set_size_request(800, 400)
        self.set_resizable(False)
        self.set_border_width(5)

        self.box = Gtk.HBox(spacing=10)
        self.box.set_size_request(800,400)
        self.add(self.box)

        self.leftbox = Gtk.VBox(spacing = 10);
        self.box.set_size_request(400,400)
        self.box.pack_start(self.leftbox, True, True, 0)

        self.scroll = Gtk.ScrolledWindow()
        self.scroll.set_hexpand(False)
        self.scroll.set_vexpand(True)

        self.store = Gtk.ListStore(str)
        self.store.append(["label1"])
        self.store.append(["label2"])
        self.store.append(["label3"])
        self.store.append(["label4"])
        self.store.append(["label5"])
        self.store.append(["label6"])
        self.store.append(["label7"])
        self.store.append(["label8"])
        self.store.append(["label9"])
        self.store.append(["label10"])
        self.store.append(["label11"])
        self.store.append(["label12"])
        self.store.append(["label13"])
        self.store.append(["label14"])
        self.store.append(["label15"])
        self.store.append(["label16"])
        self.store.append(["label17"])
        self.store.append(["label18"])
        self.store.append(["label19"])


        self.labels_list = Gtk.TreeView(self.store)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Snippet label", renderer, text=0)
        self.labels_list.append_column(column)

        self.scroll.add(self.labels_list)
        self.scroll.set_size_request(400,350)
        self.leftbox.pack_start(self.scroll, True, True, 0)

        self.buttons_box = Gtk.HBox(spacing = 10)
        self.buttons_box.set_size_request(50,50)
        self.leftbox.pack_start(self.buttons_box, True, True, 0)

        self.add_button = Gtk.Button(label="Add")
        self.add_button.set_size_request(50,50)
        self.buttons_box.pack_start(self.add_button, True, True, 0)

        self.delete_button = Gtk.Button(label="Delete")
        self.delete_button.set_size_request(50,50)
        self.buttons_box.pack_start(self.delete_button, True, True, 0)

        self.rightbox = Gtk.Box(spacing=10)
        self.rightbox.set_size_request(400,400)
        self.box.pack_start(self.rightbox, True, True, 0)

        self.entry = Gtk.Entry()
        self.rightbox.pack_start(self.entry, True, True, 0)
