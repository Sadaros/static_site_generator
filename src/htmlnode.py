from typing import Optional
from project_types import HTMLTag


class HTMLNode:
    def __init__(
        self,
        tag: Optional[HTMLTag] = None,
        value: Optional[str] = None,
        children: Optional[list["HTMLNode"]] = None,
        props: Optional[dict[str, str]] = None,
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __eq__(self, target: "HTMLNode") -> bool:  # type: ignore
        return (
            self.tag == target.tag
            and self.value == target.value
            and self.children == target.children
            and self.props == target.props
        )

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.tag}, "{self.value}", {self.children}, {self.props})'

    def to_html(self) -> Exception | str:
        raise NotImplementedError

    def props_to_html(self) -> str:
        if self.props is None or not self.props:
            return ""
        props_string: str = ""
        for k, v in self.props.items():
            props_string += f' {k}="{v}"'
        return props_string


class LeafNode(HTMLNode):
    def __init__(
        self,
        value: str,
        tag: Optional[HTMLTag] = None,
        props: Optional[dict[str, str]] = None,
    ) -> None:
        super().__init__(tag, value, None, props)
        self.children = []

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("All LeafNodes must have a Value")
        if self.tag is None:
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
