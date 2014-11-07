#! /usr/bin/env python3
__author__ = 'flire'

from gi.repository import Gtk

from src.snippetParser import SnippetParser

class EditorWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Snippets editor")
        self.set_size_request(800, 400)
        self.set_resizable(False)
        self.set_border_width(5)

        self.box = Gtk.HBox(spacing=10)
        self.box.set_size_request(800, 400)
        self.add(self.box)

        self.leftbox = Gtk.VBox(spacing=10);
        self.box.set_size_request(400, 400)
        self.box.pack_start(self.leftbox, True, True, 0)

        self.scroll = Gtk.ScrolledWindow()
        self.scroll.set_hexpand(False)
        self.scroll.set_vexpand(True)

        self.parser = SnippetParser("src/snippets")
        self.snippets = self.parser.snippets

        self.store = Gtk.ListStore(str)

        for snip in self.snippets:
            self.store.append([snip["label"]])


        self.labels_list = Gtk.TreeView(self.store)
        select = self.labels_list.get_selection()
        select.connect("changed", self.on_tree_selection)

        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Snippet label", renderer, text=0)
        self.labels_list.append_column(column)
        self.scroll.add(self.labels_list)

        self.scroll.set_size_request(400, 350)
        self.leftbox.pack_start(self.scroll, True, True, 0)

        self.buttons_box = Gtk.HBox(spacing=10)
        self.buttons_box.set_size_request(50, 50)
        self.leftbox.pack_start(self.buttons_box, True, True, 0)

        self.add_button = Gtk.Button(label="Add")
        self.add_button.connect("clicked", self.add_clicked)
        self.add_button.set_size_request(50, 50)
        self.buttons_box.pack_start(self.add_button, True, True, 0)

        self.delete_button = Gtk.Button(label="Delete")
        self.delete_button.connect("clicked", self.delete_clicked)
        self.delete_button.set_size_request(50, 50)
        self.buttons_box.pack_start(self.delete_button, True, True, 0)

        self.rightbox = Gtk.VBox(spacing=10)
        self.rightbox.set_size_request(400, 400)
        self.box.pack_start(self.rightbox, True, True, 0)

        labellb = Gtk.Label("Snippet label:")
        labellb.halign = Gtk.Align.START
        labellb.valign = Gtk.Align.START
        self.rightbox.pack_start(labellb, True, True, 0)
        self.labelentry = Gtk.Entry()
        self.labelentry.halign = Gtk.Align.START
        self.labelentry.valign = Gtk.Align.START
        self.labelentry.set_size_request(300, 25)
        self.rightbox.pack_start(self.labelentry, True, True, 0)

        desclb = Gtk.Label("Snippet description:")
        labellb.halign = Gtk.Align.START
        labellb.valign = Gtk.Align.START
        self.rightbox.pack_start(desclb, True, True, 0)
        self.descentry = Gtk.Entry()
        self.descentry.set_size_request(300, 25)
        self.descentry.halign = Gtk.Align.START
        self.descentry.valign = Gtk.Align.START
        self.rightbox.pack_start(self.descentry, True, True, 0)

        textlb = Gtk.Label("Snippet text:")
        labellb.halign = Gtk.Align.START
        labellb.valign = Gtk.Align.START
        self.rightbox.pack_start(textlb, True, True, 0)
        self.textentry = Gtk.Entry()
        self.textentry.halign = Gtk.Align.START
        self.textentry.valign = Gtk.Align.START
        self.textentry.set_size_request(300, 25)
        self.rightbox.pack_start(self.textentry, True, True, 0)

        self.ok_button = Gtk.Button("Ok")
        self.ok_button.connect("clicked", self.ok_clicked)
        self.ok_button.set_size_request(300, 50)
        self.rightbox.pack_start(self.ok_button, True, True, 0)

    def on_tree_selection(self, selection):
        model, treeiter = selection.get_selected()
        if treeiter != None:
            print("You selected", model[treeiter][0])

    def add_clicked(self, button):
        print("Add clicked")

    def delete_clicked(self, button):
        print("Delete clicked")

    def ok_clicked(self, button):
        print("Ok clicked")


