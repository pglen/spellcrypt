#!/usr/bin/env python3

from __future__ import absolute_import
from __future__ import print_function

import os, sys, string, zlib, struct, platform
from datetime import date
from optparse import OptionParser

base = os.path.dirname(os.path.abspath(__file__))
#print("base", base)

sys.path.append(os.path.join(base, "gui"))

import spemod

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

    parser.add_option("-p", "--pass", dest="passwd", default="1234",
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

    parser.add_option("-g", "--debug", dest="debug", default=0,
                  help="Debug output level", metavar="level")

    return parser


# Start of program:

if __name__ == '__main__':

    if sys.version_info[0] < 3:
        print("This program was meant to run on python 3.x or later.")
        sys.exit(1)

    parser = cmdline()
    (options, args) = parser.parse_args()
    #print("args", args)

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
        print("Missing option: one of -e (--encrypt) OR -d (--decrypt) must be specified.")
        sys.exit(2);

    #print("spemod", dir(spemod))
    sssmod = spemod.spellencrypt(os.path.join(base, "data", "spell.txt"))
    #print("sssmod", dir(sssmod))

    sssmod.verbose = int(options.verbose)
    sssmod.debug = int(options.debug)
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
        try:
            fp = open(options.filename, "r")
        except:
            print("Input file", "'" + options.filename + "'" , "must exist.")
            sys.exit(1)

        for aa in fp:
            #print("line:", bb)
            ss = spemod.ascsplit(aa.strip())
            #print("split:", ss)
            for cc in ss:
                #print("cc=", "'"+cc+"'", end=" ")
                arrx.append(cc)
            arrx.append("\n")
    elif options.strx:
        ss = spemod.ascsplit(options.strx.strip())
        for cc in ss:
            arrx.append(cc)
        arrx.append("\n")
    else:
        print("Must use input file option or pass command line file arguments.")
        sys.exit(0)

    if int(options.debug) > 2:
        print("arrx", arrx)

    if options.enc:
        strx = sssmod.enc_dec(True, arrx, newpass)

    if options.dec:
        strx = sssmod.enc_dec(False, arrx, newpass)

    if wfp:
        wfp.write(strx)
    else:
        print(strx)

# EOF