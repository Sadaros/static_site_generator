import unittest
from project_types import HTMLTag, TextType
from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode(
            "div",
            "Test string",
            [HTMLNode("a", "link", None, {"href": "google.com", "target": "_blank"})],
        )
        node2 = HTMLNode(
            "div",
            "Test string",
            [HTMLNode("a", "link", None, {"href": "google.com", "target": "_blank"})],
        )
        self.assertEqual(node, node2)

    def test_repr(self):
        node = HTMLNode("p", "Test String", None, {"class": "bold"})
        repr_test = "HTMLNode(p, \"Test String\", None, {'class': 'bold'})"
        self.assertEqual(repr(node), repr_test)

    def test_props_to_html(self):
        node = HTMLNode(props={"href": "google.com", "target": "_blank"})
        test_case = ' href="google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), test_case)

    def test_props_empty(self):
        node = HTMLNode()
        test_case = ""
        self.assertEqual(node.props_to_html(), test_case)

    def test_to_html(self):
        node = HTMLNode()
        self.assertRaises(NotImplementedError, node.to_html)


class TestLeafNode(unittest.TestCase):
    def test_eq(self):
        node = LeafNode("Test", "p")
        node2 = LeafNode("Test", "p")
        self.assertEqual(node, node2)

    def test_repr(self):
        node = LeafNode("test", "a", {"href": "google.com"})
        test_case = "LeafNode(a, \"test\", [], {'href': 'google.com'})"
        self.assertEqual(repr(node), test_case)

    def test_props_to_html(self):
        node = LeafNode("test", props={"href": "google.com", "target": "_blank"})
        test_case = ' href="google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), test_case)

    def 


if __name__ == "__main__":
    unittest.main()
