const canvas = document.getElementById("mazeCanvas");
const ctx = canvas.getContext("2d");

const sizeInput = document.getElementById("mazeSize");
const speedInput = document.getElementById("speed");
const algorithmInput = document.getElementById("algorithm");

const sizeValue = document.getElementById("sizeValue");
const speedValue = document.getElementById("speedValue");
const gridLabel = document.getElementById("gridLabel");
const mazeStatus = document.getElementById("mazeStatus");
const canvasOverlay = document.getElementById("canvasOverlay");

const visitedCount = document.getElementById("visitedCount");
const pathLength = document.getElementById("pathLength");
const executionTime = document.getElementById("executionTime");
const simulationStatus = document.getElementById("simulationStatus");

const generateBtn = document.getElementById("generateBtn");
const solveBtn = document.getElementById("solveBtn");
const clearBtn = document.getElementById("clearBtn");
const overlayGenerate = document.getElementById("overlayGenerate");

let maze = [];
let visitedCells = new Set();
let finalPath = [];
let animationTimer = null;
let isAnimating = false;
let mazeReady = false;

let mazeSize = Number(sizeInput.value);
let start = { r: 1, c: 1 };
let goal = { r: mazeSize - 2, c: mazeSize - 2 };

const COLORS = {
  wall: "#263550",
  empty: "#0b1425",
  visited: "#6557c9",
  path: "#43c9df",
  start: "#50e5a2",
  goal: "#ffbd69",
  grid: "#142139"
};

function key(r, c) {
  return `${r},${c}`;
}

function getSpeedDelay() {
  const speed = Number(speedInput.value);
  return [120, 75, 35, 15, 4][speed - 1];
}

function updateStats(visited = 0, path = 0, time = 0, status = "Idle") {
  visitedCount.textContent = visited;
  pathLength.textContent = path;
  executionTime.innerHTML = `${time} <small>ms</small>`;
  simulationStatus.textContent = status;
}

function stopAnimation() {
  if (animationTimer !== null) {
    clearTimeout(animationTimer);
    animationTimer = null;
  }
  isAnimating = false;
  solveBtn.disabled = false;
  generateBtn.disabled = false;
}

function updateSizeLabels() {
  const value = Number(sizeInput.value);
  sizeValue.textContent = `${value} × ${value}`;
  gridLabel.textContent = `${value} × ${value}`;
}

function updateSpeedLabel() {
  const names = ["Very slow", "Slow", "Normal", "Fast", "Very fast"];
  speedValue.textContent = names[Number(speedInput.value) - 1];
}

function makeEmptyMaze(size) {
  return Array.from({ length: size }, () => Array(size).fill(1));
}

// Generate a maze using randomized depth-first carving.
function generateMaze() {
  stopAnimation();

  mazeSize = Number(sizeInput.value);
  start = { r: 1, c: 1 };
  goal = { r: mazeSize - 2, c: mazeSize - 2 };

  maze = makeEmptyMaze(mazeSize);

  const stack = [{ ...start }];
  maze[start.r][start.c] = 0;

  const directions = [
    [-2, 0], [2, 0], [0, -2], [0, 2]
  ];

  while (stack.length > 0) {
    const current = stack[stack.length - 1];

    const choices = directions
      .map(([dr, dc]) => ({
        r: current.r + dr,
        c: current.c + dc,
        wallR: current.r + dr / 2,
        wallC: current.c + dc / 2
      }))
      .filter(next =>
        next.r > 0 &&
        next.r < mazeSize - 1 &&
        next.c > 0 &&
        next.c < mazeSize - 1 &&
        maze[next.r][next.c] === 1
      );

    if (choices.length === 0) {
      stack.pop();
      continue;
    }

    const next = choices[Math.floor(Math.random() * choices.length)];

    maze[next.wallR][next.wallC] = 0;
    maze[next.r][next.c] = 0;
    stack.push({ r: next.r, c: next.c });
  }

  // Open the destination cell.
  maze[goal.r][goal.c] = 0;

  visitedCells.clear();
  finalPath = [];
  mazeReady = true;

  canvasOverlay.classList.add("hidden");
  updateSizeLabels();
  drawMaze();
  updateStats(0, 0, 0, "Ready");

  mazeStatus.textContent = "New maze generated. Choose an algorithm to begin.";
}

