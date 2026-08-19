# 🚜 Warehouse Logistics Agent Simulation (A* Pathfinding, Weighted Terrain & Auto-Charting)

An autonomous forklift agent navigating a 2D grid warehouse using **A* Search with Weighted Terrain, Heuristic Variants & State-Space Constraints**. The agent executes multi-package pickup missions, manages state battery levels with charging station detours, navigates high-cost narrow aisles, dynamically detects unexpected shelf obstacles, performs real-time path replanning, renders search exploration heatmaps, and auto-generates high-resolution performance charts.

---

## 🌟 Key Features

1. **Weighted Terrain Costs**:
   - Differentiates **Normal Floor** (cost 1.0) and **Narrow Congested Aisles** (cost 3.0).
   - $g(n)$ uses actual terrain movement costs.
   - Visually distinct dark amber hatching on narrow aisle grid tiles.
   - Code comment explicitly confirms Manhattan distance $h(n)$ remains **strictly admissible and consistent** since all terrain movement costs are $\ge 1.0$.

2. **Live Stats HUD (Persistent Panel Overlay)**:
   - Dedicated side panel overlay displaying real-time metrics during animation:
     - Weighted Path Cost so far
     - Total Nodes Expanded (running count)
     - Battery Level Progress Bar & Counter
     - Replanning Events Triggered count
     - Active Mission Leg status

3. **Auto-Generated Comparison Charts for Summary Sheet**:
   - Automatically generates 2 PNG charts in the project root directory upon run completion:
     - `heuristic_comparison.png`: Bar chart comparing Nodes Expanded across Manhattan A*, Euclidean A*, and Dijkstra.
     - `leg_metrics_comparison.png`: Grouped bar chart comparing Weighted Path Cost vs. Nodes Expanded per mission leg.

4. **3-Way Heuristic Comparison Analysis**:
   - Compares **Manhattan Distance**, **Euclidean Distance**, and **Dijkstra** ($h = 0$).
   - Outputs structured console table and telemetry card.

5. **Battery / Fuel State Constraint**:
   - Forklift state ($x, y, \text{battery\_level}$) with capacity (25 units).
   - Reroutes through **Charging Station** `(1, 4)` to refill when remaining battery is insufficient.

6. **Dynamic Obstacle & Live Replanning**:
   - Detects dynamic blocked shelf at runtime and re-runs A* search live from current position to goal.

---

## 📁 Repository Structure

```
hackathon/
│── grid.py                   # 12x12 Grid, weighted terrain (Narrow Aisles), obstacles, charger & packages
│── astar.py                  # A* search engine supporting Manhattan, Euclidean, Dijkstra & weighted costs
│── visualizer.py             # Pygame engine, heatmap renderer, Live Stats HUD, terrain styling & replanning
│── main.py                   # Main entry, 3-way benchmark, Matplotlib auto-charting, summary logging
│── heuristic_comparison.png  # Auto-generated chart: Heuristic Nodes Expanded
│── leg_metrics_comparison.png# Auto-generated chart: Multi-Leg Path Cost vs Nodes
└── README.md                 # Documentation and run instructions
```

---

## 📐 Mathematical Formulation

$$f(n) = g(n) + h(n)$$

- **Weighted Cost $g(n)$**: Accumulated terrain step costs ($\text{Normal}=1.0, \text{Narrow Aisle}=3.0$).
- **Manhattan Heuristic**: $h_{\text{manhattan}}(n) = |r_1 - r_2| + |c_1 - c_2|$ (Admissible: $h(n) \le h^*(n)$)
- **Euclidean Heuristic**: $h_{\text{euclidean}}(n) = \sqrt{(r_1 - r_2)^2 + (c_1 - c_2)^2}$
- **Dijkstra Heuristic**: $h_{\text{dijkstra}}(n) = 0.0$

---

## 🚀 Setup & Execution Instructions

### Prerequisites
- Python 3.8+

### 1. Install Dependencies
```bash
pip install pygame matplotlib
```

### 2. Launch Simulation
```bash
python main.py
```

Running `python main.py` immediately launches the interactive simulation and saves PNG charts automatically upon completion.

---

## 📊 Sample Output (Console Summary)

```text
======================================================================
         FINAL WAREHOUSE LOGISTICS AGENT PERFORMANCE SUMMARY      
======================================================================
  Status                     : SUCCESS - All Packages Delivered!
  Packages Collected         : 2 packages
  Battery Capacity           : 25 units
  Recharge Stops Triggered   : 1 stop at Charging Station (1, 4)
  Dynamic Replanning Events  : 1 triggered
  -------------------------------------------------------------------
  TOTAL WEIGHTED PATH COST   : 68.0 (terrain-weighted)
  TOTAL NODES EXPANDED (A*)  : 152 nodes
  TOTAL NODES EXPANDED (Dijk): 189 nodes (h=0)
  HEURISTIC EFFICIENCY GAIN  : 19.6% fewer nodes expanded by A*
  PATH OPTIMALITY VERIFIED   : Path costs match Dijkstra (68.0)
======================================================================
[CHART GENERATED] Saved Heuristic Comparison Chart: 'heuristic_comparison.png'
[CHART GENERATED] Saved Leg Performance Chart: 'leg_metrics_comparison.png'
```
