from enum import Enum, unique
import os 
import re

from leafnode import LeafNode
from parentnode import ParentNode
from textnode import TextNode

class SSSyntaxError(Exception):
    pass

class SSTypeError(Exception):
    pass

@unique
class BlockType(Enum):
    PARAGRAPH = 0
    HEADING = 1
    CODE = 2
    QUOTE = 3
    UNORDERED_LIST = 4
    ORDERED_LIST = 5

@unique
class TextType(Enum):
    TEXT = 0
    BOLD = 1
    ITALIC = 2
    CODE = 3
    LINK = 4
    IMAGE = 5

MD_IMG_REGEX = r"!\[(.*?)\]\((.*?)\)"
MD_LINK_REGEX = r"(?<!\!)\[(.*?)\]\((.*?)\)"

def extract_markdown_images(text):
    global MD_IMG_REGEX
    return re.findall(MD_IMG_REGEX, text)

def extract_markdown_links(text):
    global MD_LINK_REGEX
    return re.findall(MD_LINK_REGEX, text)
    
def text_node_to_html_node(text_node):
    if not text_node.text_type in TextType:
        print(text_node)
        raise SSTypeError(f"invalid text type:{text_node.text_type}")

    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.LINK:
            return LeafNode(tag="a", value=text_node.text, props={"href":text_node.url})
        case TextType.IMAGE:
            return LeafNode(tag="img", value="", props={"alt": text_node.text, "src":text_node.url})
        case _:
            raise ValueError("you f'd up")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        spl = node.text.split(delimiter)
        if len(spl) == 1:
            new_nodes.append(node)
            continue
        elif len(spl) == 2:
            raise SSSyntaxError(f"invalid markdown syntax - delimiter=\"{delimiter}\"/str=\"{node.text}\"")

        styling = False
        for s in spl:
            if s!= "":
                n = TextNode(s, text_type if styling else TextType.TEXT)
                new_nodes.append(n)
            styling = not styling

    return new_nodes

def split_nodes_images(old_nodes):
    new_nodes = []
    for node in old_nodes:
        imgs = extract_markdown_images(node.text)
        if len(imgs) == 0:
            new_nodes.append(node)
        else:
            text = node.text
            for img_tuple in imgs:
                (before, after) = text.split(f"![{img_tuple[0]}]({img_tuple[1]})", 1)
                if before != "":
                    new_nodes.append(TextNode(before, TextType.TEXT))
                new_nodes.append(TextNode(img_tuple[0], TextType.IMAGE, img_tuple[1]))
                text = after
            if text != "":
                new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes

def split_nodes_links(old_nodes):
    new_nodes = []
    for node in old_nodes:
        links = extract_markdown_links(node.text)
        if len(links) == 0:
            new_nodes.append(node)
        else:
            text = node.text
            for link_tuple in links:
                (before, after) = text.split(f"[{link_tuple[0]}]({link_tuple[1]})", 1)
                if before != "":
                    new_nodes.append(TextNode(before, TextType.TEXT))
                new_nodes.append(TextNode(link_tuple[0], TextType.LINK, link_tuple[1]))
                text = after
            if text != "":
                new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_images(nodes)
    nodes = split_nodes_links(nodes)
    return nodes

def markdown_to_blocks(md_text):
    # "" element indicates the separation of blocks;
    split_text = md_text.split("\n")
    blocks = []
    current_block = []
    for s in md_text.split("\n"):
        if s != "":
            current_block.append(s)
        else:
            if len(current_block) > 0:
                block_str = "\n".join(current_block)
                blocks.append(block_str)
                current_block.clear()
    if len(current_block) > 0:
        block_str = "\n".join(current_block)
        blocks.append(block_str)
    return blocks

