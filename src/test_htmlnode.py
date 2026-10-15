import unittest
from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_init_defaults(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_init_with_values(self):
        child = HTMLNode("span", "child")
        props = {"class": "box"}
        node = HTMLNode("div", "hello", [child], props)
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "hello")
        self.assertEqual(node.children, [child])
        self.assertEqual(node.props, props)

    def test_to_html_not_implemented(self):
        node = HTMLNode("p", "text")
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_props_to_html_none(self):
        node = HTMLNode("a", "link")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_empty_dict(self):
        node = HTMLNode("a", "link", props={})
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_single(self):
        node = HTMLNode("a", "link", props={"href": "https://example.com"})
        self.assertEqual(node.props_to_html(), ' href="https://example.com"')

    def test_props_to_html_multiple(self):
        node = HTMLNode(
            "a", "link",
            props={"href": "https://example.com", "target": "_blank"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' href="https://example.com" target="_blank"',
        )

    def test_repr(self):
        node = HTMLNode("p", "text", None, {"class": "x"})
        self.assertEqual(
            repr(node),
            "HTMLNode(tag=p, value=text, children=None, props={'class': 'x'})",
        )

    def test_repr_with_children(self):
        child = HTMLNode("b", "bold")
        node = HTMLNode("p", None, [child])
        self.assertIn("children=[HTMLNode(tag=b, value=bold", repr(node))

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_img(self):
        node = LeafNode("img", "", {"src": "image.jpg", "alt": "An image"})
        self.assertEqual(node.to_html(), '<img src="image.jpg" alt="An image"></img>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Just text")
        self.assertEqual(node.to_html(), "Just text") 

    def test_leaf_to_html_no_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_repr(self):
        node = LeafNode("p", "Hello", {"class": "text"})
        self.assertEqual(
            repr(node),
            "LeafNode(tag=p, value=Hello, props={'class': 'text'})",
        )

if __name__ == "__main__":
    unittest.main()