#! /usr/bin/env python3

from gi.repository import Gtk
from gi.repository import Gdk

import src.snippets_utils as s_u


class SnippetsWindow(Gtk.Window):
    def __init__(self, callback=None):
        Gtk.Window.__init__(self, title="Snippets")

        self.snippets = s_u.load_snippets()

        self.callback = callback

        self.completion = self.calculate_completion(self.on_completion_selected)

        self.entry = self.calculate_entry(self.completion, self.on_entry_text_changed, self.on_entry_tab_pressed,
                                          self.on_entry_tab_released, self.on_entry_activated)

        self.add(self.entry)

    def reload(self):
        self.entry.set_text("")
        self.snippets = s_u.load_snippets()

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
        self.expand_label(model[pos][0])

        return True

    def expand_label(self, label):
        expanded_snippet = s_u.get_expanded_snippet_by_label(self.snippets, label)

        self.entry.set_text(expanded_snippet)

        l = expanded_snippet.find(s_u.separator)

        if l != -1:
            r = expanded_snippet.find(s_u.separator, l + 1) + 1
            self.entry.select_region(l, r)

    def on_entry_text_changed(self, entry):
        model = Gtk.ListStore(str, str)
        text = entry.get_text()

        for snippet in s_u.get_suggested_snippets(self.snippets, text):
            model.append([snippet['label'], snippet['description']])

        self.completion.set_model(model)

        return True

    def on_entry_tab_pressed(self, entry, event, *args):
        if event.keyval == Gdk.KEY_Tab:
            return True

    def on_entry_tab_released(self, entry, event, *args):
        if event.keyval == Gdk.KEY_Tab:
            text = entry.get_text()

            l = text.find(s_u.separator, entry.get_position())

            if l != -1:
                r = text.find(s_u.separator, l + 1) + 1
                entry.select_region(l, r)
                return True

            suggested_snippets = s_u.get_suggested_snippets(self.snippets, text)

            if len(suggested_snippets) == 1:
                self.expand_label(suggested_snippets[0]['label'])
                return True

            return True

    def on_entry_activated(self, entry, *args):
        if self.callback is not None:
            self.callback(
                s_u.convert_expanded_snippet_to_result(self.snippets, entry.get_text())
            )

        return True


if __name__ == '__main__':
    window = SnippetsWindow()
    window.connect("delete-event", Gtk.main_quit)
    window.show_all()
    Gtk.main()