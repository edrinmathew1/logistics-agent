"""
grid.py - Grid environment setup for Warehouse Logistics Agent simulation.
Defines the 12x12 warehouse matrix, static & dynamic shelf obstacles, weighted terrain costs (Narrow Aisles),
multi-package locations, charging station, and loading bay.
"""

from typing import List, Tuple

class WarehouseGrid:
    def __init__(self, width=12, height=12):
        self.width = width
        self.height = height
        
        # Key landmark positions (row, col)
        self.start = (1, 1)
        
        # Multi-package locations
        self.packages = [
            (10, 2),  # Package 1 (Bottom-left aisle)
            (2, 10)   # Package 2 (Top-right aisle)
        ]
        
        self.loading_bay = (10, 10)
        self.charging_station = (1, 4)
        
        # Fixed static shelf obstacles (row, col)
        self.static_obstacles = set([
            # Top Left Aisle Block
            (2, 2), (2, 3), (3, 2), (3, 3), (4, 2), (4, 3),
            
            # Mid-Left Horizontal Obstacle (forces detour from start)
            (6, 0), (6, 1), (6, 2),
            
            # Center Shelf Block
            (2, 6), (3, 6), (4, 6), (5, 6),
            (2, 7), (3, 7), (4, 7), (5, 7),
            
            # Bottom Horizontal Barrier (forces detour between package and loading bay)
            (10, 3), (10, 4), (10, 5), (10, 6),
            
            # Bottom Right Aisle Block
            (7, 8), (8, 8), (9, 8), (10, 8),
            (7, 9), (8, 9), (9, 9),
            
            # Top Right Shelf Block
            (1, 8), (2, 8), (3, 8), (4, 8),
            
            # Additional interior dividers
            (8, 2), (8, 3), (8, 4),
            (0, 5), (1, 5)
        ])
        
        # Weighted Terrain: Narrow Congested Aisles (Cost = 3.0 vs Normal Floor = 1.0)
        self.narrow_aisles = set([
            (5, 1), (5, 2), (5, 3), (5, 4),
            (6, 3), (6, 4), (7, 3), (7, 4),
            (3, 9), (4, 9), (5, 9)
        ])

        # Dynamic obstacles added during simulation
        self.dynamic_obstacles = set()

    @property
    def obstacles(self) -> set:
        """Returns union of static and dynamic obstacles."""
        return self.static_obstacles | self.dynamic_obstacles

    def add_dynamic_obstacle(self, row: int, col: int):
        """Inject a dynamic obstacle at runtime."""
        self.dynamic_obstacles.add((row, col))

    def is_valid(self, row: int, col: int) -> bool:
        """Check if cell (row, col) is within bounds and not an obstacle."""
        if 0 <= row < self.height and 0 <= col < self.width:
            return (row, col) not in self.obstacles
        return False

    def is_obstacle(self, row: int, col: int) -> bool:
        """Check if cell is a static or dynamic obstacle."""
        return (row, col) in self.obstacles

    def is_dynamic_obstacle(self, row: int, col: int) -> bool:
        """Check if cell is specifically a dynamic obstacle."""
        return (row, col) in self.dynamic_obstacles

    def is_narrow_aisle(self, row: int, col: int) -> bool:
        """Check if cell is a high-cost narrow congested aisle."""
        return (row, col) in self.narrow_aisles

    def get_movement_cost(self, row: int, col: int) -> float:
        """
        Returns weighted movement cost for entering cell (row, col).
        - Narrow Aisle: Cost 3.0
        - Normal Open Floor: Cost 1.0
        """
        if (row, col) in self.narrow_aisles:
            return 3.0
        return 1.0

    def get_neighbors(self, row: int, col: int):
        """Get valid 4-directional neighboring cells (Up, Down, Left, Right)."""
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)] # Up, Down, Left, Right
        neighbors = []
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if self.is_valid(r, c):
                neighbors.append((r, c))
        return neighbors

    def determine_greedy_package_order(self, start_pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        Determines multi-package pickup order using Nearest-Neighbor greedy selection based on Manhattan Distance.
        """
        unvisited = list(self.packages)
        curr_pos = start_pos
        ordered_packages = []

        while unvisited:
            # Find closest remaining package
            closest_pkg = min(
                unvisited,
                key=lambda pkg: abs(curr_pos[0] - pkg[0]) + abs(curr_pos[1] - pkg[1])
            )
            ordered_packages.append(closest_pkg)
            unvisited.remove(closest_pkg)
            curr_pos = closest_pkg

        return ordered_packages
