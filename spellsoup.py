#!/usr/bin/env python3

from __future__ import absolute_import
from __future__ import print_function

import os, sys, string, zlib, struct, platform, random
from datetime import date
from optparse import OptionParser

base = os.path.dirname(os.path.abspath(__file__))
#print("base", base)

sys.path.append(os.path.join(base, "gui"))

import spemod

verbose = 0

def cmdline():

    parser = OptionParser()

    #parser.add_option("-f", "--force",
    #              action="store_true", dest="force",
    #              help="Force overwrite")

    parser.add_option("-l", "--len", dest="xlen", default="8",
                  help="Length of soup string (word count)", metavar="len")

    #parser.add_option("-o", "--out", dest="outname", default="",
    #              help="Write to file; stdout if none specified.",
    #                metavar="filename")
    #
    #parser.add_option("-p", "--pass", dest="passwd", default="1234",
    #              help="Password to use", metavar="pass")
    #
    #parser.add_option("-s", "--str", dest="strx", default="",
    #              help="String to encrypt (quote if space or newline)",
    #                metavar="string")
    #
    #parser.add_option("-q", "--quiet",
    #              action="store_true", dest="quiet",
    #              help="Don't print status messages to stdout")
    #
    #parser.add_option("-e", "--encrypt",
    #              action="store_true", dest="enc", default = 0,
    #              help="Encrypt data")
    #
    #parser.add_option("-d", "--decrypt",
    #              action="store_true", dest="dec", default = 0,
    #              help="Decrypt data")
    #
    parser.add_option("-v", "--verbose", dest="verbose", default=0,
                  action="store_true",
                  help="Status message verbosity")

    parser.add_option("-g", "--debug", dest="debug", default=0,
                  help="Debug output level", metavar="num")

    return parser


# Start of program:

if __name__ == '__main__':

    if sys.version_info[0] < 3:
        print("This program was meant to run on python 3.x or later.")
        sys.exit(1)

    parser = cmdline()
    (options, args) = parser.parse_args()

    #print("args", args)
    #if len (args) == 2:
    #    options.filename = args[0]
    #    if options.outname:
    #        print("Both output option and second argument present.")
    #        sys.exit(1)
    #    else:
    #        options.outname = args[1]
    #
    #if len (args) == 1:
    #    options.filename = args[0]
    #else:
    #    pass
    #
    #if options.enc and options.dec:
    #    print("Conflicting options: both enc / dec specified.")
    #    sys.exit(2);

    #print("spemod", dir(spemod))
    sssmod = spemod.spellencrypt(os.path.join(base, "data", "spell.txt"))
    #print("sssmod", dir(sssmod))

    sssmod.verbose = int(options.verbose)
    sssmod.debug = int(options.debug)
    verbose =  options.verbose

    if not options.xlen:
        options.xlen = int(random.random() * 10 + 2)

    idx = int(random.random() * sssmod.arrlen)
    sss = sssmod.bigarr[idx]
    sss = sss[0].upper() + sss[1:]
    print(sss, end="")

    for aa in range(int(options.xlen)-1):
        idx = int(random.random() * sssmod.arrlen)
        #print("rand", idx)
        nnn = sssmod.bigarr[idx]
        if int(random.random() * 8) == 1:
            print(".", end = "")
            if int(random.random() * 3) == 1:
                print("")
            nnn =  nnn[0].upper() + nnn[1:]
        print("", nnn, end="")

    print(".")

    if int(random.random() * 30) % 2 :
        print()

# EOF
