#!/bin/bash
AA=$1
if [ "$AA" == "" ] ; then
    echo use: testone.sh filename
    exit 1
fi

./spellcrypt.py -f -e $AA -o $AA.enc
./spellcrypt.py -f -d $AA.enc -o $AA.dec
diff $AA $AA.dec
