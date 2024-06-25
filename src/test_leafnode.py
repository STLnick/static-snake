import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_value_required(self):
        with self.assertRaises(ValueError):
            leaf = LeafNode(None)
    
    def test_to_html(self):
        anchor = LeafNode("a", "i am link", { "href": "boot.dev" })
        p = LeafNode("p", "i am paragraph", { "style": "font-weight:bold;" })
        self.assertEqual(anchor.to_html(), "<a href=\"boot.dev\">i am link</a>")
        self.assertEqual(p.to_html(), "<p style=\"font-weight:bold;\">i am paragraph</p>")
