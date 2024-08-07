from abc import ABC, abstractmethod
from typing import Optional, Sequence
from project_types import HTMLTag
import html


class HTMLNode(ABC):
    def __init__(
        self,
        tag: Optional[HTMLTag] = None,
        value: Optional[str] = None,
        children: Optional[Sequence["ParentNode | LeafNode | HTMLNode"]] = None,
        props: Optional[dict[str, str]] = None,
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __eq__(self, target: object) -> bool:
        if not isinstance(target, HTMLNode):
            return False
        return (
            self.tag == target.tag
            and self.value == target.value
            and self.children == target.children
            and self.props == target.props
        )

    def __repr__(self) -> str:
        repr_value = f'"{self.value}"' if self.value is not None else "None"
        return f"{self.__class__.__name__}({self.tag}, {repr_value}, {self.children}, {self.props})"

    @abstractmethod
    def to_html(self) -> str:
        raise NotImplementedError

    def props_to_html(self) -> str:
        if self.props is None or not self.props:
            return ""
        props_string: str = ""
        for k, v in self.props.items():
            props_string += f' {k}="{str(html.escape(v))}"'
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


class ParentNode(HTMLNode):
    def __init__(
        self,
        children: Sequence["ParentNode | LeafNode"],
        tag: HTMLTag,
        props: Optional[dict[str, str]] = None,
    ) -> None:
        super().__init__(tag, None, children, props)
        self.value = None

    def to_html(self) -> str:
        if not self.tag:
            raise ValueError("All ParentNodes must have a tag")
        if not self.children:
            raise ValueError("All ParentNode must have children")

        html_props = self.props_to_html()
        output = f"<{self.tag}{html_props}>"
        for node in self.children:
            if not isinstance(node, HTMLNode):  # type: ignore
                raise TypeError(f"{repr(node)} is not a valid type for child list")
            output += node.to_html()
        output += f"</{self.tag}>"
        return output
