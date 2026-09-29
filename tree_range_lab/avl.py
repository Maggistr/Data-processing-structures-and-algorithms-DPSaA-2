"""AVL-повороты (задание 7)."""
from bst import Node, preorder


def node_height(node):
    """Хранимая высота узла в узлах (None -> 0)."""
    return node.h if node else 0


def update_height(node):
    node.h = 1 + max(node_height(node.left), node_height(node.right))


def balance_factor(node):
    return node_height(node.left) - node_height(node.right) if node else 0


def rotate_right(y):
    x = y.left
    y.left = x.right
    x.right = y
    update_height(y)
    update_height(x)
    return x


def rotate_left(x):
    y = x.right
    x.right = y.left
    y.left = x
    update_height(x)
    update_height(y)
    return y


def rebalance(node, log=None):
    update_height(node)
    b = balance_factor(node)
    if b > 1:
        if balance_factor(node.left) < 0:            # LR
            if log is not None:
                log.append(f"LR в узле {node.key}: левый поворот у {node.left.key}, затем правый поворот у {node.key}")
            node.left = rotate_left(node.left)
        elif log is not None:                        # LL
            log.append(f"LL в узле {node.key}: правый поворот")
        return rotate_right(node)
    if b < -1:
        if balance_factor(node.right) > 0:           # RL
            if log is not None:
                log.append(f"RL в узле {node.key}: правый поворот у {node.right.key}, затем левый поворот у {node.key}")
            node.right = rotate_right(node.right)
        elif log is not None:                        # RR
            log.append(f"RR в узле {node.key}: левый поворот")
        return rotate_left(node)
    return node


def avl_insert(root, key, log=None):
    if root is None:
        n = Node(key)
        n.h = 1
        return n
    if key < root.key:
        root.left = avl_insert(root.left, key, log)
    elif key > root.key:
        root.right = avl_insert(root.right, key, log)
    else:
        return root
    return rebalance(root, log)


def avl_from(keys, log=None):
    root = None
    for k in keys:
        root = avl_insert(root, k, log)
    return root
