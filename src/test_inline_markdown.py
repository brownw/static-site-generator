import unittest

from inline_markdown import *
from textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_no_delimiter(self):
        # Test with no delimiters in the text
        old_nodes = [TextNode("This is plain text", TextType.TEXT)]
        result = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        expected = [TextNode("This is plain text", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_even_delimiters(self):
        # Test with even number of delimiters
        old_nodes = [TextNode("This is **bold** text", TextType.TEXT)]
        result = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_odd_delimiters(self):
        # Test with odd number of delimiters, should raise exception
        old_nodes = [TextNode("This is **bold text", TextType.TEXT)]
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        self.assertIn("is not valid Markdown syntax", str(context.exception))

    def test_non_text_node(self):
        # Test with a node that is not TextNode, should raise exception
        old_nodes = [TextNode("text", TextType.BOLD)]  # This is TextNode, but type is BOLD
        # Wait, the check is if not isinstance(node, TextNode), but all are TextNode
        # The function checks if node.type != TextType.TEXT, then appends as is
        # To test non-TextNode, I need something else, but since all are TextNode, perhaps create a mock or just test the type check
        # Actually, the code assumes all are TextNode, but to test, I can pass a list with non-TextNode
        # But in Python, I can pass anything, but since it's typed, perhaps use a different object
        old_nodes = ["not a node"]
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        self.assertIn("is not a TextNode", str(context.exception))

    def test_non_text_type_node(self):
        # Test with a node that has type other than TEXT, should append unchanged
        old_nodes = [TextNode("already bold", TextType.BOLD)]
        result = split_nodes_delimiter(old_nodes, "**", TextType.ITALIC)
        expected = [TextNode("already bold", TextType.BOLD)]
        self.assertEqual(result, expected)

    def test_multiple_nodes(self):
        # Test with multiple nodes
        old_nodes = [
            TextNode("Plain text", TextType.TEXT),
            TextNode("**bold**", TextType.TEXT),
            TextNode("more text", TextType.TEXT)
        ]
        result = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        expected = [
            TextNode("Plain text", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode("more text", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_delimiter_at_start(self):
        # Test delimiter at the beginning
        old_nodes = [TextNode("**bold** text", TextType.TEXT)]
        result = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_delimiter_at_end(self):
        # Test delimiter at the end
        old_nodes = [TextNode("text **bold**", TextType.TEXT)]
        result = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        expected = [
            TextNode("text ", TextType.TEXT),
            TextNode("bold", TextType.BOLD)
        ]
        self.assertEqual(result, expected)

    def test_multiple_delimiters(self):
        # Test multiple pairs of delimiters
        old_nodes = [TextNode("**bold** and **more**", TextType.TEXT)]
        result = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("more", TextType.BOLD)
        ]
        self.assertEqual(result, expected)

    def test_different_delimiter(self):
        # Test with different delimiter, like for italic
        old_nodes = [TextNode("This is *italic* text", TextType.TEXT)]
        result = split_nodes_delimiter(old_nodes, "*", TextType.ITALIC)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                   "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                   "link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_text_to_textnodes(self):
        text = \
        "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.maxDiff = None
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )
    
    def test_plain_text_only(self):
        text = "plain text only"
        new_nodes = text_to_textnodes(text)
        self.maxDiff = None
        self.assertListEqual(
            [
                TextNode("plain text only", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_italic_bold_code(self):
        text = "Some _italic_ and **bold** and `code`"
        new_nodes = text_to_textnodes(text)
        self.maxDiff = None
        self.assertListEqual(
            [
                TextNode("Some ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" and ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("code", TextType.CODE)
            ],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()