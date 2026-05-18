import os, sys, string, struct

# pylint: disable=C0321
# pylint: disable=C0209
# pylint: disable=C0103
# pylint: disable=C0116
# pylint: disable=C0114

__doc__ = \
'''
spellcrypt main module
'''
prepass   = string.ascii_letters * 4

UPPERFLAG   = 0x80000
CAPFLAG     = 0x100000

printable = string.ascii_letters + "'"

base = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(base))

class  spellencrypt():

    ''' Encrypt data passed by the caller '''

    def __init__(self, fname = "spell.txt"):

        self.verbose = 0
        self.bigarr = []
        self.boundsig = []
        self.boundstr = []
        self.boundarr = []
        self.arrlen = 0
        self.hashlen = 2

        cnt = 0
        with open(os.path.join(base, fname), "r", encoding="utf-8") as fpi:
            # Load to memory
            for aa in fpi:
                aa = aa.strip().lower()
                if len(aa) > 1:
                    self.bigarr.append(aa)

                    ''' We filter printable at a later stage
                    uuu = 0
                    for bb in aa:
                        if ord(bb) > 127:
                            #print ("Foreign chars", aa)
                            uuu = 1
                    '''
                #fpi.close()

        # Quick index
        oldchh = ""
        for aa in self.bigarr:
            cc =  aa[:self.hashlen]
            if  oldchh != cc:
                oldchh = cc
                #print ("Bound:", "'"+ aa +"'")
                self.boundsig.append(cc)
                self.boundarr.append(cnt)
                #self.boundstr.append(aa)
            cnt += 1
        #self.boundstr.append(aa)

        self.arrlen = len(self.bigarr)

        #for iii in range(len(boundarr)-1):
        #    print (boundarr[iii + 1] - boundarr[iii], boundstr[iii], end="    " )
        #    print

    def     getword(self, www):

        ttt = [0, 0, 0]
        cc =  www[:self.hashlen]
        cnt2 = 0

        '''  # brute
        for dd in range(self.arrlen):
            if self.bigarr[dd] == www:
                ttt = cnt2, dd, dd
                break
        '''

        for bb in self.boundsig:
            if bb == cc:
                cnt3 = self.boundarr[cnt2]
                try:
                    cnt4 = self.boundarr[cnt2+1]
                except:
                    cnt4 = cnt3
                #print  ("got:", cc, bb, cnt2, self.bigarr[cnt3], "range:", cnt4-cnt3)
                # The dictionary was broken had foreign characters, so we overscanned
                limx = cnt4-cnt3 + 100
                if cnt3 + limx > self.arrlen:
                    limx = self.arrlen - cnt3

                for dd in range(limx):
                    #print (self.bigarr[cnt3 + dd], end=" ")
                    if self.bigarr[(cnt3)+ dd] == www:
                        #print("Found: ",  self.bigarr[cnt3 + dd], cnt2, dd)
                        ttt = cnt2, dd, cnt3 + dd
                        break
                break
            cnt2 += 1

        #if ttt[2] == 0:
        #    print (www, "not found")

        return ttt[2]

    def     revwcoord(self, xxx, yyy):

        ''' Return a word from coordinates '''

        #print ("get:" , xxx, yyy)

        strx = ""
        cnt3 = self.boundarr[xxx]
        strx = self.bigarr[cnt3 + yyy]
        #print("Got: ",  strx)
        return strx

    def     _revword(self, ooo):

        '''  Return a word from ordinal. '''

        strx = ""
        #print("revword", ooo)
        if ooo < len(self.bigarr) and ooo >= 0:
            strx = self.bigarr[ooo]
        else:
            strx = "Indexerror (%d)" % ooo
        return strx

    def     _convert(self, arrx):

        ''' Convert input to array of offsets / strings '''

        arr2 = []
        for ww in arrx:
            if len (ww) == 0:
                continue
            if len (ww) > 1:
                nn = self.getword (str.lower(ww))
                if nn != 0:
                    if ww[1] in string.ascii_uppercase:
                        nn |= CAPFLAG
                    elif ww[0] in string.ascii_uppercase:
                        #print("bigg", ww, hex(nn))
                        nn |= UPPERFLAG

                    arr2.append(nn)
                    #print("'" + ww + "'", hex(nn), end = "; ")
                else:
                    arr2.append(ww)
                    #print("'" + ww + "'", hex(nn), end = "; ")
            else:
                if len (ww):
                    arr2.append( ww )
                    #print("'" + ww + "' ", hex(nn), end = "")

        return arr2

    def  enc_dec(self, flag, arrx, passwd):

        ''' Encrypt / Decrypt. Flag is true for encrypt.'''

        strx = "";  cnt = 0; passidx = 0

        if len(passwd) == 0:
            raise ValueError("Password Cannot be Empty")

        #print(arrx)
        arr2 = self._convert(arrx)
        #print (arr2)

        for ee in arr2:
            #print ("cnt", cnt, "", end="")
            #if type(ee) == type(""):
            if isinstance(ee, str):
                if self.verbose > 1:
                    print ("[" + ee + "] ", end="")
                strx +=  ee
            else:
                if flag:
                    if self.verbose > 3:
                        print ("{" + arrx[cnt] + "} ", end="")
                else:
                    if self.verbose > 3:
                        print ("{", arr2[cnt], "} ", end="")

                chh = ord(passwd[passidx])

                #if self.verbose :
                #    print ("chh ", chh, end=" ")

                passidx += 1
                if passidx >= len(passwd):
                    passidx = 0

                ee2 = ee & 0x7ffff

                if self.verbose > 1:
                    print("ee =", ee, " ", end="")

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

                if self.verbose > 1:
                    print("after_ee =", ee2, "", end="")

                # Reverse conversion
                nstr = self._revword(ee2)
                # Apply flags
                if ee & CAPFLAG:
                    nstr = nstr.upper()
                if ee & UPPERFLAG:
                    nstr = nstr.capitalize()
                if self.verbose:
                    print ("[" + nstr + "]")
                # Add it to results
                strx += nstr
            cnt = cnt + 1
        return strx

    def calcarrlen(self, arrx):

        ''' calc array length '''
        xlen = 0
        for ww in arrx:
            xlen += len(ww)
        #print("xlen", xlen)

    #def getlen(self):
    #    if self.verbose > 0:
    #        print("Parsed:", len(self.boundarr), "entries", len(self.bigarr), "total")
    #    return self.arrlen

