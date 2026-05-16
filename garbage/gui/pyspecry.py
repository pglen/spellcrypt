#!/usr/bin/env python3

import os, sys, getopt, signal, select, socket, time, struct
import random, stat

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

base = os.path.dirname(os.path.abspath(__file__))
sys.path.append(base + os.sep + ".." + os.sep + 'spelib')

from pgutil import  *
from mainwin import  *

# ------------------------------------------------------------------------
# Globals

version = "0.00"

# ------------------------------------------------------------------------

def phelp():

    print()
    print( "Usage: " + os.path.basename(sys.argv[0]) + " [options]")
    print()
    print( "Options:    -d level  - Debug level 0-10")
    print( "            -p        - Port to use (default: 9999)")
    print( "            -v        - Verbose")
    print( "            -V        - Version")
    print( "            -q        - Quiet")
    print( "            -h        - Help")
    print()
    sys.exit(0)

# ------------------------------------------------------------------------
def pversion():
    print( os.path.basename(sys.argv[0]), "Version", version)
    sys.exit(0)

        #["p:",  "port",     9999,   None],      \
        # option, var_name, initial_val, function

optarr = \
    ["d:",  "pgdebug",  0,      None],      \
    ["v",   "verbose",  0,      None],      \
    ["q",   "quiet",    0,      None],      \
    ["t",   "test",     "x",    None],      \
    ["V",   None,       None,   pversion],  \
    ["h",   None,       None,   phelp]      \

conf = Config(optarr)

def mainfunc():
    global mw
    if sys.version_info[0] < 3:
        print("This program was meant to run on python 3.x or later.")
        sys.exit(1)

    args = conf.comline(sys.argv[1:])
    mw = MainWin()
    Gtk.main()
    sys.exit(0)


if __name__ == '__main__':
    mainfunc()

# EOF