def block_to_block_type(block_text):
    # print(f"BLOCKTEXT: {block_text}")
    
    heading_re = re.compile(r"^#+ ")
    if bool(heading_re.match(block_text)):
        return BlockType.HEADING
    elif block_text.startswith("```") and block_text.endswith("```"):
        return BlockType.CODE
    
    spl = block_text.split("\n")
    is_quote = True
    for s in spl:
        if not s.startswith(">"):
            is_quote = False
            break
    if is_quote:
        return BlockType.QUOTE
    
    is_ul = True
    for s in spl:
        if not s.startswith("* ") and not s.startswith("- "):
            is_ul = False
            break
    if is_ul:
        return BlockType.UNORDERED_LIST
    
    is_ol = True
    ol_re = re.compile(r"^\d\.")
    current_num = 1
    for s in spl:
        # if not a digit then "." OR the digit isn't one more than previous number
        if not bool(ol_re.match(s)) or s[0] != f"{current_num}":
            is_ol = False
            break
        current_num += 1
    if is_ol:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

def markdown_to_html_node(md_doc):
    blocks = markdown_to_blocks(md_doc)
    children = []
    for b in blocks:
        match block_to_block_type(b):
            case BlockType.PARAGRAPH:
                children.append(create_paragraph(b))
            case BlockType.HEADING:
                children.append(create_heading(b))
            case BlockType.CODE:
                children.append(create_code(b))
            case BlockType.QUOTE:
                children.append(create_quote(b))
            case BlockType.UNORDERED_LIST:
                children.append(create_unordered_list(b))
            case BlockType.ORDERED_LIST:
                children.append(create_ordered_list(b))
    return ParentNode("div", children)

def create_code(block):
    code = LeafNode("code", block[3:len(block) - 3])
    return ParentNode("pre", [code])

def create_heading(block):
    level = 0
    for c in block:
        if c == "#":
            level += 1
        else:
            break
    value = block_to_node_value(block[level + 1:])
    return LeafNode(f"h{level}", value)

def create_ordered_list(block):
    list_items = []
    for line in block.split("\n"):
        list_items.append(LeafNode("li", line[3:]))
    
    return ParentNode("ol", list_items)

def create_paragraph(block):
    value = block_to_node_value(block)
    return LeafNode("p", value)

def create_quote(block):
    cleaned = []
    for line in block.split("\n"):
        cleaned.append(line[2:])
    value = block_to_node_value("\n".join(cleaned))
    return LeafNode("blockquote", value)

def create_unordered_list(block):
    list_items = []
    for line in block.split("\n"):
        list_items.append(LeafNode("li", line[2:]))
    
    return ParentNode("ul", list_items)

def block_to_node_value(block):
    text_nodes = text_to_textnodes(block)
    value = ""
    for node in text_nodes:
        html_node = text_node_to_html_node(node)
        value += html_node.to_html()
    return value

def extract_title(html):
    pattern = ".*<h1>(.+)<\/h1>.*"
    for block in html.split("\n"):
        result = re.search(pattern, block)
        if result != None:
            return result.group(1)
    raise SSSyntaxError

def generate_page(from_path, to_path, template_path):
    print(f"Generating page from {from_path} to {to_path} using {template_path}")
    # Get markdown file
    source = open(from_path, "r")
    md_doc = source.read()
    source.close()
    html_node = markdown_to_html_node(md_doc)
    html = html_node.to_html()
    # Get HTML template
    template = open(template_path, "r")
    template_html = template.read()
    template.close()
    # Compile template
    compiled_html = template_html.replace("{{ Title }}", extract_title(html))
    compiled_html = compiled_html.replace("{{ Content }}", html)
    # Write compiled template to to_path location
    to_dir = os.path.dirname(to_path)
    if not os.path.exists(to_dir):
        os.makedirs(to_dir)
    file_name = to_path[:-3]
    out = open(f"{file_name}.html", "w")
    out.write(compiled_html)
    out.close()

def generate_pages_recursive(dir_path_content, dest_dir_path, template_path):
    if not os.path.isdir(dir_path_content):
        raise Exception(f"source path is not a directory: {dir_path_content}")
    dir_list = os.listdir(dir_path_content)
    if len(dir_list) == 0:
        return
    for entry in dir_list:
        if os.path.isfile(os.path.join(dir_path_content, entry)) and entry.endswith(".md"):
            generate_page(os.path.join(dir_path_content, entry), os.path.join(dest_dir_path, entry), template_path)
        elif os.path.isdir(os.path.join(dir_path_content, entry)):

            generate_pages_recursive(os.path.join(dir_path_content, entry), os.path.join(dest_dir_path, entry), template_path)
    print("Done.")
