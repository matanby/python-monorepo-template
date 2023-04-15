#!/usr/bin/env bash

SERVICE_ROOT=$(realpath $(dirname $0)/../)
TESTS_FOLDER=$SERVICE_ROOT/tests
ARGS=$@

poetry run pytest -rav $TESTS_FOLDER $ARGS
