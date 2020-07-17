#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import print_function

import os, sys, string, zlib, struct
from datetime import date
from optparse import OptionParser

import spemod

verbose = 0

def cmdline():

    parser = OptionParser()

    parser.add_option("-f", "--force",
                  action="store_true", dest="force",
                  help="Force overwrite")

    parser.add_option("-i", "--in", dest="filename", default="",
                  help="Read from file", metavar="FILE")

    parser.add_option("-o", "--out", dest="outname", default="",
                  help="Write to file; stdout if none specified.", metavar="FILE")

    parser.add_option("-p", "--pass", dest="passwd", default="1234",
                  help="Password to use", metavar="STR")

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
    verbose =  options.verbose

    #sssmod.getlen()

    newpass = spemod.genpass(options.passwd)
    #print("pass:", len(newpass), newpass)

    #print(spemod.hexdump(newpass))
    #sys.exit (1)

    wfp = None
    if options.outname:
        if os.access(options.outname, os.F_OK):
            if not options.force:
                print ("Cannot overwrite file:", options.outname," use -f to force");
            sys.exit(1)
        wfp = open(options.outname, "w")
    else:
        wfp = sys.stdout

    arrx = []
    if options.filename:
        fp = open(options.filename, "r")
        for aa in fp:
            #print("line:", bb)
            ss = spemod.ascsplit(aa.strip())
            #print("split:", ss)
            for cc in ss:
                #print("cc=", "'"+cc+"'", end=" ")
                arrx.append(cc)
            arrx.append("\n")
    else:
        if not args:
            print("Must use input file option or pass command line arguments")
            sys.exit(0)
        arrx = args

    if options.enc:
        strx = sssmod.enc_dec(True, arrx, newpass)

    if options.dec:
        strx = sssmod.enc_dec(False, arrx, newpass)

    if wfp:
        wfp.write(strx)
    else:
        print(strx)







