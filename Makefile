REPO_TEST ?= pypitest
REPO ?= pypi

.PHONY: dist register register_prod upload upload_prod install uninstall
.DEFAULT_GOAL := dist

dist:
	python setup.py sdist

register:
	python setup.py register -r $(REPO_TEST)

register_prod:
	python setup.py register -r $(REPO)

upload:
	python setup.py sdist upload -r $(REPO_TEST)

upload_prod:
	python setup.py sdist upload -r $(REPO)

install:
	python setup.py install

uninstall:
	pip uninstall alertlogic-cli -y
