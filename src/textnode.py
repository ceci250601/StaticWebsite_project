from enum import Enum
import re

from htmlnode import *
from blocktype import *

class TextType(Enum):
    PLAIN = "text/plain"
    BOLD = "text/bold"
    ITALIC = "text/italic"
    CODE = "text/code"
    LINK = "text/link"
    IMAGE = "text/image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return False
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    if text_node.text_type == TextType.PLAIN:
        return LeafNode(tag=None, value=text_node.text)

    elif text_node.text_type == TextType.BOLD:
        return LeafNode(tag="b", value=text_node.text)

    elif text_node.text_type == TextType.ITALIC:
        return LeafNode(tag="i", value=text_node.text)

    elif text_node.text_type == TextType.CODE:
        return LeafNode(tag="code", value=text_node.text)

    elif text_node.text_type == TextType.LINK:
        return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})

    elif text_node.text_type == TextType.IMAGE:
        return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})

    else:
        raise Exception(f"Unsupported text type: {text_node.text_type}")

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return [(alt, url) for alt, url in matches]

def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return [(text, url) for text, url in matches]

def markdown_to_blocks(markdown):
    markdown_splitted = markdown.split("\n\n")

    return [block.strip() for block in markdown_splitted if block.strip()]    

def text_to_children(text):
    text_nodes = text_to_textnodes(text)  
    return [text_node_to_html_node(tn) for tn in text_nodes]


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        block_type = block_to_block_type(block)

        match block_type:
            case BlockType.PARAGRAPH:
                text = " ".join(block.split("\n"))
                node = ParentNode("p", text_to_children(text))

            case BlockType.HEADING:
                level = len(block) - len(block.lstrip("#"))
                text = block[level:].strip()
                node = ParentNode(f"h{level}", text_to_children(text))

            case BlockType.CODE:
                content = block[3:-3].lstrip("\n")
                code = text_node_to_html_node(TextNode(content, TextType.CODE))
                node = ParentNode("pre", [code])

            case BlockType.QUOTE:
                lines = [line.lstrip(">").strip() for line in block.split("\n")]
                node = ParentNode("blockquote", text_to_children(" ".join(lines)))

            case BlockType.UNORDERED_LIST:
                items = [line[2:] for line in block.split("\n")]
                node = ParentNode("ul", [ParentNode("li", text_to_children(i)) for i in items])

            case BlockType.ORDERED_LIST:
                items = [line.split(". ", 1)[1] for line in block.split("\n")]
                node = ParentNode("ol", [ParentNode("li", text_to_children(i)) for i in items])

        children.append(node)

    return ParentNode("div", children)

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue
        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise ValueError(f"Invalid markdown: unclosed delimiter '{delimiter}'")
        for i, part in enumerate(parts):
            if part == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.PLAIN))
            else:
                new_nodes.append(TextNode(part, text_type))
    return new_nodes

def split_nodes_image(old_nodes: list[TextNode]):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue
        matches = extract_markdown_images(node.text)
        if not matches:
            new_nodes.append(node)
            continue
        last_index = 0
        for alt, url in matches:
            start_index = node.text.find(f"![{alt}]({url})", last_index)
            if start_index > last_index:
                new_nodes.append(TextNode(node.text[last_index:start_index], TextType.PLAIN))
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
            last_index = start_index + len(f"![{alt}]({url})")
        if last_index < len(node.text):
            new_nodes.append(TextNode(node.text[last_index:], TextType.PLAIN))
    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue
        matches = extract_markdown_links(node.text)
        if not matches:
            new_nodes.append(node)
            continue
        last_index = 0
        for text, url in matches:
            start_index = node.text.find(f"[{text}]({url})", last_index)
            if start_index > last_index:
                new_nodes.append(TextNode(node.text[last_index:start_index], TextType.PLAIN))
            new_nodes.append(TextNode(text, TextType.LINK, url))
            last_index = start_index + len(f"[{text}]({url})")
        if last_index < len(node.text):
            new_nodes.append(TextNode(node.text[last_index:], TextType.PLAIN))
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.PLAIN)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def extract_title(markdown):
    lines = markdown.splitlines()
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    return None