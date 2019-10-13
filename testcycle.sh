#VERBOSE="-v 2"

./spellcrypt.py $VERBOSE -e -f tests/test_3.txt -o  aa
./spellcrypt.py $VERBOSE -d -f aa -o bb
diff -w tests/test_3.txt bb