// Draw maze and current visualization state.
function drawMaze() {
  if (!maze.length) return;

  const cell = canvas.width / mazeSize;

  ctx.clearRect(0, 0, canvas.width, canvas.height);

  for (let r = 0; r < mazeSize; r++) {
    for (let c = 0; c < mazeSize; c++) {
      const id = key(r, c);

      let color = maze[r][c] === 1 ? COLORS.wall : COLORS.empty;

      if (visitedCells.has(id)) color = COLORS.visited;
      if (finalPath.some(p => p.r === r && p.c === c)) color = COLORS.path;

      if (r === start.r && c === start.c) color = COLORS.start;
      if (r === goal.r && c === goal.c) color = COLORS.goal;

      ctx.fillStyle = color;
      ctx.fillRect(c * cell, r * cell, cell, cell);

      ctx.strokeStyle = COLORS.grid;
      ctx.lineWidth = 0.6;
      ctx.strokeRect(c * cell, r * cell, cell, cell);
    }
  }

  // Start and goal markers.
  ctx.fillStyle = "#06251b";
  ctx.font = `bold ${Math.max(8, cell * 0.55)}px Manrope`;
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";
  ctx.fillText("S", (start.c + 0.5) * cell, (start.r + 0.5) * cell);

  ctx.fillStyle = "#40260c";
  ctx.fillText("G", (goal.c + 0.5) * cell, (goal.r + 0.5) * cell);
}

function getNeighbors(point) {
  const directions = [
    [-1, 0], [1, 0], [0, -1], [0, 1]
  ];

  return directions
    .map(([dr, dc]) => ({ r: point.r + dr, c: point.c + dc }))
    .filter(p =>
      p.r >= 0 &&
      p.r < mazeSize &&
      p.c >= 0 &&
      p.c < mazeSize &&
      maze[p.r][p.c] === 0
    );
}

function reconstructPath(parent, endKey) {
  const result = [];
  let current = endKey;

  while (current) {
    const [r, c] = current.split(",").map(Number);
    result.push({ r, c });
    current = parent.get(current);
  }

  return result.reverse();
}

// Breadth First Search: explores level by level.
function bfsSearch() {
  const queue = [{ ...start }];
  let head = 0;

  const startKey = key(start.r, start.c);
  const goalKey = key(goal.r, goal.c);

  const seen = new Set([startKey]);
  const parent = new Map();
  const visited = [];

  while (head < queue.length) {
    const current = queue[head++];
    const currentKey = key(current.r, current.c);
    visited.push(current);

    if (currentKey === goalKey) {
      return { visited, path: reconstructPath(parent, goalKey) };
    }

    for (const next of getNeighbors(current)) {
      const nextKey = key(next.r, next.c);

      if (!seen.has(nextKey)) {
        seen.add(nextKey);
        parent.set(nextKey, currentKey);
        queue.push(next);
      }
    }
  }

  return { visited, path: [] };
}

// Depth First Search: explores one route deeply before backtracking.
function dfsSearch() {
  const stack = [{ ...start }];

  const startKey = key(start.r, start.c);
  const goalKey = key(goal.r, goal.c);

  const seen = new Set([startKey]);
  const parent = new Map();
  const visited = [];

  while (stack.length > 0) {
    const current = stack.pop();
    const currentKey = key(current.r, current.c);
    visited.push(current);

    if (currentKey === goalKey) {
      return { visited, path: reconstructPath(parent, goalKey) };
    }

    const neighbors = getNeighbors(current);

    // Shuffle neighbor order for a more natural DFS exploration.
    for (let i = neighbors.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [neighbors[i], neighbors[j]] = [neighbors[j], neighbors[i]];
    }

    for (const next of neighbors) {
      const nextKey = key(next.r, next.c);

      if (!seen.has(nextKey)) {
        seen.add(nextKey);
        parent.set(nextKey, currentKey);
        stack.push(next);
      }
    }
  }

  return { visited, path: [] };
}

// Dijkstra: expands the unvisited cell with the smallest distance.
function dijkstraSearch() {
  const startKey = key(start.r, start.c);
  const goalKey = key(goal.r, goal.c);

  const distance = new Map([[startKey, 0]]);
  const parent = new Map();
  const queue = [{ point: { ...start }, cost: 0 }];
  const seen = new Set();
  const visited = [];

  while (queue.length > 0) {
    queue.sort((a, b) => a.cost - b.cost);

    const currentItem = queue.shift();
    const current = currentItem.point;
    const currentKey = key(current.r, current.c);

    if (seen.has(currentKey)) continue;
    seen.add(currentKey);
    visited.push(current);

    if (currentKey === goalKey) {
      return { visited, path: reconstructPath(parent, goalKey) };
    }

    for (const next of getNeighbors(current)) {
      const nextKey = key(next.r, next.c);
      const newCost = currentItem.cost + 1;

      if (newCost < (distance.get(nextKey) ?? Infinity)) {
        distance.set(nextKey, newCost);
        parent.set(nextKey, currentKey);
        queue.push({ point: next, cost: newCost });
      }
    }
  }

  return { visited, path: [] };
}

