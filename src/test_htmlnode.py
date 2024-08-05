import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    pass  # Made HTMLNode an Abstract class


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

    def test_props_empty(self):
        node = LeafNode("no props")
        test_case = ""
        self.assertEqual(node.props_to_html(), test_case)

    def test_to_html(self):
        node = LeafNode("TestString", "h1", {"class": "heading"})
        test_case = '<h1 class="heading">TestString</h1>'
        self.assertEqual(node.to_html(), test_case)

    def test_to_html_exception(self):
        node = LeafNode(None)  # type: ignore
        self.assertRaises(ValueError, node.to_html)

    def test_to_html_no_props(self):
        node = LeafNode("No props", "p")
        test_case = "<p>No props</p>"
        self.assertEqual(node.to_html(), test_case)

    def test_to_html_no_tag(self):
        node = LeafNode("No tags")
        test_case = "No tags"
        self.assertEqual(node.to_html(), test_case)


class TestParentNode(unittest.TestCase):
    def test_eq(self):
        node = ParentNode([LeafNode("TestCase", "p")], "div")
        node2 = ParentNode([LeafNode("TestCase", "p")], "div")
        self.assertEqual(node, node2)

    def test_repr(self):
        node = ParentNode([LeafNode("test", "p"), LeafNode("case", "p")], "div")
        self.assertEqual(
            repr(node),
            'ParentNode(tag = div, value = None, children = [LeafNode(p, "test", None, None), LeafNode(p, "case", None, None)], None)',
        )

    def test_props_to_html(self):
        node = ParentNode(
            [LeafNode("test")],
            "ul",
            {"class": "list", "style": "color:red"},
        )
        self.assertEqual(node.props_to_html(), ' class="list" style="color:red"')

    def test_to_html(self):
        list_of_nodes: list[LeafNode | ParentNode] = [
            LeafNode("first", "li"),
            LeafNode("second", "li"),
        ]
        node = ParentNode(
            list_of_nodes, "ul", {"class": "list", "style": "bg-color:red"}
        )
        self.assertEqual(
            node.to_html(),
            '<ul class="list" style="bg-color:red"><li>first</li><li>second</li></ul>',
        )

    def test_to_html_nested(self):
        leaf_node = LeafNode("test", "p")
        parent_nodes: list[LeafNode | ParentNode] = [
            ParentNode("div", [leaf_node]),
            ParentNode("div", [ParentNode("div", [leaf_node])]),
        ]
        node = ParentNode("span", parent_nodes)
        self.assertEqual(
            node.to_html(),
            "<span><div><p>test</p></div><div><div><p>test</p></div></div></span>",
        )


class TestParentNodeEdgeCases(unittest.TestCase):
    def test_empty_tag(self):
        with self.assertRaises(ValueError):
            node = ParentNode("", [LeafNode("Test", "p")])  # type: ignore
            node.to_html()

    def test_no_children(self):
        with self.assertRaises(ValueError):
            node = ParentNode("div", [])  # type: ignore
            node.to_html()

    def test_invalid_children(self):
        class NotAnHTMLNode:
            pass

        with self.assertRaises(TypeError):
            node = ParentNode("div", [NotAnHTMLNode()])  # type: ignore
            node.to_html()

    def test_deeply_nested_parent_node(self):
        nested_child = LeafNode("deep text", "p")
        for _ in range(100):  # Testing deep nesting
            nested_child = ParentNode("div", [nested_child])
        node = ParentNode("span", [nested_child])
        self.assertTrue(node.to_html().startswith("<span>"))

    def test_special_chars_in_props(self):
        node = ParentNode(
            "div",
            [LeafNode("test", "p")],
            {"data-info": "some<>info", "style": "color: red;"},
        )
        self.assertEqual(
            node.to_html(),
            '<div data-info="some&lt;&gt;info" style="color: red;"><p>test</p></div>',
        )


if __name__ == "__main__":
    unittest.main()
