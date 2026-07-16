"""多个 BFS 应用场景演示"""

from .graph import Graph, bfs, bfs_shortest_path
from .maze import Maze, maze_to_graph


# ─── 场景 1：社交网络好友推荐 ────────────────────────────────────────────

def demo_social_network() -> None:
    """演示：社交网络中的好友关系与最短连接路径"""
    print("=" * 60)
    print("场景 1：社交网络 — 好友关系与最短连接")
    print("=" * 60)

    g = Graph(directed=False)
    friendships = [
        ("Alice", "Bob"), ("Alice", "Charlie"), ("Bob", "David"),
        ("Charlie", "David"), ("Charlie", "Eve"), ("David", "Frank"),
        ("Eve", "Frank"), ("Frank", "Grace"), ("Grace", "Henry"),
    ]
    for u, v in friendships:
        g.add_edge(u, v)

    print(f"\n社交网络共 {len(g.vertices())} 人，{len(g.edges())} 条好友关系\n")

    result = bfs(g, "Alice")
    print(f"从 Alice 出发的 BFS 遍历顺序: {' → '.join(result['order'])}")
    print(f"\n按层级（社交距离）划分:")
    for level, nodes in sorted(result["levels"].items()):
        label = "本人" if level == 0 else f"第{level}度好友"
        print(f"  {label}: {', '.join(nodes)}")

    # 最短路径
    pairs = [("Alice", "Henry"), ("Bob", "Grace")]
    print()
    for s, e in pairs:
        path = bfs_shortest_path(g, s, e)
        if path:
            dist = len(path) - 1
            print(f"  {s} → {e}: {' → '.join(path)} (距离: {dist})")
        else:
            print(f"  {s} → {e}: 不可达")


# ─── 场景 2：地铁线路最短路径 ────────────────────────────────────────────

def demo_metro() -> None:
    """演示：地铁站点间的最少站数路径"""
    print("\n" + "=" * 60)
    print("场景 2：地铁线路 — 最少站数路径")
    print("=" * 60)

    g = Graph(directed=False)
    connections = [
        ("天安门", "王府井"), ("王府井", "东单"), ("东单", "建国门"),
        ("建国门", "朝阳门"), ("朝阳门", "东四十条"), ("东四十条", "东直门"),
        ("天安门", "西单"), ("西单", "复兴门"), ("复兴门", "南礼士路"),
        ("东单", "灯市口"), ("灯市口", "东四"), ("东四", "张自忠路"),
        ("张自忠路", "北新桥"), ("北新桥", "雍和宫"), ("雍和宫", "东直门"),
    ]
    for u, v in connections:
        g.add_edge(u, v)

    print(f"\n地铁网络共 {len(g.vertices())} 站，{len(g.edges())} 条连接\n")

    path = bfs_shortest_path(g, "天安门", "东直门")
    if path:
        print(f"天安门 → 东直门 最短路径:")
        print(f"  {' → '.join(path)} (共 {len(path) - 1} 站)")
    else:
        print("天安门与东直门不可达")


# ─── 场景 3：迷宫求解 ──────────────────────────────────────────────────

def demo_maze() -> None:
    """演示：使用 BFS 求解迷宫"""
    print("\n" + "=" * 60)
    print("场景 3：迷宫求解 — BFS 找最短出路")
    print("=" * 60)

    maze = Maze(width=15, height=9)
    maze.generate(seed=42)
    maze_str = str(maze)
    print(f"\n迷宫地图 (S=起点, E=终点, #=墙, .=通路):\n{maze_str}")

    graph, start, end = maze_to_graph(maze)
    path = bfs_shortest_path(graph, start, end)

    if path:
        # 在迷宫中标记路径
        path_set = set(path[1:-1])  # 排除起点和终点
        marked = []
        for i, row in enumerate(maze_str.strip().split("\n")):
            line = list(row)
            for j, ch in enumerate(line):
                if (i, j) in path_set:
                    line[j] = "*"
            marked.append("".join(line))
        print(f"BFS 最短路径 (*标记):\n" + "\n".join(marked))
        print(f"最短路径长度: {len(path) - 1} 步")
    else:
        print("迷宫无解！")


# ─── 场景 4：二叉树层序遍历 ──────────────────────────────────────────────

def demo_tree_traversal() -> None:
    """演示：二叉树的层序遍历（BFS的典型应用）"""
    print("\n" + "=" * 60)
    print("场景 4：二叉树 — 层序遍历")
    print("=" * 60)

    # 构建二叉树 (用无向图模拟)
    #         1
    #        / \
    #       2   3
    #      / \   \
    #     4   5   6
    #        /
    #       7
    g = Graph(directed=False)
    tree_edges = [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (5, 7)]
    for u, v in tree_edges:
        g.add_edge(u, v)

    result = bfs(g, 1)
    print(f"\n二叉树结构:")
    print("        1")
    print("       / \\")
    print("      2   3")
    print("     / \\   \\")
    print("    4   5   6")
    print("       /")
    print("      7")
    print(f"\n层序遍历结果: {result['order']}")
    print("\n按层级输出:")
    for level, nodes in sorted(result["levels"].items()):
        print(f"  第 {level} 层: {nodes}")


def demo_word_ladder() -> None:
    """演示：单词接龙 — 用 BFS 找到最短单词转换路径"""
    print("\n" + "=" * 60)
    print("场景 5：单词接龙 — 最短单词转换路径")
    print("=" * 60)

    word_list = [
        "cat", "bat", "hat", "hot", "dot", "dog", "log", "lot",
        "rat", "mat", "map", "cap", "car", "bar", "baz", "raz",
        "red", "bed", "bet", "bit", "sit", "set", "net", "hen",
        "pen", "pin", "bin", "big", "pig", "dig", "fig", "fin",
        "tin", "win", "wing", "ring", "king", "sing", "song",
    ]

    def get_neighbors(word: str) -> list[str]:
        neighbors = []
        for w in word_list:
            if len(w) == len(word):
                diff = sum(c1 != c2 for c1, c2 in zip(word, w))
                if diff == 1:
                    neighbors.append(w)
        return neighbors

    g = Graph(directed=False)
    for word in word_list:
        g.add_vertex(word)
        for neighbor in get_neighbors(word):
            g.add_edge(word, neighbor)

    print(f"\n词库共 {len(g.vertices())} 个单词，{len(g.edges())} 条连接关系\n")

    pairs = [("cat", "dog"), ("bat", "pig"), ("red", "king")]
    for start, end in pairs:
        path = bfs_shortest_path(g, start, end)
        if path:
            dist = len(path) - 1
            print(f"  {start} → {end}: {' → '.join(path)} (距离: {dist})")
        else:
            print(f"  {start} → {end}: 无法转换")


def run_all_demos() -> None:
    """运行所有演示场景"""
    print("\n" + "╔" + "═" * 58 + "╗")
    print("║" + "  广度优先搜索 (BFS) 演示项目  ".center(58) + "║")
    print("╚" + "═" * 58 + "╝")

    demo_social_network()
    demo_metro()
    demo_maze()
    demo_tree_traversal()
    demo_word_ladder()

    print("\n" + "=" * 60)
    print("所有演示运行完毕！")
    print("打开 index.html 可查看交互式可视化演示。")
    print("=" * 60)