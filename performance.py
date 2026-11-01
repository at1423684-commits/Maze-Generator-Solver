

import tkinter as tk
from tkinter import ttk
from typing import Dict, List, Optional
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

from algorithms import MazeSolver, SolveResult


# DAA Complexity Reference Data (Syllabus Algorithms)
DAA_COMPLEXITY_TABLE = [
    {
        "algorithm": "Breadth-First Search (BFS)",
        "time_worst": "O(V + E)",
        "time_best": "O(1) [Goal adjacent]",
        "space": "O(V)",
        "data_struct": "Queue (FIFO - deque)",
        "optimality": "Optimal (Shortest Path)",
        "approach": "Uninformed / Level-order traversal"
    },
    {
        "algorithm": "Depth-First Search (DFS)",
        "time_worst": "O(V + E)",
        "time_best": "O(d) [Lucky dive to goal]",
        "space": "O(V)",
        "data_struct": "Stack (LIFO - list)",
        "optimality": "Non-Optimal (Long detours in loops)",
        "approach": "Uninformed / Deep branch backtracking"
    },
    {
        "algorithm": "Dijkstra's Algorithm",
        "time_worst": "O((V + E) log V)",
        "time_best": "O((V + E) log V)",
        "space": "O(V)",
        "data_struct": "Priority Queue (Min-Heap)",
        "optimality": "Optimal (Minimum Cost)",
        "approach": "Greedy / Uniform-cost exploration"
    }
]


