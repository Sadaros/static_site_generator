import unittest
from textnode import TextNode
from inline import (
    split_nodes_delimiter,
    extract_markdown_links,
    extract_markdown_images,
)


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_basic_functionality(self):
        node = TextNode("This is a `code block` here", "text")
        result = split_nodes_delimiter([node], "`", "code")
        self.assertEqual(
            result,
            [
                TextNode("This is a ", "text"),
                TextNode("code block", "code"),
                TextNode(" here", "text"),
            ],
        )

    def test_no_delimiter(self):
        node = TextNode("This is a regular text.", "text")
        result = split_nodes_delimiter([node], "`", "code")
        self.assertEqual(node, result[0])

    def test_multiple_same_delimiters(self):
        node = TextNode("Start `code1` middle `code2` end", "text")
        result = split_nodes_delimiter([node], "`", "code")
        self.assertEqual(
            result,
            [
                TextNode("Start ", "text"),
                TextNode("code1", "code"),
                TextNode(" middle ", "text"),
                TextNode("code2", "code"),
                TextNode(" end", "text"),
            ],
        )

    def test_unmatched_delimiter(self):
        node = TextNode("This is `unmatched delimiter", "text")
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", "code")

    def test_empty_string(self):
        node = TextNode("", "text")
        result = split_nodes_delimiter([node], "`", "code")
        self.assertEqual(result, [node])  # should return the same empty node

    def test_mixed_node_types(self):
        class SomeOtherNode:
            def __init__(self, text: str) -> None:
                self.text = text

        other_node = SomeOtherNode("Some other node")
        nodes = [
            TextNode("Text with `code` inside", "text"),
            other_node,  # assuming SomeOtherNode is another node type
        ]
        result = split_nodes_delimiter(nodes, "`", "code")  # type: ignore
        self.assertEqual(
            result,
            [
                TextNode("Text with ", "text"),
                TextNode("code", "code"),
                TextNode(" inside", "text"),
                other_node,
            ],
        )

    def test_delimiter_at_edges(self):
        node = TextNode("`code at start` and end `code`", "text")
        result = split_nodes_delimiter([node], "`", "code")
        self.assertEqual(
            result,
            [
                TextNode("code at start", "code"),
                TextNode(" and end ", "text"),
                TextNode("code", "code"),
            ],
        )

    def test_complex_unmatched_delimiter(self):
        node = TextNode("Start `code1 middle `code2` end", "text")
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", "code")


class TestMarkdownLinkImageExtractor(unittest.TestCase):
    def test_valid_link(self):
        link_tuple = extract_markdown_links(
            "This is a string, with a [link](google.com) in it"
        )
        result = [("link", "google.com")]
        self.assertEqual(link_tuple, result)

    def test_multiple_links(self):
        link_tuple = extract_markdown_links(
            "first [link](google.com), second [link2](yahoo.com)"
        )
        result = [("link", "google.com"), ("link2", "yahoo.com")]
        self.assertEqual(link_tuple, result)

    def test_valid_image(self):
        image_tuple = extract_markdown_images(
            "This is a string with an ![image](logo.png)"
        )
        result = [("image", "logo.png")]
        self.assertEqual(image_tuple, result)

    def test_invalid_image(self):
        test_case = extract_markdown_images("String with no image")
        result = []
        self.assertEqual(test_case, result)


if __name__ == "__main__":
    unittest.main()
