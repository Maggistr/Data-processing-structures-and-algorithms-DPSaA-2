"""Диапазонные запросы (задания 8-12)."""


def range_sum_naive(data, left, right):
    total = 0
    for i in range(left, right + 1):
        total += data[i]
    return total


def build_prefix(data):
    prefix = [0] * (len(data) + 1)
    for i, v in enumerate(data):
        prefix[i + 1] = prefix[i] + v
    return prefix


def range_sum_prefix(prefix, left, right):
    """Сумма на отрезке [left, right] включительно."""
    return prefix[right + 1] - prefix[left]


class FenwickTree:
    """Дерево Фенвика, внешняя индексация с 0, внутренняя с 1."""

    def __init__(self, data):
        self.n = len(data)
        self.tree = [0] * (self.n + 1)
        for i, v in enumerate(data):          # линейное построение O(n)
            j = i + 1
            self.tree[j] += v
            k = j + (j & -j)
            if k <= self.n:
                self.tree[k] += self.tree[j]

    def update(self, index, delta):
        i = index + 1
        while i <= self.n:
            self.tree[i] += delta
            i += i & -i

    def prefix_sum(self, index):
        """Сумма элементов [0..index] включительно."""
        i, result = index + 1, 0
        while i > 0:
            result += self.tree[i]
            i -= i & -i
        return result

    def range_sum(self, left, right):
        return self.prefix_sum(right) - (self.prefix_sum(left - 1) if left > 0 else 0)


class SegmentTree:
    """Дерево отрезков (сумма). Рекурсивная реализация, узлы в массиве."""

    def __init__(self, data):
        self.n = len(data)
        self.data = list(data)
        self.t = [0] * (4 * self.n)
        self._build(1, 0, self.n - 1)

    def _build(self, v, lo, hi):
        if lo == hi:
            self.t[v] = self.data[lo]
            return
        mid = (lo + hi) // 2
        self._build(2 * v, lo, mid)
        self._build(2 * v + 1, mid + 1, hi)
        self.t[v] = self.t[2 * v] + self.t[2 * v + 1]

    def query(self, left, right):
        return self._query(1, 0, self.n - 1, left, right)

    def _query(self, v, lo, hi, l, r):
        if r < lo or hi < l:
            return 0
        if l <= lo and hi <= r:
            return self.t[v]
        mid = (lo + hi) // 2
        return self._query(2 * v, lo, mid, l, r) + self._query(2 * v + 1, mid + 1, hi, l, r)

    def update(self, index, value):
        self.data[index] = value
        self._update(1, 0, self.n - 1, index, value)

    def _update(self, v, lo, hi, idx, value):
        if lo == hi:
            self.t[v] = value
            return
        mid = (lo + hi) // 2
        if idx <= mid:
            self._update(2 * v, lo, mid, idx, value)
        else:
            self._update(2 * v + 1, mid + 1, hi, idx, value)
        self.t[v] = self.t[2 * v] + self.t[2 * v + 1]


INF = float("inf")


class SegmentTreeSMM:
    """Дерево отрезков: в каждом узле (сумма, минимум, максимум)."""

    NEUTRAL = (0, INF, -INF)

    def __init__(self, data):
        self.n = len(data)
        self.t = [self.NEUTRAL] * (4 * self.n)
        self._build(1, 0, self.n - 1, data)

    @staticmethod
    def _merge(a, b):
        return (a[0] + b[0], min(a[1], b[1]), max(a[2], b[2]))

    def _build(self, v, lo, hi, data):
        if lo == hi:
            self.t[v] = (data[lo], data[lo], data[lo])
            return
        mid = (lo + hi) // 2
        self._build(2 * v, lo, mid, data)
        self._build(2 * v + 1, mid + 1, hi, data)
        self.t[v] = self._merge(self.t[2 * v], self.t[2 * v + 1])

    def query(self, left, right):
        """Возвращает (sum, min, max) на [left, right]."""
        return self._query(1, 0, self.n - 1, left, right)

    def _query(self, v, lo, hi, l, r):
        if r < lo or hi < l:
            return self.NEUTRAL
        if l <= lo and hi <= r:
            return self.t[v]
        mid = (lo + hi) // 2
        return self._merge(self._query(2 * v, lo, mid, l, r),
                           self._query(2 * v + 1, mid + 1, hi, l, r))

    def update(self, index, value):
        self._update(1, 0, self.n - 1, index, value)

    def _update(self, v, lo, hi, idx, value):
        if lo == hi:
            self.t[v] = (value, value, value)
            return
        mid = (lo + hi) // 2
        if idx <= mid:
            self._update(2 * v, lo, mid, idx, value)
        else:
            self._update(2 * v + 1, mid + 1, hi, idx, value)
        self.t[v] = self._merge(self.t[2 * v], self.t[2 * v + 1])
