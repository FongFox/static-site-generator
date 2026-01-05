from enum import Enum


class TextType(Enum):
    """
    Enum for text node types.

    Values:
        TEXT: Plain text
        BOLD: Bold text
        ITALIC: Italic text
        LINK: Hyperlink
        IMAGE: Image
        CODE: Inline code
    """

    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    LINK = "link"
    IMAGE = "image"
    CODE = "code"


class TextNode:
    """
    Represents a piece of text with a specific type and optional URL.

    Args:
        text (str): Text content
        text_type (TextType): Type of text
        url (str, optional): URL for LINK/IMAGE types

    Example:
        >>> node = TextNode("Hello", TextType.BOLD)
        >>> node2 = TextNode("Click", TextType.LINK, "https://google.com")
    """

    def __init__(self, text, text_type, url=None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other) -> bool:
        """Compares two TextNodes for equality."""
        if not isinstance(other, TextNode):
            return False
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
