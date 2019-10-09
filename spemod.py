# Return a tuple of coordinates for this word


from __future__ import absolute_import
from __future__ import print_function

import string

verbose = 0

bigarr = []
boundsig = []
boundstr = []
boundarr = []


def     getword(www):

    ttt = [0, 0, 0]
    cnt2 = 0
    cc =  www[:2]
    for bb in boundsig:
        if bb == cc:
            cnt3 = boundarr[cnt2]
            cnt4 = boundarr[cnt2+1]
            #print  ("got", bb, cnt2, bigarr[cnt3], "range:", cnt4-cnt3)
            for dd in range(cnt4-cnt3):
                #print (bigarr[cnt3 + dd], end=" ")
                if bigarr[cnt3 + dd] == www:
                    #print("Found: ",  bigarr[cnt3 + dd], cnt2, dd)
                    ttt = cnt2, dd, cnt3 + dd
                    break
            break
        cnt2 += 1
    return ttt[2]


def     getwcoord(www):

    ttt = [0, 0, 0]
    cnt2 = 0
    cc =  www[:2]
    for bb in boundsig:
        if bb == cc:
            cnt3 = boundarr[cnt2]
            cnt4 = boundarr[cnt2+1]
            #print  ("got", bb, cnt2, bigarr[cnt3], "range:", cnt4-cnt3)
            for dd in range(cnt4-cnt3):
                #print (bigarr[cnt3 + dd], end=" ")
                if bigarr[cnt3 + dd] == www:
                    #print("Found: ",  bigarr[cnt3 + dd], cnt2, dd)
                    ttt = cnt2, dd, cnt3 + dd
                    break
            break
        cnt2 += 1
    return ttt

# ------------------------------------------------------------------------
# Return a word from coordinates for this word

def     revwcoord(xxx, yyy):

    #print ("get:" , xxx, yyy)

    strx = "";
    cnt3 = boundarr[xxx]
    strx = bigarr[cnt3 + yyy]
    #print("Got: ",  strx)
    return strx

# ------------------------------------------------------------------------
# Return a word from ordinal

def     revword(ooo):

    strx = "";
    strx = bigarr[ooo]
    return strx

# ------------------------------------------------------------------------

def  init():

    cnt = 0
    fpi = open("spell.txt", "r")

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
                bigarr.append(aa)

    # Quick index
    oldchh = ""
    for aa in bigarr:
        if  oldchh != aa[:2] :
            oldchh = aa[:2]
            #print ("Bound:", "'"+ aa +"'")
            boundsig.append(aa[:2])
            boundarr.append(cnt)
            boundstr.append(aa)

        cnt += 1;
    boundstr.append(aa)

    if verbose:
        print("Parsed:", len(boundarr), "entries", len(bigarr), "total")

    #for iii in range(len(boundarr)-1):
    #    print (boundarr[iii + 1] - boundarr[iii], boundstr[iii], end="    " )
    #    print

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

#printable = string.ascii_letters

def ascsplit(strx):
    arr = [] ;  last = ""; cumm = ""
    for aa in strx:
        if aa in string.ascii_letters:
            cumm += aa
        else:
            arr.append(cumm)
            #print("c-", cumm, end=" ")
            cumm = ""
            if aa != last:
                arr.append(aa)
                last = aa
    return arr


