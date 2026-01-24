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
    elif re.match(r"^```\n[\s\S]*?^```", block):
        return BlockType.CODE
    elif re.match(r"^(?:>\s.*\n?)+", block):
        return BlockType.QUOTE
    elif re.match(r"^(?:-\s.*\n?)+", block):
        return BlockType.UNORDERED_LIST
    elif re.match(r"^1\.\s.*\n(?:(?:\d+)\.\s.*\n?)*", block):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH
