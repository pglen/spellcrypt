#!/usr/bin/env python

import os, sys
base = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(base, "../spelib"))

import spemod, spepass

mod = spemod.spellencrypt()

def esc_pass(ppp, llen = 24):

    ppp2 = "\n"  # For var decl
    for cnt, aa in enumerate(ppp):
        cc = "%02x" % ord(aa)
        ppp2 += cc
        if cnt % llen == llen-1:
            ppp2 += "\n"
    ppp2 += "\n"
    return ppp2

org = '''
709dbc239ad7fc63a4934af99cdddc0d988d18e7e21b8279
e06fd257b6cdf4598eeda6453cab06a7366f6a57aa0954d5
24637ac97cb16047aef328cf00b76efdc0e92879b4716c1b
f6b79e952c13c6cbfaa920a54a116a99b0d7e2b302236efb
0e253071d0577e6d709dbc239ad7fc63a4934af99cdddc0d
988d18e7e21b8279e06fd257b6cdf4598eeda6453cab06a7
366f6a57aa0954d524637ac97cb16047aef328cf00b76efd
c0e92879b4716c1bf6b79e952c13c6cbfaa920a54a116a99
b0d7e2b302236efb0e253071d0577e6d709dbc239ad7fc63
a4934af99cdddc0d988d18e7e21b8279e06fd257b6cdf459
8eeda6453cab06a7366f6a57aa0954d524637ac97cb16047
aef328cf00b76efdc0e92879b4716c1bf6b79e952c13c6cb
faa920a54a116a99b0d7e2b302236efb0e253071d0577e6d
709dbc239ad7fc63a4934af99cdddc0d988d18e7e21b8279
e06fd257b6cdf4598eeda6453cab06a7366f6a57aa0954d5
24637ac97cb16047aef328cf00b76efdc0e92879b4716c1b
f6b79e952c13c6cbfaa920a54a116a99b0d7e2b302236efb
0e253071d0577e6d
'''

org2 = '''
e083f06d5a4198014ef1642b805d0e8d3cddde5514bb6637
9c25c2f1b6a53c6d54c980cd3a07641dc0291cf15c9fc0df
c6fb16ad148b6887ee69dc9b6e47a4f5b87f509db0616869
148f8a25dcc38a850645183d5e85c8e51ac184034019f63b
865b2e011e0fcce7343f8edd96edb209b44fc8a76855a099
2a19e61b8ccb2c09402b44091e9b427bd20b462b70b9b4bb
5cb5522bc2134839a65d741b8853568d1c8d44c5c2a31a17
aed522e9acd3b6f75835d8b18cefd2e9bc5b267bbaef1e15
b4f984e32e2dd07576a3f2bb567ffef1f09952b9ac29e083
f06d5a4198014ef1642b805d0e8d3cddde5514bb66379c25
c2f1b6a53c6d54c980cd3a07641dc0291cf15c9fc0dfc6fb
16ad148b6887ee69dc9b6e47a4f5b87f509db0616869148f
8a25dcc38a850645183d5e85c8e51ac184034019f63b865b
2e011e0fcce7343f8edd96edb209b44fc8a76855a0992a19
e61b8ccb2c09402b44091e9b427bd20b462b70b9b4bb5cb5
522bc2134839a65d741b8853568d1c8d44c5c2a31a17aed5
22e9acd3b6f75835d8b18cefd2e9bc5b267bbaef1e15b4f9
84e32e2dd07576a3f2bb567ffef1f09952b9ac29
'''

def test_one():
    assert mod
    newpass = spepass.Primi().genpass("")
    ppp2 = esc_pass(newpass)
    #print(ppp2)
    #assert 0
    assert org == ppp2

def test_two():
    assert mod
    newpass = spepass.Primi().genpass("1234")
    ppp2 = esc_pass(newpass)
    #print(ppp2)
    #assert 0
    assert org2 == ppp2

# EOF
