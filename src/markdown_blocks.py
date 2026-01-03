from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    str_list = []

    temp_list = markdown.split("\n\n")
    for item in temp_list:
        new_item = item.strip()
        if new_item != "":
            str_list.append(new_item)

    return str_list


def is_unordered_list(lines):
    for line in lines:
        if not line.startswith("- "):
            return False
    return True


def is_ordered_list(lines):
    for index, line in enumerate(lines):
        expected_prefix = f"{index + 1}. "
        if not line.startswith(expected_prefix):
            return False
    return True


def block_to_block_type(md_txt_block):
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


# if __name__ == "__main__":
#     pass
