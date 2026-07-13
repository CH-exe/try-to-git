"""图数据结构及广度优先搜索实现"""

from collections import deque
from typing import Any


class Graph:
    """基于邻接表的图"""

    def __init__(self, directed: bool = False):
        self.adj: dict[Any, list[Any]] = {}
        self.directed = directed

    def add_edge(self, u: Any, v: Any) -> None:
        """添加一条边 u -> v"""
        self.adj.setdefault(u, []).append(v)
        if not self.directed:
            self.adj.setdefault(v, []).append(u)

    def add_vertex(self, v: Any) -> None:
        """添加一个顶点"""
        self.adj.setdefault(v, [])

    def neighbors(self, v: Any) -> list[Any]:
        """获取顶点 v 的所有邻居"""
        return self.adj.get(v, [])

    def vertices(self) -> list[Any]:
        """获取所有顶点"""
        return list(self.adj.keys())

    def edges(self) -> list[tuple[Any, Any]]:
        """获取所有边"""
        result = []
        visited = set()
        for u, neighbors in self.adj.items():
            for v in neighbors:
                if self.directed:
                    result.append((u, v))
                elif (v, u) not in visited:
                    visited.add((u, v))
                    result.append((u, v))
        return result


def bfs(graph: Graph, start: Any) -> dict[str, list | dict]:
    """
    广度优先搜索

    参数:
        graph: 图对象
        start: 起始顶点

    返回:
        {
            "order":      访问顺序列表,
            "levels":     各层级顶点 {层号: [顶点列表]},
            "parent":     父节点映射 {顶点: 父顶点},
            "discovered": 发现顺序 {顶点: 发现顺序编号}
        }
    """
    if start not in graph.adj:
        raise ValueError(f"起始顶点 {start!r} 不在图中")

    visited = {start}
    order = [start]
    levels = {0: [start]}
    parent = {start: None}
    discovered = {start: 0}
    queue = deque([(start, 0)])

    while queue:
        vertex, level = queue.popleft()
        for neighbor in graph.neighbors(vertex):
            if neighbor not in visited:
                visited.add(neighbor)
                order.append(neighbor)
                parent[neighbor] = vertex
                discovered[neighbor] = len(order) - 1
                queue.append((neighbor, level + 1))
                levels.setdefault(level + 1, []).append(neighbor)

    return {
        "order": order,
        "levels": levels,
        "parent": parent,
        "discovered": discovered,
    }


def bfs_shortest_path(graph: Graph, start: Any, end: Any) -> list[Any] | None:
    """
    使用 BFS 找到从 start 到 end 的最短路径

    参数:
        graph: 图对象
        start: 起始顶点
        end:   目标顶点

    返回:
        最短路径列表，若不可达则返回 None
    """
    if start not in graph.adj or end not in graph.adj:
        raise ValueError("起始顶点或目标顶点不在图中")

    if start == end:
        return [start]

    visited = {start}
    parent = {start: None}
    queue = deque([start])

    while queue:
        vertex = queue.popleft()
        for neighbor in graph.neighbors(vertex):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = vertex
                if neighbor == end:
                    # 回溯构建路径
                    path = []
                    cur = end
                    while cur is not None:
                        path.append(cur)
                        cur = parent[cur]
                    return path[::-1]
                queue.append(neighbor)

    return None