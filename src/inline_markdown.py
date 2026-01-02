import re

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


def extract_markdown_images(text):
    # TODO: dùng regex để tìm và trả về list các (alt, url)
    return re.findall(r"!\[([^]]+)\]\(([^)]+)\)", text)


def split_nodes_image(old_nodes):
    node_list = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            node_list.append(old_node)
            continue

        image_nodes = extract_markdown_images(old_node.text)
        if not image_nodes:
            node_list.append(old_node)
            continue

        current_text = old_node.text
        for img_alt, img_link in image_nodes:
            pattern = f"![{img_alt}]({img_link})"
            before, after = current_text.split(pattern, 1)
            if before != "":
                node_list.append(TextNode(text=before, text_type=TextType.TEXT))
            node_list.append(
                TextNode(text=img_alt, text_type=TextType.IMAGE, url=img_link)
            )
            current_text = after

        if current_text != "":
            node_list.append(TextNode(text=current_text, text_type=TextType.TEXT))

    return node_list


def extract_markdown_links(text):
    # TODO: tương tự nhưng cho link thường
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_link(old_nodes):
    node_list = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            node_list.append(old_node)
            continue

        link_nodes = extract_markdown_links(old_node.text)
        if not link_nodes:
            node_list.append(old_node)
            continue

        current_text = old_node.text
        for link_text, link_url in link_nodes:
            pattern = f"[{link_text}]({link_url})"
            before, after = current_text.split(pattern, 1)
            if before != "":
                node_list.append(TextNode(text=before, text_type=TextType.TEXT))
            node_list.append(
                TextNode(text=link_text, text_type=TextType.LINK, url=link_url)
            )
            current_text = after

        if current_text != "":
            node_list.append(TextNode(text=current_text, text_type=TextType.TEXT))

    return node_list


# if __name__ == "__main__":
#     node = TextNode(
#         "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
#         TextType.TEXT,
#     )
#     new_nodes = split_nodes_image([node])
