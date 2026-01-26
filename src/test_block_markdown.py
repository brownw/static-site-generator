import unittest

from block_markdown import *

class BlockMarkdownNode(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_extra_lines(self):
        md = """
This is a block.


Another block.
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is a block.",
                "Another block.",
            ],
        )

    def test_markdown_to_blocks_empty(self):
        md = """



"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [],
        )

class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### Level 3"), BlockType.HEADING)

    def test_code(self):
        self.assertEqual(block_to_block_type("```\ncode\n```"), BlockType.CODE)

    def test_quote(self):
        self.assertEqual(block_to_block_type("> quote\n> more"), BlockType.QUOTE)

    def test_ordered_list(self):
        self.assertEqual(block_to_block_type("1. item\n2. item"), BlockType.ORDERED_LIST)

    def test_paragraph(self):
        self.assertEqual(block_to_block_type("Just a normal block of text."), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()