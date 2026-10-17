import heapq
import sys
from collections import defaultdict

sys.setrecursionlimit(10000)
INF = float("inf")
N = 8

edges = [
    (0, 1, 4), (0, 2, 8), (1, 2, 1), (2, 0, 3), (2, 3, 2),
    (3, 4, 2), (4, 5, 3), (5, 3, 1), (5, 6, 4), (6, 7, 2),
]


def build_directed(edge_list, n=N):
    g = {v: [] for v in range(n)}
    for u, v, _ in edge_list:
        g[u].append(v)
    return g


def build_undirected(edge_list, n=N):
    pairs = {frozenset((u, v)) for u, v, _ in edge_list}  # дубликаты хранятся один раз
    g = {v: [] for v in range(n)}
    for p in sorted(map(sorted, pairs)):
        u, v = p
        g[u].append(v)
        g[v].append(u)
    return g


def dfs_order(g, start):
    visited, order = set(), []

    def dfs(v):
        visited.add(v)
        order.append(v)
        for to in g[v]:
            if to not in visited:
                dfs(to)

    dfs(start)
    return order


def components(g):
    visited, comps = set(), []
    for v in g:
        if v not in visited:
            comp = []

            def dfs(x):
                visited.add(x)
                comp.append(x)
                for to in g[x]:
                    if to not in visited:
                        dfs(to)

            dfs(v)
            comps.append(sorted(comp))
    return comps


def task1():
    print("=== Задание 1 ===")
    g = build_directed(edges)
    gu = build_undirected(edges)
    print("G :", g)
    print("Gu:", gu)
    print("Порядок DFS из 0:", dfs_order(gu, 0))
    print("Компоненты Gu:", components(gu), "->", len(components(gu)))
    gu2 = {v: list(a) for v, a in gu.items()}
    gu2[5].remove(6)
    gu2[6].remove(5)
    c = components(gu2)
    print("Без ребра {5,6}:", c, "->", len(c))


def kosaraju(g):
    visited, order = set(), []

    def dfs1(v):
        visited.add(v)
        for to in g[v]:
            if to not in visited:
                dfs1(to)
        order.append(v)

    for v in g:
        if v not in visited:
            dfs1(v)

    gt = {v: [] for v in g}
    for u in g:
        for v in g[u]:
            gt[v].append(u)

    visited, comps = set(), []

    def dfs2(v, comp):
        visited.add(v)
        comp.append(v)
        for to in gt[v]:
            if to not in visited:
                dfs2(to, comp)

    for v in reversed(order):
        if v not in visited:
            comp = []
            dfs2(v, comp)
            comps.append(sorted(comp))
    return comps


def task2():
    print("\n=== Задание 2 ===")
    comps = kosaraju(build_directed(edges))
    for i, c in enumerate(comps):
        print(f"SCC {i}: {c}")
    return comps


def bridges_and_cut_points(g):
    tin, low = {}, {}
    timer = [0]
    bridges, cuts = [], set()
    visited = set()

    def dfs(v, p):
        visited.add(v)
        tin[v] = low[v] = timer[0]
        timer[0] += 1
        children = 0
        for to in g[v]:
            if to == p:
                continue
            if to in visited:
                low[v] = min(low[v], tin[to])
            else:
                dfs(to, v)
                low[v] = min(low[v], low[to])
                if low[to] > tin[v]:
                    bridges.append(tuple(sorted((v, to))))
                if low[to] >= tin[v] and p != -1:
                    cuts.add(v)
                children += 1
        if p == -1 and children > 1:
            cuts.add(v)

    for v in g:
        if v not in visited:
            dfs(v, -1)
    return tin, low, sorted(bridges), sorted(cuts)


def task3():
    print("\n=== Задание 3 ===")
    gu = build_undirected(edges)
    tin, low, br, cuts = bridges_and_cut_points(gu)
    print("v  tin low")
    for v in range(N):
        print(f"{v}  {tin[v]:>3} {low[v]:>3}")
    print("Мосты:", br)
    print("Точки сочленения:", cuts)
    u, v = br[0]
    g2 = {x: list(a) for x, a in gu.items()}
    g2[u].remove(v)
    g2[v].remove(u)
    print(f"Удалён мост {{{u},{v}}}: компонент {len(components(gu))} -> {len(components(g2))}")


