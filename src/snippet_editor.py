#! /usr/bin/env python3

from gi.repository import Gtk

from src.snippetParser import SnippetParser


class EditorWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Editor")

        self.set_resizable(False)

        grid = Gtk.Grid()
        grid.set_border_width(5)
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)
        self.add(grid)

        self.snippets = self.load_snippets()

        model = Gtk.ListStore(str)

        for snippet in self.snippets:
            model.append([snippet['label']])

        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Label", renderer, text=0)

        self.labels = Gtk.TreeView(model)
        self.labels.append_column(column)

        select = self.labels.get_selection()
        select.connect("changed", self.on_label_selection)

        scroll = Gtk.ScrolledWindow()
        scroll.add(self.labels)

        grid.attach(scroll, 0, 0, 2, 6)

        self.label_entry = Gtk.Entry()
        self.desc_entry = Gtk.Entry()
        self.text_entry = Gtk.Entry()

        self.label_entry.set_sensitive(False)

        grid.attach(Gtk.Label("Label"), 2, 0, 1, 1)
        grid.attach(self.label_entry, 2, 1, 1, 1)

        grid.attach(Gtk.Label("Description"), 2, 2, 1, 1)
        grid.attach(self.desc_entry, 2, 3, 1, 1)

        grid.attach(Gtk.Label("Text"), 2, 4, 1, 1)
        grid.attach(self.text_entry, 2, 5, 1, 1)

        add_button = Gtk.Button("Add")
        delete_button = Gtk.Button("Delete")
        save_button = Gtk.Button("Save")

        add_button.connect("clicked", self.on_add_clicked)
        delete_button.connect("clicked", self.on_delete_clicked)
        save_button.connect("clicked", self.on_save_clicked)

        grid.attach(add_button, 0, 7, 1, 1)
        grid.attach(delete_button, 1, 7, 1, 1)
        grid.attach(save_button, 2, 7, 1, 1)

    def reload_snippets(self):
        self.snippets = self.load_snippets()

    def load_snippets(self):
        return SnippetParser("src/snippets").snippets

    def on_add_clicked(self, button):
        print("add")

        return True

    def on_delete_clicked(self, button):
        print("delete")

        return True

    def on_save_clicked(self, button):
        print("save")

        return True

    def on_label_selection(self, selection):
        print("selection")

        return True


"""
__author__ = 'flire'

from gi.repository import Gtk

from src.snippetParser import SnippetParser
from src.Exeptions import badUserSnippetExeption

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

        self.current_snippet = None
        self.current_snippet_treeiter = None

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
            label = model[treeiter][0]
            self.current_snippet_treeiter = treeiter
        for snippet in self.snippets:
            if snippet["label"]==label:
                self.current_snippet = snippet
                self.labelentry.set_text(self.current_snippet["label"])
                self.descentry.set_text(self.current_snippet["description"])
                self.textentry.set_text(self.parser.getSnippetTextBySnippet(self.current_snippet))
                break

    def add_clicked(self, button):
        if self.labelentry.get_text() and self.textentry.get_text():
            event = {}
            event["label"] = self.labelentry.get_text()
            event["text"] = self.textentry.get_text()
            event["description"] = self.descentry.get_text()

            obj = None
            try:
                obj = self.parser.getObjFromString(event)
                self.parser.addSnippet(obj)
                self.parser.saveSnippetList("src/snippets")
            except Exception:
                self.message_box("problems with addition")

            self.labelentry.set_text("")
            self.textentry.set_text("")
            self.descentry.set_text("")
            self.store.append([obj["label"]])
        else:
            self.message_box("bad snippet")

    def delete_clicked(self, button):
        for_delete = self.current_snippet["label"]
        answ = self.parser.deleteSnippet(for_delete)
        if answ:
            self.parser.saveSnippetList("src/snippets")
            self.store.remove(self.current_snippet_treeiter)
            self.current_snippet = None
            self.current_snippet_treeiter = None
        else:
            self.message_box("label not found")

    def ok_clicked(self, button):
        event = {}
        event["label"] = self.labelentry.get_text()
        event["text"] = self.textentry.get_text()
        event["description"] = self.descentry.get_text()
        new_snippet = self.parser.getObjFromString(event)
        self.parser.modifySnippet(self.current_snippet["label"], new_snippet)
        self.store.set_value(self.current_snippet_treeiter, 0, new_snippet["label"])
        self.current_snippet = new_snippet
        self.parser.saveSnippetList("src/snippets")

    def message_box(self, message):
        dialogWindow = Gtk.MessageDialog(self,
                          Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT,
                          Gtk.MessageType.WARNING,
                          Gtk.ButtonsType.OK,
                          message)
        dialogWindow.run()
        dialogWindow.destroy()
"""

