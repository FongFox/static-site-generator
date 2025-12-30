class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("Subclasses of HTMLNode must implement to_html()")

    def props_to_html(self) -> str:
        result = ""
        if self.props is None or not self.props:
            return result
        for key, value in self.props.items():
            result += f' {key}="{value}"'
        return result

    def __repr__(self) -> str:
        return f"Tag: {self.tag}; Value:{self.value}; Children:{self.children}; props:{self.props}"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None) -> None:
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self) -> str:
        if not self.value or self.value == "":
            raise ValueError("LeafNode must have a value")

        if not self.tag or self.tag == "":
            # return f"{self.value}"
            return str(self.value)

        # return f"<{self.tag}>{self.value}</{self.tag}>"
        props_str = self.props_to_html()
        return f"<{self.tag}{props_str}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None) -> None:
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if not self.tag or self.tag == "":
            raise ValueError("Must have tag")

        if not self.children:
            raise ValueError("Must have children value")

        children_html = ""
        for child in self.children:
            child_html = child.to_html()
            children_html += child_html
        prop_str = self.props_to_html()

        return f"<{self.tag}{prop_str}>{child_html}</{self.tag}>"