def pack24(mm):
    xxx = ""
    for _ in range(3):
        xxx += struct.pack("B", mm & 0xff )
        mm = mm >> 8
    return xxx

def upack24(xxx):
    uuu = 0
    for aa in range(3):
        uu = struct.unpack("B", xxx[aa:aa+1] )
        uuu += uu[0] <<  aa * 8
    return uuu

# Primitives.

def xsum(passwd):
    ''' Keep results below 128 by truncation '''
    sss = 0
    for aa in passwd:
        sss += ord(aa)
    return chr(sss & 0xff)

def fwstr(passwd):
    ''' Forward encrypt for pass '''
    passwd2 = passwd + " "
    sss = ""
    for bb in range(0, len(passwd)):
        #print ("c", passwd[bb])
        sss += chr( (ord(passwd2[bb]) + ord(passwd2[bb+1])) & 0xff)
    return sss

def xorstr(passwd):
    ''' xor constant into strings '''
    sss = ""
    for bb in passwd:
        #print ("c", passwd[bb])
        sss += chr((ord(bb) ^ 0x55) & 0xff)
    return sss

def butter(passwd):
    ''' merge the two halfs, similar to the butterfly operatopn '''
    sss = ""; rrr = ""
    for bb in range(0, len(passwd)/2):
        #print ("c", passwd[bb])
        sss += chr((ord(passwd[bb]) + ord(passwd[2*bb]) ) & 0xff)
        rrr += chr((ord(passwd[bb]) + ord(passwd[2*bb]) ) & 0xff)
    return sss + rrr

def bwstr(passwd):
    ''' Backward encrypt for pass '''
    sss = ""
    for bb in range(len(passwd)-1, -1, -1):
        #print ("c", passwd[bb])
        sss += chr( (ord(passwd[bb]) + ord(passwd[bb-1])) & 0xff)
    return sss

# ------------------------------------------------------------------------
# Corrected to handle unicode accidental

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


def hexdump(strx):

    ''' Return a hex dump formatted string '''
    lenx = len(strx)
    outx = ""
    try:
        for aa in range(lenx/16):
            outx += " "
            for bb in range(16):
                try:
                    outx += "%02x " % ord(strx[aa * 16 + bb])
                except:
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

    return outx


def     genpass(passwd):

    ''' Generate password for enc/dec/ '''

    #print ("'" + prepass + "'" )

    passwd = passwd + prepass + passwd + prepass + passwd

    for _ in range(5):
        passwd = bwstr(passwd)
        passwd = xorstr(passwd)
        passwd = fwstr(passwd)
        passwd = butter(passwd)
    return passwd

# EOF
