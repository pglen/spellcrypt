#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import print_function

import os, sys, string, zlib, struct

from datetime import date
from optparse import OptionParser

# Start of program:

if __name__ == '__main__':

    print("Cleaning dict");


    cnt = 0
    fpi = open("spell.txt.org", "r")
    fpo = open("spell.txt", "w")

    # Load to memory
    for aa in fpi:
        aa = aa.strip()   #.lower()
        if len(aa) > 1:
            if str.find(aa, "'") >= 0:
                pass
            else:
                aa += "\r\n"
                fpo.write(aa)


