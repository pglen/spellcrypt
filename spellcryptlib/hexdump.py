# ------------------------------------------------------------------------
#!/usr/bin/env python3

from __future__ import absolute_import
from __future__ import print_function

import os, sys, string, zlib, struct, platform
from datetime import date
from optparse import OptionParser
# Corrected to handle unicode accidental

class   CharClass:

    def __init__(self):
        self.ctrlchar = "\n\r| "
        pass

    def isprint(self, chh):
        ret = False
        try:
            if ord(chh) > 127:
                ret =  False
            elif ord(chh) < 32:
                ret =  False
            elif chh in string.ascii_letters:
                ret =  True
            elif chh in string.digits:
                ret =  True
            elif chh in string.punctuation:
                ret =  True
            else:
                print("classifier error?")
        except:
            pass
        #print("isprint", chh, ret)
        return ret

# ------------------------------------------------------------------------
# Return a hex dump formatted string

def HexDump(strx, llen = 16):

    lenx = len(strx);   outx = ""
    ccl = CharClass()

    try:
        for aa in range(lenx//16):
            outx += " "
            for bb in range(16):
                try:
                    outx += "%02x " % ord(strx[aa * 16 + bb])
                except:
                    pass
                    out +=  "?? "
                    #outx += "%02x " % strx[aa * 16 + bb]

            outx += " | "
            for cc in range(16):
                chh = strx[aa * 16 + cc]
                if ccl.isprint(chh):
                    outx += "%c" % chh
                else:
                    outx += "."
            outx += " | \n"

        # Print remainder on last line
        remn = lenx % 16 ;   divi = lenx // 16
        if remn:
            outx += " "
            for dd in range(remn):
                try:
                    outx += "%02x " % ord(strx[divi * 16 + dd])
                except:
                    outx +=  "?? "
                    pass
                    #outx += "%02x " % int(strx[divi * 16 + dd])

            outx += " " * ((16 - remn) * 3)
            outx += " | "
            for cc in range(remn):
                chh = strx[divi * 16 + cc]
                if ccl.isprint(chh):
                    outx += "%c" % chh
                else:
                    outx += "."
            outx += " " * ((16 - remn))
            outx += " | \n"
    except:
        print("Error on hexdump", sys.exc_info())
        #print_exc("hexdump")

    return(outx)

