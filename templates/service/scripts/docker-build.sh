#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
exec docker build -t "<SERVICE-NAME>:latest" -f Dockerfile ../.. "$@"
