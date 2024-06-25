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
                        TextNode("This has ", valid_text_types['text_type_text']),
                        TextNode("code", valid_text_types['text_type_code']),
                        TextNode(" text", valid_text_types['text_type_text']),
                    ],
                ],
                [
                    "`This is all code text`",
                    [
                        TextNode("This is all code text", valid_text_types['text_type_code']),
                    ],
                ],
            ],
            "bold": [
                [
                    "This has **bolded** text",
                    [
                        TextNode("This has ", valid_text_types['text_type_text']),
                        TextNode("bolded", valid_text_types['text_type_bold']),
                        TextNode(" text", valid_text_types['text_type_text']),
                    ],
                ],
                [
                    "**This is bolded text**",
                    [
                        TextNode("This is bolded text", valid_text_types['text_type_bold']),
                    ],
                ],
            ],
            # Image - - - - - - - -
            # TODO
            "italic": [
                [
                    "This has *italicized* text",
                    [
                        TextNode("This has ", valid_text_types['text_type_text']),
                        TextNode("italicized", valid_text_types['text_type_italic']),
                        TextNode(" text", valid_text_types['text_type_text']),
                    ]
                ],
                [
                    "*This is italicized text*",
                    [
                        TextNode("This is italicized text", valid_text_types['text_type_italic']),
                    ],
                ],
            ],
            # Link - - - - - - - -
            # TODO
        }

    def test_delimiters(self):
        for key in self.delimiter_test_values.keys():
            for (val, expected) in self.delimiter_test_values[key]:
                node = TextNode(val, valid_text_types['text_type_text'])
                result = split_nodes([node])
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
                node = TextNode(bad_value, valid_text_types['text_type_text'])
                result = split_nodes([node])

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

if __name__ == "__main__":
    unittest.main()
