#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import print_function

import os, sys, string, zlib, struct
from datetime import date
from optparse import OptionParser

import spemod

def cmdline():

    parser = OptionParser()
    parser.add_option("-f", "--file", dest="filename", default="",
                  help="Read from file", metavar="FILE")

    parser.add_option("-o", "--out", dest="outname", default="",
                  help="Write to file", metavar="FILE")

    parser.add_option("-p", "--pass", dest="passwd", default="1234",
                  help="Password to use", metavar="FILE")

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

    return parser

# ------------------------------------------------------------
# Convert input to array of offsets / strings

def convert(arrx):

    arr2 = []
    for ww in arrx:
        if len (ww) == 0:
            continue
        if len (ww) > 1:
            nn = sssmod.getword (str.lower(ww))
            if nn:
                if ww[0] in string.ascii_uppercase:
                    #print("bigg", ww, hex(nn))
                    nn |= 0x80000
                #print(ww, hex(nn))
                arr2.append(nn)
            else:
                arr2.append(ww )
        else:
            arr2.append( ww )

    return arr2


def  encrypt(arrx):

    #print("\nlen encode=", len(arr2) )

    arr2 = convert(arrx)

    passidx = 0;

    for ee in arr2:
        if type(ee) == str:
            #print ("[" + ee + "]", end="")
            print (ee, end="")
        else:
            upper = 0
            if ee & 0x80000 > 0:
                upper = 1
                ee = ee & 0x7ffff

            chh = options.passwd[passidx:passidx+1]
            #print ("chh", chh)

            passidx += 1
            if passidx >= len(options.passwd):
                passidx = 0

            # Wrap around:
            ee += ord(chh) * 1000
            #if ee >= sssmod.arrlen:
            ee = ee % sssmod.arrlen

            nn = sssmod.revword (ee)
            if upper == 1:
                nn = nn.capitalize()
            #print ("$" + nn + "$", end="")
            print (nn, end="")

    print ("")


def arrlen(arrx):

    xlen = 0;
    for ww in arrx:
        xlen += len(ww)
    print("xlen", xlen);


# Start of program:

if __name__ == '__main__':

    parser = cmdline()
    (options, args) = parser.parse_args()

    if options.enc and options.dec:
        print("Conflicting options: both enc / dec specified.")
        sys.exit(2);

    if (not options.enc) and (not options.dec):
        print("Missing  option: one of -e (--encrypt) OR -d (--decrypt) must be specified.")
        sys.exit(2);

    sssmod = spemod.spellencrypt("data/spell.txt")
    sssmod.verbose = options.verbose
    sssmod.getlen()

    for aa in range(5):
        options.passwd = spemod.xsum(options.passwd) + options.passwd
        options.passwd = spemod.fwstr(options.passwd)
        options.passwd = spemod.bwstr(options.passwd)

        #options.passwd = spemod.xsum(options.passwd) + options.passwd
        #options.passwd = spemod.fwstr(options.passwd)
        #options.passwd = spemod.bwstr(options.passwd)

    if options.verbose:
        print("Pass:", "'" + options.passwd + "'")

    #sys.exit (1)

    arrx = []
    if options.filename:
        fp = open(options.filename, "r")
        for aa in fp:
            #print("line:", bb)
            ss = spemod.ascsplit(aa)
            #print("split:", ss)
            for cc in ss:
                #print("cc=", "'"+cc+"'", end=" ")
                arrx.append(cc)
    else:
        arrx = args

    if options.enc:
        encrypt(arrx)




