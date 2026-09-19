import unittest

from scripts.i18n.apply_po_to_ja import translate_content
from scripts.i18n.update_po_from_md import extract_code_comments


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


if __name__ == "__main__":
    unittest.main()
