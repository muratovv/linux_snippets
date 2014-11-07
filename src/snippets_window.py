#! /usr/bin/env python3

from gi.repository import Gtk
from gi.repository import Gdk

from src.compliter import AutoSub


class SnippetsWindow(Gtk.Window):
    def __init__(self, callback=None):
        Gtk.Window.__init__(self, title="Snippets")

        self.completion = self.calculate_completion(self.on_completion_selected)

        self.entry = self.calculate_entry(self.completion, self.on_entry_text_changed, self.on_entry_tab_pressed,
                                          self.on_entry_tab_released, self.on_entry_activated)

        self.add(self.entry)

        self.auto_sub = AutoSub("src/snippets")

        self.callback = callback

    def clear(self):
        self.entry.set_text("")

    def calculate_completion(self, on_selected):
        desc_cell = Gtk.CellRendererText()

        completion = Gtk.EntryCompletion()

        completion.set_model(Gtk.ListStore(str, str))
        completion.set_text_column(0)

        completion.pack_start(desc_cell, True)
        completion.add_attribute(desc_cell, 'text', 1)

        completion.connect("match-selected", on_selected)

        return completion

    def calculate_entry(self, completion, on_changed, on_tab_pressed, on_tab_released, on_activated):
        entry = Gtk.Entry()

        entry.set_completion(completion)
        entry.set_width_chars(75)

        entry.connect("changed", on_changed)
        entry.connect("key-press-event", on_tab_pressed)
        entry.connect("key-release-event", on_tab_released)
        entry.connect("activate", on_activated)

        return entry

    def on_completion_selected(self, entry_completion, model, pos):
        selected = model[pos][0]
        result = self.get_expanded_snippet(selected)

        self.entry.set_text(result)

        l = result.find('#')

        if l != -1:
            self.entry.select_region(l, result.find('#', l + 1) + 1)

        return True

    def get_expanded_snippet(self, text):
        return self.auto_sub.substitution_evnt(text)

    def on_entry_text_changed(self, entry):
        model = Gtk.ListStore(str, str)
        text = entry.get_text()

        for snippet in self.get_suggested_snippets(text):
            model.append([snippet['label'], snippet['description']])

        self.completion.set_model(model)

        return True

    def get_suggested_snippets(self, text):
        return self.auto_sub.fieldCange_evnt(text)

    def on_entry_tab_pressed(self, entry, event, *args):
        if event.keyval == Gdk.KEY_Tab:
            return True

    def on_entry_tab_released(self, entry, event, *args):
        if event.keyval == Gdk.KEY_Tab:
            text = entry.get_text()

            l = text.find('#', entry.get_position())

            if l != -1:
                entry.select_region(l, text.find('#', l + 1) + 1)

            return True

    def on_entry_activated(self, entry, *args):
        if self.callback is not None:
            self.callback(self.convert_snippet_to_result(entry.get_text()))

        return True

    def convert_snippet_to_result(self, text):
        return self.auto_sub.parsedSubstitution_evnt(text)


if __name__ == '__main__':
    window = SnippetsWindow()
    window.connect("delete-event", Gtk.main_quit)
    window.show_all()
    Gtk.main()