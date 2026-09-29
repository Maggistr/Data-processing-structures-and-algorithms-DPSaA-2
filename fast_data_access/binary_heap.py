"""
binary_heap.py

Бинарная min-куча на основе списка.
Задание 7, 8, 9.
"""


class MinHeap:
    def __init__(self):
        self.data = []

    # ---- вспомогательные функции индексов ----
    @staticmethod
    def _parent(index):
        return (index - 1) // 2

    @staticmethod
    def _left(index):
        return 2 * index + 1

    @staticmethod
    def _right(index):
        return 2 * index + 2

    def parent_value(self, index):
        p = self._parent(index)
        return self.data[p] if index > 0 else None

    def left_value(self, index):
        l = self._left(index)
        return self.data[l] if l < len(self.data) else None

    def right_value(self, index):
        r = self._right(index)
        return self.data[r] if r < len(self.data) else None

    # ---- Задание 8: sift up и вставка ----
    def _sift_up(self, index):
        while index > 0:
            parent = self._parent(index)
            if self.data[parent] <= self.data[index]:
                break
            self.data[parent], self.data[index] = self.data[index], self.data[parent]
            index = parent

    def push(self, value):
        self.data.append(value)
        self._sift_up(len(self.data) - 1)

    # ---- Задание 9: sift down и извлечение корня ----
    def _sift_down(self, index):
        size = len(self.data)
        while True:
            left = self._left(index)
            right = self._right(index)
            smallest = index

            if left < size and self.data[left] < self.data[smallest]:
                smallest = left
            if right < size and self.data[right] < self.data[smallest]:
                smallest = right
            if smallest == index:
                break

            self.data[index], self.data[smallest] = self.data[smallest], self.data[index]
            index = smallest

    def pop(self):
        """Извлекает и возвращает минимальный элемент (корень кучи)."""
        if not self.data:
            raise IndexError("pop from empty heap")

        top = self.data[0]
        last = self.data.pop()  # убираем последний элемент из массива
        if self.data:
            self.data[0] = last
            self._sift_down(0)
        return top

    def peek(self):
        return self.data[0] if self.data else None

    def __len__(self):
        return len(self.data)

    def __repr__(self):
        return f"MinHeap({self.data})"


if __name__ == "__main__":
    # Задание 7: представление кучи [2, 5, 7, 9, 11, 10, 15]
    heap = MinHeap()
    heap.data = [2, 5, 7, 9, 11, 10, 15]

    print("Задание 7: индексы и родственные значения")
    for i, value in enumerate(heap.data):
        print(
            f"index={i}, value={value}, "
            f"parent={heap.parent_value(i)}, "
            f"left={heap.left_value(i)}, right={heap.right_value(i)}"
        )

    # Задание 8: последовательная вставка
    print("\nЗадание 8: вставка значений 10, 4, 7, 1, 9, 3")
    heap2 = MinHeap()
    for v in [10, 4, 7, 1, 9, 3]:
        heap2.push(v)
        print(f"push({v}) -> {heap2.data}")

    # Задание 9: последовательное извлечение
    print("\nЗадание 9: последовательное извлечение корня")
    order = []
    while len(heap2):
        order.append(heap2.pop())
        print(f"pop() -> {order[-1]}, остаток: {heap2.data}")
    print(f"Порядок извлечения: {order}")
