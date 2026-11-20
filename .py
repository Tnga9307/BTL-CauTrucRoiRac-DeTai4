from collections import defaultdict, deque

DEPOTS_DATA = [
    ("HQ01", "Tru so chinh TP.HCM", "Cap 1 - Tru so"),
    ("REG01", "Depot Vung Dong Nam Bo (Dong Nai)", "Cap 2 - Vung"),
    ("REG02", "Depot Vung Binh Duong", "Cap 2 - Vung"),
    ("REG03", "Depot Vung Tay Nam Bo (Can Tho)", "Cap 2 - Vung"),
    ("REG04", "Depot Vung Duyen Hai (Nha Trang)", "Cap 2 - Vung"),
    ("ARE01", "Depot Khu vuc Bien Hoa", "Cap 3 - Khu vuc"),
    ("ARE02", "Depot Khu vuc Vung Tau", "Cap 3 - Khu vuc"),
    ("ARE03", "Depot Khu vuc Thu Dau Mot", "Cap 3 - Khu vuc"),
    ("ARE04", "Depot Khu vuc Tan An", "Cap 3 - Khu vuc"),
    ("ARE05", "Depot Khu vuc My Tho", "Cap 3 - Khu vuc"),
    ("ARE06", "Depot Khu vuc Long Xuyen", "Cap 3 - Khu vuc"),
    ("ARE07", "Depot Khu vuc Ca Mau", "Cap 3 - Khu vuc"),
    ("ARE08", "Depot Khu vuc Tuy Hoa", "Cap 3 - Khu vuc"),
    ("LOC01", "Diem le Long Thanh", "Cap 4 - Diem le"),
    ("LOC02", "Diem le Trang Bom", "Cap 4 - Diem le"),
    ("LOC03", "Diem le Phu My", "Cap 4 - Diem le"),
    ("LOC04", "Diem le Ben Cat", "Cap 4 - Diem le"),
    ("LOC05", "Diem le Ben Luc", "Cap 4 - Diem le"),
    ("LOC06", "Diem le Cai Lay", "Cap 4 - Diem le"),
    ("LOC07", "Diem le Chau Doc", "Cap 4 - Diem le"),
    ("LOC08", "Diem le Ha Tien", "Cap 4 - Diem le"),
    ("LOC09", "Diem le Nam Can", "Cap 4 - Diem le"),
    ("LOC10", "Diem le Song Cau", "Cap 4 - Diem le"),
    ("LOC11", "Diem le Quy Nhon", "Cap 4 - Diem le"),
]

EDGES_DATA = [
    ("HQ01", "REG01", 45),
    ("HQ01", "REG02", 40),
    ("HQ01", "REG03", 150),
    ("HQ01", "REG04", 130),
    ("REG01", "ARE01", 25),
    ("REG01", "ARE02", 75),
    ("REG02", "ARE03", 20),
    ("REG03", "ARE04", 95),
    ("REG03", "ARE05", 70),
    ("REG03", "ARE06", 110),
    ("REG03", "ARE07", 280),
    ("REG04", "ARE08", 115),
    ("ARE01", "LOC01", 30),
    ("ARE01", "LOC02", 25),
    ("ARE02", "LOC03", 35),
    ("ARE03", "LOC04", 30),
    ("ARE04", "LOC05", 25),
    ("ARE05", "LOC06", 35),
    ("ARE06", "LOC07", 55),
    ("ARE06", "LOC08", 90),
    ("ARE07", "LOC09", 65),
    ("ARE08", "LOC10", 45),
    ("ARE08", "LOC11", 85),
]

depots = {ma: {"ten": ten, "cap": cap} for ma, ten, cap in DEPOTS_DATA}
depot_order = [ma for ma, _, _ in DEPOTS_DATA]

adj = defaultdict(list)
for u, v, w in EDGES_DATA:
    adj[u].append((v, w))
    adj[v].append((u, w))


