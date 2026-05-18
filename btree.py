class BTreeNode: 
    def __init__(self):
        self.keys = []
        self.values = []
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
    
    def insert_non_full(self, key, value=None):
        i = len(self.keys) - 1
        if self.is_leaf:
            self.keys.append(None)
            self.values.append(None)
            while i >= 0 and self.keys[i] is not None and key < self.keys[i]:
                self.keys[i + 1] = self.keys[i]
                self.values[i + 1] = self.values[i]
                i -= 1
            self.keys[i + 1] = key
            self.values[i + 1] = value
        else:
            while i >= 0 and key < self.keys[i]:
                i -= 1
            i += 1
            self.children[i].insert_non_full(key, value)

    def split_child(self, i, child):
        order = len(child.keys) // 2
        new_node = BTreeNode()
        new_node.is_leaf = child.is_leaf
        mid = order
        mid_key = child.keys[mid]
        new_node.keys = child.keys[mid + 1:]
        new_node.values = child.values[mid + 1:]
        child.keys = child.keys[:mid]
        child.values = child.values[:mid]
        if not child.is_leaf:
            new_node.children = child.children[mid + 1:]
            child.children = child.children[:mid + 1]
        self.keys.insert(i, mid_key)
        self.values.insert(i, None)
        self.children.insert(i + 1, new_node)

    def __repr__(self):
        return f"keys={self.keys} children={self.children}"


class BTree:
    def __init__(self, order):
        self.root = BTreeNode()
        self.order = order

    def insert(self, key, value=None):
        root = self.root
        if len(root.keys) == (2 * self.order + 1):
            new_root = BTreeNode()
            new_root.is_leaf = False
            new_root.children.append(self.root)
            new_root.split_child(0, self.root)
            self.root = new_root
        self._insert_non_full(self.root, key, value)

    def _insert_non_full(self, node, key, value=0):
        i = len(node.keys) - 1 

        if node.is_leaf:
            node.insert_non_full(key, value)
        else:
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1
            if len(node.children[i].keys) == (2 * self.order + 1):
                node.split_child(i, node.children[i])
                if key > node.keys[i]:
                    i += 1
            self._insert_non_full(node.children[i], key, value)



if __name__ == "__main__":
    tree = BTree(1)
    
    tree.insert(1, (0, 0))
    tree.insert(2, (0, 1))
    tree.insert(3, (0, 2))
    tree.insert(4, (1, 0))
    tree.insert(5, (1, 1))

    result = tree.root.search(3)
    if result:
        idx = result.keys.index(3)
        print(f"found key 3 at disk location: {result.values[idx]}")
    
    result = tree.root.search(9)
    print(f"search for 9: {result}")