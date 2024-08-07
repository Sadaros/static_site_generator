import unittest

from textnode import TextNode, text_node_to_html_node
from htmlnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_un_eq_url(self):
        node = TextNode("Text", "text", "google.com")
        node2 = TextNode("Text", "text", "bing.com")
        self.assertNotEqual(node, node2)

    def test_un_eq_type(self):
        node = TextNode("Test", "text")
        node2 = TextNode("Test", "bold")
        self.assertNotEqual(node, node2)


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_valid_text_type(self):
        text_node = TextNode("TestCase", "text")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node, LeafNode("TestCase"))

    def test_invalid_text_type(self):
        with self.assertRaises(ValueError):
            node = TextNode(" ", "invalid")  # type: ignore
            text_node_to_html_node(node)

    def test_valid_link(self):
        text_node = TextNode("A link", "link", "google.com")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node, LeafNode("A link", "a", {"href": "google.com"}))

    def test_missing_url(self):
        with self.assertRaises(ValueError):
            node = TextNode("link text", "link", "")
            text_node_to_html_node(node)

    def test_valid_image(self):
        text_node = TextNode("alt text", "image", "cool_image.png")
        html_node = LeafNode("", "img", {"src": "cool_image.png", "alt": "alt text"})
        self.assertEqual(html_node, text_node_to_html_node(text_node))


if __name__ == "__main__":
    unittest.main()
