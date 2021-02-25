# Return a tuple of coordinates for this word


from __future__ import absolute_import
from __future__ import print_function

import sys, string, os

# Globals

prepass   = string.ascii_letters * 4

SPELLFLAG   = 0x040000
UPPERFLAG   = 0x080000
CAPFLAG     = 0x100000


base = os.path.dirname(os.path.abspath(__file__))
#print("base", base)

#__all__ = ['__init__', 'enc_dec']

printable = string.ascii_letters + "'"

class   PassPad():

    def __init__(self, pass_str):
        self.pass_str = pass_str
        self.passidx = 0

    # Cycle pass character around
    def nextchr(self):
        ret = ord(self.pass_str[self.passidx])
        self.passidx += 1
        if self.passidx >= len(self.pass_str):
            self.passidx = 0

        return ret

    def rewind(self):
        self.passidx = 0


class  spellencrypt():


    def __init__(self, fname = "spell.txt"):

        self.debug = 0; self.arrlen = 0
        self.bigarr = []
        self.boundsig = [];  self.boundarr = []
        self.datadir = os.path.dirname(fname)

        #print("datadir", self.datadir)

        fpi = open(fname, "r")

        # Ignore first line
        #hash = fpi.readline()
        #print("hash", hash)

        # Load to memory
        for aa in fpi:
            aa = aa.strip().lower()
            # We fake a space here, as editors remove it
            if not aa:
                aa = ' '
            self.bigarr.append(aa)
        fpi.close()

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

        #print("boundsig", self.boundsig)
        #print("boundarr", self.boundarr)

        #print("arrlen",  self.arrlen, "aa", cnt);  # ASSERT

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

        for bb in self.boundsig:
            if bb == cc:
                cnt3 = self.boundarr[cnt2]
                cnt4 = self.boundarr[cnt2+1]
                #print  ("got:", cc, bb, cnt2, self.bigarr[cnt3], "range:", cnt4-cnt3)

                # The dictionary was broken had foreign characters, so we overscanned
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
        return strx

    def _spellmode(self, ww):

        arr = []
        for aa in ww:
            if self.debug > 5:
                print("spell mode",  "'" + aa + "'", str.lower(aa) )
            nn = self.getword (str.lower(aa))
            arr.append(nn)

        if self.debug > 5:
            print("spellmode arr", arr)
        return arr

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

    # ------------------------------------------------------------
    # Convert input to array of offsets / strings

    def _convert(self, arrx, flag = False):

        arr2 = []
        for ww in arrx:
            if self.debug > 2:
                print ("_convert():", "'"+ww+"'")

            if len (ww) == 0:
                continue
            # process exceptions
            if ww == "\n":
                arr2.append("\n")
            elif ww == " ":
                arr2.append(" ")
            else:
                nn = self.getword (str.lower(ww))
                if nn != 0:
                    #if self._isallupper(ww):
                    #    nn |= UPPERFLAG
                    #if self._isanyupper(ww):
                    #    if ww[0] in string.ascii_uppercase:
                    #        nn |= CAPFLAG
                    #    else:
                    #        print("Warn: mixed capitalization");
                    #else:
                    #    pass
                    arr2.append(nn)
                    if self.debug > 2:
                        print("'" + ww + "'", hex(nn), end = "; ")
                else:
                    #arr2.append(ww)
                    if self.debug > 3:
                        print("Unkown",  "'" + ww + "'", hex(nn), end = "; ")
                    # Enter spell mode
                    arr3 = self._spellmode(ww)
                    #for aa in arr3:
                    arr2.append(arr3)

        if self.debug > 2:
            print("_convert ret=", arr2)
        return arr2

    def _encode_one(self, ee, chh, flag):

        if self.debug > 1:
            print("ee =", ee, " ", end="")

        if ee == " ":
            return " "

        if ee == "\n":
            return "\n"

        ee2 = ee & 0x7ffff

        #                               arrlen
        # ----------|-------------------|---------------------------
        #                         ^org
        #                         ------|------

        #print("adj", ord(chh) * 500, "", end="")

        offs =  chh * 103
        if flag:
            ee2 += offs
            if ee2 > self.arrlen:
                ee2 -= self.arrlen
        else:
            ee2 -= offs
            if ee2 < 0:
                ee2 += self.arrlen

        if self.debug > 1:
            print("after_ee =", ee2, "", end="")

        # Reverse conversion
        nstr = self._revword(ee2)

        # Apply flags
        if ee & CAPFLAG:
            nstr = nstr.upper()
        if ee & UPPERFLAG:
            nstr = nstr.capitalize()
        if ee & SPELLFLAG:
            nstr = "Spell flag"

        if self.debug > 1:
            print ("$[" + nstr + "]$")

        return nstr

    # ------------------------------------------------------------------------
    # Encrypt / Decrypt. Flag is true for encrypt.

    def  enc_dec(self, flag, arrx, passwd):

        if self.debug > 5:
            print("CAPFLAG", hex(CAPFLAG), "UPPERFLAG",
                     hex(UPPERFLAG), "SPELLFLAG", hex(SPELLFLAG) )
            print("Loaded", hex(self.arrlen), "words")

        if self.debug > 4:
            print("password=", passwd)
        self.passpad = PassPad(passwd)

        strx = "";  cnt = 0; passidx = 0;

        if len(passwd) == 0:
            raise ValueError("Password Cannot be Empty")

        if self.debug > 3:
            print(arrx)

        arr2 = self._convert(arrx)

        if self.debug > 3:
            print ("arr2", arr2)

        for ee in arr2:
            if self.debug > 3:
                print ("cnt", cnt, "", end="")
            if type(ee) == str:
                if self.debug > 1:
                    print ("[" + ee + "] ", end="")
                strx +=  ee
            elif type(ee) == list:
                if self.debug > 1:
                    print ("arr[", ee, "]arr ", end="")
                for cc in ee:
                    chh = self.passpad.nextchr()

                    if self.debug > 4:
                        print ("chh ", chh, end=" ")

                    nstr = self._encode_one(cc, chh, flag)

                    # Add it to results
                    strx += nstr # + " "

            else:
                if flag:
                    if self.debug > 2:
                        print ("{" + arrx[cnt] + "} ", end=" ")
                else:
                    if self.debug > 2:
                        print ("{", arr2[cnt], "} ", end=" ")

                chh = self.passpad.nextchr()

                if self.debug > 4:
                    print ("chh ", chh, end=" ")

                nstr = self._encode_one(ee, chh, flag)

                # Add it to results
                strx += nstr # + " "

            cnt = cnt + 1

        return strx

    def calcarrlen(arrx):

        xlen = 0;
        for ww in arrx:
            xlen += len(ww)
        print("xlen", xlen);

    # ------------------------------------------------------------------------

    def getlen(self):

        if self.debug > 0:
            print("Parsed:", len(self.boundarr), "entries", len(self.bigarr), "total")

        return self.arrlen


