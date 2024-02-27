.PHONY: flake8
flake8:
	@flake8 app

.PHONY: pylint
pylint:
	pylint --module-naming-style=any app/*.py

.PHONY: test
test: flake8 pylint

.PHONY: all
all: test

.PHONY: clean
clean:
	@true
