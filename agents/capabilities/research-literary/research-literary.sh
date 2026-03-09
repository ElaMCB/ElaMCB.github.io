#!/bin/bash
# Research & Literary Agent – Monthly publish capability.
# Runs the Python monthly update script from repo root.

set +e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
cd "$REPO_ROOT" || exit 1

if ! command -v python3 >/dev/null 2>&1; then
    echo "ERROR: python3 not found" >&2
    exit 1
fi

python3 "$SCRIPT_DIR/monthly_update.py"
exit $?
