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

UPPERFLAG   = 0x80000
CAPFLAG     = 0x100000

debug = 0

printable = string.ascii_letters + "'"

base = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(base))

class  spellencrypt():

    ''' Encrypt data passed by the caller '''

    def __init__(self, fname = "spell.txt"):

        self.verbose = 0 ; self.arrlen = 0
        self.hashlen = 2    # Optimum
        self.boundarr = [] ; self.bigarr = []
        self.boundsig = [] ; self.boundstr = []
        #print("base:", base, fname)
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

# ------------------------------------------------------------------------
# Corrected to handle unicode accidental

ctrlchar = "\n\r| "

def ascsplit(strx):

    ''' Split ONE line into array '''

    if debug > 1:
        print("ascsplit()", "'"+strx+"'")

    arr = [] ;  cumm = ""; cumm2 = ""
    mode = 0; old_mode = 0

    for aa in strx:
        if aa == "\n" or aa == '\r':
            mode = 0
        elif aa == " " or aa == '\t':
            mode = 1
        elif aa in string.punctuation or ord(aa) > 255:
            mode = 2
        elif aa in string.ascii_letters:
            mode = 3
        elif aa in string.digits:
            mode = 4
        else:
            mode = 5

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
            cumm += aa
            if old_mode != mode:
                if cumm2:
                    arr.append(cumm2);    cumm2 = ""

        if mode == 5:
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
        print("acsplit() ret:", arr)
    return arr

# EOF
