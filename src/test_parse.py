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
                        TextNode("This has ", text_types['text_type_text']),
                        TextNode("code", text_types['text_type_code']),
                        TextNode(" text", text_types['text_type_text']),
                    ],
                ],
                [
                    "`This is all code text`",
                    [
                        TextNode("This is all code text", text_types['text_type_code']),
                    ],
                ],
            ],
            "bold": [
                [
                    "This has **bolded** text",
                    [
                        TextNode("This has ", text_types['text_type_text']),
                        TextNode("bolded", text_types['text_type_bold']),
                        TextNode(" text", text_types['text_type_text']),
                    ],
                ],
                [
                    "**This is bolded text**",
                    [
                        TextNode("This is bolded text", text_types['text_type_bold']),
                    ],
                ],
            ],
            # Image - - - - - - - -
            # TODO
            "italic": [
                [
                    "This has *italicized* text",
                    [
                        TextNode("This has ", text_types['text_type_text']),
                        TextNode("italicized", text_types['text_type_italic']),
                        TextNode(" text", text_types['text_type_text']),
                    ]
                ],
                [
                    "*This is italicized text*",
                    [
                        TextNode("This is italicized text", text_types['text_type_italic']),
                    ],
                ],
            ],
            # Link - - - - - - - -
            # TODO
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
            TextNode("This is an image ", text_types["text_type_text"]),
            TextNode("alty texty", text_types["text_type_image"], "https://picsum.photos/200/300"),
        ]
        result = text_to_textnodes(text)
        self.assertEqual(result, expected)
        # Multiple images in text
        text = "This is img1:![img1 alty texty](https://picsum.photos/200/300) and img2:![img2 alty texty](https://picsum.photos/200/300); after all images"
        expected = [
            TextNode("This is img1:", text_types["text_type_text"]),
            TextNode("img1 alty texty", text_types["text_type_image"], "https://picsum.photos/200/300"),
            TextNode(" and img2:", text_types["text_type_text"]),
            TextNode("img2 alty texty", text_types["text_type_image"], "https://picsum.photos/200/300"),
            TextNode("; after all images", text_types["text_type_text"]),
        ]
        result = text_to_textnodes(text)
        self.assertEqual(result, expected)

    def test_split_nodes_links(self):
        text = "This is a [link](www.google.com)"
        expected = [
            TextNode("This is a ", text_types["text_type_text"]),
            TextNode("link", text_types["text_type_link"], "www.google.com"),
        ]
        result = text_to_textnodes(text)
        self.assertEqual(result, expected)
        # Multiple links in text
        text = "This is [link one](www.google.com) and over here is [link two](www.bing.com); both are great!"
        expected = [
            TextNode("This is ", text_types["text_type_text"]),
            TextNode("link one", text_types["text_type_link"], "www.google.com"),
            TextNode(" and over here is ", text_types["text_type_text"]),
            TextNode("link two", text_types["text_type_link"], "www.bing.com"),
            TextNode("; both are great!", text_types["text_type_text"]),
        ]
        result = text_to_textnodes(text)
        self.assertEqual(result, expected)

    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
        expected = [
            TextNode("This is ", text_types["text_type_text"]),
            TextNode("text", text_types["text_type_bold"]),
            TextNode(" with an ", text_types["text_type_text"]),
            TextNode("italic", text_types["text_type_italic"]),
            TextNode(" word and a ", text_types["text_type_text"]),
            TextNode("code block", text_types["text_type_code"]),
            TextNode(" and an ", text_types["text_type_text"]),
            TextNode("image", text_types["text_type_image"], "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and a ", text_types["text_type_text"]),
            TextNode("link", text_types["text_type_link"], "https://boot.dev"),
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