function runSelectedAlgorithm() {
  const algorithm = algorithmInput.value;

  if (algorithm === "bfs") return bfsSearch();
  if (algorithm === "dfs") return dfsSearch();
  if (algorithm === "dijkstra") return dijkstraSearch();

  return bfsSearch();
}

function animateResult(result, elapsedTime) {
  stopAnimation();
  isAnimating = true;
  solveBtn.disabled = true;
  generateBtn.disabled = true;

  visitedCells.clear();
  finalPath = [];

  const visitList = result.visited;
  const pathList = result.path;
  const delay = getSpeedDelay();

  let index = 0;

  updateStats(0, 0, elapsedTime.toFixed(2), "Running");
  mazeStatus.textContent = "Exploring cells and searching for the destination...";

  function showNextVisit() {
    if (index < visitList.length) {
      const point = visitList[index];
      visitedCells.add(key(point.r, point.c));
      index++;

      if (index % 2 === 0 || index === visitList.length) {
        drawMaze();
        updateStats(index, 0, elapsedTime.toFixed(2), "Running");
      }

      animationTimer = setTimeout(showNextVisit, delay);
      return;
    }

    showPath();
  }

  let pathIndex = 0;

  function showPath() {
    if (pathIndex < pathList.length) {
      finalPath.push(pathList[pathIndex]);
      pathIndex++;

      drawMaze();
      updateStats(
        visitList.length,
        pathIndex,
        elapsedTime.toFixed(2),
        "Drawing path"
      );

      animationTimer = setTimeout(showPath, Math.max(5, delay));
      return;
    }

    stopAnimation();

    if (pathList.length > 0) {
      updateStats(
        visitList.length,
        pathList.length,
        elapsedTime.toFixed(2),
        "Completed"
      );
      mazeStatus.textContent = "Destination reached! Shortest route displayed.";
    } else {
      updateStats(
        visitList.length,
        0,
        elapsedTime.toFixed(2),
        "No path"
      );
      mazeStatus.textContent = "No route to the destination was found.";
    }

    drawMaze();
  }

  showNextVisit();
}

function solveMaze() {
  if (!mazeReady) {
    mazeStatus.textContent = "Please generate a maze first.";
    return;
  }

  if (isAnimating) return;

  stopAnimation();

  visitedCells.clear();
  finalPath = [];
  drawMaze();

  const selected = algorithmInput.value;
  const labels = {
    bfs: "Breadth First Search",
    dfs: "Depth First Search",
    dijkstra: "Dijkstra's Algorithm"
  };

  mazeStatus.textContent = `${labels[selected]} is calculating the route...`;
  updateStats(0, 0, 0, "Calculating");

  const startTime = performance.now();
  const result = runSelectedAlgorithm();
  const endTime = performance.now();

  const elapsed = endTime - startTime;

  animateResult(result, elapsed);
}

function clearPath() {
  stopAnimation();

  visitedCells.clear();
  finalPath = [];

  if (mazeReady) {
    drawMaze();
    mazeStatus.textContent = "Path cleared. You can run another algorithm.";
    updateStats(0, 0, 0, "Ready");
  } else {
    updateStats(0, 0, 0, "Idle");
  }
}

// Button events.
generateBtn.addEventListener("click", generateMaze);
overlayGenerate.addEventListener("click", generateMaze);
solveBtn.addEventListener("click", solveMaze);
clearBtn.addEventListener("click", clearPath);

sizeInput.addEventListener("input", updateSizeLabels);
speedInput.addEventListener("input", updateSpeedLabel);

algorithmInput.addEventListener("change", () => {
  const names = {
    bfs: "Breadth First Search",
    dfs: "Depth First Search",
    dijkstra: "Dijkstra's Algorithm"
  };

  mazeStatus.textContent = `Selected: ${names[algorithmInput.value]}`;
});

// Initial page setup.
updateSizeLabels();
updateSpeedLabel();
drawMaze();
updateStats(0, 0, 0, "Idle");
