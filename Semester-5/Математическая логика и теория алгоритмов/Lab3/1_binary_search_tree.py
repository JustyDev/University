class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    # Вставка
    def insert(self, key):
        parent = None
        node = self.root
        while node:
            parent = node
            if key < node.key:
                node = node.left
            else:
                node = node.right
        new_node = Node(key)
        if parent is None:
            self.root = new_node
        else:
            if key < parent.key:
                parent.left = new_node
            else:
                parent.right = new_node

    # Поиск
    def find(self, key):
        node = self.root
        while node:
            if node.key == key:
                return node
            elif key < node.key:
                node = node.left
            else:
                node = node.right
        return None

    # Удаление
    def delete(self, key):
        node = self.root
        parent = None
        while node and node.key != key:
            parent = node
            if key < node.key:
                node = node.left
            else:
                node = node.right

        if node is None:
            return  # Элемент не найден

        if node.left is None or node.right is None:
            new_child = node.left if node.left else node.right
            if parent is None:
                self.root = new_child
            else:
                if parent.left == node:
                    parent.left = new_child
                else:
                    parent.right = new_child
        else:
            succ_parent = node
            succ = node.right
            while succ.left:
                succ_parent = succ
                succ = succ.left
            node.key = succ.key
            if succ_parent.left == succ:
                succ_parent.left = succ.right
            else:
                succ_parent.right = succ.right

    # Симметричный обход
    def traverse_inorder(self):
        result = []
        stack = []
        node = self.root
        while stack or node:
            while node:
                stack.append(node)
                node = node.left
            node = stack.pop()
            result.append(node.key)
            node = node.right
        return result

    # Прямой обход
    def traverse_preorder(self):
        result = []
        if not self.root:
            return result
        stack = [self.root]
        while stack:
            node = stack.pop()
            result.append(node.key)
            if node.right:
                stack.append(node.right)
            if node.left:
                stack.append(node.left)
        return result

    # Обратный обход
    def traverse_postorder(self):
        result = []
        stack1 = []
        stack2 = []
        if not self.root:
            return result
        stack1.append(self.root)
        while stack1:
            node = stack1.pop()
            stack2.append(node)
            if node.left:
                stack1.append(node.left)
            if node.right:
                stack1.append(node.right)
        while stack2:
            node = stack2.pop()
            result.append(node.key)
        return result

    # Минимум
    def min(self):
        node = self.root
        if not node:
            return None
        while node.left:
            node = node.left
        return node.key

    # Максимум
    def max(self):
        node = self.root
        if not node:
            return None
        while node.right:
            node = node.right
        return node.key

# Демонстрация BST
print("BST:")
bst = BST()
for v in [7, 3, 9, 2, 5, 8, 11]:
    bst.insert(v)
print("Inorder:", bst.traverse_inorder())
print("Preorder:", bst.traverse_preorder())
print("Postorder:", bst.traverse_postorder())
print("Min:", bst.min())
print("Max:", bst.max())
