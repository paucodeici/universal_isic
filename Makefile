.PHONY: build publish

help:
	@grep '^[a-zA-Z]' $(MAKEFILE_LIST) | \
	awk -F ':.*?# ' 'NF==2 {printf "  %-26s%s\n", $$1, $$2}'

build: # Build the the package
	rm -vfr build dist
	python setup.py sdist bdist_wheel --universal

publish: # Push the package to PyPI
	twine upload dist/*
