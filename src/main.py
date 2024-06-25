from textnode import TextNode
from leafnode import LeafNode
from parse import *

node1 = TextNode("hi there", "text")
node2 = TextNode("hi bold", "bold")
node3 = TextNode("hi italic", "italic")
node4 = TextNode("hi code", "code")
node5 = TextNode("hi link", "link", "www.google.com")
node6 = TextNode("hi image", "image", "https://picsum.photos/200/300")

# Text Nodes
print(node1)
print(node2)
print(node3)
print(node4)
print(node5)
print(node6)

# HTML Nodes
print(text_node_to_html_node(node1))
print(text_node_to_html_node(node2))
print(text_node_to_html_node(node3))
print(text_node_to_html_node(node4))
print(text_node_to_html_node(node5))
print(text_node_to_html_node(node6))
