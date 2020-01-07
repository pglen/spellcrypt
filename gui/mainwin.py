#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import print_function

import os, sys, getopt, signal, string
import random, time, subprocess

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GLib
from gi.repository import GObject

sys.path.append('..')

import spemod

def message(strx, title=None):

        dialog = Gtk.MessageDialog(title, None,
            Gtk.ButtonsType.NONE , Gtk.ButtonsType.CLOSE,
            'Message: \n\n%s' % (strx) )

        # Close dialog on user response

        dialog.set_transient_for(mainwin.window)

        dialog.connect ("response", lambda d, r: d.destroy())
        dialog.show()

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
        print ("Cannot resolve path", fname, sys.exc_info())
    return None

# ------------------------------------------------------------------------
# An N pixel vertical spacer. Default to 5.

class Spacer(Gtk.Label):

    def __init__(self, sp = 5):
        GObject.GObject.__init__(self)
        #sp *= 1000
        #self.set_markup("<span  size=\"" + str(sp) + "\"> </span>")
        self.set_text(" " * sp)

# ------------------------------------------------------------------------

class MainWin():

    def __init__(self):

        self.sssmod = None
        self.orig = None;  self.encr = None;  self.decr = None

        self.window = Gtk.Window(Gtk.WindowType.TOPLEVEL)

        #if not self.sssmod:
        self.sssmod =  spemod.spellencrypt("../data/spell.txt")

        #os.chdir( os.path.dirname(os.getcwd()) )

        self.window.set_title("Spell Encryptor UI")
        self.window.set_position(Gtk.WindowPosition.CENTER)

        #ic = Gtk.Image(); ic.set_from_stock(Gtk.STOCK_DIALOG_INFO, Gtk.IconSize.BUTTON)
        #self.window.set_icon(ic.get_pixbuf())

        www = Gdk.Screen.width(); hhh = Gdk.Screen.height();
        #self.window.set_default_size(6*www/8, 6*hhh/8)

        self.window.set_default_size(8*hhh/8, 6*hhh/8)

        #self.window.set_default_size(1024, 768)

        #self.window.set_flags(Gtk.CAN_FOCUS | Gtk.SENSITIVE)

        self.window.set_events(  Gdk.EventMask.POINTER_MOTION_MASK |
                            Gdk.EventMask.POINTER_MOTION_HINT_MASK |
                            Gdk.EventMask.BUTTON_PRESS_MASK |
                            Gdk.EventMask.BUTTON_RELEASE_MASK |
                            Gdk.EventMask.KEY_PRESS_MASK |
                            Gdk.EventMask.KEY_RELEASE_MASK |
                            Gdk.EventMask.FOCUS_CHANGE_MASK )

        self.window.connect("destroy", self.OnExit)
        self.window.connect("key-press-event", self.key_press_event)
        self.window.connect("button-press-event", self.button_press_event)

        try:
            self.window.set_icon_from_file("icon.png")
        except:
            pass

        vbox = Gtk.VBox();
        vbox.pack_start( Spacer(1), 0, 0, 0)

        hbox = Gtk.HBox();  hbox2 = Gtk.HBox(); hbox3 = Gtk.VBox();

        hbox2.pack_start( Spacer(1), 0, 0, False)
        lab3 = Gtk.Label(label="  Enter PassWord: ");
        hbox2.pack_start( Spacer(1), 0, 0, False)
        hbox2.pack_start(lab3, 0, 0, False)
        self.entry = Gtk.Entry(); self.entry.set_visibility(False)
        hbox2.pack_start( Spacer(1), 0, 0, False)
        hbox2.pack_start(self.entry, 0, 0, 0)

        hbox2.pack_start( Spacer(1), 0, 0, False)
        butt3 = Gtk.Button.new_with_mnemonic(" _Reveal ")
        butt3.connect("clicked", self.reveal, self.window)
        hbox2.pack_start(butt3, 0, 0, False)

        hbox2.pack_start(Spacer(1), 0, 0, False)
        butt3f = Gtk.Button.new_with_mnemonic(" Load _File ")
        butt3f.connect("clicked", self.load, self.window, 0)
        hbox2.pack_start(butt3f, 0, 0, False)

        hbox2.pack_start( Spacer(1), 0, 0, False)
        butt3e = Gtk.Button.new_with_mnemonic(" _Encrypt ")
        butt3e.connect("clicked", self.encrypt, self.window)
        hbox2.pack_start(butt3e, 0, 0, False)

        hbox2.pack_start( Spacer(1), 0, 0, False)
        butt3e = Gtk.Button.new_with_mnemonic(" _Decrypt ")
        butt3e.connect("clicked", self.decrypt, self.window)
        hbox2.pack_start(butt3e, 0, 0, False)

        hbox2.pack_start( Spacer(1), 0, 0, False)
        butt3f = Gtk.Button.new_with_mnemonic(" _Check ")
        butt3f.connect("clicked", self.check, self.window)
        hbox2.pack_start(butt3f, 0, 0, False)

        hbox2.pack_start( Spacer(1), 0, 0, False)
        butt2 = Gtk.Button.new_with_mnemonic(" E_xit ")
        butt2.connect("clicked", self.OnExit, self.window)
        hbox2.pack_start(butt2, 1, 1, True)

        lab4 = Gtk.Label(label="  ");   hbox2.pack_start(lab4, 0,0, False)

        sc1 = Gtk.ScrolledWindow()
        self.text1 = Gtk.TextView();    self.text1.set_wrap_mode(True)
        sc1.add_with_viewport(self.text1)

        hbox5a = Gtk.HBox(); hbox5a.set_spacing(2)
        hbox5a.pack_start(sc1, True, True, True)

        #hbox5a.pack_start(hbox5v, 0, 0, 0)
        #hbox5a.pack_start(self.buttcol(0), 0, 0, 0)
        hbox3.pack_start(hbox5a, True, True, True)

        sc2 = Gtk.ScrolledWindow()
        self.text2 = Gtk.TextView();    self.text2.set_wrap_mode(True)
        sc2.add_with_viewport(self.text2)
        hbox6a = Gtk.HBox(); hbox6a.set_spacing(2)
        hbox6a.pack_start(sc2, True, True, True)

        #hbox6a.pack_start(self.buttcol(1), 0, 0, 0)
        hbox3.pack_start(hbox6a, True, True, padding = 2)

        sc3 = Gtk.ScrolledWindow()
        self.text3 = Gtk.TextView();    self.text3.set_wrap_mode(True)
        sc3.add_with_viewport(self.text3)
        hbox7a = Gtk.HBox(); hbox7a.set_spacing(2)
        hbox7a.pack_start(sc3, True, True, padding = 2)

        #hbox7a.pack_start(self.buttcol(2), 0, 0, 0)
        hbox3.pack_start(hbox7a, True, True, padding = 2)

        lab1 = Gtk.Label(label="");  hbox.pack_start(lab1, True, True, 0)
        lab2 = Gtk.Label(label="");  hbox.pack_start(lab2, True, True, 0)

        vbox.pack_start( Spacer(1), 0,0, False)
        vbox.pack_start(hbox2, 0,0, False)
        vbox.pack_start(Spacer(1), 0, 0, 0)

        vbox.pack_start(hbox3, True, True, 0)

        hbox8 = Gtk.HBox()
        lab1a = Gtk.Label(label="");
        lab2a = Gtk.Label(label="");
        lab3a = Gtk.Label(label=" Status:  ");
        self.statlab =  Gtk.Label(label="  Idle ");

        #self.statlab.set_justify(Gtk.Justification.LEFT)
        #self.statlab.set_xalign(Gtk.Align.START)
        self.statlab.set_xalign(0)
        #self.statlab.set_yalign(Gtk.Align.START)

        hbox8.pack_start(lab1a, False, False, 0)
        hbox8.pack_start(lab3a, False, False, 0)
        hbox8.pack_start(self.statlab, True, True, 0)
        hbox8.pack_start(lab2a, False, False, 0)

        vbox.pack_start(hbox8, False, True, 0)

        self.window.add(vbox)
        self.window.show_all()

    def buttcol(self, idx):

        hbox5v = Gtk.VBox(); hbox5v.set_spacing(2)
        hbox5v.pack_start(Spacer(), True, True, True)
        butt5 = Gtk.Button.new_with_mnemonic(" Load ")
        butt5.connect("clicked", self.load, self.window, idx)
        hbox5v.pack_start(butt5, 0, 0, 0)

        butt5a = Gtk.Button.new_with_mnemonic(" Copy ")
        butt5a.connect("clicked", self.paste, self.window, idx)
        hbox5v.pack_start(butt5a, 0, 0, 0)

        butt5b = Gtk.Button.new_with_mnemonic(" Paste ")
        butt5b.connect("clicked", self.copy, self.window, idx)
        hbox5v.pack_start(butt5b, 0, 0, 0)

        butt5c = Gtk.Button.new_with_mnemonic(" SelAll ")
        butt5c.connect("clicked", self.paste,idx, self.window, idx)
        hbox5v.pack_start(butt5c, 0, 0, 0)
        hbox5v.pack_start(Spacer(), True, True, True)

        return hbox5v

    def reveal(self, arg1, arg2):
        self.entry.set_visibility(not self.entry.get_visibility())

    # --------------------------------------------------------------------

    def copy(self, win, butt, idx):
        #print("Copy clip")
        clip = Gtk.Clipboard.get_default(Gdk.Display().get_default())
        self.text2.get_buffer().copy_clipboard(clip)

    def paste(self, win, butt, idx):
        clip = Gtk.Clipboard.get_default(Gdk.Display().get_default())
        self.text1.get_buffer().paste_clipboard(clip, None, True)

    def check(self, win, butt):

        #print ("check", self.orig)

        if not self.orig:
            message("No text loaded")
            return

        if not self.encr:
            message("No encrypted text.")
            return

        if not self.decr:
            message("No decrypted text.")
            return

        s1 = spemod.rmspace(self.orig); s2 = spemod.rmspace(self.decr)
        if  s1 == s2:
            message("Original and decrypted texts match.")
        else:
            offs = 0
            for aa in range(len(s1)):
                if s1[aa] != s2[aa]:
                    offs = aa
                    break

            message("Error on decryption. DIFF at offset %d" % aa)
            print("orig", "'" + self.orig[aa:aa+66] + "'")
            print("decr", "'" + self.decr[aa:aa+66] + "'")

    # --------------------------------------------------------------------

    def encrypt(self, win, butt):
        #print ("encrypt", self.orig)

        self.show_stat("Started Encryption")

        ppp = self.entry.get_text()
        if len(ppp) == 0:
            message("Cannot have an empty password.")
            return

        self.newpass = spemod.genpass(ppp)

        try:
            if not self.sssmod:
                self.sssmod =  spemod.spellencrypt("data/spell.txt")
        except:
            print ("Cannot load encryption.")
            raise ValueError("Cannot load dictionary.")

        pppx = []; arrx = []

        buff =  self.text1.get_buffer()
        for ccc in range(buff.get_line_count()):
            iter = buff.get_iter_at_line(ccc)
            iter2 = buff.get_iter_at_line(ccc+1)
            aa = buff.get_text(iter, iter2, False)
            #print ("buff", , "eee")

            ss = spemod.ascsplit(aa.strip())
            for cc in ss:
                #print("cc=", ("'"+cc+"'", end=" ")
                arrx.append(cc)

            arrx.append("\n")

        self.encr = self.sssmod.enc_dec(True, arrx, self.newpass)

        self.text2.get_buffer().set_text(self.encr)


    def decrypt(self, win, butt):
        #print ("encrypt", self.orig)

        self.show_stat("Started Decryption")

        ppp = self.entry.get_text()
        if len(ppp) == 0:
            message("Cannot have an empty password.")
            return

        self.newpass = spemod.genpass(ppp)

        try:
            if not self.sssmod:
                self.sssmod =  spemod.spellencrypt("../data/spell.txt")
        except:
            print ("Cannot load encryption.")
            raise ValueError("Cannot load dictionary.")

        pppx = []; arrx = []

        buff =  self.text2.get_buffer()
        for ccc in range(buff.get_line_count()):
            iter = buff.get_iter_at_line(ccc)
            iter2 = buff.get_iter_at_line(ccc+1)
            aa = buff.get_text(iter, iter2, False)
            #print ("buff", , "eee")

            aa = aa.strip()
            ss = spemod.ascsplit(aa)
            for cc in ss:
                #print("cc=", ("'"+cc+"'", end=" ")
                arrx.append(cc)
            arrx.append("\n")

        self.decr = self.sssmod.enc_dec(False, arrx, self.newpass)

        self.text3.get_buffer().set_text(self.decr)

    def show_stat(self, strx):
        global time_label
        self.statlab.set_text(strx);
        time_label = 0;

    # --------------------------------------------------------------------
    def exec_open(self, win, resp, old):

        #print  ("done_mac_fc", resp)

        # Back to original dir
        #os.chdir(os.path.dirname(old))

        if resp == Gtk.ButtonsType.OK:
            try:
                fname = win.get_filename()
                if not fname:
                    print("Must have filename")
                else:
                    self.show_stat("Loading file: '%s' " % fname)
                    fh = open(fname, "rb"); buff2 = fh.read()
                    fh.close()

                    if sys.version_info.major < 3:
                        self.orig  = buff2
                    else:
                        try:
                            self.orig  = buff2.decode('UTF-8')
                        except UnicodeDecodeError:
                            self.orig  = buff2.decode('cp437')

                    #print("type", type(self.orig))

                    self.orig = spemod.rmjunk(self.orig)
                    self.text1.get_buffer().set_text(self.orig)
                    self.show_stat("Loaded %d bytes" % len(self.orig))

            except:
                print("Cannot load file", sys.exc_info())
        win.destroy()

    def load(self, win, butt, idx):
        #print("Loading file:")

        global time_label
        self.show_stat("Opening File");

        old = os.getcwd()
        but =   "Cancel", Gtk.ButtonsType.CANCEL, "Load Macro", Gtk.ButtonsType.OK
        fc = Gtk.FileChooserDialog("Load file for encryption:", None, Gtk.FileChooserAction.OPEN, \
            but)
        #fc.set_current_folder(xfile)
        fc.set_current_folder(old)
        fc.set_default_response(Gtk.ButtonsType.OK)
        fc.connect("response", self.exec_open, old)
        fc.run()

    def lookup(self):

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
            print ("Cannot execute", pppx, sys.exc_info())
            self.text1.get_buffer().set_text("Cannot execute 'wn', please install it.")

        self.entry.grab_focus()

    def  OnExit(self, arg, srg2 = None):
        self.exit_all()

    def exit_all(self):
        Gtk.main_quit()

    def key_press_event(self, win, event):
        #print ("key_press_event", win, event)
        pass

    def button_press_event(self, win, event):
        #print ("button_press_event", win, event)
        pass

time_done = 0
time_label = 0

mainwin =  None

# ------------------------------------------------------------------------
# App timer tick

def handler_tick():

    global time_done, time_label, mainwin

    try:
        #print ("Tick %d" % time_done)

        time_done += 1; time_label += 1

        if time_label == 5:
            mainwin.statlab.set_text("")

        if time_label == 7:
            mainwin.statlab.set_text("Idle.")

    except:
        print("Exception in timer handler", sys.exc_info())

    try:
        GLib.timeout_add(1000, handler_tick)
    except:
        print("Exception starting new timer handler", sys.exc_info())


# Start of program:

if __name__ == '__main__':

    mainwin = MainWin()
    GLib.timeout_add(1000, handler_tick)
    Gtk.main()

# EOF



