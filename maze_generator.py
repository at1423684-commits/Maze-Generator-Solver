import random
from typing import List, Tuple, Set, Optional
import numpy as np


# Cell Type Constants
PATH = 0      # Open passage
WALL = 1      # Impassable wall
START = 2     # Maze starting location
GOAL = 3      # Maze destination location
VISITED = 4   # Cell visited during search
SOLUTION = 5  # Cell on the final reconstructed path


class Maze:
    

    # Size configurations: rows x cols (must be odd integers for wall/passage alternation)
    PRESET_SIZES = {
        "Small": (15, 15),
        "Medium": (27, 27),
        "Large": (41, 41)
    }

    def __init__(self, size_name: str = "Medium", custom_dims: Optional[Tuple[int, int]] = None):
        """
        Initialize the maze dimensions and prepare the grid.
        
        Args:
            size_name: One of 'Small', 'Medium', 'Large', or 'Custom'.
            custom_dims: Optional (rows, cols) tuple if size_name is 'Custom'.
        """
        self.size_name = size_name
        if custom_dims:
            rows, cols = custom_dims
        else:
            rows, cols = self.PRESET_SIZES.get(size_name, (27, 27))

        # Enforce odd dimensions for wall-passage geometry
        self.rows = rows if rows % 2 != 0 else rows + 1
        self.cols = cols if cols % 2 != 0 else cols + 1

        # Standard start at top-left corridor, goal at bottom-right corridor
        self.start: Tuple[int, int] = (1, 1)
        self.goal: Tuple[int, int] = (self.rows - 2, self.cols - 2)

        # Initialize grid full of walls
        self.grid = np.ones((self.rows, self.cols), dtype=np.int32)
        
        # Generation metadata
        self.generation_method = "Recursive Backtracking (DFS)"
        self.has_loops = False

    def generate(self, braid_factor: float = 0.05, seed: Optional[int] = None) -> None:
       
        if seed is not None:
            random.seed(seed)

        # Step 1: Initialize all cells as walls
        self.grid = np.ones((self.rows, self.cols), dtype=np.int32)

        # Step 2: Set start cell as open passage and initialize DFS stack
        start_r, start_c = self.start
        self.grid[start_r, start_c] = PATH
        stack: List[Tuple[int, int]] = [(start_r, start_c)]

        # Directions: Up, Down, Left, Right at step distance 2
        directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]

        # Step 3: DFS carving loop
        while stack:
            curr_r, curr_c = stack[-1]

            # Find unvisited neighbors at distance 2
            unvisited_neighbors = []
            for dr, dc in directions:
                nr, nc = curr_r + dr, curr_c + dc
                if 1 <= nr < self.rows - 1 and 1 <= nc < self.cols - 1:
                    if self.grid[nr, nc] == WALL:
                        unvisited_neighbors.append((nr, nc, dr, dc))

            if unvisited_neighbors:
                # Random selection (introduces branching factor)
                nr, nc, dr, dc = random.choice(unvisited_neighbors)

                # Carve wall between current cell and neighbor (distance 1)
                self.grid[curr_r + dr // 2, curr_c + dc // 2] = PATH
                # Carve neighbor cell (distance 2)
                self.grid[nr, nc] = PATH

                # Push neighbor to stack
                stack.append((nr, nc))
            else:
                # Backtrack when dead end is reached
                stack.pop()

        # Step 4: Braiding (Optional dead-end elimination to create cycles)
        if braid_factor > 0:
            self._braid_maze(braid_factor)
            self.has_loops = True
        else:
            self.has_loops = False

        # Step 5: Ensure start and goal are open
        self.grid[self.start[0], self.start[1]] = PATH
        self.grid[self.goal[0], self.goal[1]] = PATH

    def _braid_maze(self, factor: float) -> None:
       
        dead_ends: List[Tuple[int, int]] = []
        for r in range(1, self.rows - 1, 2):
            for c in range(1, self.cols - 1, 2):
                if self.grid[r, c] == PATH:
                    # Count passage neighbors
                    passages = 0
                    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        if self.grid[r + dr, c + dc] == PATH:
                            passages += 1
                    # A dead-end has only 1 exit
                    if passages == 1:
                        dead_ends.append((r, c))

        # Randomly remove wall for a fraction of dead ends
        num_to_remove = int(len(dead_ends) * factor)
        random.shuffle(dead_ends)
        for r, c in dead_ends[:num_to_remove]:
            # Find a wall separating this cell from another passage
            candidates = []
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                wr, wc = r + dr, c + dc
                nr, nc = r + 2 * dr, c + 2 * dc
                if 1 <= nr < self.rows - 1 and 1 <= nc < self.cols - 1:
                    if self.grid[wr, wc] == WALL and self.grid[nr, nc] == PATH:
                        candidates.append((wr, wc))
            if candidates:
                wr, wc = random.choice(candidates)
                self.grid[wr, wc] = PATH

    def get_neighbors(self, r: int, c: int) -> List[Tuple[int, int]]:
       
        neighbors = []
        # Cardinal directions: Up, Down, Left, Right
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                if self.grid[nr, nc] == PATH:
                    neighbors.append((nr, nc))
        return neighbors

    def is_wall(self, r: int, c: int) -> bool:
        """Returns True if cell (r, c) is a wall or out of bounds."""
        if 0 <= r < self.rows and 0 <= c < self.cols:
            return self.grid[r, c] == WALL
        return True

    def count_total_open_cells(self) -> int:
        """Returns total count of walkable passage cells in the maze."""
        return int(np.sum(self.grid == PATH))

    def copy(self) -> "Maze":
        """Returns an independent deep copy of the current maze."""
        new_maze = Maze(self.size_name, (self.rows, self.cols))
        new_maze.grid = np.copy(self.grid)
        new_maze.start = self.start
        new_maze.goal = self.goal
        new_maze.has_loops = self.has_loops
        new_maze.generation_method = self.generation_method
        return new_maze
