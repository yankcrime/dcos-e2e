# Make commands for linting

SHELL := /bin/bash -euxo pipefail

.PHONY: fix-yapf
fix-yapf:
	yapf \
		--style='{DEDENT_CLOSING_BRACKETS: true}' \
		--in-place \
		--recursive \
		--exclude='**/_vendor' \
		--exclude='versioneer.py' \
		--exclude='**/_version.py' \
		.

.PHONY: mypy
mypy:
	mypy *.py src/ tests/ admin/

.PHONY: doc8
doc8:
	doc8 .

.PHONY: pip-extra-reqs
pip-extra-reqs:
	pip-extra-reqs src/

.PHONY: pip-missing-reqs
pip-missing-reqs:
	pip-missing-reqs src/

.PHONY: pylint
pylint:
	pylint *.py src/ tests/ admin/

.PHONY: pyroma
pyroma:
	pyroma --min 10 .

.PHONY: linkcheck
linkcheck:
	$(MAKE) -C docs/library linkcheck SPHINXOPTS=$(SPHINXOPTS)
	$(MAKE) -C docs/cli linkcheck SPHINXOPTS=$(SPHINXOPTS)

.PHONY: spelling
spelling:
	$(MAKE) -C docs/library spelling SPHINXOPTS=$(SPHINXOPTS)
	$(MAKE) -C docs/cli spelling SPHINXOPTS=$(SPHINXOPTS)

.PHONY: custom-linters
custom-linters:
	pytest -vvv -x admin/custom_linters.py

.PHONY: shellcheck
shellcheck:
	shellcheck --exclude SC2164,SC1091 admin/*.sh

.PHONY: strictest
strictest:
	strictest lint \
		--skip='**/_vendor/*' \
		--skip='versioneer.py' \
		--skip="**/_version.py"

.PHONY: autoflake
autoflake:
	autoflake \
	    --in-place \
	    --recursive \
	    --remove-all-unused-imports \
	    --remove-unused-variables \
	    --expand-star-imports \
	    --exclude _vendor,src/*/_version.py,versioneer.py,release \
	    .
