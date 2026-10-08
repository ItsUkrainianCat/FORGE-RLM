#!/usr/bin/env bash
set -eu
cd "${CLAUDE_PROJECT_DIR:-$(pwd)}"
mkdir -p artifacts
printf '%s config changed session=%s cwd=%s
' "$(date -Iseconds)" "${CLAUDE_SESSION_ID:-unknown}" "$PWD" >> artifacts/config-changes.log
exit 0
