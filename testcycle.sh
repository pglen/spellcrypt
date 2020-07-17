#!/bin/bash
#VERBOSE="-v 2"
echo Diff should be silent
rm aa bb
./spellcrypt.py $VERBOSE -e -f -i tests/test_3.txt -o  aa
./spellcrypt.py $VERBOSE -d -f -i aa -o bb
diff -w tests/test_3.txt bb


