from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "block/paragraph"
    HEADING = "block/heading"
    CODE = "block/code"
    QUOTE = "block/quote"
    UNORDERED_LIST = "block/unordered_list"
    ORDERED_LIST = "block/ordered_list"

def block_to_block_type(markdown_block: str) -> BlockType:
    stripped_block = markdown_block.strip()
    if stripped_block.startswith("#"):
        return BlockType.HEADING
    elif stripped_block.startswith("- "):
        return BlockType.UNORDERED_LIST
    elif stripped_block[0].isdigit() and stripped_block[1:3] == ". ":
        return BlockType.ORDERED_LIST
    elif stripped_block.startswith(">"):
        return BlockType.QUOTE
    elif stripped_block.startswith("```"):
        return BlockType.CODE
    else:
        return BlockType.PARAGRAPH