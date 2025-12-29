import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_prop_to_html_multiple_props(self):
        link_props = {
            "href": "https://www.boot.dev",
            "target": "_blank",
        }
        html_node = HTMLNode(tag="a", value="This link", props=link_props)

        result = html_node.props_to_html()
        expected = ' href="https://www.boot.dev" target="_blank"'
        self.assertEqual(result, expected)

    def test_props_to_html_blank_prop(self):
        link_props = {}
        html_node = HTMLNode(tag="p", value="This is a text", props=link_props)

        result = html_node.props_to_html()
        expected = ""
        self.assertEqual(result, expected)

    def test_props_to_html_single_prop(self):
        link_props = {
            "href": "https://www.google.com",
        }
        html_node = HTMLNode(tag="a", value="Google", props=link_props)

        result = html_node.props_to_html()
        expected = ' href="https://www.google.com"'
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
