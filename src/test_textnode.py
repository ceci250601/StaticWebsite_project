import unittest
from textnode import *


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_url_none(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertIsNone(node.url)

    def test_text_type_different(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)


def test_text(self):
    node = TextNode("This is a text node", TextType.TEXT)
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, None)
    self.assertEqual(html_node.value, "This is a text node")

def test_extract_markdown_images(self):
    matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
    )
    self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

def test_basic(self):
    md = "# Titolo\n\nParagrafo\n\n- item 1\n- item 2"
    self.assertEqual(
        markdown_to_blocks(md),
        ["# Titolo", "Paragrafo", "- item 1\n- item 2"],
    )

def test_strips_and_ignores_empty_blocks(self):
    md = "\n\n  Blocco 1  \n\n\n\n\nBlocco 2\n\n"
    self.assertEqual(markdown_to_blocks(md), ["Blocco 1", "Blocco 2"])

def test_empty_string(self):
    self.assertEqual(markdown_to_blocks(""), [])

def test_paragraphs(self):
    md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
        html,
        "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
    )


def test_codeblock(self):
    md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
        html,
        "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
    )

def test_basic_title(self):
    self.assertEqual(extract_title("# Hello"), "Hello")

def test_title_not_on_first_line(self):
    md = "Testo iniziale\n\n# Titolo\n\nAltro testo"
    self.assertEqual(extract_title(md), "Titolo")

def test_no_title(self):
    self.assertIsNone(extract_title("## Sottotitolo\n\nSolo testo"))

if __name__ == "__main__":
    unittest.main()