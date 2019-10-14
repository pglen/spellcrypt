#!/usr/bin/env python

import os, sys, getopt, signal, string
#import gobject, gtk, pango
import random, time, subprocess

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject


# ------------------------------------------------------------------------
# Resolve path name

def respath(fname):

    try:
        ppp = string.split(os.environ['PATH'], os.pathsep)
        for aa in ppp:
            ttt = aa + os.sep + fname
            if os.path.isfile(str(ttt)):
                return ttt
    except:
        print "Cannot resolve path", fname, sys.exc_info()
    return None

# ------------------------------------------------------------------------
# An N pixel vertical spacer. Default to 5.

class Spacer(Gtk.Label):

    def __init__(self, sp = 5):
        GObject.GObject.__init__(self)
        sp *= 1000
        self.set_markup("<span  size=\"" + str(sp) + "\"> </span>")

# ------------------------------------------------------------------------

class MainWin():

    def __init__(self):

        self.window = window = Gtk.Window(Gtk.WindowType.TOPLEVEL)

        window.set_title("Spell Encryptor UI")
        window.set_position(Gtk.WindowPosition.CENTER)

        #ic = Gtk.Image(); ic.set_from_stock(Gtk.STOCK_DIALOG_INFO, Gtk.IconSize.BUTTON)
        #window.set_icon(ic.get_pixbuf())

        www = Gdk.Screen.width(); hhh = Gdk.Screen.height();
        #window.set_default_size(6*www/8, 6*hhh/8)
        window.set_default_size(800, 600)

        #window.set_flags(Gtk.CAN_FOCUS | Gtk.SENSITIVE)

        window.set_events(  Gdk.EventMask.POINTER_MOTION_MASK |
                            Gdk.EventMask.POINTER_MOTION_HINT_MASK |
                            Gdk.EventMask.BUTTON_PRESS_MASK |
                            Gdk.EventMask.BUTTON_RELEASE_MASK |
                            Gdk.EventMask.KEY_PRESS_MASK |
                            Gdk.EventMask.KEY_RELEASE_MASK |
                            Gdk.EventMask.FOCUS_CHANGE_MASK )

        window.connect("destroy", self.OnExit)
        window.connect("key-press-event", self.key_press_event)
        window.connect("button-press-event", self.button_press_event)

        try:
            window.set_icon_from_file("icon.png")
        except:
            pass

        vbox = Gtk.VBox();
        hbox = Gtk.HBox();
        hbox2 = Gtk.HBox(); hbox2.padding(12)
        hbox3 = Gtk.VBox()

        sp1 = Spacer()
        lab3 = Gtk.Label(label="  Enter Pass Word: ");   hbox2.pack_start(lab3, 0,0,False)
        self.entry = Gtk.Entry();    hbox2.pack_start(self.entry, 0,0, padding = 4)
        self.entry.connect("activate", self.lookup, window)

        butt3 = Gtk.Button.new_with_mnemonic(" Load _file:")
        butt3.connect("clicked", self.lookup, window)
        hbox2.pack_start(butt3, 0, 0, False)

        sp2 = Spacer()
        butt3e = Gtk.Button.new_with_mnemonic(" _Encrypt")
        butt3e.connect("clicked", self.lookup, window)
        hbox2.pack_start(butt3e, 0, 0, False) #, padding = 4)

        butt3e = Gtk.Button.new_with_mnemonic(" De_crypt")
        butt3e.connect("clicked", self.lookup, window)
        hbox2.pack_start(butt3e, 0, 0, False) #, padding = 4)

        sp3 = Spacer()
        butt2 = Gtk.Button.new_with_mnemonic(" E_xit ")
        butt2.connect("clicked", self.OnExit, window)
        hbox2.pack_start(butt2, 1, 1, True)

        lab4 = Gtk.Label(label="  ");   hbox2.pack_start(lab4, 0,0, False)

        #hbox3.set_spacing(4);  #hbox3.set_homogeneous(True)

        sc1 = Gtk.ScrolledWindow()
        self.text1 = Gtk.TextView();    self.text1.set_wrap_mode(True)
        sc1.add_with_viewport(self.text1)
        hbox3.pack_start(sc1, True, True, padding = 4)

        sc2 = Gtk.ScrolledWindow()
        self.text2 = Gtk.TextView();    self.text2.set_wrap_mode(True)
        sc2.add_with_viewport(self.text2)
        hbox3.pack_start(sc2, True, True, padding = 2)

        sc3 = Gtk.ScrolledWindow()
        self.text3 = Gtk.TextView();    self.text3.set_wrap_mode(True)
        sc3.add_with_viewport(self.text3)
        hbox3.pack_start(sc3, True, True, padding = 2)

        sc4 = Gtk.ScrolledWindow()
        self.text4 = Gtk.TextView();    self.text4.set_wrap_mode(True)
        sc4.add_with_viewport(self.text4)
        hbox3.pack_start(sc4, True, True, padding = 4)

        #hbox3.set_child_packing(self.text1, False, True, 4, Gtk.PACK_START)

        lab1 = Gtk.Label(label="");  hbox.pack_start(lab1, True, True, 0)

        #butt1 = Gtk.Button(" _New ")
        #butt1.connect("clicked", self.show_new, window)
        #hbox.pack_start(butt1, False)

        lab2 = Gtk.Label(label="");  hbox.pack_start(lab2, True, True, 0)

        vbox.pack_start(sp1, 0,0, False)
        vbox.pack_start(hbox2, 0,0, False)
        vbox.pack_start(hbox3, True, True, 0)
        #vbox.pack_end(hbox, False)

        window.add(vbox)
        window.show_all()

    def lookup(self, win, butt):
        #print "Lookup", self.entry.get_text()
        pppx = []
        try:
            prog = respath("wn")
            pppx = [prog]
            pppx.append(self.entry.get_text())
            pppx.append("-over")
            out = subprocess.Popen(pppx, stdout=subprocess.PIPE).communicate()[0]
            if out == "":
                self.text1.get_buffer().set_text("No entry or incorrenct spelling")
            else:
                self.text1.get_buffer().set_text(out)

            out = ""
            for aa in "nvar":
                out += "(" + aa + ") "
                pppx = [prog]
                pppx.append(self.entry.get_text())
                pppx.append("-syns" + aa)
                out += subprocess.Popen(pppx, stdout=subprocess.PIPE).communicate()[0]
            self.text2.get_buffer().set_text(out)

            out = ""
            for aa in "nvar":
                out += "(" + aa + ") "
                pppx = [prog]
                pppx.append(self.entry.get_text())
                pppx.append("-ants" + aa)
                out += subprocess.Popen(pppx, stdout=subprocess.PIPE).communicate()[0]
            self.text3.get_buffer().set_text(out)

            out = ""
            for aa in "coorn", "coorv", "hypon", "hypov", "derin", "deriv", \
                    "meron", "holon", "perta", "attrn":
                pppx = [prog]
                pppx.append(self.entry.get_text())
                pppx.append("-" + aa)
                res = subprocess.Popen(pppx, stdout=subprocess.PIPE).communicate()[0]
                if res != "":
                    out += "----------------------------------------------------------- "
                    out += res

            self.text4.get_buffer().set_text(out)

        except:
            print "Cannot execute", pppx, sys.exc_info()
            self.text1.get_buffer().set_text("Cannot execute 'wn', please install it.")

        self.entry.grab_focus()

    def  OnExit(self, arg, srg2 = None):
        self.exit_all()

    def exit_all(self):
        Gtk.main_quit()

    def key_press_event(self, win, event):
        #print "key_press_event", win, event
        pass

    def button_press_event(self, win, event):
        #print "button_press_event", win, event
        pass

# Start of program:

if __name__ == '__main__':

    mainwin = MainWin()
    Gtk.main()









