#!/usr/bin/env python3

from __future__ import print_function
import sys
if sys.version_info[0] < 3:
    print("This program was meant to run on python 3.x or later.")
    sys.exit(1)

import os, getopt, signal, select, socket, time, struct
import random, stat

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

base = os.path.dirname(os.path.abspath(__file__))
sys.path.append(base + os.sep + ".." + os.sep + 'spelib')
sys.path.append('spelib')

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


# ------------------------------------------------------------------------
# Handle command line. Interpret optarray and decorate the class
# This allows a lot of sub utils to have a common set of options.

class Config:

    def __init__(self, optarr):

        ddd = self.dupoptcheck(optarr)
        if ddd:
            raise ValueError("Duplicate options on comline.", ddd)

        global glsoptarr
        glsoptarr = optarr

        self.optarr = optarr
        self.verbose = False
        self.debug = False
        self.sess_key = ""

    def comline(self, argv):
        optletters = ""
        for aa in self.optarr:
            optletters += aa[0]
        #print( optletters    )
        # Create defaults:
        err = 0
        for bb in range(len(self.optarr)):
            if self.optarr[bb][1]:
                # Coerse type
                if type(self.optarr[bb][2]) == type(0):
                    self.__dict__[self.optarr[bb][1]] = int(self.optarr[bb][2])
                if type(self.optarr[bb][2]) == type(""):
                    self.__dict__[self.optarr[bb][1]] = str(self.optarr[bb][2])
        try:
            opts, args = getopt.getopt(argv, optletters)
        except getopt.GetoptError as err:
            print( "Invalid option(s) on command line:", err)
            raise
            return ()
        except:
            print(sys.exc_info())

        #print( "opts", opts, "args", args)
        for aa in opts:
            for bb in range(len(self.optarr)):
                if aa[0][1] == self.optarr[bb][0][0]:
                    #print( "match", aa, self.optarr[bb])
                    if len(self.optarr[bb][0]) > 1:
                        #print( "arg", self.optarr[bb][1], aa[1])
                        if self.optarr[bb][2] != None:
                            if type(self.optarr[bb][2]) == type(0):
                                self.__dict__[self.optarr[bb][1]] = int(aa[1])
                            if type(self.optarr[bb][2]) == type(""):
                                self.__dict__[self.optarr[bb][1]] = str(aa[1])
                    else:
                        #print( "set", self.optarr[bb][1], self.optarr[bb][2])
                        if self.optarr[bb][2] != None:
                            self.__dict__[self.optarr[bb][1]] = 1
                        #print( "call", self.optarr[bb][3])
                        if self.optarr[bb][3] != None:
                            self.optarr[bb][3]()
        return args

    def dupoptcheck(self, optarr):
        optdup = {}
        for bb in range(len(optarr)):
            kkk = optarr[bb][0][0]
            try:
                optdup[kkk] += 1
            except KeyError:
                optdup[kkk] = 1
            except:
                print(sys.exc_info())
        #print(optdup)
        found = False
        for cc in optdup.keys():
            if optdup[cc] > 1:
                #print("found dup", cc)
                found = cc
        return found

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
