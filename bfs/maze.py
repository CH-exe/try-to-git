"""迷宫生成与图转换"""

import random
from collections import deque

from .graph import Graph


class Maze:
    """随机迷宫生成器（递归回溯法）"""

    def __init__(self, width: int = 15, height: int = 9):
        # 迷宫实际尺寸（含墙壁）必须为奇数
        self.width = width if width % 2 == 1 else width + 1
        self.height = height if height % 2 == 1 else height + 1
        self.grid: list[list[int]] = []

    def generate(self, seed: int | None = None) -> None:
        """生成迷宫，0=通路，1=墙壁"""
        rng = random.Random(seed)
        self.grid = [[1] * self.width for _ in range(self.height)]

        def carve(y: int, x: int) -> None:
            self.grid[y][x] = 0
            directions = [(0, 2), (0, -2), (2, 0), (-2, 0)]
            rng.shuffle(directions)
            for dy, dx in directions:
                ny, nx = y + dy, x + dx
                if 0 < ny < self.height - 1 and 0 < nx < self.width - 1:
                    if self.grid[ny][nx] == 1:
                        self.grid[y + dy // 2][x + dx // 2] = 0
                        carve(ny, nx)

        carve(1, 1)
        # 设置起点和终点
        self.grid[1][0] = 0  # S
        self.grid[self.height - 2][self.width - 1] = 0  # E

    def __str__(self) -> str:
        lines = []
        for i, row in enumerate(self.grid):
            line = ""
            for j, cell in enumerate(row):
                if i == 1 and j == 0:
                    line += "S"
                elif i == self.height - 2 and j == self.width - 1:
                    line += "E"
                elif cell == 1:
                    line += "#"
                else:
                    line += "."
            lines.append(line)
        return "\n".join(lines)


def maze_to_graph(maze: Maze) -> tuple[Graph, tuple[int, int], tuple[int, int]]:
    """将迷宫转换为图，返回 (图, 起点坐标, 终点坐标)"""
    g = Graph(directed=False)
    start = (1, 0)
    end = (maze.height - 2, maze.width - 1)
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    for y in range(maze.height):
        for x in range(maze.width):
            if maze.grid[y][x] == 0:
                g.add_vertex((y, x))
                for dy, dx in directions:
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < maze.height and 0 <= nx < maze.width:
                        if maze.grid[ny][nx] == 0:
                            g.add_edge((y, x), (ny, nx))

    return g, start, end