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

