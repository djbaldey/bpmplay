#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# main.py
# Copyright (C) 2016 Grigoriy Kramarenko <djbaldey@gmail.com>
# 
# bpmplay is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# bpmplay is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

import os, sys
import time

from gi.repository import Gtk, Gdk

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UI_FILE = os.path.join(BASE_DIR, "bpmplay.ui")


class GUI:
    def __init__(self):

        self.builder = Gtk.Builder()
        self.builder.add_from_file(UI_FILE)
        self.builder.connect_signals(self)

        self.label_tempo = self.builder.get_object('label_tempo')
        self.adjustment_tempo = self.builder.get_object('adjustment_tempo')

        window = self.builder.get_object('window')
        window.show_all()

        self.bits = []
        self.previous_bit = None
        self.value = int(self.adjustment_tempo.get_value())
        self.is_playing = False

    def on_window_destroy(self, window):
        Gtk.main_quit()

    def on_window_key_press_event(self, window, event):
        press = event.type == Gdk.EventType.KEY_PRESS
        space = event.keyval == Gdk.KEY_space
        enter = event.keyval == Gdk.KEY_Return
        if press and not space and not enter:
            self.calculation()

    def on_adjustment_tempo_value_changed(self, adjustment):
        self.value = int(adjustment.get_value())
        self.change_tempo()

    def on_button_drum_clicked(self, button):
        self.calculation()

    def change_tempo(self):
        self.label_tempo.set_text('♩=%s' % self.value)
    
    def calculation(self):
        bit = time.time()
        self.bits.insert(0, bit)
        L = []
        for i,x in enumerate(self.bits):
            if i > 0:
                v = round(self.bits[i-1] - x, 5)
                if v >= 2:
                    # Restart capture
                    self.bits = self.bits[:1]
                    return
                L.append(v)
        if L:
            avg = sum(L) / len(L)
            bps = round(1 / avg, 1)
            bpm = bps * 60
            self.value = int(round(bpm))
            self.adjustment_tempo.set_value(self.value)
            self.change_tempo()

        self.bits = self.bits[:12]

def main():
    app = GUI()
    Gtk.main()

if __name__ == "__main__":
    sys.exit(main())

