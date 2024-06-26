import re
from leafnode import LeafNode
from textnode import TextNode

text_types = {
    "text_type_text": "text",
    "text_type_bold": "bold",
    "text_type_italic": "italic",
    "text_type_code": "code",
    "text_type_link": "link",
    "text_type_image": "image",
}

class SSSyntaxError(Exception):
    pass

class SSTypeError(Exception):
    pass

MD_IMG_REGEX = r"!\[(.*?)\]\((.*?)\)"
MD_LINK_REGEX = r"(?<!\!)\[(.*?)\]\((.*?)\)"

def extract_markdown_images(text):
    global MD_IMG_REGEX
    return re.findall(MD_IMG_REGEX, text)

def extract_markdown_links(text):
    global MD_LINK_REGEX
    return re.findall(MD_LINK_REGEX, text)
    
def text_node_to_html_node(text_node):
    if not text_node.text_type in text_types.values():
        print(text_node)
        raise SSTypeError(f"invalid text type:{text_node.text_type}")
    if text_node.text_type == text_types.get("text_type_text"):
        return LeafNode(value=text_node.text)
    elif text_node.text_type == text_types.get("text_type_bold"):
        return LeafNode(tag="b", value=text_node.text)
    elif text_node.text_type == text_types.get("text_type_italic"):
        return LeafNode(tag="i", value=text_node.text)
    elif text_node.text_type == text_types.get("text_type_code"):
        return LeafNode(tag="code", value=text_node.text)
    elif text_node.text_type == text_types.get("text_type_link"):
        return LeafNode(tag="a", value=text_node.text, props={"href":text_node.url})
    elif text_node.text_type == text_types.get("text_type_image"):
        return LeafNode(tag="img", value="", props={"alt": text_node.text, "src":text_node.url})
    else:
        raise ValueError("you f'd up")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != "text":
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
                n = TextNode(s, text_type if styling else text_types.get("text_type_text"))
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
                    new_nodes.append(TextNode(before, text_types.get("text_type_text")))
                new_nodes.append(TextNode(img_tuple[0], text_types.get("text_type_image"), img_tuple[1]))
                text = after
            if text != "":
                new_nodes.append(TextNode(text, text_types.get("text_type_text")))
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
                    new_nodes.append(TextNode(before, text_types.get("text_type_text")))
                new_nodes.append(TextNode(link_tuple[0], text_types.get("text_type_link"), link_tuple[1]))
                text = after
            if text != "":
                new_nodes.append(TextNode(text, text_types.get("text_type_text")))
    return new_nodes

def text_to_textnodes(text):
    node = TextNode(text, text_types.get("text_type_text"))
    nodes = split_nodes_delimiter([node], "**", text_types.get("text_type_bold"));
    nodes = split_nodes_delimiter(nodes, "*", text_types.get("text_type_italic"));
    nodes = split_nodes_delimiter(nodes, "`", text_types.get("text_type_code"));
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

