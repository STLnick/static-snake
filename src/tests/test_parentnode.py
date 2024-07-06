import unittest

from leafnode import LeafNode
from parentnode import ParentNode

class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        parent = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        expected = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(parent.to_html(), expected)

    def test_nested_parents(self):
        parent1 = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        parent2= ParentNode(
            "span",
            [
                LeafNode("b", "Bold text"),
                LeafNode("i", "italic text"),
            ],
            { "style": "letter-spacing:2px;" }
        )
        parent3 = ParentNode(
            "div",
            [
                parent1,
                LeafNode(None, "Normal text"),
                parent2,
            ],
            { "style": "display:flex;align-items:center;" },
        )
        expected_parent_1 = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        expected_parent_2 = "<span style=\"letter-spacing:2px;\"><b>Bold text</b><i>italic text</i></span>"
        expected_parent_3 = f"<div style=\"display:flex;align-items:center;\">{expected_parent_1}Normal text{expected_parent_2}</div>"
        self.assertEqual(parent1.to_html(), expected_parent_1)
        self.assertEqual(parent2.to_html(), expected_parent_2)
        self.assertEqual(parent3.to_html(), expected_parent_3)

