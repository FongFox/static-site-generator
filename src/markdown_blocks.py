import re
from enum import Enum

from htmlnode import ParentNode
from inline_markdown import text_node_to_html_node, text_to_textnodes
from textnode import TextNode, TextType


class BlockType(Enum):
    """
    Markdown block types.

    PARAGRAPH: Regular text
    HEADING: # headings (h1-h6)
    CODE: ``` code blocks
    QUOTE: > blockquotes
    UNORDERED_LIST: - bullet lists
    ORDERED_LIST: 1. numbered lists
    """

    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    """
    Splits markdown into blocks (separated by blank lines).

    Args:
        markdown (str): Full markdown document

    Returns:
        list[str]: List of trimmed, non-empty blocks

    Example:
        >>> markdown_to_blocks("# Title\\n\\nParagraph")
        ['# Title', 'Paragraph']

    Note:
        Blocks separated by \\n\\n (double newline).
    """
    str_list = []

    temp_list = markdown.split("\n\n")
    for item in temp_list:
        new_item = item.strip()
        if new_item != "":
            str_list.append(new_item)

    return str_list


def is_unordered_list(lines):
    """
    Checks if all lines start with "- ".

    Args:
        lines (list[str]): Lines to check

    Returns:
        bool: True if all lines start with "- "
    """
    for line in lines:
        if not line.startswith("- "):
            return False
    return True


def is_ordered_list(lines):
    """
    Checks if lines form ordered list (1. 2. 3. ...).

    Args:
        lines (list[str]): Lines to check

    Returns:
        bool: True if consecutive numbers starting from 1

    Note:
        Must be 1, 2, 3... in order. Not 1, 3, 5.
    """
    for index, line in enumerate(lines):
        expected_prefix = f"{index + 1}. "
        if not line.startswith(expected_prefix):
            return False
    return True


def block_to_block_type(md_txt_block):
    """
    Determines block type of markdown block.

    Args:
        md_txt_block (str): Markdown block (can be multi-line)

    Returns:
        BlockType: Type of the block

    Check order:
        1. CODE (starts/ends with ```)
        2. HEADING (starts with #)
        3. QUOTE (starts with >)
        4. UNORDERED_LIST (all lines "- ")
        5. ORDERED_LIST (lines "1. 2. 3. ...")
        6. PARAGRAPH (default)
    """
    md_txt_block = md_txt_block.strip()
    lines = md_txt_block.split("\n")
    first_line = lines[0]
    last_line = lines[-1]

    if first_line.startswith("```") and last_line.startswith("```"):
        return BlockType.CODE

    if first_line.startswith("#"):
        heading_counter = 0
        for char in first_line:
            if char == "#":
                heading_counter += 1
            else:
                break
        return BlockType.HEADING

    if first_line.startswith(">"):
        return BlockType.QUOTE

    if is_unordered_list(lines):
        return BlockType.UNORDERED_LIST

    if is_ordered_list(lines):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def convert_line_type_to_html_tag(line_type, line=None):
    """
    Converts BlockType to HTML tag name.

    Args:
        line_type (BlockType): Block type
        line (str, optional): Needed for HEADING to count #

    Returns:
        str: HTML tag name

    Mapping:
        PARAGRAPH → "p"
        HEADING → "h1" to "h6" (counts #)
        CODE → "pre"
        QUOTE → "blockquote"
        UNORDERED_LIST → "ul"
        ORDERED_LIST → "ol"

    Raises:
        TypeError: If HEADING without line parameter
    """
    match line_type:
        case BlockType.PARAGRAPH:
            return "p"
        case BlockType.HEADING:
            if line is not None:
                heading_counter = 0
                for char in line:
                    if char == "#":
                        heading_counter += 1
                    else:
                        break
                return f"h{heading_counter}"
            else:
                raise TypeError("Invalid line value parameter")
        case BlockType.CODE:
            return "pre"
        case BlockType.QUOTE:
            return "blockquote"
        case BlockType.UNORDERED_LIST:
            return "ul"
        case BlockType.ORDERED_LIST:
            return "ol"
        case _:
            raise Exception("Invalid line type")


