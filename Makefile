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
	#git push local

test:


clean:
	@rm -f  aa* bb* cc* dd*
	@rm -rf __pycache__/
	@rm -rf gui/__pycache__
	@rm -rf spelib/__pycache__/
	@find . -name "*.pyc" -delete

cleankeys:
	@rm -rf ./data/keys

md5:

test_env:
	@echo ${SUB}













