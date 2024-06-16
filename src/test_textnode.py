import unittest

from textnode import TextNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("abc", "bold", "123")
        node2 = TextNode("abc", "bold", "123")
        node3 = TextNode("abc", "italic", "123")
        node4 = TextNode("def", "bold")
        self.assertEqual(node1, node2)
        self.assertNotEqual(node1, node3)
        self.assertNotEqual(node1, node4)

    def test_empty_url(self):
        empty_url_1 = TextNode("abc", "bold")
        empty_url_2 = TextNode("abc", "bold", "")
        self.assertEqual(empty_url_1.url, None)
        self.assertEqual(empty_url_2.url, None)

if __name__ == "__main__":
    unittest.main()
