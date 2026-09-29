import random
MAX_LEVEL = 10


GENERATED_NAMES = ["Endless Night 1", "Endless Night 2", "Endless Night 3",
                   "Endless Night 4", "Endless Night 5"]
from game_state import (GRID_SIZE, SAFE_HOUSE, SURVIVOR_START,
                        VAMPIRE1_START, VAMPIRE2_START, build_obstacle_grid)


LAYOUTS = [
    ("Primary Yard", [(3, 2, 3, 8), (9, 5, 9, 11)]),
    ("Secondary Yard", [(3, 2, 3, 8), (7, 4, 7, 10), (11, 1, 11, 7),
                       (5, 11, 10, 11), (2, 6, 2, 12)]),
    ("Third Yard", [(4, 0, 4, 9), (8, 5, 8, 14), (11, 0, 11, 9), (0, 11, 3, 11)]),
    ("Fourth Yard", [(1, 3, 12, 3), (2, 7, 14, 7), (0, 11, 12, 11)]),
    ("Fifth Yard", [(3, 0, 3, 10), (6, 4, 6, 14), (9, 0, 9, 10),
                        (12, 4, 12, 14), (0, 12, 2, 12)]),
]

_KEY_CELLS = (SURVIVOR_START, VAMPIRE1_START, VAMPIRE2_START, SAFE_HOUSE)


def _valid(walls):
    """True if key cells are free and all are connected to the Survivor start."""
    grid = build_obstacle_grid(walls)
    if any(grid[y][x] == 1 for (x, y) in _KEY_CELLS):
        return False
    seen = {SURVIVOR_START}
    stack = [SURVIVOR_START]
    while stack:
        x, y = stack.pop()
        for c in ((x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)):
            if (0 <= c[0] < GRID_SIZE and 0 <= c[1] < GRID_SIZE
                    and grid[c[1]][c[0]] == 0 and c not in seen):
                seen.add(c)
                stack.append(c)
    return all(c in seen for c in _KEY_CELLS)


def _safe(walls):
    """Drops trailing segments until the map is valid (safety net)."""
    walls = list(walls)
    while walls and not _valid(walls):
        walls.pop()
    return walls


def _random_walls(level, target=None):
    rng = random.Random(level * 7919)
    walls = []
    if target is None:
        target= min(5 + level // 2, 10)
    tries = 0
    while len(walls) < target and tries < 500:
        tries += 1
        length = rng.randint(3, 7)
        if rng.random() < 0.5:
            x = rng.randint(0, GRID_SIZE - length)
            y = rng.randint(0, GRID_SIZE - 1)
            seg = (x, y, x + length - 1, y)
        else:
            x = rng.randint(0, GRID_SIZE - 1)
            y = rng.randint(0, GRID_SIZE - length)
            seg = (x, y, x, y + length - 1)
        if _valid(walls + [seg]):
            walls.append(seg)
    return walls

DIFFICULTY = {"Easy": (0.75, -1), "Medium": (1.0, 0), "Hard": (1.2, 1)}
def get_level(n, difficulty="Medium"):
    """Returns the config dict for level n (1-based)."""
    mult, depth_delta = DIFFICULTY[difficulty]
    if n <= len(LAYOUTS):
        title, walls = LAYOUTS[n - 1]
        walls = _safe(walls)
    else:
        title, walls = GENERATED_NAMES[n - len(LAYOUTS) - 1], _random_walls(n)
    base_speed = min(0.4 + 0.1 * (n - 1), 0.9)
    base_depth = 2 if n < 3 else 3
    return {
        "level": n,
        "title": title,
        "walls": walls,
        "speed": round(min(base_speed * mult, 1.0), 2),
        "depth": max(1, base_depth + depth_delta),
    }