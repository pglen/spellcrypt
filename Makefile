# Use to build modules

.PHONY: test tests testall clean docs git

all:
	@echo Targets: git test testall clean docs  \
        \(\'SUB\' env for git commit message\)

SUB ?= "auto checkin"

git:
	git add .
	git commit -m "${SUB}"
	git push

git-local:
	git push local

pip-up:
	./pip-build.sh
	./pip-upload.sh

tests:
	pytest tests/test_*.py

test:
	@echo Testing ... diff should be silent
	@./spellcrypt.py -e -i sayings.txt -f -o sayings.tmp
	@./spellcrypt.py -d -i sayings.tmp -f -o sayings.dec
	diff sayings.txt sayings.dec
	@rm -f sayings.tmp sayings.dec

testall:
	@cd alltests ; ./testall.sh

clean:
	@rm -f  aa* bb* cc* dd*
	@rm -f  Makefile.enc Makefile.dec
	@rm -rf __pycache__/
	@rm -rf build/* dist/* spellcrypt.egg-info/*
	@rm -rf gui/__pycache__
	@rm -rf spelib/__pycache__/
	@find . -name "*.pyc" -delete
	@find tests -name "*.txt.enc" -delete

cleankeys:
	@rm -rf ./data/keys

PPP=PYTHONPATH="" python3 -W ignore::DeprecationWarning `which pdoc` --force --html

docs:
	@${PPP} -o docs/ spellcrypt.py
	@${PPP} -o spelib/docs spelib/spemod.py
	@${PPP} -o spelib/docs spelib/mainwin.py
	@${PPP} -o spelib/docs spelib/hexdump.py
	@${PPP} -o spelib/docs spelib/pgutil.py
	@${PPP} -o spelib/docs spelib/spepass.py

test-env:
	@echo var: ${SUB}

# EOF
