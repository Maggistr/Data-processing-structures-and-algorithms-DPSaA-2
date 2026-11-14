# -*- coding: utf-8 -*-
"""Лабораторная работа №4. Минимальное соединение и эвристический поиск пути."""
import heapq
import math
from collections import deque

# ====================== ЗАДАНИЕ 1: DSU + Краскал ======================
EDGES = [
    (4, 'A', 'B'), (3, 'A', 'C'), (1, 'B', 'C'), (2, 'B', 'D'),
    (4, 'C', 'D'), (2, 'C', 'E'), (3, 'D', 'E'), (2, 'D', 'F'),
    (3, 'E', 'F'), (6, 'E', 'G'), (1, 'F', 'G'),
]
VERTICES = ['A', 'B', 'C', 'D', 'E', 'F', 'G']


class DSU:
    def __init__(self, items):
        self.parent = {x: x for x in items}
        self.size = {x: 1 for x in items}

    def find(self, v):
        if self.parent[v] != v:
            self.parent[v] = self.find(self.parent[v])   # сжатие путей
        return self.parent[v]

    def union(self, a, b):
        a, b = self.find(a), self.find(b)
        if a == b:
            return False
        if self.size[a] < self.size[b]:                  # объединение по размеру
            a, b = b, a
        self.parent[b] = a
        self.size[a] += self.size[b]
        return True


def kruskal(vertices, edges):
    dsu = DSU(vertices)
    mst, total = [], 0
    for w, u, v in sorted(edges):
        if dsu.union(u, v):
            mst.append((u, v, w))
            total += w
            if len(mst) == len(vertices) - 1:
                break
    return mst, total


# ====================== Поле (задания 2-6) ======================
GRID = [
    "S..#........",
    ".#.#.######.",
    ".#...#......",
    ".###.#.####.",
    ".....#....#.",
    ".#####.##.#.",
    ".......##...",
    ".#####....#.",
    ".#...####.#.",
    ".#.#......#.",
    "...#.####...",
    "####......G.",
]
ROWS, COLS = len(GRID), len(GRID[0])
START, GOAL = (0, 0), (11, 10)
DIRS = [(1, 0), (-1, 0), (0, 1), (0, -1)]   # вниз, вверх, вправо, влево
HEAVY = {(6, 2), (6, 3), (6, 4), (6, 5), (6, 6)}


def neighbors(cell):
    r, c = cell
    for dr, dc in DIRS:
        nr, nc = r + dr, c + dc
        if 0 <= nr < ROWS and 0 <= nc < COLS and GRID[nr][nc] != '#':
            yield (nr, nc)


def step_cost(cell, weighted=False):
    return 5 if (weighted and cell in HEAVY) else 1


def restore(parent, goal):
    path, cur = [], goal
    while cur is not None:
        path.append(cur)
        cur = parent[cur]
    return path[::-1]


def path_cost(path, weighted=False):
    return sum(step_cost(c, weighted) for c in path[1:])


def draw(path):
    g = [list(row) for row in GRID]
    for r, c in path:
        if (r, c) not in (START, GOAL):
            g[r][c] = '*'
    return "\n".join("".join(row) for row in g)


# ---------- Задание 2: BFS ----------
def bfs(start=START, goal=GOAL):
    parent = {start: None}
    q = deque([start])
    processed = 0
    while q:
        cur = q.popleft()
        processed += 1
        if cur == goal:
            return restore(parent, goal), processed
        for nb in neighbors(cur):
            if nb not in parent:
                parent[nb] = cur
                q.append(nb)
    return None, processed


# ---------- Задание 3: эвристики ----------
def manhattan(a, b=GOAL):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def euclidean(a, b=GOAL):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


# ---------- Задание 4: Greedy Best-First ----------
def greedy(h=manhattan, start=START, goal=GOAL):
    parent = {start: None}
    open_heap = [(h(start), 0, start)]
    closed = set()
    cnt = 0                     # счётчик для стабильного разрешения равных приоритетов (FIFO)
    processed = 0
    while open_heap:
        _, _, cur = heapq.heappop(open_heap)
        if cur in closed:
            continue
        closed.add(cur)
        processed += 1
        if cur == goal:
            return restore(parent, goal), processed
        for nb in neighbors(cur):
            if nb not in parent:
                parent[nb] = cur
                cnt += 1
                heapq.heappush(open_heap, (h(nb), cnt, nb))
    return None, processed


