# Echo to crypter
echo -e $@ | ./spellcrypt.py -g 3 -e - | ./spellcrypt.py -d  -