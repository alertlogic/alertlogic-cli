.PHONY: dist install uninstall
.DEFAULT_GOAL := dist

test:
	pytest tests/*_tests.py

lint:
	pycodestyle .

dist:
	python setup.py sdist

pypi_upload: dist
	twine upload dist/alertlogic-cli-*.tar.gz

install:
	python setup.py install

uninstall:
	pip uninstall alertlogic-cli -y
