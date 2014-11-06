#! /usr/bin/env python3
__author__ = 'flire'

from Xlib import X, XK, display, protocol, ext
from gi.repository import Gtk
import pyperclip
import time
from keybinder.keybinder_gtk import KeybinderGtk

class main_window(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        self.display = display.Display()

        self.keybinder = KeybinderGtk()
        self.keybinder.register("<Ctrl>9", self.restore_callback)
        self.keybinder.start()

        quitbutton = Gtk.Button("Paste")
        quitbutton.connect("clicked", self.callback)
        self.add(quitbutton)

        self.connect("delete-event", self.quit)
        self.show_all()
        Gtk.main()

    def restore_callback(self):
        self.cbcache = pyperclip.paste()
        focus_request = self.display.get_input_focus()
        self.focus = focus_request.focus
        revert_to = focus_request.revert_to
        print("Hotkey pressed!")
        self.show()
        self.present()

    def callback(self, button):
        self.hide()
        pyperclip.copy("Some random text to paste!")
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
        return True

    def quit(self,window, event):
        #quit the gtk main loop
        self.keybinder.stop()
        Gtk.main_quit()

if __name__ == "__main__":
    wind = main_window()
    # cbcache = pyperclip.paste()
    # displ = display.Display()
    # focus = None
    #
    # pyperclip.copy("Some random text to paste!")
    #
    # root = Gtk.Window()
    # keybinder = KeybinderGtk()
    #
    #
    # def restore_callback():
    #     focus_request = displ.get_input_focus()
    #     global focus
    #     focus = focus_request.focus
    #     revert_to = focus_request.revert_to
    #     print("Hotkey pressed!")
    #     root.present()
    #
    # def callback(widget, event):
    #     keysym = XK.string_to_keysym('V')
    #     keycode = displ.keysym_to_keycode(keysym)
    #     # ext.xtest.fake_input(displ, X.KeyPress, keycode)
    #     # ext.xtest.fake_input (displ, X.KeyRelease, keycode)
    #     ev = protocol.event.KeyPress(
    #         time = int(time.time()),
    #         root = displ.screen().root,
    #         window = focus,
    #         root_x = 0,
    #         root_y = 0,
    #         event_x = 0,
    #         event_y = 0,
    #         same_screen = 0, child = X.NONE,
    #         state = X.ControlMask,
    #         detail = keycode
    #     )
    #     displ.send_event(focus,ev)
    #     displ.sync()
    #     time.sleep(0.5)
    #     keybinder.stop()
    #     pyperclip.copy(cbcache)
    #     root.hide_on_delete()
    #     #Gtk.main_quit(widget, event)
    #
    # keybinder.register("<Ctrl>L", restore_callback)
    # keybinder.start()
    # root.connect("delete-event", callback)
    # root.show()
    # Gtk.main()