from bs4 import Comment, NavigableString


class Tree:

    class Node:
        def __init__(self):
            self.parent = None
            self.children = []
            self.data = None
            self.name = None

    def __init__(self, doc):
        if doc.title:
            self.title = doc.title.string
        self.root = self.create_node(doc.body)
