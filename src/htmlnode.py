class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        props = ""
        if self.props == None or len(self.props) == 0:
            return props
        for key, value in self.props.items():
            props += f" {key}=\"{value}\""
        return props

    def __repr__(self):
        return f"HTMLNode(tag:{self.tag}, value:{self.value}, children:{self.children}, properties:{self.props})"

class LeafNode (HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, props=props)


    def to_html(self):
        if self.value == None:
            raise ValueError("All leaf nodes must have values")
        if self.tag == None:
            return self.value
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'


    def __repr__(self):
        return f"LeafNode(tag:{self.tag}, value:{self.value}, properties:{self.props})"

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