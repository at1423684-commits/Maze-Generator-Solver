import time
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Dict

from maze_generator import Maze, PATH, WALL
from algorithms import MazeSolver, SolveResult
from visualization import MazeCanvas, COLOR_START, COLOR_GOAL, COLOR_WALL, COLOR_PATH
from algorithm_race import AlgorithmRaceEngine, FourWayRaceWindow
from performance import PerformancePanel


class MazeApplication(tk.Tk):
   

    def __init__(self):
        super().__init__()
        self.title("Maze Generator and Solver with Algorithm Race | MCA Mini-Project")
        self.geometry("1340x860")
        self.minsize(1050, 700)

        # ---- Application State ----
        self.maze: Maze = Maze("Medium")
        self.maze.generate(braid_factor=0.08)
        self.last_results: Dict[str, SolveResult] = {}

        # Animation state
        self.is_animating = False
        self.current_generator = None
        self.anim_job_id: Optional[str] = None
        self._resize_timer: Optional[str] = None

        # Build UI
        self._build_layout()
        self._bind_events()

        # Initial render after window is ready
        self.after(100, self._initial_setup)

    # =========================================================================
    # LAYOUT BUILDER
    # =========================================================================
    def _build_layout(self):
        """Constructs the overall layout: Header, Middle body, Bottom panel."""
        self._build_header()

        middle = tk.Frame(self)
        middle.pack(fill=tk.BOTH, expand=True, padx=10, pady=6)

        self._build_left_panel(middle)
        self._build_center_panel(middle)
        self._build_right_panel(middle)

        self._build_bottom_panel()

    # =========================================================================
    # 1. HEADER
    # =========================================================================
    def _build_header(self):
        """Top banner showing project title and status."""
        header = tk.Frame(self, relief=tk.RIDGE, bd=1, pady=6, padx=12)
        header.pack(fill=tk.X)

        title_box = tk.Frame(header)
        title_box.pack(side=tk.LEFT)

        tk.Label(
            title_box,
            text="Maze Generator and Solver with Algorithm Race",
            font=("Arial", 15, "bold")
        ).pack(anchor="w")

        tk.Label(
            title_box,
            text="MCA Mini-Project  |  Python Programming  &  Design and Analysis of Algorithms (DAA)",
            font=("Arial", 9)
        ).pack(anchor="w")

        # Status label on the right
        self.global_status_label = tk.Label(
            header,
            text="Status: Ready",
            font=("Arial", 9, "bold"),
            relief=tk.SUNKEN,
            padx=8, pady=2
        )
        self.global_status_label.pack(side=tk.RIGHT)

    # =========================================================================
    # 2. LEFT PANEL  (Controls)
    # =========================================================================
    def _build_left_panel(self, parent: tk.Widget):
        """Control panel: maze settings, algorithm selection, action buttons."""
        left = tk.Frame(parent, relief=tk.RIDGE, bd=1, width=250, padx=8, pady=8)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 6))
        left.pack_propagate(False)

        # ---- Section 1: Maze Configuration ----
        tk.Label(left, text="1. MAZE CONFIGURATION", font=("Arial", 9, "bold")).pack(anchor="w", pady=(0, 4))

        tk.Label(left, text="Grid Size:", font=("Arial", 9)).pack(anchor="w")
        self.size_var = tk.StringVar(value="Medium (27x27)")
        size_combo = ttk.Combobox(
            left,
            textvariable=self.size_var,
            values=["Small (15x15)", "Medium (27x27)", "Large (41x41)"],
            state="readonly",
            width=22
        )
        size_combo.pack(fill=tk.X, pady=(2, 6))
        size_combo.bind("<<ComboboxSelected>>", self._on_size_change)

        tk.Label(left, text="Maze Topology:", font=("Arial", 9)).pack(anchor="w")
        self.topo_var = tk.StringVar(value="Braid (Loops / Multi-Path)")
        topo_combo = ttk.Combobox(
            left,
            textvariable=self.topo_var,
            values=["Braid (Loops / Multi-Path)", "Perfect (Tree / Single Path)"],
            state="readonly",
            width=22
        )
        topo_combo.pack(fill=tk.X, pady=(2, 8))

        self.gen_btn = tk.Button(
            left,
            text="Generate New Maze",
            command=self.action_generate_maze,
            font=("Arial", 10, "bold"),
            width=22
        )
        self.gen_btn.pack(fill=tk.X, pady=(0, 8))

        ttk.Separator(left, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=4)

        # ---- Section 2: Algorithm Selection ----
        tk.Label(left, text="2. ALGORITHM SELECTION", font=("Arial", 9, "bold")).pack(anchor="w", pady=(4, 4))

        self.algo_var = tk.StringVar(value=MazeSolver.ALGORITHMS[0])
        for algo in MazeSolver.ALGORITHMS:
            tk.Radiobutton(
                left,
                text=algo,
                variable=self.algo_var,
                value=algo,
                font=("Arial", 9),
                command=self._on_algorithm_select
            ).pack(anchor="w", pady=1)

        # Animation speed
        tk.Label(left, text="Animation Speed:", font=("Arial", 9)).pack(anchor="w", pady=(8, 0))
        self.speed_var = tk.IntVar(value=10)
        tk.Scale(
            left,
            from_=1, to=40,
            orient=tk.HORIZONTAL,
            variable=self.speed_var,
            length=200
        ).pack(fill=tk.X, pady=(0, 8))

        ttk.Separator(left, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=4)

        # ---- Section 3: Action Buttons ----
        tk.Label(left, text="3. ACTIONS", font=("Arial", 9, "bold")).pack(anchor="w", pady=(4, 4))

        self.solve_btn = tk.Button(
            left,
            text="Solve Maze (Animated)",
            command=self.action_solve_maze,
            font=("Arial", 10, "bold"),
            width=22
        )
        self.solve_btn.pack(fill=tk.X, pady=(0, 4))

        self.race_btn = tk.Button(
            left,
            text="3-Way Live Race",
            command=self.action_open_race_arena,
            font=("Arial", 9, "bold"),
            width=22
        )
        self.race_btn.pack(fill=tk.X, pady=(0, 4))

        self.bench_btn = tk.Button(
            left,
            text="Instant Benchmark",
            command=self.action_instant_benchmark,
            font=("Arial", 9),
            width=22
        )
        self.bench_btn.pack(fill=tk.X, pady=(0, 8))

        ttk.Separator(left, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=4)

        # Utility buttons in a row
        util_row = tk.Frame(left)
        util_row.pack(fill=tk.X, pady=(4, 0))

        self.clear_btn = tk.Button(
            util_row,
            text="Clear Path",
            command=self.action_clear_solution,
            font=("Arial", 9),
            width=10
        )
        self.clear_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 2))

        self.reset_btn = tk.Button(
            util_row,
            text="Reset",
            command=self.action_reset,
            font=("Arial", 9),
            width=10
        )
        self.reset_btn.pack(side=tk.RIGHT, expand=True, fill=tk.X, padx=(2, 0))

    # =========================================================================
    # 3. CENTER PANEL  (Maze Canvas + Legend)
    # =========================================================================
    def _build_center_panel(self, parent: tk.Widget):
        """Center frame containing the color legend and the maze canvas."""
        center = tk.Frame(parent, relief=tk.RIDGE, bd=1)
        center.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=6)

        # Color legend bar
        legend_bar = tk.Frame(center, bd=1, relief=tk.SUNKEN, pady=4, padx=6)
        legend_bar.pack(fill=tk.X, side=tk.TOP)

        legends = [
            ("Start (S)", COLOR_START),
            ("Goal (G)",  COLOR_GOAL),
            ("Wall",      COLOR_WALL),
            ("Passage",   "#ffffff"),
            ("Visited",   "#60a5fa"),
            ("Frontier",  "#f59e0b"),
            ("Solution",  COLOR_PATH)
        ]

        for label_text, color in legends:
            item = tk.Frame(legend_bar)
            item.pack(side=tk.LEFT, padx=6)

            # Small colored square
            tk.Label(
                item, text="  ",
                bg=color, width=2, height=1,
                relief=tk.SOLID, bd=1
            ).pack(side=tk.LEFT, padx=(0, 3))

            tk.Label(
                item, text=label_text,
                font=("Arial", 8)
            ).pack(side=tk.LEFT)

        # Main canvas
        self.canvas = tk.Canvas(center, bg="white", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

        self.visualizer = MazeCanvas(self.canvas)

    # =========================================================================
    # 4. RIGHT PANEL  (Live Metrics + Algorithm Info)
    # =========================================================================
    def _build_right_panel(self, parent: tk.Widget):
        """Right panel displaying live search metrics and algorithm details."""
        right = tk.Frame(parent, relief=tk.RIDGE, bd=1, width=270, padx=8, pady=8)
        right.pack(side=tk.RIGHT, fill=tk.Y, padx=(6, 0))
        right.pack_propagate(False)

        # ---- Live Metrics ----
        tk.Label(right, text="LIVE SEARCH METRICS", font=("Arial", 9, "bold")).pack(anchor="w", pady=(0, 4))

        metrics_frame = tk.LabelFrame(right, text="Results", font=("Arial", 8), padx=6, pady=6)
        metrics_frame.pack(fill=tk.X, pady=(0, 8))

        self.metric_labels = {}
        fields = [
            ("Algorithm",      "algo",    "Breadth-First Search (BFS)"),
            ("Status",         "status",  "Idle / Ready"),
            ("Execution Time", "time",    "0.00 ms"),
            ("Nodes Visited",  "visited", "0 cells"),
            ("Path Length",    "path",    "0 steps"),
            ("Optimality",     "opt",     "Optimal"),
            ("Data Structure", "ds",      "Queue (FIFO)")
        ]

        for title, key, default_val in fields:
            row = tk.Frame(metrics_frame)
            row.pack(fill=tk.X, pady=2)

            tk.Label(row, text=f"{title}:", font=("Arial", 8), anchor="w").pack(side=tk.LEFT)

            v_lbl = tk.Label(
                row, text=default_val,
                font=("Arial", 8, "bold"),
                wraplength=130,
                justify=tk.RIGHT
            )
            v_lbl.pack(side=tk.RIGHT)
            self.metric_labels[key] = v_lbl

        # ---- Algorithm Information ----
        tk.Label(right, text="DAA ALGORITHM INSIGHT", font=("Arial", 9, "bold")).pack(anchor="w", pady=(4, 4))

        self.info_box = tk.Text(
            right,
            wrap=tk.WORD,
            font=("Arial", 9),
            padx=6, pady=6,
            relief=tk.SUNKEN,
            bd=1,
            height=14
        )
        self.info_box.pack(fill=tk.BOTH, expand=True)
        self._update_algorithm_info(MazeSolver.ALGORITHMS[0])

    # =========================================================================
    # 5. BOTTOM PANEL  (Matplotlib Charts + Complexity Table)
    # =========================================================================
    def _build_bottom_panel(self):
        """Bottom section containing performance charts and DAA complexity view."""
        bottom = tk.Frame(self, relief=tk.RIDGE, bd=1, height=230)
        bottom.pack(fill=tk.X, side=tk.BOTTOM, padx=10, pady=(0, 8))
        bottom.pack_propagate(False)

        self.performance_panel = PerformancePanel(bottom)
        self.performance_panel.pack(fill=tk.BOTH, expand=True)

    # =========================================================================
    # EVENT BINDINGS
    # =========================================================================
    def _bind_events(self):
        """Binds canvas resize event with debouncing."""
        self.canvas.bind("<Configure>", self._on_canvas_configure)

    def _initial_setup(self):
        """Renders maze and runs initial benchmark after window is ready."""
        self.visualizer.render_maze(self.maze)
        self.action_instant_benchmark()

    def _on_canvas_configure(self, event):
        """Debounced resize handler to avoid excessive redraws."""
        if self.is_animating:
            return
        if self._resize_timer:
            self.after_cancel(self._resize_timer)
        self._resize_timer = self.after(150, self._handle_resize)

    def _handle_resize(self):
        if self.maze and not self.is_animating:
            self.visualizer.render_maze(self.maze)

    def _on_size_change(self, event=None):
        """Generates a new maze when user changes grid size."""
        self.action_generate_maze()

    def _on_algorithm_select(self):
        """Updates right-panel information when user changes algorithm radio button."""
        selected = self.algo_var.get()
        self.metric_labels["algo"].config(text=selected)
        meta = MazeSolver.METADATA[selected]
        self.metric_labels["opt"].config(text=meta["optimality"].split()[0])
        self.metric_labels["ds"].config(text=meta["data_structure"].split()[0])
        self._update_algorithm_info(selected)

    def _update_algorithm_info(self, algo_name: str):
        """Fills the info text box with theoretical details of the selected algorithm."""
        meta = MazeSolver.METADATA[algo_name]
        content = (
            f"Algorithm : {algo_name}\n\n"
            f"Time Complexity  : {meta['time_complexity']}\n"
            f"Space Complexity : {meta['space_complexity']}\n"
            f"Data Structure   : {meta['data_structure']}\n"
            f"Optimality       : {meta['optimality']}\n\n"
            f"Description:\n{meta['description']}"
        )
        self.info_box.config(state=tk.NORMAL)
        self.info_box.delete("1.0", tk.END)
        self.info_box.insert(tk.END, content)
        self.info_box.config(state=tk.DISABLED)

    # =========================================================================
    # ACTIONS
    # =========================================================================
    def action_generate_maze(self):
        """Generates a new random maze using Recursive Backtracking (DFS)."""
        if self.is_animating:
            self._stop_animation()

        size_str = self.size_var.get().split()[0]          # "Small", "Medium", or "Large"
        braid = 0.08 if "Braid" in self.topo_var.get() else 0.0

        self.maze = Maze(size_str)
        self.maze.generate(braid_factor=braid)

        self.visualizer.render_maze(self.maze)
        self.global_status_label.config(text="Status: Maze Generated")
        self._reset_metric_labels()
        self.action_instant_benchmark()

    def action_clear_solution(self):
        """Clears visited-node colors and solution path without changing walls."""
        if self.is_animating:
            self._stop_animation()
        self.visualizer.clear_solution()
        self.global_status_label.config(text="Status: Path Cleared")
        self._reset_metric_labels()

    def action_reset(self):
        """Resets by generating a fresh maze."""
        self.action_generate_maze()

    def _reset_metric_labels(self):
        """Resets the metric values in the right panel to defaults."""
        self.metric_labels["status"].config(text="Idle / Ready")
        self.metric_labels["time"].config(text="0.00 ms")
        self.metric_labels["visited"].config(text="0 cells")
        self.metric_labels["path"].config(text="0 steps")

    def action_solve_maze(self):
        """Starts animated step-by-step solving using the selected algorithm."""
        if self.is_animating:
            return

        self.action_clear_solution()
        algo_name = self.algo_var.get()

        self.is_animating = True
        self.global_status_label.config(text="Status: Solving...")
        self.metric_labels["status"].config(text="Searching...")
        self._set_controls_state(tk.DISABLED)

        # Create the step generator from the selected algorithm
        self.current_generator = MazeSolver.solve_step_generator(self.maze, algo_name)
        self._animation_loop()

    def _animation_loop(self):
        
        if not self.is_animating or not self.current_generator:
            return

        delay = self.speed_var.get()
        batch_size = max(1, 30 // max(1, delay))

        done = False
        final_event = None

        for _ in range(batch_size):
            try:
                event = next(self.current_generator)
                if event[0] == "visit":
                    r, c = event[1]
                    self.visualizer.mark_visited(r, c)
                elif event[0] == "done":
                    done = True
                    final_event = event
                    break
            except StopIteration:
                done = True
                break

        if done:
            self.is_animating = False
            self._set_controls_state(tk.NORMAL)

            if final_event and final_event[1]:      # Maze was solved
                solved, path, visited_count, elapsed = (
                    final_event[1], final_event[2], final_event[3], final_event[4]
                )
                self.visualizer.mark_path(path)
                self.global_status_label.config(text="Status: Maze Solved!")
                self.metric_labels["status"].config(text="Solved Successfully")
                self.metric_labels["time"].config(text=f"{elapsed:.2f} ms")
                self.metric_labels["visited"].config(text=f"{visited_count} cells")
                self.metric_labels["path"].config(text=f"{len(path)} steps")
            else:
                self.global_status_label.config(text="Status: No Path Found")
                self.metric_labels["status"].config(text="No Path Found")
        else:
            self.anim_job_id = self.after(delay, self._animation_loop)

    def _stop_animation(self):
        """Safely cancels any ongoing animation."""
        self.is_animating = False
        if self.anim_job_id:
            self.after_cancel(self.anim_job_id)
            self.anim_job_id = None
        self.current_generator = None
        self._set_controls_state(tk.NORMAL)

    def _set_controls_state(self, state):
        """Enables or disables action buttons during animation."""
        self.gen_btn.config(state=state)
        self.solve_btn.config(state=state)
        self.bench_btn.config(state=state)
        self.race_btn.config(state=state)

    def action_instant_benchmark(self):
        """Runs all 3 algorithms silently (no animation) and updates the charts."""
        self.last_results = AlgorithmRaceEngine.run_benchmark(self.maze)
        self.performance_panel.update_results(self.last_results)
        self.global_status_label.config(text="Status: Benchmark Updated")

    def action_open_race_arena(self):
        """Opens the 3-Way Visual Race window (separate Toplevel window)."""
        if self.is_animating:
            self._stop_animation()
        race_window = FourWayRaceWindow(self, self.maze)
        race_window.grab_set()


# =============================================================================
# ENTRY POINT
# =============================================================================
if __name__ == "__main__":
    app = MazeApplication()
    app.mainloop()
