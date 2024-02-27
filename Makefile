.PHONY: flake8
flake8:
	@flake8 app

.PHONY: pylint
pylint:
	pylint --module-naming-style=any app/*.py

.PHONY: check
check: flake8 pylint
