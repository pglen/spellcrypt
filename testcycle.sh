#!/bin/bash
#VERBOSE="-v 2"
echo Diff should be silent
./spellcrypt.py $VERBOSE -e -f -i orig/$1$1   -o  orig/$1$1$1
./spellcrypt.py $VERBOSE -d -f -i orig/$1$1$1 -o  orig/$1$1$1$1
diff  orig/$1$1 orig/$1$1$1$1


