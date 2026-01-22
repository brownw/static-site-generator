import unittest

from htmlnode import HTMLNode


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

if __name__ == "__main__":
    unittest.main()