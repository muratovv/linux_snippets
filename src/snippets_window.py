#! /usr/bin/env python3

from gi.repository import Gtk
from gi.repository import Gdk

from src.compliter import AutoSub


class SnippetsWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Snippets")

        self.result = ""

        self.completion = self.calculate_completion()

        self.entry = self.calculate_entry(self.completion, self.on_text_changed)

        self.add(self.entry)

        self.auto_sub = AutoSub("src/snippets")

    def calculate_completion(self):
        desc_cell = Gtk.CellRendererText()

        completion = Gtk.EntryCompletion()

        completion.set_model(Gtk.ListStore(str, str))
        completion.set_text_column(0)

        completion.pack_start(desc_cell, True)
        completion.add_attribute(desc_cell, 'text', 1)

        return completion

    def calculate_entry(self, completion, on_text_changed):
        entry = Gtk.Entry()

        entry.set_completion(completion)

        entry.connect("changed", on_text_changed)
        # entry.connect("key-press-event", self.on_tab_pressed)
        # entry.connect("key-release-event", self.on_tab_released)

        return entry

    def on_text_changed(self, entry):
        model = Gtk.ListStore(str, str)
        text = entry.get_text()

        for snippet in self.get_suggested_snippets(text):
            model.append([snippet['label'], snippet['description']])

        self.completion.set_model(model)
        self.update_result(text)

    def get_suggested_snippets(self, text):
        return self.auto_sub.fieldCange_evnt(text)

    def update_result(self, text):
        self.result = self.auto_sub.substitution_evnt(text)

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