#!/usr/bin/env bash

SERVICE_ROOT=$(realpath $(dirname $0)/../)
DOCKERFILE_PATH=${SERVICE_ROOT}/Dockerfile
ARGS=("$@")

docker build -t <SERVICE-NAME>:latest -f ${DOCKERFILE_PATH} ${SERVICE_ROOT} ${ARGS[@]}
