#!/usr/bin/env python3

from __future__ import absolute_import
from __future__ import print_function

import os, sys, string, zlib, struct, platform
from datetime import date
from optparse import OptionParser

# Spell crypt main module
#
# Flow of data:
#
#       line by line
#        parse word / no word
#        get tuple of coordinates for this word
#          modulate tuple
#        reverse resulting tuple into words
#        return new string
#

import sys, string, os
from hexdump import *

# Dict size:  Sun 28.Feb.2021  0x24109

LETTERMASK  = 0x3ffff

SPELLFLAG   = 0x40000
UPPERFLAG   = 0x80000
CAPFLAG     = 0x100000
NEWFLAG     = 0x200000

debug = 0
mask = 0

MASK = 0x100
PARSEMASK = 0x200

base = os.path.dirname(os.path.abspath(__file__))
#print("base", base)

def assertNERaise(aa, bb):
    if aa != bb:
        raise Warning("Assert NE raised.", "Values must match.")

#__all__ = ['__init__', 'enc_dec']

printable = string.ascii_letters # + "'"

#-------------------------------------------------------------------------
#

class   PassPad():

    def __init__(self, pass_str):
        self.pass_str = pass_str
        self.passidx = 0
        self.xlen = len(self.pass_str)

    # Cycle pass character around
    def nextchr(self):
        ret = ord(self.pass_str[self.passidx])
        self.passidx += 1
        if self.passidx >= self.xlen:
            self.passidx = 0
        return ret

    def rewind(self):
        self.passidx = 0

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

# ------------------------------------------------------------
# Convert input to array of offsets / strings

