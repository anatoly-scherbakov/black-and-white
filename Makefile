SHELL:=/usr/bin/env bash

.PHONY: lint
lint:
	mypy black_and_white tests/**/*.py
	flake8 .
	doc8 -q docs

.PHONY: unit
unit:
	pytest

.PHONY: package0
package:
	poetry check
	pip check
	safety check --bare --full-report

.PHONY: test
test: lint unit package
