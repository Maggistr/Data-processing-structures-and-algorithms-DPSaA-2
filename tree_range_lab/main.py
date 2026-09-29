import random
import time

from bst import (Node, insert, build_bst, search, preorder, inorder, postorder,
                 delete, height, show)
from avl import avl_from, balance_factor, node_height
from range_queries import (range_sum_naive, build_prefix, range_sum_prefix,
                           FenwickTree, SegmentTree, SegmentTreeSMM)
from sensors import SensorAnalyzer, SensorSeries

random.seed(42)


def title(s):
    print("\n" + "=" * 70 + f"\n{s}\n" + "=" * 70)


KEYS = [8, 4, 12, 2, 6, 10, 14]

# ---------------------------------------------------------------- 1
title("Задание 1. Ручное создание бинарного дерева")
root = Node(8)
root.left, root.right = Node(4), Node(12)
root.left.left, root.left.right = Node(2), Node(6)
root.right.left, root.right.right = Node(10), Node(14)
print("Корень:", root.key)
print("Потомки корня:", root.left.key, root.right.key)
print("Лист (левый потомок узла 4):", root.left.left.key)

# ---------------------------------------------------------------- 2
title("Задание 2. Вставка в BST")
bst = build_bst(KEYS)
print("Вставка:", KEYS)
print("Дерево (повёрнуто на 90°, правое поддерево сверху):")
print(show(bst))

# ---------------------------------------------------------------- 3
title("Задание 3. Поиск с подсчётом посещённых узлов")
for key, desc in [(12, "близко к корню"), (14, "нижний уровень"), (7, "отсутствует")]:
    node, visited = search(bst, key)
    print(f"search({key:>2}) [{desc}]: найден={node is not None}, посещено узлов={visited}")

# ---------------------------------------------------------------- 4
title("Задание 4. Обходы")
print("preorder :", preorder(bst))
print("inorder  :", inorder(bst))
print("postorder:", postorder(bst))

# ---------------------------------------------------------------- 5
title("Задание 5. Удаление")
t = build_bst(KEYS)
t = delete(t, 2)
print("Удалён лист 2          -> inorder:", inorder(t), "| preorder:", preorder(t))
t = build_bst(KEYS + [1])                       # у узла 2 появился один потомок (1)
print("Подготовка: добавлен 1, у узла 2 один потомок; preorder:", preorder(t))
t = delete(t, 2)
print("Удалён узел 2 (1 потомок) -> preorder:", preorder(t))
t = delete(t, 8)                                 # корень с двумя потомками
print("Удалён корень 8 (2 потомка), преемник = 10 -> preorder:", preorder(t), "| inorder:", inorder(t))
print("Дерево:")
print(show(t))

# ---------------------------------------------------------------- 6
title("Задание 6. Порядок вставки и высота")
seq1 = [8, 4, 12, 2, 6, 10, 14]
seq2 = [2, 4, 6, 8, 10, 12, 14]
t1, t2 = build_bst(seq1), build_bst(seq2)
for name, tr, seq in [("Дерево 1 (сбалансированное)", t1, seq1), ("Дерево 2 (отсортированный ввод)", t2, seq2)]:
    _, v = search(tr, seq[-1])
    print(f"{name}: высота={height(tr)}, поиск {seq[-1]} -> посещено {v}")
print("Дерево 2:")
print(show(t2))

# ---------------------------------------------------------------- 7
title("Задание 7. AVL: баланс-факторы и повороты")
for name, seq in [("LL", [30, 20, 10]), ("RR", [10, 20, 30]), ("LR", [30, 10, 20]), ("RL", [10, 30, 20])]:
    # без балансировки
    plain = build_bst(seq)
    log = []
    avl = avl_from(seq, log)
    print(f"\n{name}: вставка {seq}")
    print(f"  до балансировки : preorder={preorder(plain)}, высота={height(plain)}")
    print(f"  действие        : {log[0] if log else 'нет'}")
    print(f"  после           : preorder={preorder(avl)}, высота={height(avl)}, "
          f"баланс-факторы корня/левого/правого = "
          f"{balance_factor(avl)}/{balance_factor(avl.left)}/{balance_factor(avl.right)}")

# ---------------------------------------------------------------- 8-9
N, Q = 200_000, 2000
data = [random.randint(-1000, 1000) for _ in range(N)]
queries = []
for _ in range(Q):
    l = random.randrange(N)
    r = random.randrange(l, N)
    queries.append((l, r))

title(f"Задание 8. Наивные запросы (N={N}, запросов={Q})")
t0 = time.perf_counter()
naive = [range_sum_naive(data, l, r) for l, r in queries]
t_naive = time.perf_counter() - t0
print(f"Время: {t_naive:.4f} с")

title("Задание 9. Префиксные суммы")
t0 = time.perf_counter()
prefix = build_prefix(data)
t_build = time.perf_counter() - t0
t0 = time.perf_counter()
pref = [range_sum_prefix(prefix, l, r) for l, r in queries]
t_pref = time.perf_counter() - t0
print(f"Построение prefix: {t_build:.4f} с")
print(f"{Q} запросов     : {t_pref:.6f} с")
print(f"Результаты совпадают с наивными: {naive == pref}")
print(f"Ускорение запросов: {t_naive / t_pref:.0f}x; с учётом построения: {t_naive / (t_pref + t_build):.1f}x")
small = [4, 2, 7, 1, 8, 3, 6]
p = build_prefix(small)
print("\nДемонстрация неактуальности после изменения (small =", small, ")")
print("prefix до    :", p)
small[2] = 17
print("small[2] = 17, prefix (не пересчитан):", p)
print("prefix пересчитан                    :", build_prefix(small))

