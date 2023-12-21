#!/usr/bin/env bash
set -x
set -u
set -o pipefail

black .
isort .
pytest --cov --cov-report=term-missing --cov-report=xml:coverage.xml
mypy --install-types --non-interactive src
pylint src