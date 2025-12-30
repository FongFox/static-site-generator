import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )


if __name__ == "__main__":
    unittest.main()
