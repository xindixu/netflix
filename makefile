.PHONY: Netflix.log

FILES :=                              \
    Netflix.html                      \
    Netflix.log                       \
    Netflix.py                        \
    RunNetflix.in                     \
    RunNetflix.out                    \
    RunNetflix.py                     \
    TestNetflix.out                   \
    TestNetflix.py

#    cs329e-netflix-tests/YourGitLabID-RunNetflix.in   \
#    cs329e-netflix-tests/YourGitLabID-RunNetflix.out  \
#    cs329e-netflix-tests/YourGitLabID-TestNetflix.out \
#    cs329e-netflix-tests/YourGitLabID-TestNetflix.py  \
#

ifeq ($(shell uname), Darwin)          # Apple
    PYTHON   := python3
    PIP      := pip3
    PYLINT   := pylint
    COVERAGE := coverage
    PYDOC    := pydoc3
    AUTOPEP8 := autopep8
else ifeq ($(shell uname -p), unknown) # Windows
    PYTHON   := python                 # on my machine it's python
    PIP      := pip3
    PYLINT   := pylint
    COVERAGE := coverage
    PYDOC    := python -m pydoc        # on my machine it's pydoc
    AUTOPEP8 := autopep8
else                                   # UTCS
    PYTHON   := python3
    PIP      := pip3
    PYLINT   := pylint3
    COVERAGE := coverage
    PYDOC    := pydoc3
    AUTOPEP8 := autopep8
endif


netflix-tests:
	git clone https://gitlab.com/fareszf/cs329e-netflix-tests.git

Netflix.html: Netflix.py
	$(PYDOC) -w Netflix

Netflix.log:
	git log > Netflix.log

RunNetflix.tmp: RunNetflix.in RunNetflix.out RunNetflix.py Netflix.py
	$(PYTHON) RunNetflix.py < RunNetflix.in > RunNetflix.tmp
	# $(PYTHON) RunNetflix.py < probe.txt > RunNetflix.tmp
	diff --strip-trailing-cr RunNetflix.tmp RunNetflix.out

TestNetflix.tmp: TestNetflix.py Netflix.py
	$(COVERAGE) run    --branch TestNetflix.py >  TestNetflix.tmp 2>&1
	$(COVERAGE) report -m --omit=/usr/lib/python3/dist-packages/* >> TestNetflix.tmp
	# cat TestNetflix.tmp

check:
	@not_found=0;                                 \
    for i in $(FILES);                            \
    do                                            \
        if [ -e $$i ];                            \
        then                                      \
            echo "$$i found";                     \
        else                                      \
            echo "$$i NOT FOUND";                 \
            not_found=`expr "$$not_found" + "1"`; \
        fi                                        \
    done;                                         \
    if [ $$not_found -ne 0 ];                     \
    then                                          \
        echo "$$not_found failures";              \
        exit 1;                                   \
    fi;                                           \
    echo "success";

clean:
	rm -f  .coverage
	rm -f  *.pyc
	rm -f  RunNetflix.tmp
	rm -f  TestNetflix.tmp
	rm -rf __pycache__
	rm -rf cs329e-netflix-tests

config:
	git config -l

format:
	$(AUTOPEP8) -i Netflix.py
	$(AUTOPEP8) -i RunNetflix.py
	$(AUTOPEP8) -i TestNetflix.py

scrub:
	make clean
	rm -f  Netflix.html
	rm -f  Netflix.log
	rm -rf Netflix-tests

status:
	make clean
	@echo
	git branch
	git remote -v
	git status

versions:
	which     $(AUTOPEP8)
	autopep8 --version
	@echo
	which    $(COVERAGE)
	coverage --version
	@echo
	which    git
	git      --version
	@echo
	which    make
	make     --version
	@echo
	which    $(PIP)
	pip      --version
	@echo
#	which    $(PYDOC)
#	pydoc    --version
#	@echo
	which    $(PYLINT)
	pylint   --version
	@echo
	which    $(PYTHON)
	python   --version

test: Netflix.html Netflix.log RunNetflix.tmp TestNetflix.tmp netflix-tests check
