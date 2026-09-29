"""
main.py

Основной файл проекта fast_data_access.
Задания 2, 3, 4, 10, 11, 12.
Запуск: python main.py
"""

import random
import heapq
import itertools
from time import perf_counter

from hash_table import HashTable
from binary_heap import MinHeap


def section(title):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


# ---------------------------------------------------------------------
# Задание 2: доступ по индексу и линейный поиск
# ---------------------------------------------------------------------
def task2():
    section("Задание 2: доступ по индексу и линейный поиск")

    N = 100_000
    numbers = list(range(N))
    random.shuffle(numbers)  # чтобы поиск не был тривиальным по позиции значения

    def linear_search(numbers, target):
        for index, value in enumerate(numbers):
            if value == target:
                return index
        return -1

    # доступ по индексу: начало, середина, конец
    idx_start, idx_mid, idx_end = 0, N // 2, N - 1

    t0 = perf_counter()
    for _ in range(100_000):
        _ = numbers[idx_start]
        _ = numbers[idx_mid]
        _ = numbers[idx_end]
    t_index = (perf_counter() - t0) / (100_000 * 3)

    # цели для линейного поиска: значение в начале, середине, конце и отсутствующее
    target_start = numbers[0]
    target_mid = numbers[N // 2]
    target_end = numbers[-1]
    target_missing = -1  # такого значения в списке нет (список содержит 0..N-1)

    targets = {
        "начало": target_start,
        "середина": target_mid,
        "конец": target_end,
        "отсутствует": target_missing,
    }

    results = {}
    for name, target in targets.items():
        t0 = perf_counter()
        idx = linear_search(numbers, target)
        t_search = perf_counter() - t0
        results[name] = (idx, t_search)

    print(f"Размер списка: {N}")
    print(f"Среднее время доступа по индексу (numbers[i]): {t_index * 1e9:.1f} нс")
    print("\nЛинейный поиск:")
    for name, (idx, t_search) in results.items():
        print(f"  target={name:12s} найден index={idx:>8}  время={t_search * 1000:.3f} мс")

    print(
        "\nВывод: доступ по индексу занимает наносекунды и не зависит от N (O(1)),\n"
        "т.к. адрес элемента вычисляется напрямую по индексу. Линейный поиск\n"
        "требует в худшем случае (элемент в конце или отсутствует) просмотра\n"
        "всех N элементов — O(n), поэтому время растёт пропорционально N и на\n"
        "3-4 порядка больше, чем прямой доступ по индексу."
    )


# ---------------------------------------------------------------------
# Задание 3: доступ по ключу (список против словаря)
# ---------------------------------------------------------------------
def task3():
    section("Задание 3: доступ по ключу (список vs словарь)")

    N = 10_000
    records = [(i, f"value_{i}") for i in range(N)]
    random.shuffle(records)

    lookup_dict = {id_: value for id_, value in records}

    def linear_find(records, target_id):
        for id_, value in records:
            if id_ == target_id:
                return value
        return None

    NUM_QUERIES = 2_000
    query_ids = [random.randrange(N) for _ in range(NUM_QUERIES)]

    t0 = perf_counter()
    for qid in query_ids:
        linear_find(records, qid)
    t_list = perf_counter() - t0

    t0 = perf_counter()
    for qid in query_ids:
        _ = lookup_dict.get(qid)
    t_dict = perf_counter() - t0

    print(f"Записей: {N}, запросов: {NUM_QUERIES}")
    print(f"Поиск по списку (перебор):  {t_list * 1000:.2f} мс")
    print(f"Поиск по словарю (dict):    {t_dict * 1000:.4f} мс")
    if t_dict > 0:
        print(f"Словарь быстрее примерно в {t_list / t_dict:.0f} раз")

    print(
        "\nВывод: словарь оправдан, когда требуется МНОГОКРАТНЫЙ поиск записей\n"
        "по уникальному ключу в большом наборе данных (например, поиск\n"
        "пользователя по id, товара по артикулу). Список с перебором приемлем\n"
        "только для единичных обращений или очень малых наборов данных."
    )


# ---------------------------------------------------------------------
# Задание 4: исследование функции hash()
# ---------------------------------------------------------------------
def task4():
    section("Задание 4: исследование функции hash()")

    def bucket_index(key, table_size):
        return hash(key) % table_size

    print("Хеши нескольких значений:")
    for value in [10, 205, "student_205", "hello", 3.14]:
        print(f"  hash({value!r}) = {hash(value)}")

    print("\nПовтор вычисления для одинаковых ключей в рамках запуска:")
    key = "student_205"
    print(f"  hash({key!r}) первый раз:  {hash(key)}")
    print(f"  hash({key!r}) второй раз: {hash(key)}  (совпадает)")

    table_size = 10
    keys = [f"user_{i}" for i in range(30)]
    print(f"\nbucket_index(key, {table_size}) для 30 ключей:")

    buckets = {}
    for k in keys:
        idx = bucket_index(k, table_size)
        buckets.setdefault(idx, []).append(k)
        print(f"  {k:10s} -> корзина {idx}")

    print("\nКорзины с более чем одним ключом (коллизии):")
    for idx, ks in sorted(buckets.items()):
        if len(ks) > 1:
            print(f"  корзина {idx}: {ks}")


# ---------------------------------------------------------------------
# Задание 6: коэффициент заполнения и коллизии (использует HashTable)
# ---------------------------------------------------------------------
def task6():
    section("Задание 6: коэффициент заполнения и коллизии")

    NUM_KEYS = 300
    keys = [f"item_{i}_{random.randint(0, 10**6)}" for i in range(NUM_KEYS)]

    print(f"{'Размер таблицы':>15} | {'n':>5} | {'load_factor':>11} | "
          f"{'коллизии':>9} | {'макс. цепочка':>13}")
    for size in (10, 100, 1000):
        ht = HashTable(table_size=size)
        for i, k in enumerate(keys):
            ht.set(k, i)
        print(f"{size:>15} | {ht.count:>5} | {ht.load_factor:>11.3f} | "
              f"{ht.collision_count():>9} | {ht.max_chain_length():>13}")

    print(
        "\nВывод: при фиксированном числе ключей увеличение количества корзин\n"
        "снижает коэффициент заполнения и число коллизий, так как ключи\n"
        "распределяются по большему числу цепочек. При малом числе корзин\n"
        "(например, 10) цепочки получаются длинными, и поиск в них\n"
        "приближается по стоимости к линейному O(n)."
    )


# ---------------------------------------------------------------------
# Задание 10: приоритетная очередь
# ---------------------------------------------------------------------
def task10():
    section("Задание 10: приоритетная очередь (heapq)")

    tasks = []
    counter = itertools.count()  # для сохранения порядка поступления

    task_list = [
        (2, "Проверить лабораторную"),
        (1, "Исправить критическую ошибку"),
        (3, "Обновить документацию"),
        (1, "Ответить на письмо студента"),
        (5, "Подготовить лекцию"),
        (2, "Заполнить журнал"),
        (1, "Настроить сервер"),
        (4, "Согласовать расписание"),
    ]

    for priority, description in task_list:
        heapq.heappush(tasks, (priority, next(counter), description))

    print("Добавлено задач:", len(task_list))
    print("\nПорядок обработки (извлечение из очереди):")
    while tasks:
        priority, order, description = heapq.heappop(tasks)
        print(f"  priority={priority}  #{order:02d}  {description}")

    print(
        "\nЗадачи с одинаковым приоритетом (1 и 2) извлекаются в порядке их\n"
        "добавления благодаря дополнительному счётчику `counter`, который\n"
        "выступает вторым ключом сортировки в кортеже и не даёт heapq\n"
        "сравнивать строки описаний напрямую."
    )


# ---------------------------------------------------------------------
# Задание 11 и 12: Top-K через сортировку и через кучу
# ---------------------------------------------------------------------
def top_k_sorted(data, k):
    return sorted(data, reverse=True)[:k]


def top_k_heap(data, k):
    """Top-K без полной сортировки: min-heap размером не более k."""
    heap = []
    for value in data:
        if len(heap) < k:
            heapq.heappush(heap, value)
        elif value > heap[0]:
            heapq.heapreplace(heap, value)
    return heap


def task11_12():
    section("Задание 11 и 12: Top-K (полная сортировка vs куча)")

    N = 100_000
    data = [random.randint(0, 10_000_000) for _ in range(N)]

    print(f"{'K':>6} | {'sort, мс':>10} | {'heap, мс':>10} | {'совпадают?':>10}")
    for k in (10, 100, 1000):
        t0 = perf_counter()
        result_sorted = top_k_sorted(data, k)
        t_sorted = perf_counter() - t0

        t0 = perf_counter()
        result_heap = top_k_heap(data, k)
        t_heap = perf_counter() - t0

        match = sorted(result_heap, reverse=True) == result_sorted
        print(f"{k:>6} | {t_sorted * 1000:>10.2f} | {t_heap * 1000:>10.2f} | {str(match):>10}")

    print(
        "\nВывод: при K << N поиск Top-K через кучу размера K (сложность\n"
        "O(n log K)) заметно быстрее полной сортировки (O(n log n)), так как\n"
        "куча хранит и обновляет только K элементов, а не весь набор данных.\n"
        "Преимущество кучи растёт с увеличением N при фиксированном K и\n"
        "уменьшается по мере приближения K к N (при K ~ N выгоднее просто\n"
        "отсортировать весь массив)."
    )


if __name__ == "__main__":
    task2()
    task3()
    task4()
    task6()
    task10()
    task11_12()
