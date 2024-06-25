from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag = None, children = None, props = None):
        super().__init__(tag, None, props, children)

    def __repr__(self):
        return f"ParentNode(tag={self.tag}, props={self.props}), numChildren={len(self.children)}"

    def to_html(self):
        if self.tag == None:
            raise ValueError("parent node requires tag")
        if self.children == None or len(self.children) == 0:
            raise ValueError("parent node requires children")
        child_html = ""
        for child in self.children:
            child_html += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{child_html}</{self.tag}>"
