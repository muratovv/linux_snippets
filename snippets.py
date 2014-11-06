#! /usr/bin/env python3
__author__ = 'flire'

from Xlib import X, XK, display, protocol, ext
from gi.repository import Gtk
import pyperclip
import time
if __name__ == "__main__":
    cbcache = pyperclip.paste()
    displ = display.Display()
    focus_request = displ.get_input_focus()
    focus = focus_request.focus
    revert_to = focus_request.revert_to

    pyperclip.copy("Some random text to paste!")

    root = Gtk.Window()

    def callback(widget, event):
        keysym = XK.string_to_keysym('V')
        keycode = displ.keysym_to_keycode(keysym)
        # ext.xtest.fake_input(displ, X.KeyPress, keycode)
        # ext.xtest.fake_input (displ, X.KeyRelease, keycode)
        ev = protocol.event.KeyPress(
            time = int(time.time()),
            root = displ.screen().root,
            window = focus,
            root_x = 0,
            root_y = 0,
            event_x = 0,
            event_y = 0,
            same_screen = 0, child = X.NONE,
            state = X.ControlMask,
            detail = keycode
        )
        displ.send_event(focus,ev)
        displ.sync()
        time.sleep(0.5)
        pyperclip.copy(cbcache)
        Gtk.main_quit(widget, event)

    root.connect("delete-event", callback)
    root.show_all()
    Gtk.main()