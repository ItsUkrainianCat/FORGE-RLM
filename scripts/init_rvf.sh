#!/usr/bin/env bash
set -eu
cat <<'TXT'
FORGE intentionally does not fabricate memory/project.rvf.
Inspect the installed Ruflo/RuVector RVF surface first:
  npx ruflo@latest --help
  npx ruvector --help
If using the Ruflo marketplace, verify the current ruflo-rvf plugin commands in the installed version.
Record exact create/validate/export/import commands in docs/ENVIRONMENT.md and docs/MEMORY_ARCHITECTURE.md before initializing the artifact.
TXT
