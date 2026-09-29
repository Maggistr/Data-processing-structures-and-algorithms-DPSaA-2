"""Бинарное дерево поиска (задания 1-6)."""


class Node:
    def __init__(self, key, value=None):
        self.key = key
        self.value = value      # полезная нагрузка (используется в задании 13)
        self.left = None
        self.right = None


def insert(root, key, value=None):
    """Вставка ключа с сохранением свойства BST. Дубликаты не добавляются
    (для существующего ключа обновляется value)."""
    if root is None:
        return Node(key, value)
    current = root
    while True:
        if key == current.key:
            current.value = value
            return root
        if key < current.key:
            if current.left is None:
                current.left = Node(key, value)
                return root
            current = current.left
        else:
            if current.right is None:
                current.right = Node(key, value)
                return root
            current = current.right


def build_bst(keys):
    root = None
    for k in keys:
        root = insert(root, k)
    return root


def search(root, key):
    """Возвращает (узел или None, число посещённых узлов)."""
    current, visited = root, 0
    while current is not None:
        visited += 1
        if key == current.key:
            return current, visited
        current = current.left if key < current.key else current.right
    return None, visited


def preorder(root, out=None):
    out = [] if out is None else out
    if root is not None:
        out.append(root.key)
        preorder(root.left, out)
        preorder(root.right, out)
    return out


def inorder(root, out=None):
    out = [] if out is None else out
    if root is not None:
        inorder(root.left, out)
        out.append(root.key)
        inorder(root.right, out)
    return out


def postorder(root, out=None):
    out = [] if out is None else out
    if root is not None:
        postorder(root.left, out)
        postorder(root.right, out)
        out.append(root.key)
    return out


def min_node(node):
    while node.left is not None:
        node = node.left
    return node


def delete(root, key):
    """Удаление ключа; возвращает новый корень поддерева."""
    if root is None:
        return None
    if key < root.key:
        root.left = delete(root.left, key)
    elif key > root.key:
        root.right = delete(root.right, key)
    else:
        if root.left is None:           # лист или только правый потомок
            return root.right
        if root.right is None:          # только левый потомок
            return root.left
        succ = min_node(root.right)     # два потомка: преемник
        root.key, root.value = succ.key, succ.value
        root.right = delete(root.right, succ.key)
    return root


def height(root):
    """Высота в рёбрах (пустое дерево = -1, один узел = 0)."""
    if root is None:
        return -1
    return 1 + max(height(root.left), height(root.right))


def show(root, prefix="", is_left=None):
    """Текстовое изображение дерева (повёрнуто на 90°: правое поддерево сверху)."""
    lines = []

    def rec(node, depth):
        if node is None:
            return
        rec(node.right, depth + 1)
        lines.append("    " * depth + str(node.key))
        rec(node.left, depth + 1)

    rec(root, 0)
    return "\n".join(lines)
