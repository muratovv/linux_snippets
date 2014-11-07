#! /usr/bin/env python3
__author__ = 'flire'

from Xlib import X, XK, display, protocol, ext
from gi.repository import Gtk, Gdk, GLib
from gi.repository import AppIndicator3 as appindicator
import pyperclip
import time
from gi.repository import Keybinder
import src.snippets_window as wnd
import src.snippet_editor as editor

class main_window():
    def __init__(self):
        self.display = display.Display()

        Keybinder.init()
        Keybinder.bind("<Ctrl>9", self.restore_callback)

        self.statusicon = appindicator.Indicator.new (
            "linux-snippets",
            "onboard-mono",
            appindicator.IndicatorCategory.APPLICATION_STATUS)
        self.statusicon.set_status (appindicator.IndicatorStatus.ACTIVE)
        self.statusicon.set_attention_icon ("indicator-messages-new")

        self.menu = Gtk.Menu()

        item = Gtk.MenuItem()
        item.set_label("Editor")
        item.connect("activate", self.load_editor, '')
        item.show()
        self.menu.append(item)

        item = Gtk.MenuItem()
        item.set_label("Exit")
        item.connect("activate", self.quit, '')
        item.show()
        self.menu.append(item)

        self.statusicon.set_menu(self.menu)

        self.editor = editor.EditorWindow()
        self.editor.connect("delete-event", self.editor_deletion)

        self.wind = wnd.SnippetsWindow()
        self.wind.connect("delete-event", self.callback)

    def restore_callback(self, data):
        self.cbcache = pyperclip.paste()
        focus_request = self.display.get_input_focus()
        self.focus = focus_request.focus
        revert_to = focus_request.revert_to
        print("Hotkey pressed!")

        self.wind.show_all()
        self.wind.present_with_time(int(time.time()))
        self.wind.set_keep_above(True)

    def callback(self, window, event):
        self.wind.hide()
        pyperclip.copy(window.result)
        keysym = XK.string_to_keysym('V')
        keycode = self.display.keysym_to_keycode(keysym)
        # ext.xtest.fake_input(displ, X.KeyPress, keycode)
        # ext.xtest.fake_input (displ, X.KeyRelease, keycode)
        ev = protocol.event.KeyPress(
            time = int(time.time()),
            root = self.display.screen().root,
            window = self.focus,
            root_x = 0,
            root_y = 0,
            event_x = 0,
            event_y = 0,
            same_screen = 0, child = X.NONE,
            state = X.ControlMask,
            detail = keycode
        )
        self.display.send_event(self.focus,ev)
        self.display.sync()
        time.sleep(1)
        pyperclip.copy(self.cbcache)
        return True

    def load_editor(self, widget, data):
        self.editor.show_all()
        self.editor.present_with_time(int(time.time()))

    def editor_deletion(self, window, event):
        window.hide()
        return True

    def quit(self, widget, data):
        Gtk.main_quit()

if __name__ == "__main__":
    wind = main_window()
    Gtk.main()
