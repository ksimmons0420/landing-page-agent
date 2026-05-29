#!/usr/bin/env bash
# Update the Landing Page Agent plugin from upstream.
# Usage: ./update.sh
set -euo pipefail
cd "$(dirname "$0")"
echo "→ git pull"
git pull --ff-only
echo "→ refreshing Claude Code plugin cache"
claude plugin marketplace update scalehouse
echo ""
echo "Done. Restart Claude Code to load the new files."
