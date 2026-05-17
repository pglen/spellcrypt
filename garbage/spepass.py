def ascsplit2(strx):

    ''' Spit text into tokens '''

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
    if debug > 2:
        print("acsplit arr", arr)
    return arr


class   CharClassi():

    ''' Character / String classification '''

    def __init__(self):
        pass
    def _isallupper(self, ww):
        ret = True
        for aa in ww:
            if not aa in string.ascii_uppercase:
                ret = False
        return ret
    def _isanyupper(self, ww):
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
        return False

