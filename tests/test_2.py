#!/usr/bin/env python

import os, sys
base = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(base, "../spelib"))

import spemod
mod = spemod.spellencrypt()

def test_one():
    assert mod
    txt = "Hello New World"
    sss = spemod.ascsplit(txt)
    #print("sss", sss)
    arr = ['Hello', ' ', 'New', ' ', 'World']
    assert sss == arr

def test_two():
    assert mod
    txt = "Hello New World aaaa"
    sss = spemod.ascsplit(txt)
    #print("sss", sss)
    arr = ['Hello', ' ', 'New', ' ',
            'World', " ", "aaaa"]
    assert sss == arr

def test_three():
    assert mod
    txt = "Hello 1234 New World aaaa"
    sss = spemod.ascsplit(txt)
    #print("sss", sss)
    arr = ["Hello", " ", "1234", " ", 'New', ' ',
            "World", " ", "aaaa"]
    assert sss == arr

def test_four():
    assert mod
    txt = "Hello\tNew World"
    sss = spemod.ascsplit(txt)
    #print("sss", sss)
    arr = ['Hello', '\t', 'New', ' ', 'World']
    assert sss == arr

def test_five():
    assert mod
    txt = "Hello\tNew World\r"
    sss = spemod.ascsplit(txt)
    #print("sss", sss)
    arr = ['Hello', '\t', 'New', ' ', 'World', "\r"]
    assert sss == arr

# EOF
