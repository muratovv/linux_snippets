#! /usr/bin/env python3

from gi.repository import Gtk

import src.snippets_utils as s_u


class EditorWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title='Editor')

        self.set_resizable(False)

        grid = Gtk.Grid()
        grid.set_border_width(5)
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)
        self.add(grid)

        self.snippets = s_u.load_snippets()
        self.model = Gtk.ListStore(str)

        self.reload_model()

        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn('Label', renderer, text=0)

        self.labels = Gtk.TreeView(self.model)
        self.labels.append_column(column)

        select = self.labels.get_selection()
        select.connect('changed', self.on_label_selection)

        scroll = Gtk.ScrolledWindow()
        scroll.add(self.labels)

        grid.attach(scroll, 0, 0, 2, 6)

        self.label_entry = Gtk.Entry()
        self.desc_entry = Gtk.Entry()
        self.text_entry = Gtk.Entry()

        self.label_entry.set_sensitive(False)

        self.label_entry.set_size_request(300, 25)
        self.desc_entry.set_size_request(300, 25)
        self.text_entry.set_size_request(300, 25)

        grid.attach(Gtk.Label('Label'), 2, 0, 1, 1)
        grid.attach(self.label_entry, 2, 1, 1, 1)

        grid.attach(Gtk.Label('Description'), 2, 2, 1, 1)
        grid.attach(self.desc_entry, 2, 3, 1, 1)

        grid.attach(Gtk.Label('Text'), 2, 4, 1, 1)
        grid.attach(self.text_entry, 2, 5, 1, 1)

        add_button = Gtk.Button('Add')
        delete_button = Gtk.Button('Delete')
        save_button = Gtk.Button('Save')

        add_button.connect('clicked', self.on_add_clicked)
        delete_button.connect('clicked', self.on_delete_clicked)
        save_button.connect('clicked', self.on_save_clicked)

        grid.attach(add_button, 0, 7, 1, 1)
        grid.attach(delete_button, 1, 7, 1, 1)
        grid.attach(save_button, 2, 7, 1, 1)

    def reload(self):
        self.reload_snippets()
        self.reload_model()

    def reload_snippets(self):
        self.snippets = s_u.load_snippets()

    def reload_model(self):
        self.model.clear()

        for snippet in self.snippets:
            self.model.append([snippet['label']])

    def on_add_clicked(self, button):
        dialog = AddDialog(self)
        dialog.show_all()

        self.handle_add_dialog_response(dialog, dialog.run())

        return True

    def handle_add_dialog_response(self, dialog, response):
        if response == Gtk.ResponseType.OK:
            data = dialog.get_data()

            if len(data['label']) == 0 or len(data['text']) == 0 or self.label_exists(data['label']):
                self.invalid_snippet_dialog()

                self.handle_add_dialog_response(dialog, dialog.run())
            else:
                s_u.update_or_append_snippet(
                    s_u.convert_strs_to_snippet(data['label'], data['description'], data['text'])
                )

                self.reload()

                dialog.destroy()

    def label_exists(self, label):
        for snippet in self.snippets:
            if snippet['label'] == label:
                return True

        return False

    def on_delete_clicked(self, button):
        model, pos = self.labels.get_selection().get_selected()

        if pos is not None:
            s_u.delete_snippet(model[pos][0])
            self.reload()

        return True

    def on_save_clicked(self, button):
        s_u.update_or_append_snippet(
            s_u.convert_strs_to_snippet(self.label_entry.get_text(), self.desc_entry.get_text(),
                                        self.text_entry.get_text())
        )

        # TODO check

        self.reload_snippets()

        return True

    def on_label_selection(self, selection):
        model, pos = selection.get_selected()

        if pos is None:
            self.label_entry.set_text('')
            self.desc_entry.set_text('')
            self.text_entry.set_text('')
            return True

        snippet = self.find_snippet(model[pos][0])

        if snippet is not None:
            l, d, t = s_u.convert_snippet_to_strs(snippet)

            self.label_entry.set_text(l)
            self.desc_entry.set_text(d)
            self.text_entry.set_text(t)

        return True

    def find_snippet(self, label):
        for snippet in self.snippets:
            if snippet['label'] == label:
                return snippet

        return None

    def invalid_snippet_dialog(self):
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING,
                                   Gtk.ButtonsType.OK, "Invalid snippet")

        dialog.format_secondary_text(
            "Label and text shouldn't be empty. Label should be unique")

        dialog.run()
        dialog.destroy()


class AddDialog(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, 'Add', parent, 0,
                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                             Gtk.STOCK_OK, Gtk.ResponseType.OK))

        box = self.get_content_area()

        grid = Gtk.Grid()
        grid.set_border_width(5)
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)

        box.add(grid)

        self.label_entry = Gtk.Entry()
        self.desc_entry = Gtk.Entry()
        self.text_entry = Gtk.Entry()

        self.label_entry.set_size_request(300, 25)
        self.desc_entry.set_size_request(300, 25)
        self.text_entry.set_size_request(300, 25)

        grid.attach(Gtk.Label('Label'), 0, 0, 1, 1)
        grid.attach(self.label_entry, 0, 1, 1, 1)

        grid.attach(Gtk.Label('Description'), 0, 2, 1, 1)
        grid.attach(self.desc_entry, 0, 3, 1, 1)

        grid.attach(Gtk.Label('Text'), 0, 4, 1, 1)
        grid.attach(self.text_entry, 0, 5, 1, 1)

    def get_data(self):
        return {'label': self.label_entry.get_text(), 'description': self.desc_entry.get_text(),
                'text': self.text_entry.get_text()}

