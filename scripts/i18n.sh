#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONTENT_DIR="$ROOT_DIR/src-4/content"
PO_FILE="$ROOT_DIR/output.po"

cd "$ROOT_DIR"

usage() {
    cat <<'EOF'
Usage: scripts/i18n.sh <command>

Commands:
  update       Update output.po from Markdown (use --dry-run to preview)
  extract      Create a new PO from Markdown
  apply        Apply output.po translations to Japanese Markdown
  html-extract Create a PO from generated HTML in docs/
  html-apply   Apply the generated HTML PO translations to docs/
EOF
}

COMMAND="${1:-}"
shift || true

case "$COMMAND" in
    update)
        python3 scripts/i18n/update_po_from_md.py --dir "$CONTENT_DIR" --po "$PO_FILE" "$@"
        ;;
    extract)
        python3 scripts/i18n/md_gettext.py extract --dir "$CONTENT_DIR" --po "$PO_FILE" "$@"
        ;;
    apply)
        python3 scripts/i18n/apply_po_to_ja.py "$@"
        ;;
    html-extract)
        python3 scripts/i18n/html_gettext.py extract --dir "$ROOT_DIR/docs" --po "$ROOT_DIR/docs_extracted.po" "$@"
        ;;
    html-apply)
        python3 scripts/i18n/html_gettext.py apply --dir "$ROOT_DIR/docs" --po "$ROOT_DIR/docs_extracted.po" "$@"
        ;;
    *)
        usage
        exit 1
        ;;
esac
