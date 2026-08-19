"""
astar.py - A* Search Algorithm & Heuristic Comparison Engine with Weighted Terrain Support.
Supports Manhattan Distance, Euclidean Distance, and Dijkstra (h=0) heuristics,
weighted movement costs per cell, heatmap node expansion telemetry, and performance metrics.
"""

import heapq
import math
import time
from typing import List, Tuple, Dict, Any, Optional

class Node:
    """Represents a state node in the search tree."""
    def __init__(self, pos: Tuple[int, int], g: float = float('inf'), h: float = 0.0, parent: Optional['Node'] = None):
        self.pos = pos  # (row, col)
        self.g = g
        self.h = h
        self.f = g + h
        self.parent = parent

    def __lt__(self, other: 'Node') -> bool:
        if self.f == other.f:
            return self.h < other.h
        return self.f < other.f

    def __repr__(self):
        return f"Node{self.pos}(f={self.f:.1f}, g={self.g:.1f}, h={self.h:.1f})"


def manhattan_distance(pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
    """Calculates Manhattan Distance heuristic h(n) = |x1 - x2| + |y1 - y2|."""
    return float(abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1]))


def euclidean_distance(pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
    """Calculates Euclidean Distance heuristic h(n) = sqrt((x1 - x2)^2 + (y1 - y2)^2)."""
    return math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)


def calculate_heuristic(pos1: Tuple[int, int], pos2: Tuple[int, int], heuristic_type: str = "manhattan") -> float:
    """
    Helper to dispatch heuristic calculation by name.
    
    NOTE ON ADMISSIBILITY:
    The Manhattan Heuristic h(n) = |x1-x2| + |y1-y2| assumes a minimum step cost of 1.0.
    Since all weighted terrain costs in the warehouse grid are >= 1.0 (Normal Floor = 1.0, Narrow Aisle = 3.0),
    h(n) is guaranteed to never overestimate the true remaining path cost (h(n) <= h*(n)).
    Thus, Manhattan distance remains strictly ADMISSIBLE and CONSISTENT under weighted terrain.
    """
    htype = heuristic_type.lower()
    if htype == "manhattan":
        return manhattan_distance(pos1, pos2)
    elif htype == "euclidean":
        return euclidean_distance(pos1, pos2)
    elif htype == "dijkstra" or htype == "none":
        return 0.0
    else:
        raise ValueError(f"Unknown heuristic type: {heuristic_type}")


def a_star_search(grid, start_pos: Tuple[int, int], goal_pos: Tuple[int, int], 
                  phase_name: str = "Phase", heuristic_type: str = "manhattan", verbose: bool = True) -> Dict[str, Any]:
    """
    Executes A* Search (or Dijkstra if heuristic_type='dijkstra') on the weighted warehouse grid.
    
    Returns a dictionary containing:
      - 'path': List of (row, col) positions from start to goal
      - 'expanded_nodes': List of (row, col) in order of expansion
      - 'expanded_info': List of (row, col, g_score, expansion_index) for heatmap visualization
      - 'expansion_logs': List of log strings for each expanded node
      - 'total_cost': Accumulated weighted path cost (g-score)
      - 'nodes_expanded_count': Total number of popped nodes
      - 'exec_time_ms': Search runtime in milliseconds
      - 'heuristic_type': Selected heuristic variant name
    """
    algo_label = f"A* ({heuristic_type.title()})" if heuristic_type.lower() != "dijkstra" else "Dijkstra (h=0)"
    if verbose:
        print(f"\n==================================================")
        print(f"  STARTING {algo_label.upper()}: {phase_name.upper()}")
        print(f"  From: {start_pos} ---> Goal: {goal_pos}")
        print(f"==================================================")

    start_time = time.perf_counter()

    counter = 0  # Unique sequence number for heap stability
    open_heap = []
    
    start_h = calculate_heuristic(start_pos, goal_pos, heuristic_type)
    start_node = Node(start_pos, g=0.0, h=start_h)
    
    # Priority Queue store: (f_score, counter, node)
    heapq.heappush(open_heap, (start_node.f, counter, start_node))
    
    # Best g-score record per position
    g_score_map = {start_pos: 0.0}
    # Closed set of expanded nodes
    closed_set = set()
    
    expanded_nodes = []
    expanded_info = [] # (pos, g_score, idx)
    expansion_logs = []
    node_lookup = {start_pos: start_node}

    goal_node = None
    expansion_idx = 0

    while open_heap:
        _, _, current = heapq.heappop(open_heap)

        if current.pos in closed_set:
            continue

        closed_set.add(current.pos)
        expanded_nodes.append(current.pos)
        expanded_info.append((current.pos, current.g, expansion_idx))
        expansion_idx += 1

        log_entry = (f"[{phase_name}] Popped Node {current.pos} | "
                     f"f(n)={current.f:4.1f} | g(n)={current.g:4.1f} | h(n)={current.h:4.1f}")
        expansion_logs.append(log_entry)
        if verbose:
            print(log_entry)

        # Check goal test
        if current.pos == goal_pos:
            goal_node = current
            break

        # Expand neighbors
        for neighbor_pos in grid.get_neighbors(current.pos[0], current.pos[1]):
            if neighbor_pos in closed_set:
                continue

            # Weighted Terrain Cost addition: Normal Floor = 1.0, Narrow Aisle = 3.0
            step_cost = grid.get_movement_cost(neighbor_pos[0], neighbor_pos[1])
            tentative_g = current.g + step_cost

            if tentative_g < g_score_map.get(neighbor_pos, float('inf')):
                g_score_map[neighbor_pos] = tentative_g
                h = calculate_heuristic(neighbor_pos, goal_pos, heuristic_type)
                neighbor_node = Node(neighbor_pos, g=tentative_g, h=h, parent=current)
                node_lookup[neighbor_pos] = neighbor_node
                
                counter += 1
                heapq.heappush(open_heap, (neighbor_node.f, counter, neighbor_node))

    end_time = time.perf_counter()
    exec_time_ms = (end_time - start_time) * 1000.0

    # Reconstruct path
    path = []
    total_cost = 0.0
    if goal_node:
        curr = goal_node
        total_cost = curr.g
        while curr:
            path.append(curr.pos)
            curr = curr.parent
        path.reverse()

    if verbose:
        print(f"--------------------------------------------------")
        print(f"[{phase_name}] {algo_label.upper()} COMPLETE")
        print(f"  Path Found        : {'YES' if path else 'NO'}")
        print(f"  Weighted Path Cost: {total_cost:.1f}")
        print(f"  Nodes Expanded    : {len(expanded_nodes)}")
        print(f"  Execution Time    : {exec_time_ms:.3f} ms")
        print(f"--------------------------------------------------\n")

    return {
        'path': path,
        'expanded_nodes': expanded_nodes,
        'expanded_info': expanded_info,
        'expansion_logs': expansion_logs,
        'total_cost': total_cost,
        'nodes_expanded_count': len(expanded_nodes),
        'exec_time_ms': exec_time_ms,
        'heuristic_type': heuristic_type
    }
