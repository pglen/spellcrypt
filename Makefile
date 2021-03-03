# Use to build modules

.PHONY: test clean

all:
	@echo Targets: git build test clean deb init cleankeys
	@echo Target \'build\' makes the \'C\' libs
	@echo Target \'init\' generates an initial key.
	@echo Target \'cleankeys\' deletes all keys.

init:
	@python3 ./tools/genkey.py

git:
	git add .
	git commit -m auto
	git push
	git push local
test:
	@make -C client test

deb:  build build3
	./build-deb.sh

clean:
	@rm -rf __pycache__/
	@rm -rf gui/__pycache__
	@rm -rf spellcryptlib/__pycache__/
	find . -name "*.pyc" -delete

cleankeys:
	@rm -rf ./data/keys

md5:













