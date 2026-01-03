import unittest

from markdown_blocks import BlockType, block_to_block_type, markdown_to_blocks


class TestMarkdownBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
        """

        blocks = markdown_to_blocks(md)
        expected = [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ]
        self.assertEqual(blocks, expected)

    def test_markdown_to_blocks_with_header(self):
        md = """
# This is a heading

This is a paragraph of text.
It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item
        """

        blocks = markdown_to_blocks(md)
        expected = [
            "# This is a heading",
            "This is a paragraph of text.\nIt has some **bold** and _italic_ words inside of it.",
            "- This is the first list item in a list block\n- This is a list item\n- This is another list item",
        ]
        self.assertEqual(blocks, expected)

    def test_is_code_block(self):
        block = "```\nprint('hi')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_is_not_code_block(self):
        block = "Hello World!"
        self.assertNotEqual(block_to_block_type(block), BlockType.CODE)

    def test_is_heading_1(self):
        block = "# Heading 1"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_is_heading_3(self):
        block = "### Heading 3"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_is_not_heading(self):
        block = "Heading 1"
        self.assertNotEqual(block_to_block_type(block), BlockType.HEADING)

    def test_is_quote_block(self):
        block = "> This is a quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_is_not_quote_block(self):
        block = "This is a quote"
        self.assertNotEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_is_unordered_list(self):
        block = """
- This is the first list item in a list block
- This is a list item
- This is another list item
        """
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_is_not_unordered_list(self):
        block = """
- This is the first list item in a list block
This is a list item
- This is another list item
        """
        self.assertNotEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_is_ordered_list(self):
        block = """
1. first
2. second
3. third
        """
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_is_not_ordered_list(self):
        block = """
1. first
3. third
        """
        self.assertNotEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_is_paragraph(self):
        block = "Hello World!"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()
