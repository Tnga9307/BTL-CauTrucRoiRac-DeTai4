import csv
from collections import deque, defaultdict

depots = {}
adj = defaultdict(list)
edges = []

with open("depots (2).csv", mode="r", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    for row in reader:
        ma = row["Ma_Depot"].strip()
        depots[ma] = {
            "ten": row["Ten_Depot"].strip(),
            "cap": row["Cap_Quan_Ly"].strip()
        }
        if ma not in adj:
            adj[ma] = []

with open("edges (1).csv", mode="r", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    for row in reader:
        u = row["Depot_Cha"].strip()
        v = row["Depot_Con"].strip()
        w = float(row["Thoi_Gian_Phut"].strip())
        edges.append((u, v, w))
        adj[u].append((v, w))
        adj[v].append((u, w))


def validate_tree(depots, adj, edges):
    num_v = len(depots)
    num_e = len(edges)
    if num_e != num_v - 1:
        return False, f"Khong hop le: |V| = {num_v}, |E| = {num_e}"

    start = next(iter(depots))
    visited = {start}
    queue = deque([(start, None)])

    while queue:
        u, parent = queue.popleft()
        for v, _ in adj[u]:
            if v not in visited:
                visited.add(v)
                queue.append((v, u))
            elif v != parent:
                return False, f"Khong hop le: Co chu trinh tai ({u}, {v})"

    if len(visited) != num_v:
        return False, f"Khong hop le: Khong lien thong ({len(visited)}/{num_v} dinh)"

    return True, f"Hop le: Cay co {num_v} dinh, {num_e} canh, lien thong va khong co chu trinh."


def weighted_bfs(start, depots, adj):
    dist = {node: float("inf") for node in depots}
    parent = {node: None for node in depots}
    dist[start] = 0.0
    queue = deque([start])

    farthest_node = start
    max_dist = 0.0

    while queue:
        u = queue.popleft()
        for v, w in adj[u]:
            if dist[v] == float("inf"):
                dist[v] = dist[u] + w
                parent[v] = u
                queue.append(v)
                if dist[v] > max_dist:
                    max_dist = dist[v]
                    farthest_node = v

    return dist, parent, farthest_node, max_dist


def find_diameter(start, depots, adj):
    _, _, u, _ = weighted_bfs(start, depots, adj)
    _, parent, v, diameter = weighted_bfs(u, depots, adj)

    path = []
    curr = v
    while curr is not None:
        path.append(curr)
        curr = parent[curr]
    path.reverse()

    return u, v, diameter, path


valid, msg = validate_tree(depots, adj, edges)
print(msg)

if valid:
    root = next(iter(depots))
    u, v, diameter, path = find_diameter(root, depots, adj)
    print(f"Dinh xuat phat: {root} - {depots[root]['ten']}")
    print(f"Dau mut u: {u} - {depots[u]['ten']}")
    print(f"Dau mut v: {v} - {depots[v]['ten']}")
    print(f"Duong kinh D: {diameter:.0f} phut")
    print("Lo trinh duong kinh:", " -> ".join(path))