def condensation(g, comps):
    comp_of = {v: i for i, c in enumerate(comps) for v in c}
    cg = {i: set() for i in range(len(comps))}
    for u in g:
        for v in g[u]:
            if comp_of[u] != comp_of[v]:
                cg[comp_of[u]].add(comp_of[v])
    return {i: sorted(s) for i, s in cg.items()}, comp_of


def topo_sort(g):
    state = {v: 0 for v in g}
    result = []

    def dfs(v):
        state[v] = 1
        for to in g[v]:
            if state[to] == 1:
                return True
            if state[to] == 0 and dfs(to):
                return True
        state[v] = 2
        result.append(v)
        return False

    for v in g:
        if state[v] == 0 and dfs(v):
            return None
    return result[::-1]


def task4(comps):
    print("\n=== Задание 4 ===")
    g = build_directed(edges)
    cg, comp_of = condensation(g, comps)
    print("Компоненты:", {i: c for i, c in enumerate(comps)})
    print("Граф конденсации:", cg)
    order = topo_sort(cg)
    print("Топологический порядок (id):", order)
    print("Топологический порядок (компоненты):", [comps[i] for i in order])
    cg2 = {i: list(a) for i, a in cg.items()}
    cg2[comp_of[7]].append(comp_of[3])
    print("После добавления ребра comp(7) -> comp(3):", cg2)
    res = topo_sort(cg2)
    print("Цикл обнаружен, топологическая сортировка невозможна" if res is None else res)


def dijkstra(edge_list, start, n=N):
    adj = defaultdict(list)
    for u, v, w in edge_list:
        adj[u].append((v, w))
    dist = [INF] * n
    parent = [None] * n
    dist[start] = 0
    heap = [(0, start)]
    while heap:
        d, v = heapq.heappop(heap)
        if d > dist[v]:
            continue
        for to, w in adj[v]:
            if dist[to] > d + w:
                dist[to] = d + w
                parent[to] = v
                heapq.heappush(heap, (dist[to], to))
    return dist, parent


def restore_path(parent, s, t):
    path = []
    v = t
    while v is not None:
        path.append(v)
        v = parent[v]
    path.reverse()
    return path if path and path[0] == s else []


def task5():
    print("\n=== Задание 5 ===")
    dist, parent = dijkstra(edges, 0)
    print("Расстояния:", dist)
    print("parent:", parent)
    p = restore_path(parent, 0, 7)
    print("Путь 0->7:", " -> ".join(map(str, p)), "| длина:", dist[7])
    return dist


def bellman_ford(edge_list, start, n=N):
    dist = [INF] * n
    dist[start] = 0
    for _ in range(n - 1):
        changed = False
        for u, v, w in edge_list:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                changed = True
        if not changed:
            break
    neg_cycle = any(dist[u] != INF and dist[u] + w < dist[v] for u, v, w in edge_list)
    return dist, neg_cycle


def task6():
    print("\n=== Задание 6 ===")
    e1 = [(u, v, -2 if (u, v) == (2, 3) else w) for u, v, w in edges]
    d, neg = bellman_ford(e1, 0)
    print("Вариант 1 (2->3 = -2):", d, "| отрицательный цикл:", neg)
    e2 = [(u, v, -4 if (u, v) == (4, 5) else w) for u, v, w in e1]
    d, neg = bellman_ford(e2, 0)
    print("Вариант 2 (+ 4->5 = -4): отрицательный цикл достижим из 0!" if neg
          else d)


def floyd_warshall(edge_list, n=N):
    dist = [[INF] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0
    for u, v, w in edge_list:
        dist[u][v] = min(dist[u][v], w)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    return dist


def task7(dijkstra_dist):
    print("\n=== Задание 7 ===")
    d = floyd_warshall(edges)
    print("Матрица кратчайших расстояний:")
    print("     " + " ".join(f"{j:>3}" for j in range(N)))
    for i, row in enumerate(d):
        print(f"{i:>3}: " + " ".join(f"{'inf' if x == INF else x:>3}" for x in row))
    print("Строка 0 совпадает с Дейкстрой:", d[0] == dijkstra_dist)


if __name__ == "__main__":
    task1()
    comps = task2()
    task3()
    task4(comps)
    dd = task5()
    task6()
    task7(dd)
