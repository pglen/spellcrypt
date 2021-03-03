#!/bin/bash
#VERBOSE="-v 2"
FILE=tests/test_2.txt
echo Diff should be silent
rm -f aa bb
./spellcrypt.py $VERBOSE -e -f -i $FILE -o  aa
./spellcrypt.py $VERBOSE -d -f -i aa -o bb
diff -w $FILE bb
#rm -f aa bb


