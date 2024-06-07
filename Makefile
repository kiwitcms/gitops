# Copyright (c) 2024 Alexander Todorov <atodorov@otb.bg>
#
# Licensed under GNU Affero General Public License v3 or later (AGPLv3+)
# https://www.gnu.org/licenses/agpl-3.0.html

.PHONY: flake8
flake8:
	@flake8 app

.PHONY: pylint
pylint:
	pylint --module-naming-style=any \
	       --disable missing-class-docstring,too-few-public-methods \
	       app/*.py

.PHONY: test
test: flake8 pylint

.PHONY: all
all: test

.PHONY: clean
clean:
	@true