def ascsplit(strx):
    arr = [] ;  last = ""; cumm = ""; cumm2 = ""
    mode = 0; old_mode = 0

    for aa in strx:
        if aa in printable:
            mode = 0
        else:
            mode = 1

        if mode == 0:
            cumm += aa
            if old_mode != mode:
                arr.append(cumm2)
                cumm2 = ""

        if mode == 1:
            cumm2 += aa
            if old_mode != mode:
                arr.append(cumm)
                cumm = ""
        old_mode = mode

    # Flush the rest, if any
    if cumm2:
        arr.append(cumm2)

    if cumm:
        arr.append(cumm)

    return arr

def pack24(mm):
    xxx = ""
    for aa in range(3):
        xxx += struct.pack("B", mm & 0xff )
        mm = mm >> 8
    return xxx

def upack24(xxx):
    uuu = 0
    for aa in range(3):
        uu = struct.unpack("B", xxx[aa:aa+1] )
        uuu += uu[0] <<  aa * 8
    return uuu

# Primitives. Keep results below 128 by truncation

def xsum(passwd):
    sss = 0
    for aa in passwd:
        sss += ord(aa)
    return chr(sss & 0xff)

def fwstr(passwd):
    passwd2 = passwd + " "
    sss = ""
    for bb in range(0, len(passwd)):
        #print ("c", passwd[bb])
        sss += chr( (ord(passwd2[bb]) + ord(passwd2[bb+1])) & 0xff)
    return sss

def xorstr(passwd):
    sss = ""
    for bb in range(0, len(passwd)):
        #print ("c", passwd[bb])
        sss += chr((ord(passwd[bb]) ^ 0x55) & 0xff)
    return sss

def butter(passwd):
    sss = ""; rrr = ""
    for bb in range(0, len(passwd)//2):
        #print ("c", passwd[bb])
        sss += chr((ord(passwd[bb]) + ord(passwd[2*bb]) ) & 0xff)
        rrr += chr((ord(passwd[bb]) + ord(passwd[2*bb]) ) & 0xff)
    return sss + rrr

def bwstr(passwd):
    sss = ""
    for bb in range(len(passwd)-1, -1, -1):
        #print ("c", passwd[bb])
        sss += chr( (ord(passwd[bb]) + ord(passwd[bb-1])) & 0xff)
    return sss

# ------------------------------------------------------------------------
# corrected to handle unicode accidental

ctrlchar = "\n\r| "

def isprint(chh):

    try:
        if ord(chh) > 127:
            return False
        if ord(chh) < 32:
            return False
        if chh in ctrlchar:
            return False
        if chh in string.ascii_letters:
            return True
    except:
        pass

    return False

# ------------------------------------------------------------------------
# Return a hex dump formatted string

def hexdump(strx, llen = 16):

    lenx = len(strx)
    outx = ""

    try:
        for aa in range(lenx/16):
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
                if isprint(chh):
                    outx += "%c" % chh
                else:
                    outx += "."
            outx += " | \n"

        # Print remainder on last line
        remn = lenx % 16 ;   divi = lenx / 16
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
                if isprint(chh):
                    outx += "%c" % chh
                else:
                    outx += "."
            outx += " " * ((16 - remn))
            outx += " | \n"
    except:
        print("Error on hexdump", sys.exc_info())
        #print_exc("hexdump")

    return(outx)


def     genpass(passwd):

    #print ("'" + prepass + "'" )

    passwd = passwd + prepass + passwd + prepass + passwd

    for aa in range(5):

        passwd = bwstr(passwd)
        passwd = xorstr(passwd)
        passwd = fwstr(passwd)
        passwd = butter(passwd)

    return passwd

# EOF