class PerformanceVisualizer:
    """
    Renders Matplotlib comparative performance charts and textual DAA reports.
    """

    CHART_COLORS = ["#38bdf8", "#f43f5e", "#10b981"]

    @classmethod
    def create_comparison_figure(cls, results: Dict[str, SolveResult]) -> Figure:
        """
        Creates a 3-subplot Matplotlib Figure comparing:
        1. Execution Time (milliseconds)
        2. Nodes Visited / Explored
        3. Solution Path Length
        
        Args:
            results: Dictionary mapping algorithm name to SolveResult.
            
        Returns:
            matplotlib.figure.Figure instance configured with dark theme.
        """
        # Create figure with dark styling
        fig = Figure(figsize=(9.5, 4.2), dpi=100, facecolor="#1e293b")

        # Syllabus algorithms
        algos_short = ["BFS", "DFS", "Dijkstra"]
        full_names = [
            "Breadth-First Search (BFS)",
            "Depth-First Search (DFS)",
            "Dijkstra's Algorithm"
        ]

        times = [results.get(name).execution_time_ms if results.get(name) else 0.0 for name in full_names]
        nodes = [results.get(name).nodes_visited if results.get(name) else 0 for name in full_names]
        paths = [results.get(name).path_length if results.get(name) else 0 for name in full_names]

        x = np.arange(len(algos_short))
        width = 0.50

        # Subplot 1: Execution Time
        ax1 = fig.add_subplot(131, facecolor="#0f172a")
        bars1 = ax1.bar(x, times, width, color=cls.CHART_COLORS, edgecolor="#334155")
        ax1.set_title("Execution Time (ms)", color="#f8fafc", fontsize=10, fontweight="bold", pad=8)
        ax1.set_xticks(x)
        ax1.set_xticklabels(algos_short, color="#cbd5e1", fontsize=8, fontweight="bold")
        ax1.tick_params(colors="#94a3b8", labelsize=8)
        ax1.grid(axis="y", linestyle="--", alpha=0.3, color="#64748b")
        for bar in bars1:
            h = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width() / 2.0, h + max(0.05, h * 0.03),
                     f"{h:.1f}", ha="center", va="bottom", color="#f8fafc", fontsize=8, fontweight="bold")

        # Subplot 2: Nodes Explored
        ax2 = fig.add_subplot(132, facecolor="#0f172a")
        bars2 = ax2.bar(x, nodes, width, color=cls.CHART_COLORS, edgecolor="#334155")
        ax2.set_title("Nodes Explored (Count)", color="#f8fafc", fontsize=10, fontweight="bold", pad=8)
        ax2.set_xticks(x)
        ax2.set_xticklabels(algos_short, color="#cbd5e1", fontsize=8, fontweight="bold")
        ax2.tick_params(colors="#94a3b8", labelsize=8)
        ax2.grid(axis="y", linestyle="--", alpha=0.3, color="#64748b")
        for bar in bars2:
            h = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width() / 2.0, h + max(1, h * 0.03),
                     f"{int(h)}", ha="center", va="bottom", color="#f8fafc", fontsize=8, fontweight="bold")

        # Subplot 3: Path Length
        ax3 = fig.add_subplot(133, facecolor="#0f172a")
        bars3 = ax3.bar(x, paths, width, color=cls.CHART_COLORS, edgecolor="#334155")
        ax3.set_title("Path Length (Steps)", color="#f8fafc", fontsize=10, fontweight="bold", pad=8)
        ax3.set_xticks(x)
        ax3.set_xticklabels(algos_short, color="#cbd5e1", fontsize=8, fontweight="bold")
        ax3.tick_params(colors="#94a3b8", labelsize=8)
        ax3.grid(axis="y", linestyle="--", alpha=0.3, color="#64748b")
        for bar in bars3:
            h = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width() / 2.0, h + max(1, h * 0.03),
                     f"{int(h)}", ha="center", va="bottom", color="#f8fafc", fontsize=8, fontweight="bold")

        # Adjust layout
        fig.tight_layout(pad=2.0)
        return fig

    @classmethod
    def generate_analytical_report(cls, results: Dict[str, SolveResult]) -> str:
        """
        Generates a comprehensive analytical report suitable for college viva.
        """
        lines = []
        lines.append("=" * 72)
        lines.append("       ALGORITHM RACE & PERFORMANCE ANALYSIS REPORT (DAA)")
        lines.append("=" * 72)
        lines.append("")
        lines.append(f"{'Algorithm':<28} | {'Time (ms)':<10} | {'Visited':<8} | {'Path':<6} | {'Optimality':<12}")
        lines.append("-" * 72)

        for name in MazeSolver.ALGORITHMS:
            res = results.get(name)
            if res:
                opt_str = "Optimal" if "Optimal" in res.optimality else "Non-Opt"
                lines.append(f"{name:<28} | {res.execution_time_ms:<10.2f} | {res.nodes_visited:<8} | {res.path_length:<6} | {opt_str:<12}")
            else:
                lines.append(f"{name:<28} | {'N/A':<10} | {'N/A':<8} | {'N/A':<6} | {'N/A':<12}")

        lines.append("-" * 72)
        lines.append("")
        lines.append("KEY DAA THEORETICAL & EMPIRICAL FINDINGS:")
        lines.append("-" * 72)
        lines.append("1. Path Optimality:")
        lines.append("   • BFS and Dijkstra are mathematically guaranteed to find the shortest path.")
        lines.append("   • DFS finds ANY valid path by following branches to dead-ends. When cycles")
        lines.append("     or alternative routes exist, DFS path length can be significantly longer.")
        lines.append("")
        lines.append("2. Search Mechanism Comparison:")
        lines.append("   • BFS uses a FIFO Queue (deque) with O(1) operations per vertex.")
        lines.append("   • DFS uses a LIFO Stack (list) with O(1) push and pop operations.")
        lines.append("   • Dijkstra uses a Min-Heap Priority Queue (heapq) with O(log V) operations.")
        lines.append("   • In this unweighted grid (cost = 1), BFS and Dijkstra explore identical")
        lines.append("     nodes, but BFS runs faster due to lower constant-factor queue overhead.")
        lines.append("")
        lines.append("3. Execution Time Nuance:")
        lines.append("   • Measured using high-resolution time.perf_counter().")
        lines.append("   • System scheduling, CPU frequency scaling, and background OS processes")
        lines.append("     may cause minor execution time fluctuations between test runs.")
        lines.append("=" * 72)

        return "\n".join(lines)


