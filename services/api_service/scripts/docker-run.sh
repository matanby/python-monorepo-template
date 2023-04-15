#!/usr/bin/env bash

ARGS="$@"

docker run -it --rm \
  --name api-service \
  api-service:latest \
  $ARGS
