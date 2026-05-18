class BTreeNode: 
    def __init__(self):
        self.keys = []
        self.children = []
        self.is_leaf = True
    
    def search(self, key):
        i = 0
        while i < len(self.keys) and key > self.keys[i]:
            i += 1
        if i < len(self.keys) and key == self.keys[i]:
            return self
        if self.is_leaf:
            return None
        return self.children[i].search(key)
    
    def insert_non_full(self, key):
        i = len(self.keys) - 1
        if self.is_leaf:
            self.keys.append(None)
            while i >= 0 and key < self.keys[i]:
                self.keys[i + 1] = self.keys[i]
                i -= 1
            self.keys[i + 1] = key
        else:
            while i >= 0 and key < self.keys[i]:
                i -= 1
            i += 1
            self.children[i].insert_non_full(key)

    def split_child(self, i, child):
        order = len(child.keys) // 2
        new_node = BTreeNode()
        new_node.is_leaf = child.is_leaf
        mid = order
        mid_key = child.keys[mid]
        new_node.keys = child.keys[mid + 1:]
        child.keys = child.keys[:mid]
        if not child.is_leaf:
            new_node.children = child.children[mid + 1:]
            child.children = child.children[:mid + 1]
        self.keys.insert(i, mid_key)
        self.children.insert(i + 1, new_node)

    def __repr__(self):
        return f"keys={self.keys} children={self.children}"


class BTree:
    def __init__(self, order):
        self.root = BTreeNode()
        self.order = order

    def insert(self, key):
        root = self.root
        if len(root.keys) == (2 * self.order + 1):
            new_root = BTreeNode()
            new_root.is_leaf = False
            new_root.children.append(self.root)
            new_root.split_child(0, self.root)
            self.root = new_root
        self._insert_non_full(self.root, key)

    def _insert_non_full(self, node, key):
        i = len(node.keys) - 1 

        if node.is_leaf:
            node.insert_non_full(key)
        else:
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1
            if len(node.children[i].keys) == (2 * self.order + 1):
                node.split_child(i, node.children[i])
                if key > node.keys[i]:
                    i += 1
            self._insert_non_full(node.children[i], key)



if __name__ == "__main__":
    tree = BTree(1)
    for key in [4, 2, 6, 1, 3, 5, 7, 8]:
        tree.insert(key)
    print("root:", tree.root)
    for child in tree.root.children:
        print("child:", child)