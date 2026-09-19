import unittest

from scripts.i18n.apply_po_to_ja import translate_content
from scripts.i18n.update_po_from_md import (
    extract_code_comments,
    extract_gdscript_comments,
    validate_gdscript_comments,
)


class TestCodeCommentTranslations(unittest.TestCase):
    def test_extracts_full_comment_lines_only(self):
        content = """```gdscript
# Top-level comment
    # Indented comment
value = "# Not a comment"
value += 1 # Inline comment
```"""

        self.assertEqual(
            extract_code_comments(content),
            {"# Top-level comment", "# Indented comment"},
        )

    def test_translates_comments_inside_code_without_changing_code(self):
        content = """# Heading

説明文

```gdscript
# Hello
    # Indented comment
var value = 1
print("# Not a comment")
```"""
        translations = {
            "# Heading": "# 見出し",
            "説明文": "日本語の説明",
            "# Hello": "# こんにちは",
            "# Indented comment": "# インデントされたコメント",
        }

        translated = translate_content(content, translations)

        self.assertIn("# 見出し", translated)
        self.assertIn("日本語の説明", translated)
        self.assertIn("# こんにちは", translated)
        self.assertIn("    # インデントされたコメント", translated)
        self.assertIn('var value = 1', translated)
        self.assertIn('print("# Not a comment")', translated)

    def test_only_gdscript_fenced_comments_are_extracted(self):
        content = """```gdscript
# GDScript comment
var text = "# Not a comment"
value += 1 # Inline comment
```

```python
# Python comment must not be included
```"""

        self.assertEqual(
            extract_gdscript_comments(content),
            {"# GDScript comment"},
        )

    def test_validates_comment_msgids_and_references(self):
        import polib

        po = polib.POFile()
        po.append(
            polib.POEntry(
                msgid="# Hello",
                msgstr="# こんにちは",
                occurrences=[("example.md", "")],
            )
        )

        missing, missing_references = validate_gdscript_comments(
            po, {"# Hello": {"example.md"}}
        )
        self.assertEqual(missing, [])
        self.assertEqual(missing_references, [])

        missing, missing_references = validate_gdscript_comments(
            po, {"# Hello": {"other.md"}, "# Missing": {"example.md"}}
        )
        self.assertEqual(missing, ["# Missing"])
        self.assertEqual(missing_references, [("# Hello", "other.md")])


if __name__ == "__main__":
    unittest.main()
