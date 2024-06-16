import unittest

from textnode import TextNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("abc", "bold", "123")
        node2 = TextNode("abc", "bold", "123")
        self.assertEqual(node1, node2)

    # TODO: write test for empty url
    # TODO: write test for different text_types

if __name__ == "__main__":
    unittest.main()
