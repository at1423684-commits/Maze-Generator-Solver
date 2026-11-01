# 🧩 Maze Generator and Solver with Algorithm Race

A Python-based desktop application that generates random mazes, solves them using different graph algorithms, and compares their performance through visualisation and an algorithm race.

This project demonstrates important concepts from **Design and Analysis of Algorithms (DAA)**, including graph traversal, stacks, queues, shortest-path algorithms, and time and space complexity.

## 📌 Project Overview

The Maze Generator and Solver allows users to generate different types of mazes and find paths from a starting point to a destination using three algorithms:

1. **Breadth-First Search (BFS)**
2. **Depth-First Search (DFS)**
3. **Dijkstra's Algorithm**

The application also provides an algorithm race where all three algorithms solve the same maze, making it easier to compare their performance.

## ✨ Features

- **Maze Generation:** Generates random mazes using the Recursive Backtracking algorithm.
- **Perfect Maze:** Creates a maze with a unique path between connected points.
- **Braid Maze:** Adds extra passages to create loops and alternative routes.
- **Multiple Maze Sizes:** Choose between Small, Medium, and Large maze presets.
- **Three Solving Algorithms:** Compare BFS, DFS, and Dijkstra.
- **Algorithm Race:** Run all three algorithms on the same maze.
- **Visualisation:** Watch how algorithms explore the maze and find a solution.
- **Animation Controls:** Adjust the solving animation speed.
- **Performance Metrics:** Compare execution time, visited nodes, and path length.
- **Performance Charts:** Visualise algorithm results using Matplotlib.

## 🧠 Algorithms Used

### 1. Maze Generation: Recursive Backtracking (DFS)

Recursive Backtracking is used to generate the maze. It explores unvisited neighbouring cells and creates passages between them. When it reaches a dead end, it backtracks to explore another possible direction.

### 2. Breadth-First Search (BFS)

BFS explores the maze level by level using a queue. It finds the shortest path in an unweighted maze where every movement has the same cost.

### 3. Depth-First Search (DFS)

DFS explores one direction as deeply as possible before backtracking. It uses a stack to manage the search process. It can find a path, but the path is not always the shortest.

### 4. Dijkstra's Algorithm

Dijkstra's algorithm finds the shortest path by exploring the node with the smallest known distance first. It uses a priority queue (min-heap) to select the next node.

Dijkstra is included as an additional shortest-path algorithm to extend the graph algorithm comparison.

## 📊 Algorithm Complexity

Let:
- **V** = Number of vertices (cells)
- **E** = Number of edges (connections between cells)

| Algorithm | Time Complexity | Space Complexity | Data Structure |
|---|---|---|---|
| BFS | O(V + E) | O(V) | Queue |
| DFS | O(V + E) | O(V) | Stack |
| Dijkstra | O((V + E) log V) | O(V) | Priority Queue |

*Note: These are standard complexity bounds for graph representations using adjacency lists and a binary heap for Dijkstra. Actual execution time depends on maze size, implementation, and system performance.*

## 🖥️ Technologies Used

- **Python:** Main programming language.
- **Tkinter:** Used to create the graphical user interface.
- **Matplotlib:** Used to display performance comparison charts.
- **NumPy:** Used for numerical and array-related operations.
- **heapq:** Used to implement the priority queue in Dijkstra's algorithm.
- **collections.deque:** Used to implement the BFS queue.

## 📁 Project Structure

```text
Maze_Generator_Solver/
│
├── main.py
├── maze_generator.py
├── algorithms.py
├── visualization.py
├── algorithm_race.py
├── performance.py
├── requirements.txt
├── README.md
├── PROJECT_REPORT.md
│
└── assets/
    ├── benchmark_comparison.png
    └── maze_solution_comparison.png
```

*This is the expected structure. Keep only the files and folders that are actually present in your project.*

## ⚙️ Installation and Setup

### Prerequisites

- Python 3.8 or above
- pip (Python package installer)

### Step 1: Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### Step 2: Open the Project Folder

```bash
cd Maze_Generator_Solver
```

### Step 3: Install Required Libraries

```bash
pip install -r requirements.txt
```

### Step 4: Run the Application

```bash
python main.py
```

The application window should open, allowing you to generate and solve mazes.

## 🚀 How to Use

1. Run the application using `python main.py`.
2. Select a maze size.
3. Choose the maze type: Perfect Maze or Braid Maze.
4. Generate a new maze.
5. Select BFS, DFS, or Dijkstra to solve the maze.
6. Watch the algorithm explore the maze and find a path.
7. Use the Algorithm Race feature to compare all three algorithms.
8. Observe the performance metrics and comparison charts.

## 📈 Performance Comparison

The application compares the algorithms using three main parameters:

| Parameter | Description |
|---|---|
| Execution Time | Time taken by the algorithm to find a path. |
| Nodes Visited | Number of maze cells explored during the search. |
| Path Length | Number of steps in the final path. |

The results help us understand how different algorithms behave when solving the same maze.

The fastest algorithm may vary depending on the maze structure and size. BFS and Dijkstra find shortest paths in an unweighted maze, while DFS may find a longer path.

## 📚 DAA Concepts Covered

This project connects practical implementation with several DAA concepts:

- Graph representation and traversal.
- Breadth-First Search and Depth-First Search.
- Queue and stack data structures.
- Priority queue and min-heap.
- Shortest-path algorithms.
- Recursive problem-solving.
- Time and space complexity.
- Big-O analysis.
- Performance comparison of algorithms.

## 🎯 Learning Outcomes

Through this project, I learned how to:

- Understand maze generation using recursive backtracking.
- Apply BFS and DFS to graph traversal problems.
- Implement Dijkstra's shortest-path algorithm.
- Use queues, stacks, and priority queues.
- Analyse time and space complexity.
- Compare algorithms through practical experiments.
- Create a graphical application using Python and Tkinter.
- Present algorithm performance through visualisation and charts.

## 🔮 Future Scope

The project can be improved further by adding:

- More maze generation techniques.
- Weighted mazes with different movement costs.
- Additional pathfinding algorithms.
- Exporting performance results.
- More visualisation and customisation options.

## 👨‍💻 Author

Aman Thakur 
MCA (AI/ML)
26MCI10276

## 📄 License

This project was developed for academic and learning purposes as part of the MCA curriculum.