# ---------------------------------------------------------------- 10
title("Задание 10. Дерево Фенвика")
test = [4, 2, 7, 1, 8, 3, 6]
fw = FenwickTree(test)
print("Массив:", test, "| внутренний массив:", fw.tree)
for l, r in [(0, 6), (2, 5), (3, 3), (1, 4), (0, 0)]:
    print(f"range_sum({l},{r}) = {fw.range_sum(l, r)}, sum() = {sum(test[l:r+1])}")
fw.update(2, +10)
test[2] += 10
print("update(2, +10): range_sum(2,5) =", fw.range_sum(2, 5), ", sum() =", sum(test[2:6]))
print("Проверка низкого бита i & -i:", {i: i & -i for i in range(1, 9)})
fw_big = FenwickTree(data)
t0 = time.perf_counter()
fw_res = [fw_big.range_sum(l, r) for l, r in queries]
t_fw = time.perf_counter() - t0
print(f"На больших данных: {Q} запросов = {t_fw:.4f} с, совпадает с наивными: {fw_res == naive}")

# ---------------------------------------------------------------- 11
title("Задание 11. Дерево отрезков (сумма)")
arr = [5, 3, 8, 6, 2, 7, 4, 1, 9, 10]
st = SegmentTree(arr)
for l, r in [(0, 9), (2, 5), (4, 4), (3, 8), (1, 7), (6, 9)]:
    print(f"query({l},{r}) = {st.query(l, r)}, sum() = {sum(arr[l:r+1])}")
st.update(3, 100)
arr[3] = 100
print("update(3, 100):")
for l, r in [(0, 9), (2, 5), (3, 3)]:
    print(f"query({l},{r}) = {st.query(l, r)}, sum() = {sum(arr[l:r+1])}")

# ---------------------------------------------------------------- 12
title("Задание 12. Сумма, минимум, максимум")
arr = [5, 3, 8, 6, 2, 7, 4, 1, 9, 10]
sm = SegmentTreeSMM(arr)
for l, r in [(0, 9), (0, 0), (2, 5), (7, 7), (3, 8)]:
    seg = arr[l:r + 1]
    print(f"query({l},{r}) = (sum={sm.query(l, r)[0]}, min={sm.query(l, r)[1]}, max={sm.query(l, r)[2]}); "
          f"проверка: ({sum(seg)}, {min(seg)}, {max(seg)})")
sm.update(4, -50)
arr[4] = -50
print("После update(4, -50): query(0,9) =", sm.query(0, 9), "| проверка:", (sum(arr), min(arr), max(arr)))

# ---------------------------------------------------------------- 13
title("Задание 13. Анализ измерений датчиков")
an = SensorAnalyzer()
sensor_ids = [50, 20, 80, 10, 30, 70, 90, 60, 40]
series = {}
for sid in sensor_ids:
    m = [round(random.gauss(20 + sid / 10, 3), 2) for _ in range(1200)]
    an.add_sensor(sid, m)
print("Датчики (inorder):", an.sorted_ids())
for sid in (70, 35):
    val, visited = an.find(sid)
    print(f"find({sid}): {'найден, измерений=' + str(len(val)) if val else 'не найден'}, посещено узлов={visited}")

measurements, _ = an.find(70)
ss = SensorSeries(measurements)
L, R = 100, 899
print(f"\nДатчик 70, диапазон [{L}, {R}] до обновления:")
print(f"  naive   : {ss.sum_naive(L, R):.2f}")
print(f"  prefix  : {ss.sum_prefix(L, R):.2f}")
print(f"  fenwick : {ss.sum_fenwick(L, R):.2f}")
s, mn, mx = ss.sum_min_max(L, R)
print(f"  segment : sum={s:.2f}, min={mn}, max={mx}")
idx, newv = 500, 999.0
print(f"\nОбновление: измерение #{idx}: {ss.data[idx]} -> {newv}")
ss.update(idx, newv)
print(f"После обновления, диапазон [{L}, {R}]:")
print(f"  naive   : {ss.sum_naive(L, R):.2f}")
print(f"  prefix  : {ss.sum_prefix(L, R):.2f}  (после пересчёта O(n))")
print(f"  fenwick : {ss.sum_fenwick(L, R):.2f}")
s, mn, mx = ss.sum_min_max(L, R)
print(f"  segment : sum={s:.2f}, min={mn}, max={mx}")
print(f"  проверка min/max: {min(ss.data[L:R+1])}, {max(ss.data[L:R+1])}")
ok = all(abs(ss.sum_naive(a, b) - ss.sum_fenwick(a, b)) < 1e-6 and abs(ss.sum_naive(a, b) - ss.sum_min_max(a, b)[0]) < 1e-6
         for a, b in [(0, 1199), (10, 20), (500, 500), (300, 700)])
print("Согласованность структур на контрольных запросах:", ok)
