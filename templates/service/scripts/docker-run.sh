#!/usr/bin/env bash

ARGS="$@"

docker run -it --rm \
  --name <SERVICE-NAME> \
  <SERVICE-NAME>:latest \
  $ARGS
