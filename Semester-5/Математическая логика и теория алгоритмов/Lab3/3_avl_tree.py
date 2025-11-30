class AVLNode:
    def __init__(self, key):
        self.key = key
        self.height = 1
        self.left = None
        self.right = None

class AVLTree:
    def __init__(self):
        self.root = None

    def height(self, node):
        return node.height if node else 0

    def balance_factor(self, node):
        return self.height(node.left) - self.height(node.right) if node else 0

    def rotate_right(self, y):
        x = y.left
        y.left = x.right
        x.right = y
        y.height = max(self.height(y.left), self.height(y.right)) + 1
        x.height = max(self.height(x.left), self.height(x.right)) + 1
        return x

    def rotate_left(self, x):
        y = x.right
        x.right = y.left
        y.left = x
        x.height = max(self.height(x.left), self.height(x.right)) + 1
        y.height = max(self.height(y.left), self.height(y.right)) + 1
        return y

    def insert(self, key):
        if not self.root:
            self.root = AVLNode(key)
            return
        stack = []
        node = self.root
        # Обычная вставка как в BST, плюс сохраняем путь
        while True:
            stack.append(node)
            if key < node.key:
                if not node.left:
                    node.left = AVLNode(key)
                    break
                node = node.left
            else:
                if not node.right:
                    node.right = AVLNode(key)
                    break
                node = node.right
        # Балансировка вверх по пути
        while stack:
            node = stack.pop()
            node.height = max(self.height(node.left), self.height(node.right)) + 1
            bf = self.balance_factor(node)
            if bf > 1:
                if key < node.left.key:
                    if stack:
                        parent = stack[-1]
                        if parent.left == node:
                            parent.left = self.rotate_right(node)
                        else:
                            parent.right = self.rotate_right(node)
                    else:
                        self.root = self.rotate_right(node)
                else:
                    node.left = self.rotate_left(node.left)
                    if stack:
                        parent = stack[-1]
                        if parent.left == node:
                            parent.left = self.rotate_right(node)
                        else:
                            parent.right = self.rotate_right(node)
                    else:
                        self.root = self.rotate_right(node)
            elif bf < -1:
                if key > node.right.key:
                    if stack:
                        parent = stack[-1]
                        if parent.left == node:
                            parent.left = self.rotate_left(node)
                        else:
                            parent.right = self.rotate_left(node)
                    else:
                        self.root = self.rotate_left(node)
                else:
                    node.right = self.rotate_right(node.right)
                    if stack:
                        parent = stack[-1]
                        if parent.left == node:
                            parent.left = self.rotate_left(node)
                        else:
                            parent.right = self.rotate_left(node)
                    else:
                        self.root = self.rotate_left(node)

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

# Демонстрация AVL
print("\nAVL:")
avl = AVLTree()
for v in [20, 4, 15, 70, 50, 100, 3]:
    avl.insert(v)
print("AVL inorder:", avl.traverse_inorder())