def handle_clean_line(line_type, line):
    """
    Removes markdown syntax from content.

    Args:
        line_type (BlockType): Type of block
        line (str): Content to clean

    Returns:
        str: Cleaned content

    Processing:
        HEADING: Remove leading #
        QUOTE: Remove leading >
        CODE: Remove ```, add \\n at end
        PARAGRAPH: Replace \\n with space
        Other: Return unchanged
    """
    if line_type == BlockType.HEADING:
        return line.lstrip("#").strip()
    elif line_type == BlockType.QUOTE:
        return line.lstrip(">").strip()
    elif line_type == BlockType.CODE:
        result = line.strip()
        if result.startswith("```"):
            result = result[3:]

        if result.endswith("```"):
            result = result[:-3]

        return result.strip() + "\n"
    elif line_type == BlockType.PARAGRAPH:
        return line.replace("\n", " ")
    else:
        return line


def clean_inner_line(inner_line):
    """
    Removes list markers from line start.

    - "- " or "* " for unordered lists
    - "1. ", "2. " ... for ordered lists
    """
    line = inner_line.lstrip()  # bỏ space thừa bên trái cho chắc

    if line.startswith("- ") or line.startswith("* "):
        return line[2:].strip()

    # xử lý dạng "1. text", "2. text"
    match = re.match(r"^\d+\.\s*(.*)$", line)
    if match:
        return match.group(1).strip()

    # nếu không khớp gì, trả lại như cũ
    return line.strip()


def markdown_to_html_node(md):
    """
    Main function: converts full markdown document to HTMLNode tree.

    This is the primary markdown-to-HTML converter. Handles all block
    types and inline markdown.

    Args:
        md (str): Complete markdown document

    Returns:
        ParentNode: Root <div> containing all HTML

    Processing:
        1. Split markdown into blocks
        2. For each block:
           - Detect type (heading, list, code, etc)
           - Convert to appropriate HTML tag
           - Clean markdown syntax
           - Parse inline markdown (bold, links, etc)
           - Build ParentNode tree
        3. Wrap all in <div> root

    Special handling:
        CODE: Wraps in <pre><code>...</code></pre>
        LISTS: Creates <li> for each item, parses inline markdown
        Others: Parses inline markdown, wraps in tag

    Example:
        >>> md = "# Title\\n\\nThis is **bold**"
        >>> node = markdown_to_html_node(md)
        >>> node.to_html()
        '<div><h1>Title</h1><p>This is <b>bold</b></p></div>'

    Note:
        This function ties together all the other modules:
        - Uses markdown_to_blocks() to split
        - Uses block_to_block_type() to classify
        - Uses text_to_textnodes() for inline parsing
        - Uses text_node_to_html_node() to convert to HTML
        - Builds tree with ParentNode and LeafNode
    """
    lines = markdown_to_blocks(md)
    html_nodes = []

    for line in lines:
        line_type = block_to_block_type(line)
        html_type = convert_line_type_to_html_tag(line_type, line)
        clean_line = handle_clean_line(line_type, line)

        if line_type == BlockType.CODE:
            text_node = TextNode(clean_line, TextType.TEXT)
            code_html = text_node_to_html_node(text_node)

            code_node = ParentNode(tag="code", children=[code_html])

            parent_node = ParentNode(tag=html_type, children=[code_node])
            html_nodes.append(parent_node)
        elif (
            line_type == BlockType.UNORDERED_LIST or line_type == BlockType.ORDERED_LIST
        ):
            inner_lines = line.splitlines()
            li_nodes = []

            for inner_line in inner_lines:
                cleaned_inner_line = clean_inner_line(inner_line)
                text_node_list = text_to_textnodes(cleaned_inner_line)
                children = []

                for text_node in text_node_list:
                    html_node = text_node_to_html_node(text_node)
                    children.append(html_node)

                li_node = ParentNode(tag="li", children=children)
                li_nodes.append(li_node)

            parent_node = ParentNode(tag=html_type, children=li_nodes)
            html_nodes.append(parent_node)
        else:
            text_node_list = text_to_textnodes(clean_line)
            children = []

            for text_node in text_node_list:
                html_node = text_node_to_html_node(text_node)
                children.append(html_node)

            parent_node = ParentNode(tag=html_type, children=children)
            html_nodes.append(parent_node)

    return ParentNode(tag="div", children=html_nodes)


if __name__ == "__main__":
    md = """
This is **bolded** paragraph text in a p tag here

This is another paragraph with _italic_ text and `code` here
    """
    print(markdown_to_html_node(md))
