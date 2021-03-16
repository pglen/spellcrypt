#!/usr/bin/env python3

from __future__ import absolute_import
from __future__ import print_function

import os, string, random

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

from hexdump import *
from spepass import *

# Dict size:  Sun 28.Feb.2021  0x24109

LETTERMASK  =   0xfffff

SPELLFLAG   =  0x400000
UPPERFLAG   =  0x800000
CAPFLAG     = 0x1000000
NEWFLAG     = 0x2000000

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

globword  = ""
globword2 = ""

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

def print_hexarr(arrx, strx = "arr"):
    print(strx, "arr: ", end="")
    for aa in arrx:

        if type(aa) == type(0):
            print("0x" + hex(aa), end=", ")

            '''if aa & CAPFLAG:
                print("CAP", end = " ")
            if aa & SPELLFLAG:
                print("SP", end = " ")'''
        else:
            print("'" + aa + "'", end=", ")


    print("end_arr")


# ------------------------------------------------------------
# Convert input to array of offsets / strings

class  spellencrypt():

    def __init__(self, fname = "spell.txt"):

        self.debug = 0; self.arrlen = 0; self.mask = 0
        self.bigarr = []
        self.boundsig = [];  self.boundarr = []
        self.datadir = os.path.dirname(fname)
        self.cli = CharClassi()

        self.datadir = os.path.dirname(os.path.abspath(__file__))
        #print("datadir", self.datadir)

        fpi = open(self.datadir + os.sep + fname, "r")

        # Ignore first line
        #hash = fpi.readline()
        #print("hash", hash)

        # Load to memory
        for aa in fpi:
            aa = aa.strip().lower()
            self.bigarr.append(aa)
        fpi.close()

        # Add all single character
        for aa in range(255):
            self.bigarr.append(chr(aa))

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

    # --------------------------------------------------------------------
    # Prefix the original with a random sentence. This is then used as
    # parameters later

    def randpre(self):

        pre = []
        rrr = int(random.random() * 4) + 5

        global globword, globword2

        for aa in range(rrr):
            idx = int(random.random() * self.arrlen)
            #print("rand", idx)
            nnn = self.bigarr[idx]
            if aa == 0:
                nnn = nnn.capitalize()
            if aa == 1:
                globword = nnn
            if aa == 2:
                globword2 = nnn[:2] + " "

            pre.append(nnn)
            if aa < rrr-2 and random.random() * 10 < 1.0:
                pre.append(',')
            if aa < rrr-1:
                pre.append(' ')

        pre.append(".")
        pre.append(' ')

        print("globwords:", globword, globword2)
        return pre


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

    '''# ------------------------------------------------------------------------
    # Return a word from coordinates for this word

    def _revwcoord(self, xxx, yyy):
        #print ("get:" , xxx, yyy)
        strx = "";
        cnt3 = self.boundarr[xxx]
        strx = self.bigarr[cnt3 + yyy]
        #print("Got: ",  strx)
        return strx'''

    def _capflag(self, ww):
        nn = 0
        if self.cli._isanyupper(ww):
            if self.cli._isallupper(ww):
                nn |= UPPERFLAG
            elif self.cli._isupper(ww[0]):
                nn |= CAPFLAG
            else:
                print("Warn: mixed capitalization");

        #print("capflag", ww, hex(nn))
        return nn

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

    # ------------------------------------------------------------------------
    # Not in dictionary, decompose

    def _spellmode(self, ww):

        global globword
        arr = []
        for aa in ww:
            if self.debug > 3:
                print("spell mode",  wrap(aa))
            nn = self.getword (str.lower(aa))
            if self.cli._isupper(aa):
                nn |= CAPFLAG
            arr.append(nn)

        print("globword", globword)
        ttt = self.getword(globword)
        print("ttt", ttt)
        arr.append(ttt)

        #if self.debug > 5:
        #    print_hexarr(arr)
        return arr

    # --------------------------------------------------------------------
    # Convert the array of tokens to

    def _convert_arr(self, arrx, flag):

        arr2 = []; spell = False

        for ww in arrx:
            if self.debug > 5:
                print ("_convert():", wrap(ww))

            if len (ww) == 0:
                continue

            uni = False
            if len(ww) == 1 and ord(ww) > 255:
                uni = True

            # Process direct entities
            if ww in string.punctuation:
                if not spell:
                    arr2.append(ww[0]) # + "*p")
                    if self.debug > 3:
                        print("punct", wrap(ww))
                #spell = False
                continue
            elif uni:
                if not spell:
                    arr2.append(ww[0]) # + "*u")
                    if self.debug > 3:
                        print("uni",  wrap(ww))
                #spell = False
                continue
            elif ww[0] in string.whitespace:
                if not spell:
                    if self.debug > 3:
                        print("white", wrap(ww))
                    arr2.append(ww)
                    #arr2.append(wrap(ww)+ "*w ")
                #spell = False
                continue

            #elif ww[0] in string.digits:
            #    if not spell:
            #        if self.debug > 3:
            #            print("white", wrap(ww))
            #        #arr2.append(ww)
            #        arr2.append(wrap(ww)+ "*n ")
            #    #spell = False
            #    continue

            # Create a lower case copy
            str2 = str.lower(ww)

            # Dec only
            if not flag:
                if ww[-2:] == globword2 or ww[-2:] == globword2.upper():
                    nn = self.getword(str2[:-2])
                    if nn:
                        if self.debug > 6:
                            print("despell", wrap(ww[:-1]), nn)

                        nn |= SPELLFLAG
                        if ww[-2:] == globword2.upper():
                            nn |= CAPFLAG
                        arr2.append(nn)
                        spell = True
                    else:
                        print("Cannot dec str")
                else:
                    if spell:
                        arr2.append(" ")
                        #print_hexarr(arr2, "tmp")
                    spell = False
                    #print("arr2", arr2)
                    #continue

            # Enc / Dec
            nn = self.getword(str2)
            if nn != 0:
                nn |= self._capflag(ww)
                if spell:
                    arr2.append("xxx ")
                    #print_hexarr(arr2, "tmp")
                #spell = False

                arr2.append(nn)
                if self.debug > 1:
                    print(wrap(ww), hex(nn) ) #, end = "; ")
            else:
                if self.debug > 6:
                    print("Unkown", wrap(ww), hex(nn), flag)

                # Enter spell mode
                if flag:
                    arr3 = self._spellmode(ww)
                    #if self.debug > 3:
                    #    print("got spell res:", arr3)
                    arr2.append(arr3)

        return arr2

    # Encode one entity
    def _encode_one(self, ee, flag):

        if self.debug > 9:
            print("ee =", ee, " ", end="")

        chh = self.passpad.nextchr()
        if self.debug > 8:
            print ("chh ", chh, end=" ")

        ee2 = ee & LETTERMASK

        #                               arrlen
        # ----------|-------------------|---------------------------
        #                         ^org
        #                         ------|------

        #print("adj", chh, "", end="")
        offs =  chh * 103

        # Crypt by offetting and wrapping

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

        if self.debug > 9:
            print("after_ee =", ee2, "", end="")

        # Reverse conversion
        nstr = self._revword(ee2)

        return nstr

    # ------------------------------------------------------------------------
    # Encrypt / Decrypt. Flag is true for encrypt.

    def  enc_dec(self, flag, arrx, passwd):

        if len(passwd) == 0:
            raise ValueError("Password Cannot be Empty")

        #if self.debug > 8:
        #    print("CAPFLAG", hex(CAPFLAG), "UPPERFLAG",
        #             hex(UPPERFLAG), "SPELLFLAG", hex(SPELLFLAG) )
        #    print("Loaded", hex(self.arrlen), "words")
        #if self.debug > 4:
            #print("password=", HexDump(passwd)[:300], "....")
            #print("password=\n", "'"+passwd +"'")

        self.passpad = PassPad(passwd)
        strx = "";  cnt = 0; passidx = 0;

        #if self.debug > 3:
        #    print("flag:", flag)

        if self.debug > 3:
            print(arrx)

        if flag:
            prex = self.randpre()
            arrx = prex + arrx;

        if self.debug > 3:
            print("pre arrx", arrx)

        global globword, globword2

        # Cut point for prelude
        cutpoint = 0
        if not flag:
            for cutpoint in range(len(arrx)):
                if cutpoint == 2:
                    globword = arrx[cutpoint]
                if cutpoint == 4:
                    globword2 = arrx[cutpoint][:2]
                if arrx[cutpoint] == ".":
                    cutpoint += 2  # For ".", " " at the end
                    break;

        #print("cutpoint", cutpoint)
        print("globword:", globword, "globword2:", globword2)

        arr2 = self._convert_arr(arrx, flag)

        if self.mask & 0x200:
            print ("arr2", arr2)

        cnt3 = 0
        for ee in arr2:
            if self.debug > 3:
                print ("cnt=", cnt, ee, end=" ")

            if type(ee) == type(""):
                if self.debug > 3:
                    print (wrap(ee, " [", "] "), end="\n")
                cnt3 += 1
                if cnt3 > cutpoint:
                    strx +=  ee # + "$"

            elif type(ee) == type([]):
                if self.debug > 3:
                    print_hexarr(ee, "list")

                for cc in ee:
                    pad = globword2
                    if cc & CAPFLAG:
                        pad = globword2.upper()
                    nstr = self._encode_one(cc, flag)
                    # Add it to results
                    if self.debug > 4:
                        print ("&" + nstr + "& ", end=" ")
                    if self.debug > 3:
                        print ("cc", hex(cc), end=" ")
                    strx += nstr + pad

            elif type(ee) == type(0):

                if self.debug > 3:
                    print ("{", ee, "} ", end=" ")

                nstr = self._encode_one(ee, flag)

                # Apply flags
                if ee & CAPFLAG:
                    nstr = nstr.capitalize()
                if ee & UPPERFLAG:
                    nstr = nstr.upper()

                cnt3 += 1
                if cnt3 > cutpoint:
                    strx += nstr #  + "@ "

                if self.debug > 3:
                    print ("$[" + nstr + "]$")

                if self.mask & 0x400:
                    print (nstr, end= " " )
            else:
                print("non intercepted type")

            cnt = cnt + 1

        return strx

# EOF