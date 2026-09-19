#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

case "${1:-}" in
    fix-links)
        shift
        python3 scripts/maintenance/fix_links_proper2.py "$@"
        ;;
    split-translation)
        python3 scripts/maintenance/split_script_safe.py
        ;;
    *)
        echo "Usage: scripts/maintenance.sh {fix-links|split-translation}"
        exit 1
        ;;
esac
