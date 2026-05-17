#!/usr/bin/env python3

# pylint: disable=C0321
# pylint: disable=C0209
# pylint: disable=C0103
# pylint: disable=C0116

from __future__ import print_function

import os, sys
if sys.version_info[0] < 3:
    print("This program was meant to run on python 3.x or later.")
    sys.exit(1)

#from datetime import date
from optparse import OptionParser

__doc__ = \
'''
  The spellcrypt utility encrypts / decrypts a text file
  into a new text file.
'''
base = os.path.dirname(os.path.abspath(__file__))
#print("base", base)
sys.path.append(os.path.join(base, "spelib"))
sys.path.append("spelib")

import spemod, spepass, hexdump

VERSION = "1.0.4"
options = None
args = None

def cmdline():

    xparse = OptionParser(usage="spellcrypt.py [options] [infile] [outfile]")
    #xparse.epilog = \
    #    "Use filename '-' for  stdin"
    xparse.add_option("-e", "--encrypt",
                  action="store_true", dest="enc", default = 0,
                  help="encrypt data")

    xparse.add_option("-d", "--decrypt",
                  action="store_true", dest="dec", default = 0,
                  help="eecrypt data")

    xparse.add_option("-i", "--in", dest="filename", default="",
                  help="read from file; use '-' for stdin",
                    metavar="infname")

    xparse.add_option("-o", "--out", dest="outname", default="",
                  help="write to file; stdout if no file specified.",
                    metavar="outfname")

    xparse.add_option("-s", "--str", dest="strx", default="",
                  help="string to operate on (quote if space or newline)",
                    metavar="instring")

    xparse.add_option("-p", "--pass", dest="passwd", default="",
                  help="password to use", metavar="pass")

    xparse.add_option("-f", "--force",
                  action="store_true", dest="force",
                  help="force overwrite")

    xparse.add_option("-q", "--quiet",
                  action="store_true", dest="quiet",
                  help="print fewer status messages")

    xparse.add_option("-v", "--verbose", dest="verbose", default=0,
                  action="store_true",
                  help="status message verbosity")

    xparse.add_option("-V", "--version", dest="version", default=0,
                  action="store_true",
                  help="show version")

    xparse.add_option("-z", "--zoo", dest="zoo", default=0,
                  action="store_true",
                  help="show password quality")

    xparse.add_option("-g", "--debug", dest="debug", default=0,
                  help="debug output level", metavar="dlevel")

    xparse.add_option("-m", "--mask", dest="mask", default=0,
                  help="debug output mask", metavar="dmask")

    return xparse

def file2arr(fp):
    arrx = []
    for aa in fp:
        if int(options.debug) > 4:
            print("line:", aa)
        ss = spepass.ascsplit(aa)
        if  options.mask & 0x400:
            print("split:", ss)
        for cc in ss:
            arrx.append(cc)
    return arrx

# ------------------------------------------------------------------------
# Start of program:

def mainfunc():

    global options, args

    if sys.version_info[0] < 3:
        print("This program was meant to run on python 3.x or later.")
        sys.exit(1)

    parser = cmdline()
    options, args = parser.parse_args()

    if options.version:
        print("%s version: %s" % (os.path.basename(sys.argv[0]), VERSION) )
        sys.exit()

    # Convert debug options
    if options.debug:
        if options.debug[:2] == "0x":
            options.debug = int(options.debug, base=16)
        else:
            options.debug = int(options.debug)

    # Convert
    if options.mask:
        if options.mask[:2] == "0x":
            options.mask = int(options.mask, base=16)
        else:
            options.mask = int(options.mask)

    # Propgate to submods
    spepass.debug = options.debug

    if options.debug > 1:
        print("options:", options)

    #print ("debug level", options.debug, "mask", hex(options.mask))
    #if int(options.debug) > 4:
    #    print("args", args)

    if len(args) > 1:
        options.filename = args[0]
        if options.outname:
            print("Both output option and second argument present.")
            sys.exit(2)
        else:
            options.outname = args[1]

    if len (args) == 1:
        options.filename = args[0]
    else:
        pass

    if options.enc and options.dec:
        print("Conflicting options: both enc / dec specified.")
        sys.exit(2)

    if (not options.enc) and (not options.dec):
        print("Missing option: one of -e (--encrypt) or -d (--decrypt) must be specified.")
        sys.exit(2)

    #print("pass in:", len(options.passwd), options.passwd)
    newpass = spepass.Primi().genpass(options.passwd)
    #print("pass:", len(newpass), newpass)

    if options.zoo:
        print("Password head:\n" + hexdump.HexDump(newpass)[:300], "....")
        print ("Frequency distribution:")
        print(spepass.testpass(newpass))
        sys.exit(0)

    #print("spemod", dir(spemod))
    #os.path.join(base, "spelib", "spell.txt"))
    sssmod = spemod.spellencrypt()
    #print("sssmod", dir(sssmod))

    # Propagate to sub systems
    sssmod.verbose = int(options.verbose)
    sssmod.debug = options.debug
    sssmod.mask  = options.mask

    spemod.debug = options.debug
    spemod.mask = options.mask

    arrx = [];  fp = None
    if options.filename:
        if options.filename == "-":
            fp = sys.stdin
        else:
            try:
                fp = open(options.filename, "r")
            except:
                print("Input file", "'" + options.filename + "'" , "must exist.")
                sys.exit(1)

        arrx = file2arr(fp)

    elif options.strx:
        ss = spepass.ascsplit(options.strx)
        for cc in ss:
            arrx.append(cc)

    else:
        print("Must use input file option or pass command line file arguments.")
        sys.exit(0)

    wfp = None
    if options.outname:
        if os.access(options.outname, os.R_OK):
            if not options.force:
                print ("Cannot overwrite file:", options.outname," use -f to force")
                sys.exit(1)
            try:
                os.remove(options.outname)
            except:
                print("Warn: cannot remove old file:", options.outname, sys.exc_info()[1])
        try:
            wfp = open(options.outname, "w")
        except:
            print ("Cannot create outfile:", "'" + options.outname + "'", sys.exc_info()[1])
            sys.exit(2)

    if  options.mask & 0x100:
        print("arrx:", arrx)

    if options.enc:
        strx = sssmod.enc_dec(True, arrx, newpass)
        #strx = ""
        #for aa in arrx:
        #    strx += aa
    elif options.dec:
        strx = sssmod.enc_dec(False, arrx, newpass)
        #strx = ""
        #for aa in arrx:
        #    strx += aa
    else:
        print("Bad command ")

    if  options.mask & 0x100:
        print("strx:", strx)
    if wfp:
        wfp.write(strx)
        wfp.close()
    else:
        print(strx, end = "")

if __name__ == '__main__':
    mainfunc()

# EOF
