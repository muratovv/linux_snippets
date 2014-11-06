#! /usr/bin/env python3

from gi.repository import Gtk


class SnippetsWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Snippets")

        self.box = Gtk.VBox(spacing=5)
        self.add(self.box)

        self.entry = Gtk.Entry()
        self.entry.connect("changed", self.on_text_changed)

        self.combo_box = Gtk.ComboBox()

        self.box.pack_start(self.entry, True, True, 0)
        self.box.pack_start(self.combo_box, True, True, 0)

    def on_text_changed(self, entry):
        text = self.entry.get_text()

        if len(text) == 0:
            self.combo_box.hide()

        if len(text) != 0:
            self.combo_box.show()

        print(text)


win = SnippetsWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()