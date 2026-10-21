#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
exec uv run --locked --package "<SERVICE-NAME>" "<SERVICE-NAME>" "$@"
