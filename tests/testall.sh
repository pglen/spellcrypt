#!/bin/bash

LLL="test_1.txt test_3.txt test_5.txt test_2.txt test_4.txt test_6.txt"

for AA in $LLL; do
    ../spellcrypt.py -f -e $AA -o $AA.enc
    ../spellcrypt.py -f -d $AA.enc -o $AA.dec
    diff $AA $AA.dec
    #rm -f $AA.enc
    rm -f $AA.dec
done
