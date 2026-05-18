#!/usr/bin/env python

import spelib.spemod
mod = spelib.spemod.spellencrypt()

def test_one():
    assert mod
    arr = ["Hello", " ", "World"]
    passx = "1234"
    enc = mod.enc_dec(True, arr, passx)
    #print(enc)
    assert enc == "Inactivenesses Allerie"

def test_two():
    arr = ["Hello", " ", "World", " ", "1234"]
    passx = "1234"
    enc = mod.enc_dec(True, arr, passx)
    #print(enc)
    assert enc == "Inactivenesses Allerie 1234"

# EOF