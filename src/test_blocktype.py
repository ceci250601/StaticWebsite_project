from blocktype import *

import unittest

class TestBlockToBlockType(unittest.TestCase):
    def test_heading_and_paragraph(self):
        self.assertEqual(block_to_block_type("# Titolo"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("Testo normale"), BlockType.PARAGRAPH)

    def test_lists(self):
        self.assertEqual(block_to_block_type("- a\n- b"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("1. a\n2. b"), BlockType.ORDERED_LIST)

    def test_quote_and_code(self):
        self.assertEqual(block_to_block_type("> citazione"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("```\ncodice\n```"), BlockType.CODE)


if __name__ == "__main__":
    unittest.main()