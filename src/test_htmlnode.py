import unittest

from htmlnode import *


class TestHTMLNode(unittest.TestCase):
    def test_no_props(self):
        node = HTMLNode("H1","test")
        self.assertEqual(node.props_to_html(),"")
    
    def test_empty_props(self):
        node = HTMLNode("H1","test",props={})
        self.assertEqual(node.props_to_html(),"")

    def test_multiple_props(self):
        node = HTMLNode("H1","test",props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(),' href="https://www.google.com" target="_blank"')

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    def test_bold_to_html_b(self):
        node = LeafNode("b", "Hello, world!")
        self.assertEqual(node.to_html(),"<b>Hello, world!</b>")
    def test_link_to_html_a(self):
        node = LeafNode("a", "Hello, world!", props={"href": "https://www.google.com"})
        self.assertEqual(node.to_html(),'<a href="https://www.google.com">Hello, world!</a>')

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )


if __name__ == "__main__":
    unittest.main()