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
1c6cba50f03e3ca0680666e2820484d04a303e3c6266beee
a68e1c6c7a90f03e3ca0680666e2820484d04a303e3ca226
beee260e1c6cba50f03e3ca0680666e2820484d04a303e3c
6266beeea68e1c6c7a90f03e3ca0680666e2820484d04a30
3e3ca226beee260e1c6cba50f03e3ca0680666e2820484d0
4a303e3c6266beeea68e1c6c7a90f03e3ca0680666e28204
84d04a303e3ca226beee260e1c6cba50f03e3ca0680666e2
820484d04a303e3c6266beeea68e1c6c7a90f03e3ca06806
66e2820484d04a303e3ca226beee260e1c6cba50f03e3ca0
680666e2820484d04a303e3c6266beeea68e1c6c7a90f03e
3ca0680666e2820484d04a303e3ca226beee260e1c6cba50
f03e3ca0680666e2820484d04a303e3c6266beeea68e1c6c
7a90f03e3ca0680666e2820484d04a303e3ca226beee260e
1c6cba50f03e3ca0680666e2820484d04a303e3c6266beee
a68e1c6c7a90f03e3ca0680666e2820484d04a303e3ca226
beee260e1c6cba50f03e3ca0680666e2820484d04a303e3c
6266beeea68e1c6c7a90f03e3ca0680666e2820484d04a30
3e3ca226beee260e
'''

org2 = '''
301c44d25ca670b62cdc6422aec4622a8a9a38543cd8ae4e
e6d26cf07c16301054b6b09c32fafac4364404d4720c60f6
cc3eae6a3e2480200e30a0d2b66cb622280ab604e8b6629a
a6e22254329e80a89e68244c12c4cac4da8aec3e064a8e6c
22542a7282107c2a30dc28e46084b4ec4c7eb82cbeca12ae
e0e6da3a9476543c52564cb418147440a4c8d622283066c0
c2f2309a8c9c16b88ce0389ca45c988ec8a4b6f656d66c36
86b4c26816bae4d8b8189aa61c0292c894c0dc82b61c6a78
eecae620aa6cca9aaaae36e0d4aa5e1244b652ba76b2301c
44d25ca670b62cdc6422aec4622a8a9a38543cd8ae4ee6d2
6cf07c16301054b6b09c32fafac4364404d4720c60f6cc3e
ae6a3e2480200e30a0d2b66cb622280ab604e8b6629aa6e2
2254329e80a89e68244c12c4cac4da8aec3e064a8e6c2254
2a7282107c2a30dc28e46084b4ec4c7eb82cbeca12aee0e6
da3a9476543c52564cb418147440a4c8d622283066c0c2f2
309a8c9c16b88ce0389ca45c988ec8a4b6f656d66c3686b4
c26816bae4d8b8189aa61c0292c894c0dc82b61c6a78eeca
e620aa6cca9aaaae36e0d4aa5e1244b652ba76b2
'''

def test_one():
    assert mod
    ppp = spepass.genpass("")
    #print(spepass.hexdump(ppp))
    ppp2 = esc_pass(ppp)
    #print(ppp2)
    #assert 0
    assert org == ppp2

def test_two():
    assert mod
    ppp = spepass.genpass("1234")
    #print(spepass.hexdump(ppp))
    ppp2 = esc_pass(ppp)
    #print(ppp2)
    #assert 0
    assert org2 == ppp2

# EOF
