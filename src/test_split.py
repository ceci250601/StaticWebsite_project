import unittest
from textnode import *

class TestSplitNodesDelimiter(unittest.TestCase):
    # ---------- delimitatori ----------
    def test_code(self):
        node = TextNode("This is text with a `code block` word", TextType.PLAIN)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, [
            TextNode("This is text with a ", TextType.PLAIN),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.PLAIN),
        ])

    def test_bold(self):
        node = TextNode("Hello **world** again", TextType.PLAIN)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [
            TextNode("Hello ", TextType.PLAIN),
            TextNode("world", TextType.BOLD),
            TextNode(" again", TextType.PLAIN),
        ])

    def test_italic(self):
        node = TextNode("an _italic_ word", TextType.PLAIN)
        result = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(result, [
            TextNode("an ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.PLAIN),
        ])

    def test_no_delimiter(self):
        node = TextNode("plain text", TextType.PLAIN)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, [node])

    def test_delimiter_at_start(self):
        node = TextNode("`code` at start", TextType.PLAIN)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, [
            TextNode("code", TextType.CODE),
            TextNode(" at start", TextType.PLAIN),
        ])

    def test_delimiter_at_end(self):
        node = TextNode("at end `code`", TextType.PLAIN)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, [
            TextNode("at end ", TextType.PLAIN),
            TextNode("code", TextType.CODE),
        ])

    def test_multiple_delimited(self):
        node = TextNode("`a` and `b`", TextType.PLAIN)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, [
            TextNode("a", TextType.CODE),
            TextNode(" and ", TextType.PLAIN),
            TextNode("b", TextType.CODE),
        ])

    def test_non_text_node_unchanged(self):
        node = TextNode("already bold", TextType.BOLD)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, [node])

    def test_multiple_nodes(self):
        nodes = [
            TextNode("a `b` c", TextType.PLAIN),
            TextNode("bold", TextType.BOLD),
            TextNode("`d`", TextType.PLAIN),
        ]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(result, [
            TextNode("a ", TextType.PLAIN),
            TextNode("b", TextType.CODE),
            TextNode(" c", TextType.PLAIN),
            TextNode("bold", TextType.BOLD),
            TextNode("d", TextType.CODE),
        ])

    def test_unclosed_delimiter_raises(self):
        node = TextNode("This is `broken", TextType.PLAIN)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_unclosed_delimiter_message(self):
        node = TextNode("This is `broken", TextType.PLAIN)
        with self.assertRaisesRegex(ValueError, "`"):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_empty_list(self):
        self.assertEqual(split_nodes_delimiter([], "`", TextType.CODE), [])

    # ---------- immagini ----------
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_images_none(self):
        node = TextNode("No images here", TextType.PLAIN)
        self.assertListEqual([node], split_nodes_image([node]))

    def test_split_images_at_start_and_end(self):
        node = TextNode("![a](https://x.com/a.png) middle ![b](https://x.com/b.png)", TextType.PLAIN)
        self.assertListEqual(
            [
                TextNode("a", TextType.IMAGE, "https://x.com/a.png"),
                TextNode(" middle ", TextType.PLAIN),
                TextNode("b", TextType.IMAGE, "https://x.com/b.png"),
            ],
            split_nodes_image([node]),
        )

    def test_split_images_trailing_text(self):
        node = TextNode("![a](https://x.com/a.png) tail", TextType.PLAIN)
        self.assertListEqual(
            [
                TextNode("a", TextType.IMAGE, "https://x.com/a.png"),
                TextNode(" tail", TextType.PLAIN),
            ],
            split_nodes_image([node]),
        )

    def test_split_images_non_plain_unchanged(self):
        node = TextNode("![a](https://x.com/a.png)", TextType.BOLD)
        self.assertListEqual([node], split_nodes_image([node]))

    def test_split_images_multiple_nodes(self):
        nodes = [
            TextNode("one ![a](https://x.com/a.png)", TextType.PLAIN),
            TextNode("two", TextType.PLAIN),
        ]
        self.assertListEqual(
            [
                TextNode("one ", TextType.PLAIN),
                TextNode("a", TextType.IMAGE, "https://x.com/a.png"),
                TextNode("two", TextType.PLAIN),
            ],
            split_nodes_image(nodes),
        )

    def test_split_images_empty_list(self):
        self.assertListEqual([], split_nodes_image([]))

    # ---------- link ----------
    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://example.com) and another [second link](https://example.org)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode("second link", TextType.LINK, "https://example.org"),
            ],
            new_nodes,
        )

    def test_split_links_none(self):
        node = TextNode("No links here", TextType.PLAIN)
        self.assertListEqual([node], split_nodes_link([node]))

    def test_split_links_at_start_and_end(self):
        node = TextNode("[a](https://a.com) middle [b](https://b.com)", TextType.PLAIN)
        self.assertListEqual(
            [
                TextNode("a", TextType.LINK, "https://a.com"),
                TextNode(" middle ", TextType.PLAIN),
                TextNode("b", TextType.LINK, "https://b.com"),
            ],
            split_nodes_link([node]),
        )

    def test_split_links_trailing_text(self):
        node = TextNode("see [a](https://a.com) now", TextType.PLAIN)
        self.assertListEqual(
            [
                TextNode("see ", TextType.PLAIN),
                TextNode("a", TextType.LINK, "https://a.com"),
                TextNode(" now", TextType.PLAIN),
            ],
            split_nodes_link([node]),
        )

    def test_split_links_ignores_images(self):
        node = TextNode("![img](https://x.com/a.png) and [link](https://a.com)", TextType.PLAIN)
        result = split_nodes_link([node])
        self.assertIn(TextNode("link", TextType.LINK, "https://a.com"), result)
        self.assertNotIn(TextNode("img", TextType.LINK, "https://x.com/a.png"), result)

    def test_split_links_non_plain_unchanged(self):
        node = TextNode("[a](https://a.com)", TextType.ITALIC)
        self.assertListEqual([node], split_nodes_link([node]))

    # ---------- text_to_textnodes ----------
    def test_text_to_textnodes_full(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        self.assertListEqual(
            [
                TextNode("This is ", TextType.PLAIN),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.PLAIN),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.PLAIN),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.PLAIN),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            text_to_textnodes(text),
        )

    def test_text_to_textnodes_plain(self):
        self.assertListEqual(
            [TextNode("just plain text", TextType.PLAIN)],
            text_to_textnodes("just plain text"),
        )

    def test_text_to_textnodes_only_bold(self):
        self.assertListEqual(
            [TextNode("bold", TextType.BOLD)],
            text_to_textnodes("**bold**"),
        )

    def test_text_to_textnodes_adjacent_formats(self):
        self.assertListEqual(
            [
                TextNode("a", TextType.BOLD),
                TextNode("b", TextType.ITALIC),
                TextNode("c", TextType.CODE),
            ],
            text_to_textnodes("**a**_b_`c`"),
        )

    def test_text_to_textnodes_unclosed_raises(self):
        with self.assertRaises(ValueError):
            text_to_textnodes("This is **broken")


if __name__ == "__main__":
    unittest.main()