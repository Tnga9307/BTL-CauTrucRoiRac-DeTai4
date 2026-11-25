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


def compute_eccentricities(depots, adj):
    eccentricities = {}
    for node in depots:
        _, _, far_node, max_dist = weighted_bfs(node, depots, adj)
        eccentricities[node] = (max_dist, far_node)
    return eccentricities


def find_tree_center(depots, eccentricities):
    radius = min(val[0] for val in eccentricities.values())
    centers = [node for node in depots if eccentricities[node][0] == radius]
    return radius, centers


def cross_verify_center(centers, diameter_path, depots, adj):
    diameter_set = set(diameter_path)
    on_diameter = all(c in diameter_set for c in centers)

    dist_reg03, _, _, _ = weighted_bfs("REG03", depots, adj)
    manual_branch_check = (
        dist_reg03["ARE07"] == 280.0
        and dist_reg03["LOC09"] == 345.0
        and dist_reg03["LOC11"] == 480.0
    )
    return on_diameter, manual_branch_check


def print_experiment_table(depots, adj, eccentricities, centers, diameter_path):
    diameter_set = set(diameter_path)
    header = (
        f"{'Ma depot':<8} | {'Ten depot':<35} | {'Cap quan ly':<16} | "
        f"{'e(v) (phut)':<11} | {'Dinh xa nhat':<12} | {'Nhan xet'}"
    )
    print(header)
    print("-" * len(header))

    for node in depots:
        ten = depots[node]["ten"]
        cap = depots[node]["cap"]
        e_val, far_node = eccentricities[node]
        degree = len(adj[node])

        notes = []
        if node in centers:
            notes.append("Tam cay")
        if node in diameter_set:
            notes.append("Thuoc duong kinh")
        if degree == 1:
            notes.append("Depot la")

        nhan_xet = " / ".join(notes) if notes else "Depot trung gian"
        print(f"{node:<8} | {ten:<35} | {cap:<16} | {e_val:<11.0f} | {far_node:<12} | {nhan_xet}")


valid, msg = validate_tree(depots, adj, edges)
print("=== KIEM DINH CAY & DUONG KINH ===")
print(msg)

if valid:
    root = next(iter(depots))
    u, v, diameter, path = find_diameter(root, depots, adj)
    print(f"Dinh xuat phat: {root} - {depots[root]['ten']}")
    print(f"Dau mut u: {u} - {depots[u]['ten']}")
    print(f"Dau mut v: {v} - {depots[v]['ten']}")
    print(f"Duong kinh D: {diameter:.0f} phut")
    print("Lo trinh duong kinh:", " -> ".join(path))

    eccentricities = compute_eccentricities(depots, adj)
    radius, centers = find_tree_center(depots, eccentricities)
    on_diam, branch_ok = cross_verify_center(centers, path, depots, adj)

    print("\n=== KET QUA TINH DO LECH TAM & TAM CAY ===")
    print(f"Ban kinh cay R = {radius:.0f} phut")
    print(f"Tam cay C(T) = {centers} -> {depots[centers[0]]['ten']} ({depots[centers[0]]['cap']})")
    print(f"Kiem chung tam nam tren duong kinh (u -> v): {'DAT (True)' if on_diam else 'KHONG DAT (False)'}")
    print(f"Kiem thu tinh tay nhanh REG03 -> ARE07 -> LOC09 (280 + 65 = 345p) & LOC11 (480p): {'DAT (True)' if branch_ok else 'SAI'}")

    print("\n=== BANG THONG KE KET QUA THUC NGHIEM 24 DEPOT  ===")
    print_experiment_table(depots, adj, eccentricities, centers, path)