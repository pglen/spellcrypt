# Return a tuple of coordinates for this word


from __future__ import absolute_import
from __future__ import print_function

import string

class  spellencrypt():

    def __init__(self, fname = "spell.txt"):

        self.verbose = 0
        self.bigarr = []
        self.boundsig = []
        self.boundstr = []
        self.boundarr = []
        self.arrlen = 0

        cnt = 0
        fpi = open(fname, "r")

        # Load to memory
        for aa in fpi:
            aa = aa.strip().lower()
            if len(aa) > 1:
                uuu = 0
                '''for bb in aa:
                    if ord(bb) > 127:
                        #print ("Foreign chars", aa)
                        uuu = 1'''
                if not uuu:
                    self.bigarr.append(aa)

        # Quick index
        oldchh = ""
        for aa in self.bigarr:
            if  oldchh != aa[:2] :
                oldchh = aa[:2]
                #print ("Bound:", "'"+ aa +"'")
                self.boundsig.append(aa[:2])
                self.boundarr.append(cnt)
                self.boundstr.append(aa)

            cnt += 1;
        self.boundstr.append(aa)

        self.arrlen = len(self.bigarr)

        #for iii in range(len(boundarr)-1):
        #    print (boundarr[iii + 1] - boundarr[iii], boundstr[iii], end="    " )
        #    print


    def     getword(self, www):

        ttt = [0, 0, 0]
        cnt2 = 0
        cc =  www[:2]
        for bb in self.boundsig:
            if bb == cc:
                cnt3 = self.boundarr[cnt2]
                cnt4 = self.boundarr[cnt2+1]
                #print  ("got", bb, cnt2, self.bigarr[cnt3], "range:", cnt4-cnt3)
                for dd in range(cnt4-cnt3):
                    #print (self.bigarr[cnt3 + dd], end=" ")
                    if self.bigarr[cnt3 + dd] == www:
                        #print("Found: ",  self.bigarr[cnt3 + dd], cnt2, dd)
                        ttt = cnt2, dd, cnt3 + dd
                        break
                break
            cnt2 += 1
        return ttt[2]


    def     getwcoord(self, www):

        ttt = [0, 0, 0]
        cnt2 = 0
        cc =  www[:2]
        for bb in self.boundsig:
            if bb == cc:
                cnt3 = self.boundarr[cnt2]
                cnt4 = self.boundarr[cnt2+1]
                #print  ("got", bb, cnt2, self.bigarr[cnt3], "range:", cnt4-cnt3)
                for dd in range(cnt4-cnt3):
                    #print (self.bigarr[cnt3 + dd], end=" ")
                    if self.bigarr[cnt3 + dd] == www:
                        #print("Found: ",  self.bigarr[cnt3 + dd], cnt2, dd)
                        ttt = cnt2, dd, cnt3 + dd
                        break
                break
            cnt2 += 1
        return ttt

    # ------------------------------------------------------------------------
    # Return a word from coordinates for this word

    def     revwcoord(self, xxx, yyy):

        #print ("get:" , xxx, yyy)

        strx = "";
        cnt3 = self.boundarr[xxx]
        strx = self.bigarr[cnt3 + yyy]
        #print("Got: ",  strx)
        return strx

    # ------------------------------------------------------------------------
    # Return a word from ordinal

    def     revword(self, ooo):

        strx = "";
        #print("revword", ooo)
        if ooo < len(self.bigarr) and ooo >= 0:
            strx = self.bigarr[ooo]
        else:
            strx = "Indexerror (%d)" % ooo
        return strx

    # ------------------------------------------------------------------------

    def getlen(self):

        if self.verbose > 0:
            print("Parsed:", len(self.boundarr), "entries", len(self.bigarr), "total")

        return self.arrlen


printable = string.ascii_letters + "'"

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

    # Flush the rest
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


def xsum(passwd):
    sss = 0
    for aa in passwd:
        sss += ord(aa)
    return chr(sss & 0x7f)

def fwstr(passwd):
    passwd2 = passwd + " "
    sss = ""
    for bb in range(0, len(passwd)):
        #print ("c", passwd[bb])
        sss += chr( (ord(passwd2[bb]) + ord(passwd2[bb+1])) & 0x7f)
    return sss

def xostr(passwd):
    sss = ""; rrr = ""
    for bb in range(0, len(passwd) / 2):
        #print ("c", passwd[bb])
        sss += chr( (ord(passwd[bb]) + ord(passwd[2*bb]) ) & 0xff)
        rrr += chr( (ord(passwd[2*bb]) ^ 0x55) & 0xff)
    return sss + rrr

def bwstr(passwd):
    sss = ""
    for bb in range(len(passwd)-1, -1, -1):
        #print ("c", passwd[bb])
        sss += chr( (ord(passwd[bb]) + ord(passwd[bb-1])) & 0x7f)
    return sss

# EOF

