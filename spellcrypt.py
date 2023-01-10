#!/usr/bin/env python3

from __future__ import absolute_import
from __future__ import print_function

import os, sys, string, zlib, struct, platform
from datetime import date
from optparse import OptionParser

base = os.path.dirname(os.path.abspath(__file__))
#print("base", base)
#sys.path.append(os.path.join(base, "gui"))
sys.path.append(os.path.join(base, "spellcryptlib"))
#from spellcrypt import spemod

import spemod, spepass, hexdump

verbose = 0

def cmdline():

    parser = OptionParser()

    parser.add_option("-f", "--force",
                  action="store_true", dest="force",
                  help="Force overwrite")

    parser.add_option("-i", "--in", dest="filename", default="",
                  help="Read from file", metavar="filename")

    parser.add_option("-o", "--out", dest="outname", default="",
                  help="Write to file; stdout if none specified.",
                    metavar="filename")

    parser.add_option("-p", "--pass", dest="passwd", default="",
                  help="Password to use", metavar="pass")

    parser.add_option("-s", "--str", dest="strx", default="",
                  help="String to encrypt (quote if space or newline)",
                    metavar="string")

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
                  action="store_true",
                  help="Status message verbosity")

    parser.add_option("-z", "--zoo", dest="zoo", default=0,
                  action="store_true",
                  help="Show password quality")

    parser.add_option("-g", "--debug", dest="debug", default=0,
                  help="Debug output level", metavar="level")

    return parser

# ------------------------------------------------------------------------
# Start of program:

if __name__ == '__main__':

    if sys.version_info[0] < 3:
        print("This program was meant to run on python 3.x or later.")
        sys.exit(1)

    parser = cmdline()
    (options, args) = parser.parse_args()
    options.mask = 0

    # Convert debug options and debug mask
    if options.debug:
        if options.debug[:2] == "0x":
            options.debug = int(options.debug, base=16)
        else:
            options.debug = int(options.debug)

        # see if masks are specified
        if options.debug > 0xff:
            options.mask = options.debug
            options.debug &= 0xff
        else:
            options.mask = 0

    #print ("debug level", options.debug, "mask", hex(options.mask))
    #if int(options.debug) > 4:
    #    print("args", args)

    if len (args) == 2:
        options.filename = args[0]
        if options.outname:
            print("Both output option and second argument present.")
            sys.exit(1)
        else:
            options.outname = args[1]

    if len (args) == 1:
        options.filename = args[0]
    else:
        pass

    if options.enc and options.dec:
        print("Conflicting options: both enc / dec specified.")
        sys.exit(2);

    if (not options.enc) and (not options.dec):
        print("Missing option: one of -e (--encrypt) or -d (--decrypt) must be specified.")
        sys.exit(2);

    #print("pass in:", len(options.passwd), options.passwd)
    newpass = spepass.Primi().genpass(options.passwd)
    #print("pass:", len(newpass), newpass)

    if options.zoo:
        print("Password head:\n", hexdump.HexDump(newpass)[:300], "....")
        print ("Frequency distribution:\n", spemod.testpass(newpass))
        sys.exit(0)

    #print("spemod", dir(spemod))
    sssmod = spemod.spellencrypt() #os.path.join(base, "spellcryptlib", "spell.txt"))
    #print("sssmod", dir(sssmod))

    # Propagate to sub systems
    sssmod.verbose = int(options.verbose)
    sssmod.debug = options.debug
    sssmod.mask  = options.mask

    spemod.debug = options.debug
    spemod.mask = options.mask

    verbose =  options.verbose

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

        for aa in fp:
            if int(options.debug) > 4:
                print("line:", aa)

            ss = spepass.ascsplit(aa)
            #if  options.mask & 0x400:
            #    print("split:", ss)

            for cc in ss:
                arrx.append(cc)

    elif options.strx:
        if int(options.debug) > 5:
            print("line:", aa)
        ss = spemod.ascsplit(options.strx)
        for cc in ss:
            arrx.append(cc)

    else:
        print("Must use input file option or pass command line file arguments.")
        sys.exit(0)

    wfp = None
    if options.outname:
        if os.access(options.outname, os.R_OK):
            if not options.force:
                print ("Cannot overwrite file:", options.outname," use -f to force");
                sys.exit(1)
            try:
                os.remove(options.outname)
            except:
                print("Warn: cannot remove old file:", options.outname, sys.exc_info()[1])
        try:
            wfp = open(options.outname, "w")
        except:
            print ("Cannot create outfile:", "'" + options.outname + "'", sys.exc_info()[1]);
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
        print("Bad command ");

    if  options.mask & 0x100:
        print("strx:", strx)

    if wfp:
        wfp.write(strx)
        wfp.close()
    else:
        print(strx, end = "")

# EOF