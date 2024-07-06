import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        h_node_1 = HTMLNode("h1", "nick", {"style": "color:red;"}, None)
        self.assertEqual(h_node_1.props_to_html(), " style=\"color:red;\"")
    def test_equal(self):
        h_node_1 = HTMLNode("h1", "nick", {"style": "color:red;"}, None)
        h_node_2 = HTMLNode("h1", "nick", {"style": "color:red;"}, None)
        self.assertEqual(h_node_1, h_node_2)

if __name__ == "__main__":
    unittest.main()
