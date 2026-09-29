GRID_SIZE = 15
SAFE_HOUSE = (14, 14)
SURVIVOR_START = (0, 0)
VAMPIRE1_START = (14, 0)
VAMPIRE2_START = (0, 14)


def build_obstacle_grid(wall_segments):
    
    grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    for (x1, y1, x2, y2) in wall_segments:
        if x1 == x2:
            for y in range(min(y1, y2), max(y1, y2) + 1):
                grid[y][x1] = 1
        else:
            for x in range(min(x1, x2), max(x1, x2) + 1):
                grid[y1][x] = 1
    return grid


class GameState:

    def __init__(self, wall_segments=(), speed=0.5):
        self.grid = build_obstacle_grid(wall_segments)
        self.survivor = SURVIVOR_START
        self.vampire1 = VAMPIRE1_START
        self.vampire2 = VAMPIRE2_START
        self.safe_house = SAFE_HOUSE
        self.turn_count = 0
        self.game_over = False
        self.winner = None  
        self.speed = speed          
        self.vamp_budget = 0.0      

    def vampire_steps_this_turn(self):
        
        self.vamp_budget += self.speed
        steps = int(self.vamp_budget)
        self.vamp_budget -= steps
        return steps

    def is_free(self, x, y):
        if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:
            return self.grid[y][x] == 0
        return False

    def neighbors(self, pos):
        x, y = pos
        candidates = [(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)]
        return [c for c in candidates if self.is_free(*c)]

    def check_end_conditions(self):
        if self.survivor == self.vampire1 or self.survivor == self.vampire2:
            self.game_over = True
            self.winner = "vampires"
        elif self.survivor == self.safe_house:
            self.game_over = True
            self.winner = "survivor"
        return self.game_over