#!/usr/bin/env python

import os, sys
base = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(base, "../spelib"))

import spemod
mod = spemod.spellencrypt()

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