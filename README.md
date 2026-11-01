# 🏁 Maze Generator and Solver with Algorithm Race

A comprehensive desktop application developed using **Python 3**, **Tkinter**, **Matplotlib**, and **NumPy**. Designed specifically for MCA (Master of Computer Applications) academic coursework, demonstrating core paradigms from **Python Programming** and **Design and Analysis of Algorithms (DAA)**.

![Maze Visual Comparison](assets/maze_solution_comparison.png)

---

## 🌟 Key Features

1. **Random Maze Generation (Recursive Backtracking / DFS)**:
   - Generates spanning-tree perfect mazes with zero cycles.
   - Braid maze mode introduces loops to highlight differences in algorithm path optimality.
   - Multiple preset sizes: **Small (15x15)**, **Medium (27x27)**, **Large (41x41)**.
   - Color-coded grid: Start (Emerald Green `S`), Destination (Crimson Red `G`), Walls (Slate Navy), and Passages (Off-White).

2. **Four Search Algorithms**:
   - **Breadth-First Search (BFS)**: Uninformed search using a FIFO Queue (`collections.deque`). Guarantees the shortest path on unweighted grids.
   - **Depth-First Search (DFS)**: Uninformed search using a LIFO Stack (`list`). Explores deep branches; non-optimal pathfinder.
   - **Dijkstra's Algorithm**: Greedy search using a Min-Heap Priority Queue (`heapq`). Guarantees minimum cost/shortest path.
   - **A\* Search Algorithm**: Informed heuristic search using a Min-Heap Priority Queue with Manhattan Distance heuristic $h(n) = |x_1 - x_2| + |y_1 - y_2|$. Significantly reduces nodes explored while preserving 100% path optimality.

3. **⚡ 4-Way Synchronized Live Algorithm Race Arena**:
   - Dedicated multi-grid window displaying 4 synchronized mini-canvases in a 2x2 grid.
   - Watch all 4 algorithms race simultaneously in real time on the identical maze topology.
   - Automatically ranks finishing order and crowns the winner with execution time and nodes visited metrics.

4. **Interactive Step-by-Step Visualization**:
   - High-performance Tkinter canvas with 2D item-ID caching (zero redraw lag, smooth 60 FPS animation).
   - Speed control slider (from fine single-step stepping to fast batch simulation).
   - Live metrics display: execution time in milliseconds, nodes visited count, path length, and frontier memory footprint.

5. **📊 Matplotlib Comparative Performance Analysis**:
   - Embedded 3-panel bar charts comparing:
     - **Execution Time (ms)**
     - **Nodes Visited / Explored**
     - **Solution Path Length (steps)**
   - Theoretical DAA Complexity Matrix table (Worst-Case Time, Best-Case Time, Space Complexity, Data Structures).
   - Analytical academic report generation.

---

## 🏗️ Project Architecture

```
Maze_Generator_Solver/
│
├── main.py                 # Primary Tkinter GUI application & event coordinator
├── maze_generator.py       # Recursive backtracking DFS maze generator & grid model
├── algorithms.py           # BFS, DFS, Dijkstra, and A* solvers & step-generators
├── visualization.py        # Tkinter Canvas rendering & high-speed cell recoloring
├── algorithm_race.py       # Headless benchmark engine & 4-way visual race arena
├── performance.py          # Embedded Matplotlib charts & DAA complexity tables
├── requirements.txt        # Python package dependencies
├── README.md               # User manual & quickstart guide
├── PROJECT_REPORT.md       # Complete 22-section MCA college project report & Viva Q&A
│
├── assets/                 # Charts, visualizations, and icons
│   ├── benchmark_comparison.png
│   └── maze_solution_comparison.png
│
├── test_maze_suite.py      # Automated unit tests for algorithms and invariants
├── test_gui_smoke.py       # Automated GUI smoke tests & simulation integrity
└── generate_assets.py      # Script to generate sample report assets
```

---

## 💻 System Requirements

