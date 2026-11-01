const canvas = document.getElementById("mazeCanvas");
const ctx = canvas.getContext("2d");

let size = 27;
let maze = [];
let start = [1, 1];
let goal = [25, 25];
let animationTimer = null;

const directions = [
    [0, 1],
    [1, 0],
    [0, -1],
    [-1, 0]
];

function createMaze() {

    size = Number(
        document.getElementById("mazeSize").value
    );

    start = [1, 1];
    goal = [size - 2, size - 2];

    maze = Array.from(
        { length: size },
        () => Array(size).fill(1)
    );

    const stack = [[1, 1]];

    maze[1][1] = 0;

    while (stack.length > 0) {

        let current = stack[stack.length - 1];

        let r = current[0];
        let c = current[1];

        let options = directions
            .map(([dr, dc]) => [
                r + dr * 2,
                c + dc * 2,
                dr,
                dc
            ])
            .filter(([nr, nc]) =>
                nr > 0 &&
                nc > 0 &&
                nr < size - 1 &&
                nc < size - 1 &&
                maze[nr][nc] === 1
            );

        if (options.length === 0) {
            stack.pop();
            continue;
        }

        let choice = options[
            Math.floor(Math.random() * options.length)
        ];

        let [nr, nc, dr, dc] = choice;

        maze[r + dr][c + dc] = 0;
        maze[nr][nc] = 0;

        stack.push([nr, nc]);
    }

    if (document.getElementById("topology").value === "braid") {
        for (let r = 1; r < size - 1; r++) {
            for (let c = 1; c < size - 1; c++) {
                if (
                    maze[r][c] === 1 &&
                    Math.random() < 0.08
                ) {
                    let open = directions.filter(([dr, dc]) =>
                        maze[r + dr]?.[c + dc] === 0
                    );

                    if (open.length >= 2) {
                        maze[r][c] = 0;
                    }
                }
            }
        }
    }

    maze[goal[0]][goal[1]] = 0;

    drawMaze();
    clearMetrics();

    document.getElementById("status").innerText =
        "Status: New Maze Generated";
}

function drawMaze(visited = new Set(), path = []) {

    const cellSize = Math.floor(
        Math.min(600, 600) / size
    );

    canvas.width = cellSize * size;
    canvas.height = cellSize * size;

    const pathSet = new Set(
        path.map(p => p.join(","))
    );

    for (let r = 0; r < size; r++) {

        for (let c = 0; c < size; c++) {

            let color = maze[r][c] === 1
                ? "#26344c"
                : "#ffffff";

            if (visited.has(`${r},${c}`)) {
                color = "#60a5fa";
            }

            if (pathSet.has(`${r},${c}`)) {
                color = "#f4ca50";
            }

            if (r === start[0] && c === start[1]) {
                color = "#12b981";
            }

            if (r === goal[0] && c === goal[1]) {
                color = "#ef5364";
            }

            ctx.fillStyle = color;

            ctx.fillRect(
                c * cellSize,
                r * cellSize,
                cellSize,
                cellSize
            );

            ctx.strokeStyle = "#dce2eb";

            ctx.strokeRect(
                c * cellSize,
                r * cellSize,
                cellSize,
                cellSize
            );
        }
    }
}

function getNeighbors([r, c]) {

    return directions
        .map(([dr, dc]) => [r + dr, c + dc])
        .filter(([nr, nc]) =>
            nr >= 0 &&
            nc >= 0 &&
            nr < size &&
            nc < size &&
            maze[nr][nc] === 0
        );
}

function solveMaze(algorithm) {

    const startTime = performance.now();

    const startKey = start.join(",");
    const goalKey = goal.join(",");

    let visited = new Set();
    let parent = new Map();

    let queue = [start];
    let distance = new Map([[startKey, 0]]);

    let found = false;

    while (queue.length > 0) {

        let current;

        if (algorithm === "DFS") {
            current = queue.pop();
        } else if (algorithm === "Dijkstra" || algorithm === "A*") {

            queue.sort((a, b) => {
                const score = p => {
                    const d = distance.get(p.join(",")) || 0;

                    if (algorithm === "Dijkstra") return d;

                    return d +
                        Math.abs(p[0] - goal[0]) +
                        Math.abs(p[1] - goal[1]);
                };

                return score(a) - score(b);
            });

            current = queue.shift();

        } else {
            current = queue.shift();
        }

        const currentKey = current.join(",");

        if (visited.has(currentKey)) continue;

        visited.add(currentKey);

        if (currentKey === goalKey) {
            found = true;
            break;
        }

        for (const neighbor of getNeighbors(current)) {

            const neighborKey = neighbor.join(",");

            if (visited.has(neighborKey)) continue;

            const newDistance =
                distance.get(currentKey) + 1;

            if (
                algorithm === "Dijkstra" ||
                algorithm === "A*"
            ) {
                if (
                    newDistance >=
                    (distance.get(neighborKey) ?? Infinity)
                ) continue;
            } else if (parent.has(neighborKey)) {
                continue;
            }

            distance.set(neighborKey, newDistance);

            parent.set(neighborKey, currentKey);

            queue.push(neighbor);
        }
    }

    let path = [];

    if (found) {

        let current = goalKey;

        while (current) {

            path.push(
                current.split(",").map(Number)
            );

            current = parent.get(current);
        }

        path.reverse();
    }

    return {
        visited,
        path,
        time: performance.now() - startTime,
        found
    };
}

