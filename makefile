.PHONY: clean test tox

NAME := hyperflask
VERSION := $(shell python setup.py --version)

VENV := venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
PYTEST := $(VENV)/bin/py.test
PEP8 := $(VENV)/bin/pep8
TOX := $(VENV)/bin/tox

PYSRC := $(shell find {hyperflask,tests} -iname '*.py')
TARGET := $(PWD)/target


###############
# Boilerplate #
###############

default: test

clean:
	rm -rf .tox htmlcov .coverage .eggs $(TARGET)

$(TARGET):
	mkdir -p $(TARGET)

#test: $(PYTEST) $(PIP)
#	$(PIP) install -U .
#	$(PYTEST) tests


##############
# Virtualenv #
##############

$(VENV)/bin/%: $(PIP)
	$(PIP) install $*

$(VENV)/bin/py.test: $(PIP)
	$(PIP) install pytest pytest-cov pytest-xdist

$(PYTHON) $(PIP):
	virtualenv -p python3 venv
	$(PIP) install virtualenv


################
# Unit Testing #
################

test: $(VENV)/bin/py.test $(PYSRC) $(PIP)
	#$(PIP) install -U . httpretty
	$(VENV)/bin/python setup.py test

tox: $(PYSRC) tox.ini $(TOX)
	$(TOX)