class PerformancePanel(tk.Frame):
   

    def __init__(self, parent: tk.Widget, *args, **kwargs):
        super().__init__(parent, bg="#1e293b", *args, **kwargs)
        self.figure_canvas: Optional[FigureCanvasTkAgg] = None
        self._build_ui()

    def _build_ui(self):
        # Notebook for switching between Charts, Complexity Matrix, and Report
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        # Tab 1: Charts
        self.chart_tab = tk.Frame(self.notebook, bg="#1e293b")
        self.notebook.add(self.chart_tab, text="Performance Charts")

        # Tab 2: Complexity Table
        self.table_tab = tk.Frame(self.notebook, bg="#1e293b")
        self.notebook.add(self.table_tab, text="DAA Complexity Matrix")

        # Tab 3: Detailed Report
        self.report_tab = tk.Frame(self.notebook, bg="#1e293b")
        self.notebook.add(self.report_tab, text="Analytical Report")

        self._build_table_tab()
        self._build_report_tab()

    def _build_table_tab(self):
        columns = ("algo", "time_w", "time_b", "space", "ds", "opt", "approach")
        tree = ttk.Treeview(self.table_tab, columns=columns, show="headings", height=5)
        
        tree.heading("algo", text="Algorithm")
        tree.heading("time_w", text="Worst Time")
        tree.heading("time_b", text="Best Time")
        tree.heading("space", text="Space Complexity")
        tree.heading("ds", text="Data Structure")
        tree.heading("opt", text="Optimality")
        tree.heading("approach", text="Algorithmic Paradigm")

        tree.column("algo", width=190, anchor="w")
        tree.column("time_w", width=120, anchor="center")
        tree.column("time_b", width=120, anchor="center")
        tree.column("space", width=120, anchor="center")
        tree.column("ds", width=180, anchor="center")
        tree.column("opt", width=190, anchor="w")
        tree.column("approach", width=220, anchor="w")

        for row in DAA_COMPLEXITY_TABLE:
            tree.insert("", tk.END, values=(
                row["algorithm"],
                row["time_worst"],
                row["time_best"],
                row["space"],
                row["data_struct"],
                row["optimality"],
                row["approach"]
            ))

        tree.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        # Informational explanation below table
        exp_frame = tk.Frame(self.table_tab, bg="#0f172a", padx=10, pady=8)
        exp_frame.pack(fill=tk.X, padx=8, pady=(0, 8))

        lbl = tk.Label(
            exp_frame,
            text="• V = Number of vertices (open passage cells) | E = Number of edges (accessible 4-directional transitions)\n"
                 "• Unweighted Graph: Edge weights equal 1. BFS & Dijkstra achieve identical shortest paths.\n"
                 "• Queue (deque) achieves O(1) amortized push/pop; Min-Heap achieves O(log V) priority queue operations.",
            font=("Segoe UI", 9),
            fg="#94a3b8",
            bg="#0f172a",
            justify=tk.LEFT
        )
        lbl.pack(anchor="w")

    def _build_report_tab(self):
        self.report_text = tk.Text(
            self.report_tab,
            wrap=tk.WORD,
            bg="#0f172a",
            fg="#e2e8f0",
            font=("Consolas", 10),
            padx=10, pady=10,
            relief=tk.FLAT
        )
        scroll = ttk.Scrollbar(self.report_tab, orient=tk.VERTICAL, command=self.report_text.yview)
        self.report_text.configure(yscrollcommand=scroll.set)

        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.report_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Initial placeholder text
        self.report_text.insert(
            tk.END,
            "Run an Algorithm Race or solve individual algorithms to generate the live comparison report.\n"
        )
        self.report_text.config(state=tk.DISABLED)

    def update_results(self, results: Dict[str, SolveResult]):
        """Updates the Matplotlib chart tab and analytical report with fresh results."""
        # Update Chart
        if self.figure_canvas:
            self.figure_canvas.get_tk_widget().destroy()

        fig = PerformanceVisualizer.create_comparison_figure(results)
        self.figure_canvas = FigureCanvasTkAgg(fig, master=self.chart_tab)
        self.figure_canvas.draw()
        self.figure_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Update Report
        report_str = PerformanceVisualizer.generate_analytical_report(results)
        self.report_text.config(state=tk.NORMAL)
        self.report_text.delete("1.0", tk.END)
        self.report_text.insert(tk.END, report_str)
        self.report_text.config(state=tk.DISABLED)
