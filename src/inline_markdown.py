from htmlnode import LeafNode
from textnode import TextNode, TextType


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(tag=None, value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.LINK:
            link_props = {"href": text_node.url}
            return LeafNode(tag="a", value=text_node.text, props=link_props)
        case TextType.IMAGE:
            img_props = {"src": text_node.url, "alt": text_node.text}
            return LeafNode(tag="img", value="", props=img_props)
        case _:
            raise Exception("Invalid text type")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    node_list = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            node_list.append(TextNode(text=old_node.text, text_type=old_node.text_type))
            continue
        split_parts = old_node.text.split(delimiter)
        if len(split_parts) % 2 == 0:
            raise Exception("Invalid Markdown syntax")
        for index, part in enumerate(split_parts):
            if index % 2 == 0:
                node_list.append(TextNode(text=part, text_type=TextType.TEXT))
                continue
            node_list.append(TextNode(text=part, text_type=text_type))
    return node_list
