#! /usr/bin/env python3
__author__ = 'flire'

import time

from Xlib import X, XK, display, protocol
from gi.repository import Gtk
from gi.repository import AppIndicator3
import pyperclip
from gi.repository import Keybinder

import src.snippets_window as sn_w
import src.snippet_editor as sn_e


class Application():
    def __init__(self):
        self.display = display.Display()

        Keybinder.init()
        Keybinder.bind("<Ctrl>9", self.on_snippets_activated)

        menu = Gtk.Menu()

        item = Gtk.MenuItem()
        item.set_label("Editor")
        item.connect("activate", self.on_editor_activated)
        item.show()
        menu.append(item)

        item = Gtk.MenuItem()
        item.set_label("Exit")
        item.connect("activate", Gtk.main_quit)
        item.show()
        menu.append(item)

        self.status_icon = AppIndicator3.Indicator.new(
            "linux-snippets",
            "onboard-mono",
            AppIndicator3.IndicatorCategory.APPLICATION_STATUS
        )

        self.status_icon.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.status_icon.set_attention_icon("indicator-messages-new")
        self.status_icon.set_menu(menu)

        self.editor = sn_e.EditorWindow()
        self.editor.connect("delete-event", self.on_window_deleted)

        self.snippets = sn_w.SnippetsWindow(self.on_snippets_completed)
        self.snippets.connect("delete-event", self.on_window_deleted)

    def on_snippets_activated(self, data):
        self.cb_cache = pyperclip.paste()
        focus_request = self.display.get_input_focus()
        self.focus = focus_request.focus

        print("Hotkey pressed!")

        self.snippets.reload()
        self.snippets.show_all()
        self.snippets.present_with_time(int(time.time()))
        self.snippets.set_keep_above(True)

        return True

    def on_snippets_completed(self, text):
        self.snippets.hide()

        pyperclip.copy(text)

        keysym = XK.string_to_keysym('V')
        keycode = self.display.keysym_to_keycode(keysym)
        ev = protocol.event.KeyPress(
            time=int(time.time()),
            root=self.display.screen().root,
            window=self.focus,
            root_x=0,
            root_y=0,
            event_x=0,
            event_y=0,
            same_screen=0, child=X.NONE,
            state=X.ControlMask,
            detail=keycode
        )

        self.display.send_event(self.focus, ev)
        self.display.sync()
        time.sleep(1)

        pyperclip.copy(self.cb_cache)

        return True

    def on_window_deleted(self, window, event):
        window.hide()

        return True

    def on_editor_activated(self, widget):
        self.editor.reload()
        self.editor.show_all()
        self.editor.present_with_time(int(time.time()))

        return True


if __name__ == "__main__":
    app = Application()
    Gtk.main()
