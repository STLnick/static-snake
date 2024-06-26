import unittest

from parse import *
from textnode import TextNode

class TestParse(unittest.TestCase):
    def setUp(self):
        self.delimiter_test_values = {
            "code": [
                [
                    "This has `code` text",
                    [
                        TextNode("This has ", TextType.TEXT),
                        TextNode("code", TextType.CODE),
                        TextNode(" text", TextType.TEXT),
                    ],
                ],
                [
                    "`This is all code text`",
                    [
                        TextNode("This is all code text", TextType.CODE),
                    ],
                ],
            ],
            "bold": [
                [
                    "This has **bolded** text",
                    [
                        TextNode("This has ", TextType.TEXT),
                        TextNode("bolded", TextType.BOLD),
                        TextNode(" text", TextType.TEXT),
                    ],
                ],
                [
                    "**This is bolded text**",
                    [
                        TextNode("This is bolded text", TextType.BOLD),
                    ],
                ],
            ],
            "italic": [
                [
                    "This has *italicized* text",
                    [
                        TextNode("This has ", TextType.TEXT),
                        TextNode("italicized", TextType.ITALIC),
                        TextNode(" text", TextType.TEXT),
                    ]
                ],
                [
                    "*This is italicized text*",
                    [
                        TextNode("This is italicized text", TextType.ITALIC),
                    ],
                ],
            ],
        }

    def test_delimiters(self):
        for key in self.delimiter_test_values.keys():
            for (val, expected) in self.delimiter_test_values[key]:
                result = text_to_textnodes(val)
                self.assertEqual(result, expected)
        
    def test_invalid_syntax(self):
        bad_syntax_values = [
            "*This is not italicized",
            "This is not italicized*",
            "`italicized*",
            "`italicized**",
            "**what is going on here`",
            "nope`",
        ]
        for bad_value in bad_syntax_values:
            with self.assertRaises(SSSyntaxError):
                result = text_to_textnodes(bad_value)

    def test_extract_markdown_images(self):
        # Valid
        text = "This is an image ![alty texty](https://picsum.photos/200/300)"
        expected = [ ("alty texty", "https://picsum.photos/200/300") ]
        result = extract_markdown_images(text)
        self.assertEqual(result, expected)
        # Missing "!" to start image tag
        text = "This is a [link](www.google.com)"
        expected = []
        result = extract_markdown_images(text)
        self.assertEqual(result, expected)
    
    def test_extract_markdown_links(self):
        # Has "!" to start image tag instead of link tag
        text = "This is an image ![alty texty](https://picsum.photos/200/300)"
        expected = []
        result = extract_markdown_links(text)
        self.assertEqual(result, expected)
        # Valid
        text = "This is a [link](www.google.com)"
        expected = [ ("link", "www.google.com") ]
        result = extract_markdown_links(text)
        self.assertEqual(result, expected)

    def test_split_nodes_images(self):
        text = "This is an image ![alty texty](https://picsum.photos/200/300)"
        expected = [
            TextNode("This is an image ", TextType.TEXT),
            TextNode("alty texty", TextType.IMAGE, "https://picsum.photos/200/300"),
        ]
        result = text_to_textnodes(text)
        self.assertEqual(result, expected)
        # Multiple images in text
        text = "This is img1:![img1 alty texty](https://picsum.photos/200/300) and img2:![img2 alty texty](https://picsum.photos/200/300); after all images"
        expected = [
            TextNode("This is img1:", TextType.TEXT),
            TextNode("img1 alty texty", TextType.IMAGE, "https://picsum.photos/200/300"),
            TextNode(" and img2:", TextType.TEXT),
            TextNode("img2 alty texty", TextType.IMAGE, "https://picsum.photos/200/300"),
            TextNode("; after all images", TextType.TEXT),
        ]
        result = text_to_textnodes(text)
        self.assertEqual(result, expected)

    def test_split_nodes_links(self):
        text = "This is a [link](www.google.com)"
        expected = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "www.google.com"),
        ]
        result = text_to_textnodes(text)
        self.assertEqual(result, expected)
        # Multiple links in text
        text = "This is [link one](www.google.com) and over here is [link two](www.bing.com); both are great!"
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("link one", TextType.LINK, "www.google.com"),
            TextNode(" and over here is ", TextType.TEXT),
            TextNode("link two", TextType.LINK, "www.bing.com"),
            TextNode("; both are great!", TextType.TEXT),
        ]
        result = text_to_textnodes(text)
        self.assertEqual(result, expected)

    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        result = text_to_textnodes(text)
        self.assertEqual(result, expected)

    def test_markdown_to_blocks(self):
        expected = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is a list item\n* This is another list item",
        ]
        md = "\n\n".join(expected)
        result = markdown_to_blocks(md)
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()
