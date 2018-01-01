from collections import defaultdict
from heapq import *


def dijkstra(edges, f, t):
    g = defaultdict(list)
    for l, r, c in edges:
        g[l].append((c, r))

    q, seen = [(0, f, ())], set()
    while q:
        (cost, v1, path) = heappop(q)
        if v1 not in seen:
            seen.add(v1)
            path = (v1, path)
            if v1 == t:
                return alhorythm(path, [])

            for c, v2 in g.get(v1, ()):
                if v2 not in seen:
                    heappush(q, (cost+c, v2, path))

    return []


def alhorythm(path, norm_path):
    if path[1] != ():
        norm_path.append(path[0])
        alhorythm(path[1], norm_path)
    else:
        norm_path.append(path[0])
        norm_path.reverse()
    return norm_path
            

if __name__ == '__main__':
    edges = [
        (0, 1, 18),
        (1, 0, 18),
        (1, 4, 6),
        (4, 1, 6),
        (2, 4, 3),
        (4, 2, 3),
        (2, 3, 5),
        (3, 2, 5)
    ]

    print(dijkstra(edges, 0, 1))
    print(dijkstra(edges, 0, 2))
    print(dijkstra(edges, 0, 3))
    print(dijkstra(edges, 0, 4))
