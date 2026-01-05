import re

from htmlnode import LeafNode
from textnode import TextNode, TextType


def text_node_to_html_node(text_node):
    """
    Converts TextNode to HTMLNode (LeafNode).

    Args:
        text_node (TextNode): Text node to convert

    Returns:
        LeafNode: Corresponding HTML node

    Raises:
        Exception: If text_type is invalid

    Conversion mapping:
        TEXT → plain text (no tag)
        BOLD → <b>
        ITALIC → <i>
        CODE → <code>
        LINK → <a href="...">
        IMAGE → <img src="..." alt="...">
    """
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
    """
    Splits TextNodes by delimiter (e.g., ** for bold, ` for code).

    Args:
        old_nodes (list[TextNode]): Nodes to process
        delimiter (str): Delimiter string
        text_type (TextType): Type for delimited content

    Returns:
        list[TextNode]: Split nodes

    Raises:
        Exception: If delimiters are unpaired (odd count)

    Example:
        >>> nodes = [TextNode("text **bold**", TEXT)]
        >>> split_nodes_delimiter(nodes, "**", BOLD)
        [TextNode("text ", TEXT), TextNode("bold", BOLD)]

    Note:
        Only processes TEXT type nodes. Others pass through.
    """
    node_list = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            node_list.append(old_node)
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
    """
    Extracts all markdown images: ![alt](url)

    Args:
        text (str): Markdown text

    Returns:
        list[tuple]: [(alt_text, url), ...]

    Example:
        >>> extract_markdown_images("![cat](cat.jpg)")
        [('cat', 'cat.jpg')]
    """
    return re.findall(r"!\[([^]]+)\]\(([^)]+)\)", text)


def split_nodes_image(old_nodes):
    """
    Splits TextNodes containing markdown images.

    Args:
        old_nodes (list[TextNode]): Nodes to process

    Returns:
        list[TextNode]: Nodes split into TEXT and IMAGE types

    Example:
        >>> nodes = [TextNode("see ![cat](cat.jpg)", TEXT)]
        >>> split_nodes_image(nodes)
        [TextNode("see ", TEXT), TextNode("cat", IMAGE, "cat.jpg")]
    """
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
    """
    Extracts markdown links (not images): [text](url)

    Args:
        text (str): Markdown text

    Returns:
        list[tuple]: [(link_text, url), ...]

    Example:
        >>> extract_markdown_links("[Google](https://google.com)")
        [('Google', 'https://google.com')]

    Note:
        Uses negative lookbehind to exclude images (![...]).
    """
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_link(old_nodes):
    """
    Splits TextNodes containing markdown links.

    Args:
        old_nodes (list[TextNode]): Nodes to process

    Returns:
        list[TextNode]: Nodes split into TEXT and LINK types

    Example:
        >>> nodes = [TextNode("Visit [Google](https://google.com)", TEXT)]
        >>> split_nodes_link(nodes)
        [TextNode("Visit ", TEXT), TextNode("Google", LINK, "https://google.com")]
    """
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


def text_to_textnodes(text):
    """
    Main function: converts markdown text to parsed TextNodes.

    Handles all inline markdown: images, links, bold, italic, code.

    Args:
        text (str): Raw markdown text

    Returns:
        list[TextNode]: Fully parsed nodes

    Processing order:
        1. Images (![alt](url))
        2. Links ([text](url))
        3. Bold (**)
        4. Italic (_)
        5. Code (`)

    Example:
        >>> text_to_textnodes("**bold** and _italic_")
        [TextNode("bold", BOLD), TextNode(" and ", TEXT), TextNode("italic", ITALIC)]

    Note:
        Order matters! Images/links first to avoid parsing URLs.
    """
    nodes = [TextNode(text=text, text_type=TextType.TEXT)]

    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    return nodes
