# Imports
from project_types import TextType
from typing import Optional
from htmlnode import LeafNode


class TextNode:
    def __init__(
        self, text: str, text_type: TextType, url: Optional[str] = None
    ) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, target: "TextNode") -> bool:  # type: ignore
        return (
            self.text == target.text
            and self.text_type == target.text_type
            and self.url == target.url
        )

    def __repr__(self) -> str:
        return f'TextNode("{self.text}", {self.text_type}, {self.url})'


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    if text_node.text_type == "text":
        return LeafNode(text_node.text)
    if text_node.text_type == "bold":
        return LeafNode(text_node.text, "b")
    if text_node.text_type == "italic":
        return LeafNode(text_node.text, "i")
    if text_node.text_type == "code":
        return LeafNode(text_node.text, "code")

    if text_node.url:
        if text_node.text_type == "link":
            return LeafNode(text_node.text, "a", {"href": text_node.url})
        if text_node.text_type == "image":
            return LeafNode("", "img", {"src": text_node.url, "alt": text_node.text})

    raise ValueError(f"{repr(text_node)} is an invalid TextNode")


def main():
    node = TextNode("hello", "text", "google.com")
    print(node)


if __name__ == "__main__":
    main()
