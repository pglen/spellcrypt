#!/usr/bin/env python3
# ------------------------------------------------------------------------

from __future__ import absolute_import
from __future__ import print_function

import os, sys, string, zlib, struct, platform
from datetime import date

debug = 0

# Primitives. Keep results below 255 by truncation

class Primi():

    def __init__(self):
        self.prepass   = string.ascii_letters * 4
        pass

    # Generate password from passed string by extending / modulating
    def     genpass(self, passwd):
        #print ("'" + prepass + "'" )
        passwd = passwd + self.prepass + passwd + self.prepass + passwd

        for aa in range(7):
            passwd = self.bwstr(passwd)
            passwd = self.xorstr(passwd, 0x55)
            passwd = self.butter(passwd)

            passwd = self.fwstr(passwd)
            passwd = self.xorstr(passwd, 0x55)
            passwd = self.butter(passwd)

            passwd = self.modstr(passwd, "12345678")
            passwd = self.xorstr(passwd, 0x55)
            passwd = self.butter(passwd)

        for aa in range(5):

            passwd = self.fwstr(passwd)
            passwd = self.xorstr(passwd, 0x55)
            passwd = self.butter(passwd)

            passwd = self.modstr(passwd, "12345678")
            passwd = self.xorstr(passwd, 0x55)
            passwd = self.butter(passwd)


        return passwd

    def _xsum(self, passwd):
        sss = 0
        for aa in passwd:
            sss += ord(aa)
        return chr(sss & 0xff)

    # All below primitives are reversible

    def fwstr(self, passwd):
        passwd2 = passwd + " "
        sss = ""
        for bb in range(0, len(passwd)):
            #print ("c", passwd[bb])
            sss += chr( (ord(passwd2[bb]) + ord(passwd2[bb+1])) & 0xff)
        return sss

    def xorstr(self, passwd, chh):
        sss = ""
        for bb in range(0, len(passwd)):
            #print ("c", passwd[bb])
            sss += chr((ord(passwd[bb]) ^ chh) & 0xff)
        return sss

    def modstr(self, passwd, mod):
        sss = ""
        cc = 0
        for bb in range(0, len(passwd)):
            #print ("c", passwd[bb])
            sss += chr((ord(passwd[bb]) + ord(mod[cc]) ) & 0xff)
            cc += 1
            if cc >= len(mod): cc = 0

        return sss

    def butter(self, passwd):
        sss = ""; rrr = ""
        for bb in range(0, len(passwd)//2):
            #print ("c", passwd[bb])
            sss += chr((ord(passwd[bb]) + ord(passwd[2*bb]) ) & 0xff)
            rrr += chr((ord(passwd[bb]) + ord(passwd[2*bb]) ) & 0xff)
        return sss + rrr

    def bwstr(self, passwd):
        sss = ""
        for bb in range(len(passwd)-1, -1, -1):
            #print ("c", passwd[bb])
            sss += chr( (ord(passwd[bb]) + ord(passwd[bb-1])) & 0xff)
        return sss

# ------------------------------------------------------------------------
# Split line into array

def ascsplit(strx):

    if debug > 1:
        print("ascsplit", "'"+strx+"'")

    arr = [] ;  last = ""; cumm = ""; cumm2 = ""
    mode = 0; old_mode = 0

    for aa in strx:
        if aa == "\n":
            mode = 0
        elif aa == " ":
            mode = 1
        if aa in string.punctuation:
            mode = 2
        elif aa in string.ascii_letters:
            mode = 3
        else:
            mode = 4

        # ----------------------------------------------------------
        if mode == 0:
            if old_mode != mode:
                if cumm:
                    arr.append(cumm); cumm = ""
            # Always add
            arr.append(aa)

        if mode == 1:
            if old_mode != mode:
                if cumm:
                    arr.append(cumm);  cumm = ""
            # Always add
            arr.append(aa)

        if mode == 2:
            if old_mode != mode:
                if cumm:
                    arr.append(cumm);  cumm = ""
            # Always add
            arr.append(aa)

        if mode == 3:
            cumm += aa
            if old_mode != mode:
                if cumm2:
                    arr.append(cumm2);  cumm2 = ""

        if mode == 4:
            cumm2 += aa
            if old_mode != mode:
                if cumm:
                    arr.append(cumm);    cumm = ""

        old_mode = mode

    # Flush the rest, if any
    if cumm2:
        arr.append(cumm2)
    if cumm:
        arr.append(cumm)
    if debug > 2:
        print("acsplit ret:", arr)
    return arr


# ------------------------------------------------------------------------

def testpass(passwd):

    testarr = [];   numarr = []
    for cc in range(256):
        testarr.append(0)
        numarr.append(cc)

    for aa in passwd:
        vvv = ord(aa)
        #print("vvv", vvv)
        testarr[vvv] = testarr[vvv] + 1

    #for bb in range(len(testarr)):
    #    print(numarr[bb], testarr[bb])

    return testarr

# Character / string classification

class   CharClassi():

    def __init__(self):
        pass

    def _isallupper(sel, ww):
        ret = True
        for aa in ww:
            if not aa in string.ascii_uppercase:
                ret = False
        return ret

    def _isanyupper(sel, ww):
        ret = False
        for aa in ww:
            if aa in string.ascii_uppercase:
                ret = True
                break
        return ret

    def _isallspace(self, ww):
        ret = True
        for aa in ww:
            if aa != " ":
                ret = False
        return ret

    def _isupper(self, ww):
        if ww in string.ascii_uppercase:
            return True

