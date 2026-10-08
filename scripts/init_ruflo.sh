#!/usr/bin/env bash
set -euo pipefail

if ! command -v node >/dev/null 2>&1; then
  echo "Node 20+ required before Ruflo setup." >&2
  exit 1
fi

npx ruflo@latest doctor --fix || true
cat <<'EOF'
If full Ruflo is desired and not initialized, run:
  npx ruflo@latest init wizard
Then register one intended MCP server:
  claude mcp add ruflo -- npx ruflo@latest mcp start
Do not register duplicate Ruflo MCP servers.
EOF
