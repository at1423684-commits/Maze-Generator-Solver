import time
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, List, Tuple, Optional
from maze_generator import Maze, PATH, WALL
from algorithms import MazeSolver, SolveResult


class AlgorithmRaceEngine:
   

    @staticmethod
    def run_benchmark(maze: Maze) -> Dict[str, SolveResult]:
       
        results: Dict[str, SolveResult] = {}
        for algo_name in MazeSolver.ALGORITHMS:
            res = MazeSolver.solve(maze, algo_name)
            results[algo_name] = res

        return results

    @staticmethod
    def determine_winners(results: Dict[str, SolveResult]) -> Dict[str, str]:
       
        valid_results = [r for r in results.values() if r.solved]
        if not valid_results:
            return {
                "fastest_time": "None",
                "least_nodes": "None",
                "shortest_path": "None",
                "overall_winner": "None"
            }

        # 1. Fastest Execution Time
        fastest = min(valid_results, key=lambda r: r.execution_time_ms)

        # 2. Least Nodes Visited (Search Efficiency)
        least_nodes = min(valid_results, key=lambda r: r.nodes_visited)

        # 3. Shortest Path (Optimality)
        shortest_path = min(valid_results, key=lambda r: r.path_length)

        # 4. Overall Winner: Must find shortest path + best balance of time and node expansions
        min_path = shortest_path.path_length
        optimal_algos = [r for r in valid_results if r.path_length == min_path]

        if optimal_algos:
            overall = min(optimal_algos, key=lambda r: (r.nodes_visited * 0.5 + r.execution_time_ms * 10 * 0.5))
        else:
            overall = fastest

        return {
            "fastest_time": fastest.algorithm_name,
            "least_nodes": least_nodes.algorithm_name,
            "shortest_path": shortest_path.algorithm_name,
            "overall_winner": overall.algorithm_name
        }


