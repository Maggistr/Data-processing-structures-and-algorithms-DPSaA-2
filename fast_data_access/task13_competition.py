"""
task13_competition.py

Задание 13: Самостоятельная работа.
Система обработки результатов соревнования.

Используемые структуры данных и обоснование:

- Поиск участника по id -> dict.
  Обоснование: id уникален, требуется быстрый доступ O(1) в среднем
  для добавления/обновления/чтения записи участника. Это классический
  сценарий "доступ по ключу", для которого хеш-таблица (dict) подходит
  лучше, чем список с линейным поиском O(n).

- Очередь результатов, ожидающих проверки -> heapq (приоритетная очередь).
  Обоснование: меньший номер приоритета = более срочная проверка,
  то есть нужен постоянный быстрый доступ к элементу с минимальным
  приоритетом и возможность добавлять новые заявки в любой момент.
  Бинарная куча даёт O(log n) на вставку и извлечение минимума, что
  эффективнее, чем поддержание отсортированного списка.

- Top-K участников по результату -> min-heap размера K, реализованный
  вручную (без heapq.nlargest и без полной сортировки).
  Обоснование: если K существенно меньше числа участников n, куча
  размера K позволяет получить Top-K за O(n log K), а не O(n log n),
  как при полной сортировке.
"""

import itertools


class CompetitionSystem:
    def __init__(self):
        # dict: id -> {"name": ..., "score": ...}
        self.participants = {}

        # приоритетная очередь заявок на проверку: (priority, order, participant_id)
        self._review_queue = []
        self._counter = itertools.count()

    # ------------------------------------------------------------------
    # 1-2. Хранение участников: быстрый доступ и обновление по id (dict)
    # ------------------------------------------------------------------
    def add_or_update_participant(self, participant_id, name, score):
        """Использованная структура данных: dict (хеш-таблица)."""
        self.participants[participant_id] = {"name": name, "score": score}
        print(f"[dict] Участник id={participant_id} '{name}' (score={score}) сохранён/обновлён")

    def get_participant(self, participant_id):
        """Использованная структура данных: dict (хеш-таблица)."""
        return self.participants.get(participant_id)

    # ------------------------------------------------------------------
    # 3. Очередь результатов, ожидающих проверки (heapq, min-heap)
    # ------------------------------------------------------------------
    def submit_for_review(self, participant_id, priority):
        """
        Меньший priority — более срочная проверка.
        Использованная структура данных: приоритетная очередь (heapq).
        """
        import heapq
        heapq.heappush(self._review_queue, (priority, next(self._counter), participant_id))
        print(f"[heapq] Заявка участника id={participant_id} добавлена в очередь "
              f"(приоритет={priority})")

    def process_next_review(self):
        """Извлекает следующую по срочности заявку на проверку."""
        import heapq
        if not self._review_queue:
            return None
        priority, order, participant_id = heapq.heappop(self._review_queue)
        participant = self.participants.get(participant_id)
        name = participant["name"] if participant else "неизвестен"
        print(f"[heapq] Проверка заявки id={participant_id} '{name}' "
              f"(приоритет={priority})")
        return participant_id

    # ------------------------------------------------------------------
    # 4. Top-K участников по результату без полной сортировки
    # ------------------------------------------------------------------
    def top_k_by_score(self, k):
        """
        Top-K реализован вручную через min-heap размера k (без nlargest,
        без sorted() всего набора данных).
        Использованная структура данных: бинарная куча (min-heap) размера K.
        """
        import heapq

        heap = []  # элементы вида (score, participant_id)
        for pid, info in self.participants.items():
            score = info["score"]
            if len(heap) < k:
                heapq.heappush(heap, (score, pid))
            elif score > heap[0][0]:
                heapq.heapreplace(heap, (score, pid))

        # сортируем только K элементов (а не весь набор) для красивого вывода
        result = sorted(heap, key=lambda item: item[0], reverse=True)
        print(f"[min-heap size {k}] Top-{k} участников по результату:")
        for score, pid in result:
            name = self.participants[pid]["name"]
            print(f"  id={pid:3d}  {name:12s}  score={score}")
        return result


if __name__ == "__main__":
    system = CompetitionSystem()

    demo_names = [
        "Иванов", "Петров", "Сидорова", "Кузнецов", "Смирнова",
        "Попов", "Васильева", "Соколов", "Михайлова", "Новиков",
    ]

    print("=== Добавление участников ===")
    for pid, name in enumerate(demo_names, start=1):
        score = (pid * 37) % 100  # детерминированные "случайные" очки для примера
        system.add_or_update_participant(pid, name, score)

    print("\n=== Обновление результата участника id=3 ===")
    system.add_or_update_participant(3, "Сидорова", 95)

    print("\n=== Постановка заявок в очередь проверки ===")
    review_priorities = {1: 2, 2: 1, 3: 3, 4: 1, 5: 2}
    for pid, priority in review_priorities.items():
        system.submit_for_review(pid, priority)

    print("\n=== Обработка очереди проверки (по срочности) ===")
    while True:
        pid = system.process_next_review()
        if pid is None:
            break

    print("\n=== Top-3 участников по результату ===")
    system.top_k_by_score(3)
