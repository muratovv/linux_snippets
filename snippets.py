#! /usr/bin/env python3
__author__ = 'flire'

from Xlib import X, XK, display, protocol, ext
from gi.repository import Gtk
import pyperclip
import time
from keybinder.keybinder_gtk import KeybinderGtk
import src.snippets_window as wnd

class main_window():
    def __init__(self):
        #Gtk.Window.__init__(self)
        self.display = display.Display()

        self.keybinder = KeybinderGtk()
        self.keybinder.register("<Ctrl>9", self.restore_callback)
        self.keybinder.start()

        #quitbutton = Gtk.Button("Paste")
        #quitbutton.connect("clicked", self.callback)
        #self.add(quitbutton)

        #self.connect("delete-event", self.quit)
        #self.show_all()
        #Gtk.main()

    def restore_callback(self):
        self.cbcache = pyperclip.paste()
        focus_request = self.display.get_input_focus()
        self.focus = focus_request.focus
        revert_to = focus_request.revert_to
        print("Hotkey pressed!")

        self.wind = wnd.SnippetsWindow()
        self.wind.connect("delete-event", self.callback)
        # self.wind.connect("delete-event", Gtk.main_quit)
        self.wind.show_all()
        Gtk.main()
        self.wind.present()
        #self.show_all()
        #self.present()

    def callback(self, window, event):
        Gtk.main_quit()
        #self.hide()
        pyperclip.copy(window.text)
        self.wind.connect("delete-event", Gtk.main_quit)
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
        time.sleep(0.5)
        pyperclip.copy(self.cbcache)
        # Gtk.main_quit()Some random text to paste!Some random text to paste!
        #return True

    # def quit(self,window, event):
    #     self.keybinder.stop()
    #     Gtk.main_quit()

if __name__ == "__main__":
    wind = main_window()
    while True:
        time.sleep(0.1)
