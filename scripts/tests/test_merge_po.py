import tempfile
import unittest
from pathlib import Path

import polib

from scripts.i18n.merge_po import merge_po_files


class TestMergePo(unittest.TestCase):
    def test_adds_new_entries_and_preserves_existing_translation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source_path = root / "docs_extracted.po"
            target_path = root / "output.po"

            source = polib.POFile()
            source.append(
                polib.POEntry(
                    msgid="Existing",
                    msgstr="",
                    occurrences=[("4.x/index.html", "")],
                )
            )
            source.append(
                polib.POEntry(
                    msgid="New",
                    msgstr="",
                    occurrences=[("4.x/new/index.html", "")],
                )
            )
            source.append(
                polib.POEntry(
                    msgid="Japanese page only",
                    msgstr="",
                    occurrences=[("4.x/ja/index.html", "")],
                )
            )
            source.save(source_path)

            target = polib.POFile()
            target.append(
                polib.POEntry(
                    msgid="Existing",
                    msgstr="既存の翻訳",
                    occurrences=[("_index.md", "")],
                )
            )
            target.save(target_path)

            stats = merge_po_files(str(source_path), str(target_path))
            merged = polib.pofile(target_path)

            self.assertEqual(stats["added"], 1)
            self.assertEqual(stats["skipped_japanese_only"], 1)
            self.assertEqual(merged.find("Existing").msgstr, "既存の翻訳")
            self.assertEqual(merged.find("New").msgstr, "")
            self.assertIsNone(merged.find("Japanese page only"))

    def test_dry_run_does_not_write(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source_path = root / "source.po"
            target_path = root / "target.po"

            source = polib.POFile()
            source.append(polib.POEntry(msgid="New", msgstr=""))
            source.save(source_path)
            target = polib.POFile()
            target.save(target_path)

            merge_po_files(str(source_path), str(target_path), dry_run=True)

            self.assertIsNone(polib.pofile(target_path).find("New"))


if __name__ == "__main__":
    unittest.main()
