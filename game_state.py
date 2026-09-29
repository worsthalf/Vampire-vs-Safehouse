"""
game_state.py
Holds the GameState class: the 15x15 grid, obstacle layout, and the
live positions of the Survivor and the two Vampires.
"""

GRID_SIZE = 15
SAFE_HOUSE = (14, 14)

# Wall segments as (x1, y1, x2, y2) - each is a straight horizontal
# or vertical line of obstacle cells.
WALL_SEGMENTS = [
    (3, 2, 3, 8),
    (7, 4, 7, 10),
    (11, 1, 11, 7),
    (5, 11, 10, 11),
    (2, 6, 2, 12),
]


def build_obstacle_grid():
    """Builds a 2D grid (list of lists) where 1 = obstacle, 0 = free cell."""
    grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    for (x1, y1, x2, y2) in WALL_SEGMENTS:
        if x1 == x2:
            for y in range(min(y1, y2), max(y1, y2) + 1):
                grid[y][x1] = 1
        else:
            for x in range(min(x1, x2), max(x1, x2) + 1):
                grid[y1][x] = 1
    return grid


class GameState:
    """Holds the full mutable state of a single game session."""

    def __init__(self):
        self.grid = build_obstacle_grid()
        self.survivor = (0, 0)
        self.vampire1 = (14, 0)
        self.vampire2 = (0, 14)
        self.safe_house = SAFE_HOUSE
        self.turn_count = 0
        self.game_over = False
        self.winner = None  # "survivor" or "vampires"

    def is_free(self, x, y):
        """Returns True if (x, y) is inside the grid and not an obstacle."""
        if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:
            return self.grid[y][x] == 0
        return False

    def neighbors(self, pos):
        """Returns the walkable neighboring cells (up/down/left/right) of pos."""
        x, y = pos
        candidates = [(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)]
        return [c for c in candidates if self.is_free(*c)]

    def check_end_conditions(self):
        """Checks win/loss conditions and updates game_over / winner."""
        if self.survivor == self.vampire1 or self.survivor == self.vampire2:
            self.game_over = True
            self.winner = "vampires"
        elif self.survivor == self.safe_house:
            self.game_over = True
            self.winner = "survivor"
        return self.game_over