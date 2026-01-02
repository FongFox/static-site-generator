import unittest

from inline_markdown import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    text_node_to_html_node,
)
from textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_split_nodes_delimiter_with_no_delimiter(self):
        node = TextNode("hello world", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.TEXT)
        expected = [TextNode("hello world", TextType.TEXT)]
        self.assertEqual(expected, new_nodes)

    def test_split_nodes_delimiter_with_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(expected, new_nodes)

    def test_split_nodes_delimiter_raises_on_unmatched_delimiter(self):
        node = TextNode("This is invalid `code", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_and_links(self):
        sample_text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and [to boot dev](https://www.boot.dev)"
        expected_images = [("rick roll", "https://i.imgur.com/aKaOqIh.gif")]
        expected_links = [("to boot dev", "https://www.boot.dev")]

        self.assertListEqual(extract_markdown_images(sample_text), expected_images)
        self.assertListEqual(extract_markdown_links(sample_text), expected_links)


if __name__ == "__main__":
    unittest.main()
