import time
import heapq
from collections import deque
from dataclasses import dataclass
from typing import List, Tuple, Dict, Set, Optional, Generator
from maze_generator import Maze


@dataclass
class SolveResult:
    """
    Encapsulates all statistical and behavioral outputs from solving a maze.
    """
    algorithm_name: str
    solved: bool
    path: List[Tuple[int, int]]
    path_length: int
    visited_order: List[Tuple[int, int]]
    nodes_visited: int
    execution_time_ms: float
    max_frontier_size: int
    time_complexity: str
    space_complexity: str
    optimality: str
    data_structure: str
    description: str


def reconstruct_path(parent: Dict[Tuple[int, int], Tuple[int, int]],
                     start: Tuple[int, int],
                     goal: Tuple[int, int]) -> List[Tuple[int, int]]:
    
    if goal not in parent and start != goal:
        return []

    curr = goal
    path = []
    while curr is not None:
        path.append(curr)
        if curr == start:
            break
        curr = parent.get(curr)

    path.reverse()
    return path


class MazeSolver:
    

    ALGORITHMS = [
        "Breadth-First Search (BFS)",
        "Depth-First Search (DFS)",
        "Dijkstra's Algorithm"
    ]

    METADATA = {
        "Breadth-First Search (BFS)": {
            "time_complexity": "O(V + E)",
            "space_complexity": "O(V)",
            "optimality": "Optimal (Shortest Path)",
            "data_structure": "Queue (collections.deque - FIFO)",
            "description": "Explores neighbors layer-by-layer uniformly in all directions. Guaranteed to find the shortest path in unweighted graphs."
        },
        "Depth-First Search (DFS)": {
            "time_complexity": "O(V + E)",
            "space_complexity": "O(V)",
            "optimality": "Non-Optimal (May wander into long dead ends)",
            "data_structure": "Stack (Python list - LIFO)",
            "description": "Explores deeply down a single path until hitting a dead end before backtracking. Not guaranteed to find the shortest path."
        },
        "Dijkstra's Algorithm": {
            "time_complexity": "O((V + E) log V)",
            "space_complexity": "O(V)",
            "optimality": "Optimal (Guaranteed Minimum Cost)",
            "data_structure": "Min-Heap Priority Queue (heapq)",
            "description": "Finds shortest path by greedily expanding the node with the lowest cumulative edge weight (cost = 1 per step here)."
        }
    }

    @classmethod
    def solve(cls, maze: Maze, algorithm_name: str) -> SolveResult:
       
        start_time = time.perf_counter()

        if algorithm_name == "Breadth-First Search (BFS)":
            solved, path, visited_order, max_frontier = cls._solve_bfs(maze)
        elif algorithm_name == "Depth-First Search (DFS)":
            solved, path, visited_order, max_frontier = cls._solve_dfs(maze)
        elif algorithm_name == "Dijkstra's Algorithm":
            solved, path, visited_order, max_frontier = cls._solve_dijkstra(maze)
        else:
            raise ValueError(f"Unknown algorithm: {algorithm_name}")

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0
        meta = cls.METADATA[algorithm_name]

        return SolveResult(
            algorithm_name=algorithm_name,
            solved=solved,
            path=path,
            path_length=len(path),
            visited_order=visited_order,
            nodes_visited=len(visited_order),
            execution_time_ms=round(elapsed_ms, 3),
            max_frontier_size=max_frontier,
            time_complexity=meta["time_complexity"],
            space_complexity=meta["space_complexity"],
            optimality=meta["optimality"],
            data_structure=meta["data_structure"],
            description=meta["description"]
        )

    # -------------------------------------------------------------------------
    # 1. BREADTH-FIRST SEARCH (BFS)
    # -------------------------------------------------------------------------
    @classmethod
    def _solve_bfs(cls, maze: Maze):
        start, goal = maze.start, maze.goal
        queue = deque([start])
        visited: Set[Tuple[int, int]] = {start}
        parent: Dict[Tuple[int, int], Tuple[int, int]] = {start: None}
        visited_order: List[Tuple[int, int]] = []
        max_frontier = 1

        while queue:
            max_frontier = max(max_frontier, len(queue))
            curr = queue.popleft()
            visited_order.append(curr)

            if curr == goal:
                path = reconstruct_path(parent, start, goal)
                return True, path, visited_order, max_frontier

            for neighbor in maze.get_neighbors(curr[0], curr[1]):
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = curr
                    queue.append(neighbor)

        return False, [], visited_order, max_frontier

    # -------------------------------------------------------------------------
    # 2. DEPTH-FIRST SEARCH (DFS)
    # -------------------------------------------------------------------------
    @classmethod
    def _solve_dfs(cls, maze: Maze):
        start, goal = maze.start, maze.goal
        stack: List[Tuple[int, int]] = [start]
        visited: Set[Tuple[int, int]] = set()
        parent: Dict[Tuple[int, int], Tuple[int, int]] = {start: None}
        visited_order: List[Tuple[int, int]] = []
        max_frontier = 1

        while stack:
            max_frontier = max(max_frontier, len(stack))
            curr = stack.pop()

            if curr in visited:
                continue
            visited.add(curr)
            visited_order.append(curr)

            if curr == goal:
                path = reconstruct_path(parent, start, goal)
                return True, path, visited_order, max_frontier

            # Reverse neighbors for intuitive exploration order (Up, Right, Down, Left)
            neighbors = maze.get_neighbors(curr[0], curr[1])
            for neighbor in reversed(neighbors):
                if neighbor not in visited:
                    if neighbor not in parent:
                        parent[neighbor] = curr
                    stack.append(neighbor)

        return False, [], visited_order, max_frontier

    # -------------------------------------------------------------------------
    # 3. DIJKSTRA'S ALGORITHM
    # -------------------------------------------------------------------------
    @classmethod
    def _solve_dijkstra(cls, maze: Maze):
        start, goal = maze.start, maze.goal
        # Heap elements: (distance, insertion_counter, node)
        counter = 0
        pq: List[Tuple[float, int, Tuple[int, int]]] = [(0.0, counter, start)]
        distances: Dict[Tuple[int, int], float] = {start: 0.0}
        parent: Dict[Tuple[int, int], Tuple[int, int]] = {start: None}
        visited: Set[Tuple[int, int]] = set()
        visited_order: List[Tuple[int, int]] = []
        max_frontier = 1

        while pq:
            max_frontier = max(max_frontier, len(pq))
            dist, _, curr = heapq.heappop(pq)

            if curr in visited:
                continue
            visited.add(curr)
            visited_order.append(curr)

            if curr == goal:
                path = reconstruct_path(parent, start, goal)
                return True, path, visited_order, max_frontier

            for neighbor in maze.get_neighbors(curr[0], curr[1]):
                weight = 1.0  # Unit cost in unweighted grid
                new_dist = dist + weight
                if neighbor not in distances or new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    parent[neighbor] = curr
                    counter += 1
                    heapq.heappush(pq, (new_dist, counter, neighbor))

        return False, [], visited_order, max_frontier

    # -------------------------------------------------------------------------
    # STEP GENERATORS (FOR SMOOTH ANIMATIONS IN TKINTER)
    # -------------------------------------------------------------------------
    @classmethod
    def solve_step_generator(cls, maze: Maze, algorithm_name: str) -> Generator:
       
        start_time = time.perf_counter()
        start, goal = maze.start, maze.goal

        if algorithm_name == "Breadth-First Search (BFS)":
            queue = deque([start])
            visited = {start}
            parent = {start: None}
            visited_count = 0

            while queue:
                curr = queue.popleft()
                visited_count += 1
                yield ('visit', curr, set(queue))

                if curr == goal:
                    path = reconstruct_path(parent, start, goal)
                    elapsed = (time.perf_counter() - start_time) * 1000.0
                    yield ('done', True, path, visited_count, elapsed)
                    return

                for neighbor in maze.get_neighbors(curr[0], curr[1]):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        parent[neighbor] = curr
                        queue.append(neighbor)

            elapsed = (time.perf_counter() - start_time) * 1000.0
            yield ('done', False, [], visited_count, elapsed)

        elif algorithm_name == "Depth-First Search (DFS)":
            stack = [start]
            visited = set()
            parent = {start: None}
            visited_count = 0

            while stack:
                curr = stack.pop()
                if curr in visited:
                    continue
                visited.add(curr)
                visited_count += 1
                yield ('visit', curr, set(stack))

                if curr == goal:
                    path = reconstruct_path(parent, start, goal)
                    elapsed = (time.perf_counter() - start_time) * 1000.0
                    yield ('done', True, path, visited_count, elapsed)
                    return

                for neighbor in reversed(maze.get_neighbors(curr[0], curr[1])):
                    if neighbor not in visited:
                        if neighbor not in parent:
                            parent[neighbor] = curr
                        stack.append(neighbor)

            elapsed = (time.perf_counter() - start_time) * 1000.0
            yield ('done', False, [], visited_count, elapsed)

        elif algorithm_name == "Dijkstra's Algorithm":
            counter = 0
            pq = [(0.0, counter, start)]
            distances = {start: 0.0}
            parent = {start: None}
            visited = set()
            visited_count = 0

            while pq:
                dist, _, curr = heapq.heappop(pq)
                if curr in visited:
                    continue
                visited.add(curr)
                visited_count += 1
                frontier_cells = {item[2] for item in pq}
                yield ('visit', curr, frontier_cells)

                if curr == goal:
                    path = reconstruct_path(parent, start, goal)
                    elapsed = (time.perf_counter() - start_time) * 1000.0
                    yield ('done', True, path, visited_count, elapsed)
                    return

                for neighbor in maze.get_neighbors(curr[0], curr[1]):
                    new_dist = dist + 1.0
                    if neighbor not in distances or new_dist < distances[neighbor]:
                        distances[neighbor] = new_dist
                        parent[neighbor] = curr
                        counter += 1
                        heapq.heappush(pq, (new_dist, counter, neighbor))

            elapsed = (time.perf_counter() - start_time) * 1000.0
            yield ('done', False, [], visited_count, elapsed)
        else:
            raise ValueError(f"Unknown algorithm: {algorithm_name}")
