#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import print_function

import os, sys, string, zlib, struct

from datetime import date
from optparse import OptionParser

# Start of program:

printable = string.ascii_letters + "'"

if __name__ == '__main__':

    print("Cleaning dict");

    cnt = 0
    fpi = open("spell.txt.org", "r")
    fpo = open("spell.txt", "w")

    # Load to memory
    for aa in fpi:
        aa = aa.strip().lower()
        if len(aa) > 1:
            mode = 0
            if str.find(aa, "'") >= 0:
                mode = 1
            else:
                for bb in aa:
                    if not bb in printable:
                        mode = 1

            if mode == 0:
                aa += "\r\n"
                fpo.write(aa)



