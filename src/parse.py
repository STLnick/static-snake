from leafnode import LeafNode
from textnode import TextNode

valid_text_types = {
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
    
def text_node_to_html_node(text_node):
    if not text_node.text_type in valid_text_types.values():
        print(text_node)
        raise SSTypeError(f"invalid text type:{text_node.text_type}")
    if text_node.text_type == valid_text_types.get("text_type_text"):
        return LeafNode(value=text_node.text)
    
    elif text_node.text_type == valid_text_types.get("text_type_bold"):
        return LeafNode(tag="b", value=text_node.text)
    
    elif text_node.text_type == valid_text_types.get("text_type_italic"):
        return LeafNode(tag="i", value=text_node.text)
    
    elif text_node.text_type == valid_text_types.get("text_type_code"):
        return LeafNode(tag="code", value=text_node.text)
    
    elif text_node.text_type == valid_text_types.get("text_type_link"):
        return LeafNode(tag="a", value=text_node.text, props={"href":text_node.url})
    
    elif text_node.text_type == valid_text_types.get("text_type_image"):
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
                n = TextNode(s, text_type if styling else valid_text_types.get("text_type_text"))
                new_nodes.append(n)
            styling = not styling

    return new_nodes

def split_nodes(old_nodes):
    delimiters = {
        "**": valid_text_types.get("text_type_bold"),
        "*": valid_text_types.get("text_type_italic"),
        "`": valid_text_types.get("text_type_code"),

        # TODO: Add remaining delmiters with types
        # "[]()": valid_text_types.get("text_type_link"),
        # "![]()": valid_text_types.get("text_type_image"),
    }
    new_nodes = old_nodes
    for delimiter, text_type in delimiters.items():
        new_nodes = split_nodes_delimiter(new_nodes, delimiter, text_type);
    return new_nodes

