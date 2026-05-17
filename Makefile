# Use to build modules

.PHONY: test clean

all:
	@echo Targets: git test clean

init:
	@python3 ./tools/genkey.py

SUB=auto

git:
	git add .
	git commit -m $SUB
	git push

git-local:
	git push local

test:
	@echo Testing ... diff should be silent
	@./spellcrypt.py -e -i sayings.txt -f -o sayings.tmp
	@./spellcrypt.py -d -i sayings.tmp -f -o sayings.dec
	diff sayings.txt sayings.dec
	@rm -f sayings.tmp sayings.dec

testall:
	@cd tests ; ./testall.sh

clean:
	@rm -f  aa* bb* cc* dd*
	@rm -rf __pycache__/
	@rm -rf build/* dist/*
	@rm -rf gui/__pycache__
	@rm -rf spelib/__pycache__/
	@find . -name "*.pyc" -delete
	@find tests -name "*.txt.enc" -delete

cleankeys:
	@rm -rf ./data/keys

#test_env:
#	@echo ${SUB}













