from enum import Enum
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

def markdown_to_html_node(document):
    blocks = markdown_to_blocks(document)
    html_nodes = []
    for block in blocks:
        type = block_to_block_type(block)
        # 2. Based on type of block create a new HTMLNode
        # 3. Assign the proper child HTMLNode objects to the block node. Maybe:
        #  create a shared text_to_children(text) function that works for all block types. 
        #  It takes a string of text and returns a list of HTMLNodes that represent the inline markdown using previously created functions 
        # (think TextNode -> HTMLNode)
        # 4. The "code" block is a bit of a special case: 
        # it should not do any inline markdown parsing of its children. 
        # I didn't use my text_to_children function for this block type, 
        # I manually made a TextNode and used text_node_to_html_node.
    # 5 Create a parent div HTMLNode and make all the block nodes children under it and return
    