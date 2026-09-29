"""
hash_table.py

Простая хеш-таблица с разрешением коллизий методом цепочек.
Задание 5, Задание 6.
"""


class HashTable:
    def __init__(self, table_size=10):
        self.table_size = table_size
        self.buckets = [[] for _ in range(table_size)]
        self.count = 0  # количество хранимых элементов (n)

    def _bucket_index(self, key):
        return hash(key) % self.table_size

    def set(self, key, value):
        """Добавляет новую пару (key, value) или обновляет существующий ключ."""
        index = self._bucket_index(key)
        bucket = self.buckets[index]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))
        self.count += 1

    def get(self, key):
        """Возвращает значение по ключу или None, если ключ отсутствует."""
        index = self._bucket_index(key)
        bucket = self.buckets[index]
        for k, v in bucket:
            if k == key:
                return v
        return None

    def remove(self, key):
        """Удаляет пару по ключу. Возвращает True, если элемент был удалён."""
        index = self._bucket_index(key)
        bucket = self.buckets[index]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                self.count -= 1
                return True
        return False

    @property
    def load_factor(self):
        """Коэффициент заполнения alpha = n / m."""
        return self.count / self.table_size

    def collision_count(self):
        """
        Количество элементов, размещённых в корзинах "сверх первого элемента".
        Если в корзине k элементов, k-1 из них считаются коллизиями.
        """
        total = 0
        for bucket in self.buckets:
            if len(bucket) > 1:
                total += len(bucket) - 1
        return total

    def max_chain_length(self):
        """Максимальная длина цепочки среди всех корзин."""
        return max((len(bucket) for bucket in self.buckets), default=0)

    def __repr__(self):
        rows = []
        for i, bucket in enumerate(self.buckets):
            rows.append(f"table[{i}] -> {bucket}")
        return "\n".join(rows)


if __name__ == "__main__":
    # Демонстрация: несколько ключей, попавших в одну корзину (Задание 5, п.6)
    ht = HashTable(table_size=5)
    demo_keys = [f"key_{i}" for i in range(20)]
    for i, k in enumerate(demo_keys):
        ht.set(k, i)

    print("Демонстрация хеш-таблицы (table_size=5, 20 ключей):")
    print(ht)
    print(f"n (count) = {ht.count}, load_factor = {ht.load_factor:.2f}")
    print(f"collision_count = {ht.collision_count()}")
    print(f"max_chain_length = {ht.max_chain_length()}")
