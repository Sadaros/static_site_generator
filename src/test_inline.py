import unittest
from textnode import TextNode
from inline import split_nodes_delimiter


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
