#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
exec docker run --rm --init "<SERVICE-NAME>:latest" "$@"