class AlgorithmRaceWindow(tk.Toplevel):
    

    COLORS = {
        "wall": "#1e293b",
        "path": "#f8fafc",
        "start": "#10b981",
        "goal": "#ef4444",
        "visited": "#60a5fa",
        "solution": "#facc15",
        "frontier": "#f59e0b"
    }

    def __init__(self, parent: tk.Tk, maze: Maze):
        super().__init__(parent)
        self.title("3-Way Algorithm Live Race (BFS vs DFS vs Dijkstra)")
        self.geometry("1150x650")
        self.minsize(950, 500)
        self.configure(bg="#0f172a")

        self.maze = maze
        self.is_running = False
        self.race_generators = {}
        self.race_states = {}
        self.finish_ranks: List[str] = []
        self.anim_job_id: Optional[str] = None

        self._build_ui()
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.render_all_mazes()

    def _build_ui(self):
        # Header Banner
        header = tk.Frame(self, bg="#1e293b", pady=10, padx=20)
        header.pack(fill=tk.X)

        title_lbl = tk.Label(
            header,
            text="3-Way Synchronized Algorithm Race",
            font=("Segoe UI", 16, "bold"),
            fg="#f8fafc",
            bg="#1e293b"
        )
        title_lbl.pack(side=tk.LEFT)

        sub_lbl = tk.Label(
            header,
            text=f"Maze Size: {self.maze.rows}x{self.maze.cols} | Fair Evaluation on Identical Graph",
            font=("Segoe UI", 10),
            fg="#94a3b8",
            bg="#1e293b"
        )
        sub_lbl.pack(side=tk.LEFT, padx=15)

        # Control Buttons in Header
        btn_frame = tk.Frame(header, bg="#1e293b")
        btn_frame.pack(side=tk.RIGHT)

        self.start_btn = tk.Button(
            btn_frame,
            text="Start Live Race",
            command=self.start_race,
            font=("Segoe UI", 10, "bold"),
            bg="#10b981",
            fg="#ffffff",
            activebackground="#059669",
            padx=12, pady=4,
            relief=tk.FLAT,
            cursor="hand2"
        )
        self.start_btn.pack(side=tk.LEFT, padx=5)

        self.reset_btn = tk.Button(
            btn_frame,
            text="Reset Arena",
            command=self.reset_race,
            font=("Segoe UI", 10),
            bg="#475569",
            fg="#ffffff",
            padx=10, pady=4,
            relief=tk.FLAT,
            cursor="hand2"
        )
        self.reset_btn.pack(side=tk.LEFT, padx=5)

        # Speed Control
        spd_frame = tk.Frame(self, bg="#0f172a", pady=6)
        spd_frame.pack(fill=tk.X, padx=20)

        spd_lbl = tk.Label(spd_frame, text="Race Animation Speed:", fg="#e2e8f0", bg="#0f172a", font=("Segoe UI", 9))
        spd_lbl.pack(side=tk.LEFT)

        self.speed_var = tk.IntVar(value=15)
        self.speed_slider = tk.Scale(
            spd_frame,
            from_=1, to=50,
            orient=tk.HORIZONTAL,
            variable=self.speed_var,
            bg="#0f172a",
            fg="#38bdf8",
            troughcolor="#334155",
            highlightthickness=0,
            length=200
        )
        self.speed_slider.pack(side=tk.LEFT, padx=10)

        spd_hint = tk.Label(spd_frame, text="(Lower = Faster)", fg="#94a3b8", bg="#0f172a", font=("Segoe UI", 8))
        spd_hint.pack(side=tk.LEFT)

        # 1x3 Arena Grid
        arena_frame = tk.Frame(self, bg="#0f172a")
        arena_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        self.algo_widgets = {}
        algos = MazeSolver.ALGORITHMS

        arena_frame.grid_rowconfigure(0, weight=1)
        for i in range(len(algos)):
            arena_frame.grid_columnconfigure(i, weight=1)

        for idx, algo_name in enumerate(algos):
            card = tk.Frame(arena_frame, bg="#1e293b", bd=2, relief=tk.GROOVE)
            card.grid(row=0, column=idx, padx=8, pady=8, sticky="nsew")

            # Title & status bar
            top_bar = tk.Frame(card, bg="#334155", padx=8, pady=4)
            top_bar.pack(fill=tk.X)

            name_lbl = tk.Label(top_bar, text=algo_name, font=("Segoe UI", 11, "bold"), fg="#f8fafc", bg="#334155")
            name_lbl.pack(side=tk.LEFT)

            rank_lbl = tk.Label(top_bar, text="Ready", font=("Segoe UI", 9, "bold"), fg="#38bdf8", bg="#334155")
            rank_lbl.pack(side=tk.RIGHT)

            # Mini Canvas
            canvas = tk.Canvas(card, bg="#0f172a", highlightthickness=0)
            canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

            # Stats Footer
            stat_bar = tk.Frame(card, bg="#1e293b", padx=8, pady=4)
            stat_bar.pack(fill=tk.X)

            stat_lbl = tk.Label(
                stat_bar,
                text="Visited: 0 | Path: 0 | Time: 0.0 ms",
                font=("Segoe UI", 9),
                fg="#cbd5e1",
                bg="#1e293b"
            )
            stat_lbl.pack(side=tk.LEFT)

            self.algo_widgets[algo_name] = {
                "canvas": canvas,
                "rank_lbl": rank_lbl,
                "stat_lbl": stat_lbl,
                "rect_ids": [],
                "finished": False
            }

    def render_all_mazes(self):
        """Draws initial maze state across all three canvases."""
        self.update_idletasks()
        for algo_name, data in self.algo_widgets.items():
            canvas = data["canvas"]
            canvas.delete("all")

            cw = canvas.winfo_width()
            ch = canvas.winfo_height()
            if cw <= 10 or ch <= 10:
                cw, ch = 350, 360

            margin = 8
            cell_w = (cw - 2 * margin) / self.maze.cols
            cell_h = (ch - 2 * margin) / self.maze.rows
            cell_size = max(2.5, min(cell_w, cell_h))

            ox = (cw - cell_size * self.maze.cols) / 2.0
            oy = (ch - cell_size * self.maze.rows) / 2.0

            data["cell_size"] = cell_size
            data["ox"] = ox
            data["oy"] = oy

            rect_ids = [[None for _ in range(self.maze.cols)] for _ in range(self.maze.rows)]
            outline = "#334155" if cell_size >= 10 else ""

            for r in range(self.maze.rows):
                for c in range(self.maze.cols):
                    x1 = ox + c * cell_size
                    y1 = oy + r * cell_size
                    x2 = x1 + cell_size
                    y2 = y1 + cell_size

                    if (r, c) == self.maze.start:
                        fill = self.COLORS["start"]
                    elif (r, c) == self.maze.goal:
                        fill = self.COLORS["goal"]
                    elif self.maze.grid[r, c] == WALL:
                        fill = self.COLORS["wall"]
                    else:
                        fill = self.COLORS["path"]

                    rid = canvas.create_rectangle(x1, y1, x2, y2, fill=fill, outline=outline, width=1 if outline else 0)
                    rect_ids[r][c] = rid

            data["rect_ids"] = rect_ids

    def start_race(self):
        """Initializes generators and starts the animated race loop."""
        if self.is_running:
            return

        self.is_running = True
        self.start_btn.config(state=tk.DISABLED)
        self.finish_ranks.clear()

        # Initialize generators for all algorithms
        self.race_generators = {
            algo: MazeSolver.solve_step_generator(self.maze, algo)
            for algo in MazeSolver.ALGORITHMS
        }
        self.race_states = {
            algo: {"finished": False, "visited": 0, "path_len": 0, "time_ms": 0.0}
            for algo in MazeSolver.ALGORITHMS
        }

        for algo, data in self.algo_widgets.items():
            data["rank_lbl"].config(text="Racing...", fg="#f59e0b")

        self._race_step()

    def _race_step(self):
        """Executes one step across all active algorithm generators."""
        if not self.is_running:
            return

        # Execute iterations per frame for responsive race tempo
        batch_size = max(1, 40 // max(1, self.speed_var.get()))

        for _ in range(batch_size):
            for algo, gen in self.race_generators.items():
                if self.race_states[algo]["finished"]:
                    continue

                try:
                    event = next(gen)
                    data = self.algo_widgets[algo]
                    canvas = data["canvas"]
                    rect_ids = data["rect_ids"]

                    if event[0] == 'visit':
                        curr = event[1]
                        if curr != self.maze.start and curr != self.maze.goal:
                            canvas.itemconfig(rect_ids[curr[0]][curr[1]], fill=self.COLORS["visited"])
                        self.race_states[algo]["visited"] += 1

                    elif event[0] == 'done':
                        solved, path, visited_count, elapsed = event[1], event[2], event[3], event[4]
                        self.race_states[algo]["finished"] = True
                        self.race_states[algo]["visited"] = visited_count
                        self.race_states[algo]["path_len"] = len(path)
                        self.race_states[algo]["time_ms"] = elapsed

                        # Highlight solution path
                        for pr, pc in path:
                            if (pr, pc) != self.maze.start and (pr, pc) != self.maze.goal:
                                canvas.itemconfig(rect_ids[pr][pc], fill=self.COLORS["solution"])

                        self.finish_ranks.append(algo)
                        rank_num = len(self.finish_ranks)
                        rank_text = f"Rank #{rank_num} ({elapsed:.1f}ms)"
                        color = "#10b981" if rank_num == 1 else "#38bdf8"
                        data["rank_lbl"].config(text=rank_text, fg=color)
                        data["stat_lbl"].config(
                            text=f"Visited: {visited_count} | Path: {len(path)} | Time: {elapsed:.2f} ms"
                        )
                except StopIteration:
                    self.race_states[algo]["finished"] = True

        all_done = all(self.race_states[algo]["finished"] for algo in self.race_generators)

        if not all_done and self.is_running:
            self.anim_job_id = self.after(self.speed_var.get(), self._race_step)
        else:
            self.is_running = False
            self.anim_job_id = None
            self.start_btn.config(state=tk.NORMAL)
            self._announce_winner()

    def _announce_winner(self):
        """Displays completion celebration with winner details."""
        if self.finish_ranks:
            winner = self.finish_ranks[0]
            stats = self.race_states[winner]
            messagebox.showinfo(
                "Race Finished",
                f"Live Race Winner: {winner}\n\n"
                f"• Execution Time: {stats['time_ms']:.2f} ms\n"
                f"• Nodes Visited: {stats['visited']}\n"
                f"• Solution Path Length: {stats['path_len']} steps\n\n"
                f"View the Performance Analysis tab in the main window for full Matplotlib graphs!"
            )

    def reset_race(self):
        """Resets the arena and canvases back to clean state."""
        self.is_running = False
        if self.anim_job_id:
            try:
                self.after_cancel(self.anim_job_id)
            except Exception:
                pass
            self.anim_job_id = None

        self.start_btn.config(state=tk.NORMAL)
        self.finish_ranks.clear()
        for algo, data in self.algo_widgets.items():
            data["rank_lbl"].config(text="Ready", fg="#38bdf8")
            data["stat_lbl"].config(text="Visited: 0 | Path: 0 | Time: 0.0 ms")
        self.render_all_mazes()

    def on_close(self):
        """Safe cleanup when closing window."""
        self.is_running = False
        if self.anim_job_id:
            try:
                self.after_cancel(self.anim_job_id)
            except Exception:
                pass
            self.anim_job_id = None
        self.destroy()


# Backwards compatibility alias
FourWayRaceWindow = AlgorithmRaceWindow