function clearMetrics() {

    document.getElementById("metricAlgo").innerText = "BFS";
    document.getElementById("metricStatus").innerText = "Ready";
    document.getElementById("metricTime").innerText = "0 ms";
    document.getElementById("metricVisited").innerText = "0";
    document.getElementById("metricPath").innerText = "0";
}

function updateMetrics(algorithm, result) {

    document.getElementById("metricAlgo").innerText = algorithm;

    document.getElementById("metricStatus").innerText =
        result.found ? "Solved" : "Not Found";

    document.getElementById("metricTime").innerText =
        result.time.toFixed(2) + " ms";

    document.getElementById("metricVisited").innerText =
        result.visited.size;

    document.getElementById("metricPath").innerText =
        result.path.length > 0
            ? result.path.length - 1
            : 0;
}

function animateSolution() {

    if (animationTimer) {
        clearTimeout(animationTimer);
        animationTimer = null;
    }

    const algorithm = document.querySelector(
        'input[name="algorithm"]:checked'
    ).value;

    const result = solveMaze(algorithm);

    const visitedArray = [...result.visited];

    const visited = new Set();

    let index = 0;

    const speed = Number(
        document.getElementById("speed").value
    );

    const delay = Math.max(5, 100 - speed * 2);

    function animate() {

        for (
            let i = 0;
            i < Math.max(1, Math.floor(speed / 4)) &&
            index < visitedArray.length;
            i++
        ) {
            visited.add(visitedArray[index]);
            index++;
        }

        drawMaze(visited);

        if (index < visitedArray.length) {

            animationTimer = setTimeout(animate, delay);

        } else {

            drawMaze(visited, result.path);

            updateMetrics(algorithm, result);

            document.getElementById("status").innerText =
                result.found
                    ? "Status: Maze Solved!"
                    : "Status: No Path Found";
        }
    }

    document.getElementById("status").innerText =
        "Status: Solving...";

    animate();
}

function runBenchmark() {

    const algorithms = [
        "BFS",
        "DFS",
        "Dijkstra",
        "A*"
    ];

    let output = "<table><tr><th>Algorithm</th><th>Time</th><th>Visited</th><th>Path</th></tr>";

    algorithms.forEach(algorithm => {

        const result = solveMaze(algorithm);

        output += `
            <tr>
                <td>${algorithm}</td>
                <td>${result.time.toFixed(2)} ms</td>
                <td>${result.visited.size}</td>
                <td>${result.path.length ? result.path.length - 1 : 0}</td>
            </tr>
        `;
    });

    output += "</table>";

    document.getElementById(
        "benchmarkResults"
    ).innerHTML = output;
}

function clearPath() {
    if (animationTimer) clearTimeout(animationTimer);
    animationTimer = null;
    drawMaze();
    clearMetrics();
    document.getElementById("status").innerText =
        "Status: Path Cleared";
}

function algorithmRace() {

    const algorithms = ["BFS", "DFS", "Dijkstra", "A*"];

    let output = "<h3>4-Way Algorithm Race</h3>";

    algorithms.forEach(name => {

        const result = solveMaze(name);

        output += `
            <p>
                <b>${name}</b>:
                ${result.time.toFixed(2)} ms |
                ${result.visited.size} nodes visited |
                ${result.path.length ? result.path.length - 1 : 0} steps
            </p>
        `;
    });

    document.getElementById("benchmarkResults").innerHTML =
        output;
}

document.getElementById("generateBtn")
    .addEventListener("click", createMaze);

document.getElementById("resetBtn")
    .addEventListener("click", createMaze);

document.getElementById("solveBtn")
    .addEventListener("click", animateSolution);

document.getElementById("clearBtn")
    .addEventListener("click", clearPath);

document.getElementById("benchmarkBtn")
    .addEventListener("click", runBenchmark);

document.getElementById("raceBtn")
    .addEventListener("click", algorithmRace);

document.querySelectorAll('input[name="algorithm"]')
    .forEach(input => {
        input.addEventListener("change", () => {

            const info = {
                BFS: "BFS uses a Queue (FIFO).",
                DFS: "DFS uses a Stack (LIFO).",
                Dijkstra: "Dijkstra uses a Priority Queue.",
                "A*": "A* uses a Priority Queue and heuristic."
            };

            document.getElementById(
                "algorithmInfo"
            ).innerText = info[input.value];

            document.getElementById(
                "metricAlgo"
            ).innerText = input.value;
        });
    });

createMaze();
