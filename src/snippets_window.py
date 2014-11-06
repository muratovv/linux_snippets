#! /usr/bin/env python3

from gi.repository import Gtk
from gi.repository import Gdk


class SnippetsWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Snippets")

        self.box = Gtk.VBox(spacing=5)
        self.add(self.box)

        self.entry = Gtk.Entry()
        self.entry.connect("changed", self.on_text_changed)
        self.entry.connect("key-press-event", self.on_tab_pressed)
        self.entry.connect("key-release-event", self.on_tab_released)

        model = Gtk.ListStore(str)

        self.combo_box = Gtk.ComboBox.new_with_model_and_entry(model)
        self.combo_box.set_entry_text_column(0)
        self.combo_box.connect("changed", self.on_combobox_changed)

        self.box.pack_start(self.entry, True, True, 0)
        self.box.pack_start(self.combo_box, True, True, 0)

    def on_text_changed(self, entry):
        # TODO send request, update model
        text = entry.get_text()

        model = self.combo_box.get_model()

        model.clear()
        model.append([text])
        model.append([2 * text])

        self.combo_box.set_model(model)
        self.combo_box.show()

    def on_tab_pressed(self, entry, event, *args):
        if event.keyval == Gdk.KEY_Tab:
            # print("TAB_P")
            return True

    def on_tab_released(self, entry, event, *args):
        if event.keyval == Gdk.KEY_Tab:
            # print("TAB_R")
            return True

    def on_combobox_changed(self, combobox):
        active = combobox.get_active()

        if active != -1:
            # TODO send result
            print(combobox.get_model()[active][0])


def run():
    win = SnippetsWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()


if __name__ == '__main__':
    run()