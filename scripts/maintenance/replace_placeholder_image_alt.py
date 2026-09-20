#!/usr/bin/env python3
"""Replace the literal Markdown image alt text ``alt`` with useful fallback text.

The source content contains legacy ``![alt](...)`` markup.  Hugo also applies a
render-time fallback, but storing a meaningful value in the Markdown keeps the
content accessible to other renderers and content tooling.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


IMAGE_PATTERN = re.compile(r"!\[alt\]\(([^\n)]+)\)")
YAML_TITLE_PATTERN = re.compile(r'^title:\s*["\']?(.*?)["\']?\s*$', re.MULTILINE)
TOML_TITLE_PATTERN = re.compile(r'^title\s*=\s*["\'](.*?)["\']\s*$', re.MULTILINE)


def page_title(content: str, path: Path) -> str:
    """Return the page title, falling back to a readable file stem."""
    for pattern in (YAML_TITLE_PATTERN, TOML_TITLE_PATTERN):
        match = pattern.search(content)
        if match:
            return match.group(1).strip()
    return path.stem.replace("_", " ").replace("-", " ")


def image_label(title: str, destination: str) -> str:
    """Create an accessible label from the page topic and image filename."""
    image_path = destination.split("?", 1)[0].split("#", 1)[0]
    filename = Path(image_path).stem.replace("_", " ").replace("-", " ")
    return f"Godot 4: {title} ({filename})"


def replace_in_file(path: Path, write: bool) -> int:
    content = path.read_text(encoding="utf-8")
    title = page_title(content, path)

    def replacement(match: re.Match[str]) -> str:
        return f"![{image_label(title, match.group(1))}]({match.group(1)})"

    updated, count = IMAGE_PATTERN.subn(replacement, content)
    if count and write:
        path.write_text(updated, encoding="utf-8")
    return count


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("content_dir", type=Path)
    parser.add_argument("--write", action="store_true", help="apply replacements")
    args = parser.parse_args()

    total = 0
    changed_files = 0
    for path in sorted(args.content_dir.rglob("*.md")):
        count = replace_in_file(path, args.write)
        if count:
            changed_files += 1
            total += count

    action = "Replaced" if args.write else "Would replace"
    print(f"{action} {total} placeholder alt texts in {changed_files} files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
