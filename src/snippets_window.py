#! /usr/bin/env python3

from gi.repository import Gtk
from gi.repository import Gdk

from src.compliter import AutoSub


class SnippetsWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Snippets")

        self.text = ""

        self.completion = Gtk.EntryCompletion()
        self.completion.set_model(None)
        self.completion.set_text_column(0)

        self.entry = Gtk.Entry()
        self.entry.set_completion(self.completion)

        self.entry.connect("changed", self.on_text_changed)
        # self.entry.connect("key-press-event", self.on_tab_pressed)
        # self.entry.connect("key-release-event", self.on_tab_released)

        self.add(self.entry)

        self.auto_sub = AutoSub("src/snippets")

    def on_text_changed(self, entry):
        suggests = Gtk.ListStore(str)

        for suggest in self.auto_sub.fieldCange_evnt(entry.get_text()):
            suggests.append([(suggest['label'])])

        self.completion.set_model(suggests)

    def on_tab_pressed(self, entry, event, *args):
        if event.keyval == Gdk.KEY_Tab:
            # print("TAB_P")
            return True

    def on_tab_released(self, entry, event, *args):
        if event.keyval == Gdk.KEY_Tab:
            # print("TAB_R")
            return True


# window = SnippetsWindow()
# window.connect("delete-event", Gtk.main_quit)
# window.show_all()
# Gtk.main()