#!/usr/bin/env bash

SERVICE_ROOT=$(realpath $(dirname $0)/../)
SRC_FOLDER=$SERVICE_ROOT/src
TESTS_FOLDER=$SERVICE_ROOT/tests
ARGS=$@

poetry run black $SRC_FOLDER $TESTS_FOLDER $ARGS
