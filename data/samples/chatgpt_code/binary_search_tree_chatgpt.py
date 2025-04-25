class Node:
    """
    A class representing a node in the Binary Search Tree.

    Attributes:
        key (int): The value stored in the node.
        left (Node): Pointer to the left child node.
        right (Node): Pointer to the right child node.
    """
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None


class BinarySearchTree:
    """
    A class representing the Binary Search Tree (BST).
    
    Methods:
        insert(key): Inserts a new key into the BST.
        search(key): Searches for a key in the BST.
        delete(key): Deletes a key from the BST.
        inorder(): Returns the in-order traversal of the BST.
    """

    def __init__(self):
        self.root = None

    def insert(self, key):
        """Inserts a new key into the BST."""
        self.root = self._insert(self.root, key)

    def _insert(self, node, key):
        if node is None:
            return Node(key)
        if key < node.key:
            node.left = self._insert(node.left, key)
        elif key > node.key:
            node.right = self._insert(node.right, key)
        return node

    def search(self, key):
        """Searches for a key in the BST."""
        return self._search(self.root, key)

    def _search(self, node, key):
        if node is None or node.key == key:
            return node
        if key < node.key:
            return self._search(node.left, key)
        return self._search(node.right, key)

    def delete(self, key):
        """Deletes a key from the BST."""
        self.root = self._delete(self.root, key)

    def _delete(self, node, key):
        if node is None:
            return node

        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            # Node with only one child or no child
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            # Node with two children
            temp = self._min_value_node(node.right)
            node.key = temp.key
            node.right = self._delete(node.right, temp.key)
        return node

    def _min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def inorder(self):
        """Returns a list containing the in-order traversal of the BST."""
        return self._inorder(self.root)

    def _inorder(self, node):
        result = []
        if node:
            result = self._inorder(node.left)
            result.append(node.key)
            result += self._inorder(node.right)
        return result


# Example usage:
if __name__ == "__main__":
    bst = BinarySearchTree()
    bst.insert(50)
    bst.insert(30)
    bst.insert(70)
    bst.insert(20)
    bst.insert(40)
    bst.insert(60)
    bst.insert(80)

    print("Inorder traversal:", bst.inorder())
    print("Search for 40:", bst.search(40) is not None)

    bst.delete(20)
    print("After deleting 20:", bst.inorder())

    bst.delete(30)
    print("After deleting 30:", bst.inorder())

    bst.delete(50)
    print("After deleting 50:", bst.inorder())
