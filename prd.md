PRD — Warehouse Logistics Agent (A* Pathfinding)

1. Objective
Build an autonomous forklift agent that navigates a grid warehouse from a start cell to a package pickup cell, then to a designated loading bay, avoiding static shelf obstacles, using A* search with Manhattan Distance heuristic. The agent must animate visually in real time and log its decision process (nodes expanded, path cost, frontier/open-set activity).

2. PEAS Framework

Performance Measure: Path cost minimized (steps/distance), nodes expanded (efficiency), successful delivery (goal reached), time to solution.
Environment: 2D grid warehouse — static shelf obstacles (impassable cells), one forklift start position, one package location, one loading bay (goal). Fully observable, static (obstacles don't move), deterministic, discrete.
Actuators: Move Up / Down / Left / Right (grid-cell transitions); pick-up action at package cell; drop-off action at bay cell.
Sensors: Full grid-state read (agent position, obstacle map, package/bay coordinates) — since environment is fully observable for this track.

3. Functional Requirements

Grid representation: 2D matrix (e.g., 10x10 or 12x12) with walls/shelves marked.
A* implementation: priority queue (min-heap) on f(n) = g(n) + h(n).
Heuristic: Manhattan Distance, h(n) = |x1-x2| + |y1-y2|.
Two-leg pathing: Start → Package → Loading Bay (sequential A* calls, or single combined search).
Real-time visualization: agent icon moves cell-by-cell along the computed path (animate, don't just draw final path).
Live console/log panel: prints each expanded node, current f/g/h values, and final summary (total path cost, total nodes expanded, time taken).
Split-screen friendly layout: visualization window + log panel visible simultaneously (or two separate windows) for the demo video.

4. Non-Functional Requirements

Runs standalone, one command to launch (e.g. python main.py).
No external paid APIs/services — must run locally for the video demo.
Clean, readable code structure (counts toward GitHub Code Quality marks): separate modules/files for grid, search algorithm, visualization, logging.
README.md with setup + run instructions.

5. Deliverables Mapping

Visual grid sim + live log → satisfies "Live Agent Movement" (4 marks).
Correct A* + Manhattan heuristic implementation → "Algorithmic Correctness" (3 marks).
Structured repo, all 3 members commit → "GitHub Code Quality" (2 marks).
SUMMARY.pdf with PEAS, state space/heuristic formulas, complexity analysis → "Technical Summary Sheet" (1 mark).

6. Core Algorithmic Formulation (for your summary sheet too)

State: (x, y) position of forklift on grid.
Initial State: Forklift's starting cell.
Goal Test: Two-phase — state == package location (phase 1), then state == loading bay location (phase 2).
Path Cost: g(n) = number of moves taken (uniform cost = 1 per move), or sum of step costs if weighted.
Heuristic: h(n) = |x_current - x_goal| + |y_current - y_goal| (admissible & consistent for 4-directional grid movement).
f(n) = g(n) + h(n)
Complexity: Time O(b^d) worst case / O(E log V) with heap in practice; Space O(b^d) for stored nodes — compare against observed nodes expanded from your log.