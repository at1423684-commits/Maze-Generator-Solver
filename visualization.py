import tkinter as tk
from typing import List, Tuple, Optional, Dict
from maze_generator import Maze, PATH, WALL, START, GOAL


# UI Theme Colors
COLOR_WALL = "#1e293b"       # Dark slate navy
COLOR_PATH = "#f8fafc"       # Crisp off-white
COLOR_START = "#10b981"      # Emerald green
COLOR_GOAL = "#ef4444"       # Vibrant crimson red
COLOR_FRONTIER = "#f59e0b"   # Warm amber/orange
COLOR_VISITED = "#60a5fa"    # Soft sky blue
COLOR_VISITED_ALT = "#93c5fd"# Alternate lighter blue for depth
COLOR_PATH_FINAL = "#facc15" # Radiant electric yellow/gold
COLOR_PATH_START = "#34d399" # Pale emerald
COLOR_BORDER = "#0f172a"     # Outer canvas border


class MazeCanvas:
    

    def __init__(self, canvas: tk.Canvas):
        
        self.canvas = canvas
        self.maze: Optional[Maze] = None
        self.cell_size: float = 20.0
        self.offset_x: float = 0.0
        self.offset_y: float = 0.0
        
        # 2D list of canvas rectangle IDs: rect_ids[r][c]
        self.rect_ids: List[List[Optional[int]]] = []
        self.text_ids: Dict[str, int] = {}

    def render_maze(self, maze: Maze) -> None:
        
        self.maze = maze
        self.canvas.delete("all")
        self.rect_ids = [[None for _ in range(maze.cols)] for _ in range(maze.rows)]
        self.text_ids.clear()

        # Get canvas current dimensions
        c_width = self.canvas.winfo_width()
        c_height = self.canvas.winfo_height()

        # Fallback if canvas is not yet drawn or has 1x1 initial size
        if c_width <= 10 or c_height <= 10:
            c_width = 650
            c_height = 550

        # Calculate cell size and centering offsets with margin
        margin = 15
        available_w = max(100, c_width - 2 * margin)
        available_h = max(100, c_height - 2 * margin)

        cell_w = available_w / maze.cols
        cell_h = available_h / maze.rows
        self.cell_size = max(4.0, min(cell_w, cell_h))

        grid_w = self.cell_size * maze.cols
        grid_h = self.cell_size * maze.rows
        self.offset_x = (c_width - grid_w) / 2.0
        self.offset_y = (c_height - grid_h) / 2.0

        outline_color = "#334155" if self.cell_size >= 12 else ""

        # Draw cells
        for r in range(maze.rows):
            for c in range(maze.cols):
                x1 = self.offset_x + c * self.cell_size
                y1 = self.offset_y + r * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                val = maze.grid[r, c]
                if (r, c) == maze.start:
                    fill = COLOR_START
                elif (r, c) == maze.goal:
                    fill = COLOR_GOAL
                elif val == WALL:
                    fill = COLOR_WALL
                else:
                    fill = COLOR_PATH

                rect_id = self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=fill,
                    outline=outline_color,
                    width=1 if outline_color else 0
                )
                self.rect_ids[r][c] = rect_id

        # Draw start/goal marker badges if cell size is large enough
        if self.cell_size >= 14:
            self._draw_markers()

    def _draw_markers(self) -> None:
        """Draws 'S' (Start) and 'G' (Goal) textual labels on their respective cells."""
        if not self.maze:
            return

        # Start Marker
        sr, sc = self.maze.start
        sx = self.offset_x + (sc + 0.5) * self.cell_size
        sy = self.offset_y + (sr + 0.5) * self.cell_size
        font_size = max(8, int(self.cell_size * 0.45))
        s_id = self.canvas.create_text(
            sx, sy,
            text="S",
            fill="#ffffff",
            font=("Segoe UI", font_size, "bold")
        )
        self.text_ids["start"] = s_id

        # Goal Marker
        gr, gc = self.maze.goal
        gx = self.offset_x + (gc + 0.5) * self.cell_size
        gy = self.offset_y + (gr + 0.5) * self.cell_size
        g_id = self.canvas.create_text(
            gx, gy,
            text="G",
            fill="#ffffff",
            font=("Segoe UI", font_size, "bold")
        )
        self.text_ids["goal"] = g_id

    def color_cell(self, r: int, c: int, color: str) -> None:
        
        if not self.maze or not self.rect_ids:
            return
        if (r, c) == self.maze.start or (r, c) == self.maze.goal:
            return

        if 0 <= r < self.maze.rows and 0 <= c < self.maze.cols:
            rect_id = self.rect_ids[r][c]
            if rect_id is not None:
                self.canvas.itemconfig(rect_id, fill=color)

    def mark_frontier(self, cells: List[Tuple[int, int]]) -> None:
        """Recolors cells currently in the search frontier (queue/stack/heap)."""
        for r, c in cells:
            self.color_cell(r, c, COLOR_FRONTIER)

    def mark_visited(self, r: int, c: int) -> None:
        """Recolors cell as explored/visited."""
        self.color_cell(r, c, COLOR_VISITED)

    def mark_path(self, path: List[Tuple[int, int]]) -> None:
        
        for r, c in path:
            self.color_cell(r, c, COLOR_PATH_FINAL)

    def clear_solution(self) -> None:
        
        if not self.maze or not self.rect_ids:
            return

        for r in range(self.maze.rows):
            for c in range(self.maze.cols):
                if (r, c) == self.maze.start:
                    self.canvas.itemconfig(self.rect_ids[r][c], fill=COLOR_START)
                elif (r, c) == self.maze.goal:
                    self.canvas.itemconfig(self.rect_ids[r][c], fill=COLOR_GOAL)
                elif self.maze.grid[r, c] == PATH:
                    self.canvas.itemconfig(self.rect_ids[r][c], fill=COLOR_PATH)
                else:
                    self.canvas.itemconfig(self.rect_ids[r][c], fill=COLOR_WALL)

        # Bring text markers to top
        if "start" in self.text_ids:
            self.canvas.tag_raise(self.text_ids["start"])
        if "goal" in self.text_ids:
            self.canvas.tag_raise(self.text_ids["goal"])
