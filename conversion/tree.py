


class Tree:
    def __init__(self, root):
        self.root = root
        self.children = []

    def addChild(self, child):
        self.children.append(child)

    def addChildren(self, children):
        self.children += children

    #Adds a tree to this tree, if this tree already has a the given root node, it combines the children of the root node
    def insert(self, tree):
        child = self.get(tree.root)
        child.addChildren(tree.children) if child else self.addChildren(tree.children)

    def has(self, child):
        if(child.root == self.root):
            return True
        for next_child in self.children:
                if(next_child.has(child)):
                    return True
        return False

    def get(self, root):
        if(root == self.root):
            return self
        for next_child in self.children:
            child = next_child.get(root)
            if(child):
                return child
        return None

    def __str__(self):
        children_str = ""
        for child in self.children:
            children_str += str(child.root)
        for child in self.children:
            pass
        begin = '{} \n {} '.format(self.root, children_str)
        return begin