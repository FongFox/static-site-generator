import unittest

from gencontent import extract_title


class TestGenContent(unittest.TestCase):
    def test_extract_title_basic(self):
        markdown = "# Tolkien Fan Club"
        result = extract_title(markdown)
        expected = "Tolkien Fan Club"
        self.assertEqual(result, expected)

    def test_extract_title_multiline(self):
        markdown = "# Tolkien Fan Club\n\nSome content\n## Subheading"
        result = extract_title(markdown)
        expected = "Tolkien Fan Club"
        self.assertEqual(result, expected)

    def test_extract_title_with_leading_spaces(self):
        markdown = "   #   Weird Title   \nOther line"
        result = extract_title(markdown)
        expected = "Weird Title"
        self.assertEqual(result, expected)

    def test_extract_title_no_h1_raises(self):
        markdown = "## Not h1\nJust text"
        with self.assertRaises(Exception):
            extract_title(markdown)