class  spellencrypt():


    def __init__(self, fname = "spell.txt"):

        self.debug = 0; self.arrlen = 0
        self.bigarr = []
        self.boundsig = [];  self.boundarr = []
        self.datadir = os.path.dirname(fname)
        self.cli = CharClassi()

        #print("datadir", self.datadir)

        fpi = open(fname, "r")

        # Ignore first line
        #hash = fpi.readline()
        #print("hash", hash)

        # Load to memory
        for aa in fpi:
            aa = aa.strip().lower()
            self.bigarr.append(aa)
        fpi.close()

        # We fake a space here, as editors remove it
        self.bigarr.append(" ")

        # Quick index
        cnt = 0; oldchh = ""
        for aa in self.bigarr:
            chh =  aa[:1]
            if  oldchh != chh:
                self.boundsig.append(chh)
                self.boundarr.append(cnt)
                oldchh = chh
            cnt += 1;
        # Mark end of array (so idx+1 scans last element)
        self.boundarr.append(cnt)

        self.arrlen = len(self.bigarr)

        if self.debug > 5:
            print("boundsig", self.boundsig)
            #print("boundarr", self.boundarr)

        if self.debug > 3:
            print("arrlen",  self.arrlen, hex(self.arrlen))

        #assertNERaise(self.arrlen, cnt)
        #print("cmp", hex(self.arrlen), hex(LETTERMASK))

        #fps = open(os.path.join(self.datadir, "spellmode.txt"), "r")
        # Load to memory
        #for aaa in fps:
        #    aaa = aaa.strip().lower().split()
        #    self.splarr.append(aaa[0])
        #fps.close()
        #print("splarr", self.splarr);
        #for iii in range(len(boundarr)-1):
        #    print (boundarr[iii + 1] - boundarr[iii], boundstr[iii], end="    " )
        #    print

    def getword(self, www):

        ttt = [0, -1, 0]; cnt2 = 0; cc =  www[:1]

        '''
        # Brute method
        for dd in range(self.arrlen):
            if self.bigarr[dd] == www:
                ttt = cnt2, dd, dd
                break
        '''

        # Single hash
        for bb in self.boundsig:
            if bb == cc:
                cnt3 = self.boundarr[cnt2]
                cnt4 = self.boundarr[cnt2+1]
                if self.debug > 9:
                    print  ("got:", cc, bb, cnt2, self.bigarr[cnt3], "range:", cnt4-cnt3)

                # The dictionary was broken had foreign characters, so we overscanned (FIXED)
                limx = cnt4 - cnt3 + 100
                if cnt3 + limx > self.arrlen:
                    limx = self.arrlen - cnt3

                for dd in range(limx):
                    #print (self.bigarr[cnt3 + dd], end=" ")
                    if self.bigarr[(cnt3) + dd] == www:
                        #print("Found: ",  self.bigarr[cnt3 + dd], cnt2, dd)
                        ttt = cnt2, dd, cnt3 + dd
                        break
                break
            cnt2 += 1

        if self.debug > 8:
            if ttt[2] == -1:
                print ("Word not found", www)

        return ttt[2]

    # ------------------------------------------------------------------------
    # Return a word from coordinates for this word

    def revwcoord(self, xxx, yyy):

        #print ("get:" , xxx, yyy)

        strx = "";
        cnt3 = self.boundarr[xxx]
        strx = self.bigarr[cnt3 + yyy]
        #print("Got: ",  strx)
        return strx

    # ------------------------------------------------------------------------
    # Return a word from ordinal

    def _revword(self, ooo):

        strx = "";
        #print("revword", ooo)
        if ooo < len(self.bigarr) and ooo >= 0:
            strx = self.bigarr[ooo]
        else:
            strx = "Indexerror (%d)" % ooo
            raise ValuError()
        return strx

    def _spellmode(self, ww):
        arr = []
        for aa in ww:
            if self.debug > 5:
                print("spell mode",  "'" + aa + "'", str.lower(aa) )
            nn = self.getword (str.lower(aa))
            nn |=  SPELLFLAG
            arr.append(nn)
        if self.debug > 5:
            print("spellmode arr", arr)
        return arr


    def _convert(self, arrx, flag = False):
        arr2 = []
        for ww in arrx:
            #if self.debug > 2:
            #    print ("_convert():", "'"+ww+"'")
            if len (ww) == 0:
                continue

            # process exceptions
            if ww == "\n":
                arr2.append("\n")
            #elif self.cli._isallspace(ww):
            elif ww == " ":
                arr2.append(ww)
            else:
                nn = self.getword (str.lower(ww))
                if nn != 0:
                    if self.cli._isanyupper(ww):
                        if self.cli._isallupper(ww):
                            nn |= UPPERFLAG
                        elif self.cli._isupper(ww[0]):
                            nn |= CAPFLAG
                        else:
                            print("Warn: mixed capitalization");
                            # Todo: spell mode

                    arr2.append(nn)
                    if self.debug > 2:
                        print("'" + ww + "'", hex(nn), end = "; ")
                else:
                    if self.debug > 3:
                        print("Unkown",  "'" + ww + "'", hex(nn), end = "; ")
                    # Enter spell mode
                    arr3 = self._spellmode(ww)
                    arr2.append(arr3)
        if self.debug > 2:
            print("_convert ret=", arr2)
        return arr2

    # Encode one entity
    def _encode_one(self, ee, chh, flag):

        if self.debug > 3:
            print("ee =", ee, " ", end="")

        #if ee == " ":
        #    return " "
        #if ee == "\n":
        #    return "\n"

        ee2 = ee & LETTERMASK

        #                               arrlen
        # ----------|-------------------|---------------------------
        #                         ^org
        #                         ------|------

        #print("adj", chh, "", end="")
        offs =  chh * 103

        #''' Disable crypt with uncommented hash mark
        if flag:
            ee2 += offs
            if ee2 > self.arrlen:
                ee2 -= self.arrlen
        else:
            ee2 -= offs
            if ee2 < 0:
                ee2 += self.arrlen
        #'''

        if self.debug > 3:
            print("after_ee =", ee2, "", end="")

        # Reverse conversion
        nstr = self._revword(ee2)

        '''
        # Apply flags
        if ee & CAPFLAG:
            nstr = nstr.capitalize()
        if ee & UPPERFLAG:
            nstr = nstr.upper()
        if ee & SPELLFLAG:
            nstr += "s` " #" Spell_flag "
        '''

        if self.debug > 3:
            print ("$[" + nstr + "]$")

        return nstr

    # ------------------------------------------------------------------------
    # Encrypt / Decrypt. Flag is true for encrypt.

    def  enc_dec(self, flag, arrx, passwd):

        #if self.debug > 8:
        #    print("CAPFLAG", hex(CAPFLAG), "UPPERFLAG",
        #             hex(UPPERFLAG), "SPELLFLAG", hex(SPELLFLAG) )
        #    print("Loaded", hex(self.arrlen), "words")
        #if self.debug > 4:
            #print("password=", HexDump(passwd)[:300], "....")
            #print("password=\n", "'"+passwd +"'")

        self.passpad = PassPad(passwd)
        strx = "";  cnt = 0; passidx = 0;
        if len(passwd) == 0:
            raise ValueError("Password Cannot be Empty")

        if self.debug > 3:
            print(arrx)

        arr2 = self._convert(arrx)
        if self.mask & 0x200:
            print ("arr2", arr2)
        for ee in arr2:
            if self.debug > 3:
                print ("cnt", cnt, "", end="")
            if type(ee) == str:
                if self.debug > 3:
                    print ("[" + ee + "] ", end="")
                strx +=  ee
            elif type(ee) == list:
                if self.debug > 3:
                    print ("arr[", ee, "]arr ", end="")
                for cc in ee:
                    chh = self.passpad.nextchr()

                    if self.debug > 4:
                        print ("chh ", chh, end=" ")
                    nstr = self._encode_one(cc, chh, flag)
                    # Add it to results
                    strx += nstr #+ "# "
            else:
                if flag:
                    if self.debug > 3:
                        print ("{" + arrx[cnt] + "} ", end=" ")
                else:
                    if self.debug > 3:
                        print ("{", arr2[cnt], "} ", end=" ")
                chh = self.passpad.nextchr()
                if self.debug > 4:
                    print ("chh ", chh, end=" ")
                nstr = self._encode_one(ee, chh, flag)
                # Add it to results
                strx += nstr  #+ "@ "
            cnt = cnt + 1
        return strx


# EOF