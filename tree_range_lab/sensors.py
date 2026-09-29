"""Задание 13: анализ измерений датчиков."""
import random
from bst import insert, search, inorder
from range_queries import build_prefix, range_sum_prefix, FenwickTree, SegmentTreeSMM, range_sum_naive


class SensorAnalyzer:
    def __init__(self):
        self.root = None            # BST: id датчика -> список измерений (в Node.value)

    def add_sensor(self, sensor_id, measurements):
        self.root = insert(self.root, sensor_id, list(measurements))

    def find(self, sensor_id):
        node, visited = search(self.root, sensor_id)
        return (node.value if node else None), visited

    def sorted_ids(self):
        return inorder(self.root)


class SensorSeries:
    """Структуры для одного выбранного датчика."""

    def __init__(self, data):
        self.data = list(data)
        self.prefix = build_prefix(self.data)
        self.fenwick = FenwickTree(self.data)
        self.seg = SegmentTreeSMM(self.data)

    def sum_naive(self, l, r):
        return range_sum_naive(self.data, l, r)

    def sum_prefix(self, l, r):          # корректна только пока нет обновлений без пересчёта
        return range_sum_prefix(self.prefix, l, r)

    def sum_fenwick(self, l, r):
        return self.fenwick.range_sum(l, r)

    def sum_min_max(self, l, r):
        return self.seg.query(l, r)

    def update(self, index, new_value):
        delta = new_value - self.data[index]
        self.data[index] = new_value
        self.fenwick.update(index, delta)
        self.seg.update(index, new_value)
        self.prefix = build_prefix(self.data)   # O(n): именно поэтому prefix плох при обновлениях
