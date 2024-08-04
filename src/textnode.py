# Imports
from project_types import TextType
from typing import Optional


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


def main():
    node = TextNode("hello", "text", "google.com")
    print(node)


if __name__ == "__main__":
    main()
