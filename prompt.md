Build a Warehouse Logistics Agent simulation for a hackathon demo. No need to explain code, just build it directly and make it runnable immediately.

CONTEXT:
Autonomous forklift agent in a 2D grid warehouse. It must navigate from a start 
position to a package location, pick it up, then navigate to a loading bay (goal), 
avoiding static shelf obstacles, using A* Search with Manhattan Distance heuristic.

REQUIREMENTS:

1. GRID ENVIRONMENT
- 2D grid (12x12), represented as a matrix
- Static obstacles ("shelves") placed at fixed cells, marked visually distinct
- Three key cells: Forklift Start, Package Location, Loading Bay (Goal) — all visually distinct colors/icons
- Grid should be dense enough with obstacles to make the A* path non-trivial (forks, dead-ends)

2. A* SEARCH ALGORITHM
- Implement A* using a priority queue (min-heap) on f(n) = g(n) + h(n)
- Heuristic: Manhattan Distance h(n) = |x1-x2| + |y1-y2|
- 4-directional movement (up/down/left/right), cost = 1 per move
- Two-phase pathing: Start -> Package, then Package -> Loading Bay
- Track and store: total path cost, total nodes expanded, execution time per phase

3. VISUALIZATION (choose Pygame for smooth animation)
- Render the grid, obstacles, start/package/goal markers
- Animate the forklift moving cell-by-cell along the computed optimal path (not an instant jump — visible step-by-step movement with small delay/frame update)
- Highlight explored/expanded nodes briefly during search (optional but valuable for demo) so the audience visually sees A* exploring
- Show current path cost and nodes expanded as on-screen text overlay, updating live

4. LIVE LOGGING (console, side-by-side with the visual window)
- Print each node as it's expanded/popped from the priority queue with its f(n), g(n), h(n) values
- Print phase transitions ("Package picked up", "Heading to loading bay")
- Print final summary block: total path cost, total nodes expanded, total execution time, path length

5. CODE STRUCTURE (for clean GitHub submission)
- grid.py -> grid setup, obstacle placement, start/goal/package definitions
- astar.py -> A* algorithm, heuristic function, node class
- visualizer.py -> Pygame rendering and animation loop
- main.py -> orchestrates: run A* phase 1, animate, run A* phase 2, animate, print summary
- README.md -> setup instructions (pip installs), how to run, brief explanation of approach

6. OUTPUT BEHAVIOR
- Running `python main.py` should immediately open the Pygame window and start the full demo automatically (no manual clicking needed) — this needs to work smoothly for a 60-90 second screen recording
- Make sure window doesn't auto-close instantly at the end — pause on final state showing the completed path and summary text for a few seconds

Build this fully working and runnable, optimized for a live screen-recorded demo under time pressure. Prioritize getting something visually working over exhaustive edge-case handling.

