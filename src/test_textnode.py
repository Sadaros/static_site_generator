import unittest

from textnode import TextNode


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


if __name__ == "__main__":
    unittest.main()
