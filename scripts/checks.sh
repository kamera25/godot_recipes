#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PO_FILE="${1:-$ROOT_DIR/output.po}"

cd "$ROOT_DIR"
echo "== PO checks =="
python3 scripts/checks/check_backticks.py "$PO_FILE" -o "$ROOT_DIR/mismatch_report.txt"
python3 scripts/checks/find_icon_mismatch.py "$PO_FILE"
python3 scripts/checks/find_untranslated.py "$PO_FILE"

echo "== Python tests =="
python3 -m unittest discover -s scripts/tests -p 'test_*.py'

if [[ -x "/Applications/Godot.app/Contents/MacOS/Godot" ]]; then
    echo "== GDScript checks =="
    python3 scripts/checks/check_gdscript_syntax.py "$ROOT_DIR/src-4/content"
else
    echo "Skipping GDScript checks: Godot was not found."
fi

if [[ -d "$ROOT_DIR/docs" ]]; then
    echo "== HTML link checks =="
    python3 scripts/checks/link_checker.py
else
    echo "Skipping HTML link checks: docs directory was not found."
fi
