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
                    if chunk != "":
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

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if not isinstance(node, TextNode):
            raise Exception(f"{node} is not a TextNode")
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        original_text = node.text
        images = extract_markdown_images(node.text)

        if not images:
            new_nodes.append(node)
            continue
    
        for image in images:
            image_alt, image_url = image
            sections = original_text.split(f"![{image_alt}]({image_url})", 1)
            
            if len(sections) != 2:
                   raise ValueError("Invalid markdown, image section not found")
            
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0],TextType.TEXT))
            
            new_nodes.append(TextNode(image_alt,TextType.IMAGE,image_url))
            original_text = sections[1]
        
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if not isinstance(node, TextNode):
            raise Exception(f"{node} is not a TextNode")
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        original_text = node.text
        links = extract_markdown_links(node.text)

        if not links:
            new_nodes.append(node)
            continue
    
        for link in links:
            link_text, link_url = link
            sections = original_text.split(f"[{link_text}]({link_url})", 1)
            
            if len(sections) != 2:
                   raise ValueError("Invalid markdown, link section not found")
            
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0],TextType.TEXT))
            
            new_nodes.append(TextNode(link_text,TextType.LINK,link_url))
            original_text = sections[1]
        
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    start = TextNode(text, TextType.TEXT)
    new_nodes = split_nodes_delimiter([start], '**', TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    return new_nodes