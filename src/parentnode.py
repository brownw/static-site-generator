from htmlnode import HTMLNode

class ParentNode (HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, children=children, props=props)


    def to_html(self):
        if self.tag == None:
            raise ValueError("All parent nodes must have a tag")
        if self.tag == None:
            raise ValueError("All parent nodes must have children")
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        return f'<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>'


    def __repr__(self):
        return f"LeafNode(tag:{self.tag}, children:{self.children}, properties:{self.props})"