- **Operating System**: Windows 10 / 11, Linux, or macOS
- **Python**: Python 3.8 to Python 3.15+
- **Python Libraries**:
  - `tkinter` (included with standard Python on Windows/macOS)
  - `numpy >= 1.20.0`
  - `matplotlib >= 3.5.0`

---

## 🚀 Installation & Execution

### 1. Clone or Open Project Directory
Open PowerShell or your terminal in the project directory:
```powershell
cd "c:\Users\HP\Downloads\anti projects\Maze_Generator_Solver"
```

### 2. Install Required Dependencies
```powershell
pip install -r requirements.txt
```

### 3. Launch the Application
```powershell
python main.py
```

### 4. Run Automated Test Suites
To verify algorithm correctness, path optimality invariants, and GUI stability:
```powershell
python test_maze_suite.py
python test_gui_smoke.py
```

---

## 🎮 How to Use the Application

1. **Generate a Maze**:
   - Select a grid size (`Small`, `Medium`, or `Large`).
   - Select topology: `Braid (Loops / Multi-Path)` or `Perfect (Tree / Single Path)`.
   - Click **"✨ Generate New Maze"**.

2. **Solve with Step-by-Step Animation**:
   - Choose an algorithm (BFS, DFS, Dijkstra, or A* Search) via the radio buttons.
   - Adjust the **Animation Speed** slider.
   - Click **"▶ Solve Maze (Animated)"**.
   - Observe the frontier expanding (Amber), visited nodes (Sky Blue), and final path (Radiant Gold).

3. **Launch the 4-Way Live Race Arena**:
   - Click **"⚡ 4-Way Live Race Arena"**.
   - In the pop-up window, click **"▶ Start Live Race"**.
   - Watch all four algorithms navigate the same maze simultaneously!
   - Receive the winner announcement with execution time and nodes visited.

4. **Instant Benchmark & Performance Charts**:
   - Click **"📊 Instant Benchmark Race"** or solve any maze.
   - View the bottom notebook tabs:
     - **Tab 1: 📊 Performance Charts** (embedded Matplotlib bar charts).
     - **Tab 2: 📑 DAA Complexity Matrix** (Big-O analysis and data structures).
     - **Tab 3: 📋 Analytical Report** (academic findings and optimality breakdown).

---

## 📈 DAA Complexity Comparison Summary

| Algorithm | Worst-Case Time | Best-Case Time | Space Complexity | Data Structure | Optimality |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Breadth-First Search (BFS)** | $O(V + E)$ | $O(1)$ | $O(V)$ | Queue (`deque`, FIFO) | **Optimal** |
| **Depth-First Search (DFS)** | $O(V + E)$ | $O(d)$ | $O(V)$ | Stack (`list`, LIFO) | **Non-Optimal** |
| **Dijkstra's Algorithm** | $O((V + E) \log V)$ | $O((V + E) \log V)$ | $O(V)$ | Min-Heap (`heapq`) | **Optimal** |
| **A\* Search Algorithm** | $O((V + E) \log V)$ | $O(d)$ | $O(V)$ | Min-Heap ($f = g + h$) | **Optimal** |

*Note: In an unweighted maze, vertices $V$ are passage cells, and edges $E$ are valid 4-directional transitions.*

---

## 🎓 Academic Presentation Tips

For your college presentation or viva examination:
1. Explain **why DFS finds long paths on braid mazes**: DFS dives deep along the first branch it picks and only backtracks upon hitting dead ends.
2. Explain **why A\* visits fewer cells than BFS**: BFS expands uniformly in all directions (circular wave), whereas A\* uses the Manhattan distance heuristic $h(n)$ to steer the search cone toward the red destination marker.
3. Show the **4-Way Live Race Arena**: It provides an unforgettable visual proof of theoretical DAA principles in action!

---

## 📜 License & Acknowledgements
Developed for academic mini-project submission in MCA Degree Program. Released under the MIT License.
