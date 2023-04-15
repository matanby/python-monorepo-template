#!/usr/bin/env bash

PACKAGE_ROOT=$(realpath $(dirname $0)/../)
SRC_FOLDER=$PACKAGE_ROOT/src
TESTS_FOLDER=$PACKAGE_ROOT/tests
ARGS=$@

poetry run ruff $SRC_FOLDER $TESTS_FOLDER $ARGS
