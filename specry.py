#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import print_function

import os, sys, string, zlib, struct

from datetime import date
from optparse import OptionParser

import spemod

# Start of program:

if __name__ == '__main__':

    parser = OptionParser()
    parser.add_option("-f", "--file", dest="filename", default="",
                  help="Read from file", metavar="FILE")

    parser.add_option("-o", "--out", dest="outname", default="",
                  help="Write to file", metavar="FILE")

    parser.add_option("-q", "--quiet",
                  action="store_true", dest="quiet",
                  help="Don't print status messages to stdout")

    parser.add_option("-e", "--encrypt",
                  action="store_true", dest="enc", default = 0,
                  help="Encrypt data")

    parser.add_option("-d", "--decrypt",
                  action="store_true", dest="dec", default = 0,
                  help="Decrypt data")

    parser.add_option("-v", "--verbose", dest="verbose", default=0,
                  help="Status message verbosity")

    (options, args) = parser.parse_args()

    if options.enc and options.dec:
        print("Conflicting options: enc/ dec")
        sys.exit(2);

    spemod.init()

    arrx = []
    if options.filename:
        fp = open(options.filename, "r")
        for aa in fp:
            bb = str.lower(aa)
            #print("line:", bb)
            for cc in spemod.ascsplit(bb):
                #print("cc=", "'"+cc+"'", end=" ")
                arrx.append(cc)
    else:
        arrx = args

    xlen = 0;
    for ww in arrx:
        xlen += len(ww)

    #print("xlen", xlen);

    arr2 = []
    for ww in arrx:
        #print (ww, end=" ")
        if len (ww) > 1:
            nn = spemod.getword (ww)
            if nn:
                arr2.append(nn)
            else:
                arr2.append(ww)
        else:
            arr2.append(ww)
            #arr2.append("'"+ww+"'")

    #print("\nlen encode=", len(arr2) )

    for ee in arr2:
        if type(ee) == str:
            print (ee, end="")
        else:
            nn = spemod.revword (ee)
            print (nn, end=" ")

    print ("")



