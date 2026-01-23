import re
from textnode import *
from htmlnode import *

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if not isinstance(node, TextNode):
            raise Exception(f"{node} is not a TextNode")
        delim_count = node.text.count(delimiter)
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        elif delim_count == 0:
            new_nodes.append(node)
        elif delim_count % 2 == 0:
            chunks = node.text.split(delimiter)
            for idx, chunk in enumerate(chunks):
                if idx % 2 == 0:
                    new_nodes.append(TextNode(chunk,TextType.TEXT))
                else:
                    new_nodes.append(TextNode(chunk,text_type))    
        else:
            raise Exception(f"{node.text} is not valid Markdown syntax")
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    
def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
