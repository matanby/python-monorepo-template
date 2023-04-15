#!/usr/bin/env bash

PACKAGE_ROOT=$(realpath $(dirname $0)/../)
TESTS_FOLDER=$PACKAGE_ROOT/tests
ARGS=$@

poetry run pytest -rav $TESTS_FOLDER $ARGS
