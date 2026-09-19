"""Merge strings extracted from generated HTML into the translation PO file.

The generated HTML contains strings that are not always represented in the
Markdown source PO (for example, theme/navigation text and rendered titles).
This command adds those strings to the existing PO while keeping all existing
translations intact.
"""

from __future__ import annotations

import argparse
import os
from collections.abc import Iterable

import polib


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))


def _is_japanese_reference(path: str) -> bool:
    """Return whether an extracted HTML path belongs to the Japanese site."""
    normalized = path.replace(os.sep, "/").strip("/")
    return "/ja/" in f"/{normalized}/"


def _filtered_occurrences(
    occurrences: Iterable[tuple[str, str]], include_japanese: bool
) -> list[tuple[str, str]]:
    """Return sorted, deduplicated source references for an extracted entry."""
    refs = {
        (path, comment)
        for path, comment in occurrences
        if include_japanese or not _is_japanese_reference(path)
    }
    return sorted(refs)


def merge_po_files(
    source_path: str,
    target_path: str,
    *,
    include_japanese: bool = False,
    dry_run: bool = False,
) -> dict[str, int]:
    """Merge *source_path* entries into *target_path*.

    Existing target translations and entries are never removed.  New entries
    receive an empty translation unless the source entry itself has a
    translation.  Existing references are retained and source references are
    added so a later extraction can still refresh them.
    """
    source = polib.pofile(source_path)
    target = polib.pofile(target_path) if os.path.exists(target_path) else polib.POFile()

    added = 0
    updated_references = 0
    copied_translations = 0
    skipped_japanese_only = 0

    for source_entry in source:
        if not source_entry.msgid or source_entry.obsolete:
            continue

        occurrences = _filtered_occurrences(
            source_entry.occurrences, include_japanese
        )
        if not occurrences:
            skipped_japanese_only += 1
            continue

        target_entry = target.find(source_entry.msgid)
        if target_entry is None:
            target_entry = polib.POEntry(
                msgid=source_entry.msgid,
                msgstr=source_entry.msgstr,
                occurrences=occurrences,
                flags=list(source_entry.flags),
                comment=source_entry.comment,
                tcomment=source_entry.tcomment,
            )
            target.append(target_entry)
            added += 1
            if source_entry.msgstr:
                copied_translations += 1
            continue

        old_occurrences = set(target_entry.occurrences)
        merged_occurrences = sorted(old_occurrences | set(occurrences))
        if merged_occurrences != target_entry.occurrences:
            target_entry.occurrences = merged_occurrences
            updated_references += 1

        # Keep a hand-maintained translation authoritative.  This also makes
        # the command safe if the source PO is later given translated entries.
        if not target_entry.msgstr and source_entry.msgstr:
            target_entry.msgstr = source_entry.msgstr
            copied_translations += 1

    if not dry_run:
        target.save(target_path)

    return {
        "source_entries": sum(
            1 for entry in source if entry.msgid and not entry.obsolete
        ),
        "added": added,
        "updated_references": updated_references,
        "copied_translations": copied_translations,
        "skipped_japanese_only": skipped_japanese_only,
        "target_entries": len(target),
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Merge docs_extracted.po into output.po without losing translations."
    )
    parser.add_argument(
        "--source",
        default=os.path.join(PROJECT_ROOT, "docs_extracted.po"),
        help="PO file created from generated HTML",
    )
    parser.add_argument(
        "--target",
        default=os.path.join(PROJECT_ROOT, "output.po"),
        help="Translation PO file to update",
    )
    parser.add_argument(
        "--include-ja",
        action="store_true",
        help="Also import entries found only under generated Japanese pages",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show the merge result without writing the target file",
    )
    args = parser.parse_args()

    if not os.path.isfile(args.source):
        parser.error(f"source PO file not found: {args.source}")
    if not os.path.isfile(args.target):
        parser.error(f"target PO file not found: {args.target}")

    stats = merge_po_files(
        args.source,
        args.target,
        include_japanese=args.include_ja,
        dry_run=args.dry_run,
    )
    prefix = "Dry run: " if args.dry_run else ""
    print(f"{prefix}Merged {args.source} into {args.target}")
    print(f"  Source entries: {stats['source_entries']}")
    print(f"  Added: {stats['added']}")
    print(f"  References updated: {stats['updated_references']}")
    print(f"  Translations copied: {stats['copied_translations']}")
    print(f"  Japanese-only entries skipped: {stats['skipped_japanese_only']}")
    print(f"  Target entries: {stats['target_entries']}")


if __name__ == "__main__":
    main()
