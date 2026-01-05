class HTMLNode:
    """
    Base class representing an HTML node in a tree structure.

    Do not instantiate directly. Use LeafNode or ParentNode instead.

    Attributes:
        tag (str): HTML tag name
        value (str): Text value
        children (list): Child nodes
        props (dict): HTML attributes
    """

    def __init__(self, tag=None, value=None, children=None, props=None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        """Must be overridden by subclasses."""
        raise NotImplementedError("Subclasses of HTMLNode must implement to_html()")

    def props_to_html(self) -> str:
        """
        Converts props dict to HTML attributes string.

        Returns:
            str: Formatted as ' key="value" key2="value2"'

        Example:
            >>> node.props = {"href": "https://google.com"}
            >>> node.props_to_html()
            ' href="https://google.com"'
        """
        result = ""
        if self.props is None or not self.props:
            return result
        for key, value in self.props.items():
            result += f' {key}="{value}"'
        return result

    def __repr__(self) -> str:
        return f"Tag: {self.tag}; Value:{self.value}; Children:{self.children}; props:{self.props}"


class LeafNode(HTMLNode):
    """
    HTML node with no children (leaf in the tree).

    Args:
        tag (str): HTML tag (None for plain text)
        value (str): Required text value
        props (dict): Optional HTML attributes

    Example:
        >>> LeafNode("p", "Hello").to_html()
        '<p>Hello</p>'
        >>> LeafNode(None, "Text").to_html()
        'Text'
    """

    def __init__(self, tag, value, props=None) -> None:
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self) -> str:
        """
        Convert this leaf node to an HTML string.

        If the node has no tag, it returns only the raw value.
        Otherwise it wraps the value in an opening and closing tag
        and includes any HTML properties.

        Returns:
            str: The HTML representation of this node.

        Raises:
            ValueError: If the node's value is None.
        """
        if self.value is None:
            raise ValueError("invalid HTML: no value")

        if self.tag is None:
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    """
    HTML node containing child nodes.

    Args:
        tag (str): Required HTML tag
        children (list): Required list of child nodes
        props (dict): Optional HTML attributes

    Example:
        >>> parent = ParentNode("div", [LeafNode("p", "Text")])
        >>> parent.to_html()
        '<div><p>Text</p></div>'
    """

    def __init__(self, tag, children, props=None) -> None:
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        """
        Converts parent node and all children to HTML.

        Returns:
            str: HTML with nested children

        Raises:
            ValueError: If tag or children are missing

        Note:
            Recursively calls to_html() on all children.
        """
        if not self.tag or self.tag == "":
            raise ValueError("Must have tag")

        if not self.children:
            raise ValueError("Must have children value")

        children_html = ""
        for child in self.children:
            child_html = child.to_html()
            children_html += child_html
        prop_str = self.props_to_html()

        return f"<{self.tag}{prop_str}>{children_html}</{self.tag}>"