# ---------- Задание 5: A* ----------
def astar(h=manhattan, weighted=False, start=START, goal=GOAL):
    g = {start: 0}
    parent = {start: None}
    open_heap = [(h(start), 0, start)]
    closed = set()
    cnt = 0
    processed = 0
    while open_heap:
        f, _, cur = heapq.heappop(open_heap)
        if cur in closed:
            continue
        closed.add(cur)
        processed += 1
        if cur == goal:
            return restore(parent, goal), processed
        for nb in neighbors(cur):
            ng = g[cur] + step_cost(nb, weighted)
            if nb not in g or ng < g[nb]:
                g[nb] = ng
                parent[nb] = cur
                cnt += 1
                heapq.heappush(open_heap, (ng + h(nb), cnt, nb))
    return None, processed


# ---------- Дейкстра (для задания 6) ----------
def dijkstra(weighted=False, start=START, goal=GOAL):
    dist = {start: 0}
    parent = {start: None}
    open_heap = [(0, 0, start)]
    closed = set()
    cnt = 0
    processed = 0
    while open_heap:
        d, _, cur = heapq.heappop(open_heap)
        if cur in closed:
            continue
        closed.add(cur)
        processed += 1
        if cur == goal:
            return restore(parent, goal), processed
        for nb in neighbors(cur):
            nd = d + step_cost(nb, weighted)
            if nb not in dist or nd < dist[nb]:
                dist[nb] = nd
                parent[nb] = cur
                cnt += 1
                heapq.heappush(open_heap, (nd, cnt, nb))
    return None, processed


def show(title, path, processed, weighted=False):
    print(f"{title}: стоимость={path_cost(path, weighted)}, шагов={len(path) - 1}, "
          f"обработано={processed}")


def main():
    print("=" * 60, "\nЗАДАНИЕ 1\n" + "=" * 60)
    mst, total = kruskal(VERTICES, EDGES)
    for u, v, w in mst:
        print(f"  {u}-{v}: {w}")
    print("Вес MST =", total)

    print("\n" + "=" * 60, "\nЗАДАНИЕ 2 (BFS)\n" + "=" * 60)
    p_bfs, n_bfs = bfs()
    print("Путь:", p_bfs)
    show("BFS", p_bfs, n_bfs)
    print(draw(p_bfs))

    print("\n" + "=" * 60, "\nЗАДАНИЕ 3 (эвристики до G)\n" + "=" * 60)
    for cell in [(0, 0), (6, 0), (6, 6), (7, 9), (11, 9)]:
        print(f"  {cell}: manhattan={manhattan(cell)}, euclidean={euclidean(cell):.3f}")

    print("\n" + "=" * 60, "\nЗАДАНИЕ 4 (Greedy, Manhattan)\n" + "=" * 60)
    p_gr, n_gr = greedy(manhattan)
    print("Путь:", p_gr)
    show("Greedy", p_gr, n_gr)
    print(draw(p_gr))

    print("\n" + "=" * 60, "\nЗАДАНИЕ 5 (A*)\n" + "=" * 60)
    p_am, n_am = astar(manhattan)
    p_ae, n_ae = astar(euclidean)
    show("A* Manhattan", p_am, n_am)
    print(draw(p_am))
    show("A* Euclidean", p_ae, n_ae)
    print(draw(p_ae))

    print("\n" + "=" * 60, "\nЗАДАНИЕ 6\n" + "=" * 60)
    p_dj, n_dj = dijkstra()
    print("--- Единичные стоимости ---")
    show("BFS", p_bfs, n_bfs)
    show("Dijkstra", p_dj, n_dj)
    show("Greedy", p_gr, n_gr)
    show("A* Manhattan", p_am, n_am)
    show("A* Euclidean", p_ae, n_ae)

    print("--- Взвешенное поле (клетки (6,2)-(6,6) стоят 5) ---")
    pw_dj, nw_dj = dijkstra(weighted=True)
    pw_a, nw_a = astar(manhattan, weighted=True)
    show("Dijkstra", pw_dj, nw_dj, True)
    print(draw(pw_dj))
    show("A* Manhattan", pw_a, nw_a, True)
    print(draw(pw_a))
    print(f"BFS-маршрут на взвешенном поле: стоимость={path_cost(p_bfs, True)}, шагов={len(p_bfs) - 1}")
    print("BFS-маршрут проходит по тяжёлым клеткам:", sorted(set(p_bfs) & HEAVY))
    print("Маршрут Дейкстры проходит по тяжёлым клеткам:", sorted(set(pw_dj) & HEAVY))


if __name__ == "__main__":
    main()
