# Echo to crypter
echo -e $@ | ./spellcrypt.py -e - | ./spellcrypt.py -d  -