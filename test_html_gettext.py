import unittest
from html_gettext import escape_po_string, unescape_po_string

class TestHtmlGettext(unittest.TestCase):
    def test_escape_po_string(self):
        # Normal string
        self.assertEqual(escape_po_string("Hello World"), "Hello World")
        # String with newline
        self.assertEqual(escape_po_string("Hello\nWorld"), "Hello\\nWorld")
        # String with double quotes
        self.assertEqual(escape_po_string('He said "Hello"'), 'He said \\"Hello\\"')
        # String with backslashes
        self.assertEqual(escape_po_string("C:\\path\\to\\file"), "C:\\\\path\\\\to\\\\file")
        # Combination
        self.assertEqual(escape_po_string('Line 1\nLine 2 with "quotes" and \\backslashes\\'),
                         'Line 1\\nLine 2 with \\"quotes\\" and \\\\backslashes\\\\')
        # Empty string
        self.assertEqual(escape_po_string(""), "")

    def test_unescape_po_string(self):
        # Normal string
        self.assertEqual(unescape_po_string("Hello World"), "Hello World")
        # String with escaped newline
        self.assertEqual(unescape_po_string("Hello\\nWorld"), "Hello\nWorld")
        # String with escaped double quotes
        self.assertEqual(unescape_po_string('He said \\"Hello\\"'), 'He said "Hello"')
        # String with escaped backslashes
        self.assertEqual(unescape_po_string("C:\\\\path\\\\to\\\\file"), "C:\\path\\to\\file")
        # Combination
        self.assertEqual(unescape_po_string('Line 1\\nLine 2 with \\"quotes\\" and \\\\backslashes\\\\'),
                         'Line 1\nLine 2 with "quotes" and \\backslashes\\')
        # Empty string
        self.assertEqual(unescape_po_string(""), "")

    def test_roundtrip(self):
        test_strings = [
            "Hello World",
            "Hello\nWorld",
            'He said "Hello"',
            "C:\\path\\to\\file",
            'Line 1\nLine 2 with "quotes" and \\backslashes\\',
            ""
        ]
        for s in test_strings:
            self.assertEqual(unescape_po_string(escape_po_string(s)), s)

if __name__ == "__main__":
    unittest.main()
