from enum import Enum
from htmlnode import *
from inline_markdown import text_to_textnodes
from textnode import *
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    raw_blocks = markdown.split("\n\n")
    blocks = []
    for block in raw_blocks:
        if block != "":
            blocks.append(block.strip())
    return blocks

def block_to_block_type(block):
    if re.match(r"^#{1,6}\s.+", block):
       return BlockType.HEADING
    elif re.match(r"^```\n[\s\S]*?^```", block,re.MULTILINE):
        return BlockType.CODE
    elif re.match(r"^(?:>\s.*\n?)+", block):
        return BlockType.QUOTE
    elif re.match(r"^(?:-\s.*\n?)+", block):
        return BlockType.UNORDERED_LIST
    elif re.match(r"^1\.\s.*\n(?:(?:\d+)\.\s.*\n?)*", block):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH

def text_to_children(text):
    children = []
    text_nodes = text_to_textnodes(text)
    for tn in text_nodes:
        child = text_node_to_html_node(tn)
        children.append(child)
    return children

def count_leading(text, match_char):
    count = 0
    for char in text:
        if char == match_char:
            count += 1
        else:
            break
    return count

def strip_ordered_marker(line):
    line = line.lstrip()
    match = re.match(r"\d+\.\s+(.*)", line)
    if match:
        return match.group(1)
    return line

def strip_unordered_marker(line):
    line = line.lstrip()
    if line.startswith("- "):
        return line[2:]
    return line

def list_block_to_children(block, ordered):
    lines = block.split("\n")
    li_nodes = []
    for line in lines:
        if not line:
            continue
        if ordered:
            stripped = strip_ordered_marker(line)
            children = text_to_children(stripped)
            li_nodes.append(HTMLNode("li", children=children))
        else:
            stripped = strip_ordered_marker(line)
            children = text_to_children(stripped)
            li_nodes.append(HTMLNode("li", children=children))
    return li_nodes


def code_block_to_html(block):
    lines = block.split("\n")

    if lines and lines[0].strip() == "```":
        lines = lines[1:]

    if lines and lines[-1].strip() == "```":
        lines = lines[:-1]

    inner_text = "\n".join(lines) + "\n"
    return LeafNode("code", value=inner_text)

def markdown_to_html_node(document):
    div_node = ParentNode("div", children=[])
    blocks = markdown_to_blocks(document)
    for block in blocks:
        type = block_to_block_type(block)
        html_node = None
        match type:
            case BlockType.HEADING:
                leading_hashes = count_leading(block,"#")
                text = block[leading_hashes + 1 :].strip()
                html_node = ParentNode(f"h{leading_hashes}", children=text_to_children(text))
            case BlockType.CODE:
                html_node = ParentNode("pre", children=[code_block_to_html(block)])
            case BlockType.QUOTE:
                html_node = ParentNode("blockquote",children=[])
            case BlockType.UNORDERED_LIST:
                html_node = ParentNode("ul",children=list_block_to_children(block, ordered=False))
            case BlockType.ORDERED_LIST:
                html_node = ParentNode("ol",children=list_block_to_children(block, ordered=True))
            case BlockType.PARAGRAPH:
                lines = block.split("\n")
                new_paragraph = ""
                if len(lines) > 0:
                    for line in lines:
                        if line != "":
                            new_paragraph += f" {line}"
                new_paragraph = new_paragraph.strip()
                html_node = ParentNode("p",children=text_to_children(new_paragraph))
            case default:
                raise ValueError("f{type} is not a valid BlockType")
        div_node.children.append(html_node)
    return div_node