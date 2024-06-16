class HTMLNode:
    def __init__(self, tag = None, value = None, props = None, children = None):
        self.tag = tag # Node without a tag renders as raw text
        self.value = value # Node without a value is assumed to have children
        self.props = props # Node without props will have no attributes
        self.children = children # Node without children is assumed to have a value

    def __eq__(self, value):
        return (
            self.value == value.value
            and self.tag == value.tag
            and self.props == value.props
            and self.children == value.children
        )

    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, props={self.props}, children={self.children})"

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props == None or len(self.props) == 0:
            return ""
       
        attrs = []
        for key, val in self.props.items():
            attrs.append(f"{key}=\"{val}\"")
        return " " + " ".join(attrs)