def bfs_weighted(start):
    """Duyệt BFS có trọng số từ đỉnh start, trả về đỉnh xa nhất, khoảng cách và mảng truy vết."""
    dist = {node: -1 for node in depots}
    parent = {node: None for node in depots}
    dist[start] = 0
    queue = deque([start])

    while queue:
        u = queue.popleft()
        for v, w in adj[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + w
                parent[v] = u
                queue.append(v)

    farthest_node = max(dist, key=lambda k: dist[k])
    return farthest_node, dist[farthest_node], dist, parent


def kiem_tra_cay():
    so_dinh = len(depots)
    so_canh = len(EDGES_DATA)
    _, _, dist_check, _ = bfs_weighted(depot_order[0])
    lien_thong = all(d != -1 for d in dist_check.values())
    la_cay = (so_canh == so_dinh - 1) and lien_thong

    print("=== 1. KIỂM TRA TÍNH CHẤT CÂY ===")
    print(f"- Số đỉnh |V| = {so_dinh}, Số cạnh |E| = {so_canh} (|E| = |V| - 1: {so_canh == so_dinh - 1})")
    print(f"- Tính liên thông: {'Đạt (24/24 đỉnh)' if lien_thong else 'Không đạt'}")
    print(f"- Kết luận đồ thị là CÂY hợp lệ: {'HỢP LỆ' if la_cay else 'KHÔNG HỢP LỆ'}\n")


def chay_phan_tich():
    kiem_tra_cay()

    u_end, _, _, _ = bfs_weighted("HQ01")
    v_end, diameter, _, parent_u = bfs_weighted(u_end)

    diameter_path = []
    curr = v_end
    while curr is not None:
        diameter_path.append(curr)
        curr = parent_u[curr]
    diameter_path.reverse()
    diameter_set = set(diameter_path)

    print("=== 2. ĐƯỜNG KÍNH CÂY (THUẬT TOÁN 2 LƯỢT BFS) ===")
    print(f"- Đường kính D = {diameter} phút")
    print(f"- Lộ trình dài nhất: {' -> '.join(diameter_path)}\n")

    eccentricities = {}
    for node in depot_order:
        far_node, max_dist, _, _ = bfs_weighted(node)
        eccentricities[node] = (max_dist, far_node)

    radius = min(val[0] for val in eccentricities.values())
    centers = [node for node in depot_order if eccentricities[node][0] == radius]
    is_on_diameter = all(c in diameter_set for c in centers)

    print("=== 3. BÁN KÍNH, TÂM CÂY & KIỂM CHỨNG CHÉO (PHẦN TV4) ===")
    print(f"- Bán kính cây R = {radius} phút")
    print(f"- Tâm cây tối ưu C(T) = {centers} ({depots[centers[0]]['ten']})")
    print(f"- Kiểm chứng tâm cây nằm trên đường kính: {'HỢP LỆ (True)' if is_on_diameter else 'SAI (False)'}\n")

    print("=== 4. BẢNG THỐNG KÊ ĐỘ LỆCH TÂM 24 DEPOT ===")
    print(f"{'Mã':<7} | {'Tên Depot':<36} | {'Cấp quản lý':<16} | {'e(v)':<6} | {'Xa nhất':<8} | {'Nhận xét'}")
    print("-" * 115)

    for node in depot_order:
        ten = depots[node]["ten"]
        cap = depots[node]["cap"]
        e_val, far_node = eccentricities[node]
        degree = len(adj[node])

        notes = []
        if node in centers:
            notes.append("Tâm cây (Tối ưu)")
        if node in diameter_set:
            notes.append("Thuộc đường kính")
        if degree == 1:
            notes.append("Depot lá")
        if node == "HQ01":
            notes.append("Trụ sở cũ")
        note_str = ", ".join(notes) if notes else "Depot trung gian"

        print(f"{node:<7} | {ten:<36} | {cap:<16} | {e_val:<6} | {far_node:<8} | {note_str}")

if __name__ == "__main__":
    chay_phan_tich()
    