import time
import pygame

from game_state import GameState, SURVIVOR_START, SAFE_HOUSE
from astar import next_step_towards, a_star_search, last_search
from minimax import minimax_decide
from levels import get_level, MAX_LEVEL, DIFFICULTY
import renderer
import stats_logger

KEY_MOVES = {
    pygame.K_w: (0, -1), pygame.K_UP: (0, -1),
    pygame.K_s: (0, 1), pygame.K_DOWN: (0, 1),
    pygame.K_a: (-1, 0), pygame.K_LEFT: (-1, 0),
    pygame.K_d: (1, 0), pygame.K_RIGHT: (1, 0),
}
def life_reward(level):
    if level <= 1:
        return 0
    if level <= 5:
        return 1
    if level <= 7:
        return 2
    return 3


def empty_stats():
    return {"v1_states": 0, "v1_time_ms": 0.0, "v2_states": 0, "v2_time_ms": 0.0}


class Game:

    def __init__(self):
        self.mode = "menu"
        self.show_stats = False
        self.show_search = False
        self.level = 1
        self.total_score = 0
        self.level_score = 0
        self.stars = 0
        self.max_lives = 5
        self.lives = self.max_lives
        self.life_gain = 0
        self.anim = renderer.Animator()
        self.difficulty = "Medium"
        self.start_level(1)
        self.mode = "menu"

    def start_level(self, n):
        last_search["visited"] = set()
        last_search["path"] = []
        self.level = n
        self.cfg = get_level(n, self.difficulty)
        self.state = GameState(self.cfg["walls"], self.cfg["speed"])
        self.stats = empty_stats()
        self.anim.snap(self.state)
        path, _ = a_star_search(self.state, SURVIVOR_START, SAFE_HOUSE)
        self.shortest = len(path) - 1
        self.mode = "playing"

    def move_survivor(self, dx, dy):
        st = self.state
        x, y = st.survivor
        new_pos = (x + dx, y + dy)
        if not st.is_free(*new_pos):
            return  # blocked: no turn used
        st.survivor = new_pos
        st.turn_count += 1
        if not st.check_end_conditions():
            for _ in range(st.vampire_steps_this_turn()):
                self.vampire_turn()
                if st.game_over:
                    break
        if st.game_over:
            self.finish()

    def vampire_turn(self):
        st, stats, lvl = self.state, self.stats, self.level

        t0 = time.perf_counter()
        move, explored = next_step_towards(st, st.vampire2, st.survivor)
        ms = (time.perf_counter() - t0) * 1000
        st.vampire2 = move
        stats["v2_states"], stats["v2_time_ms"] = explored, ms
        stats_logger.log_turn(lvl, st.turn_count, "vampire2", "A*", explored, ms)
        if st.check_end_conditions():
            return

        # Vampire 1 - predict kortese Minimax + Alpha-Beta
        t0 = time.perf_counter()
        move, explored = minimax_decide(st, self.cfg["depth"])
        ms = (time.perf_counter() - t0) * 1000
        st.vampire1 = move
        stats["v1_states"], stats["v1_time_ms"] = explored, ms
        stats_logger.log_turn(lvl, st.turn_count, "vampire1", "Minimax+AlphaBeta", explored, ms)
        st.check_end_conditions()

    def finish(self):
        if self.state.winner == "survivor":
            turns = self.state.turn_count
            base = 500 + 100 * self.level
            self.level_score = max(100, base - max(0, turns - self.shortest) * 10)
            self.total_score += self.level_score
            ratio = turns / max(1, self.shortest)
            self.stars = 3 if ratio <= 1.3 else 2 if ratio <= 1.8 else 1
            before = self.lives
            self.lives = min(self.max_lives, self.lives + life_reward(self.level))
            self.life_gain = self.lives - before
            self.mode = "level_complete"
        else:
            self.lives -= 1
            self.mode = "game_over" if self.lives <= 0 else "caught"

    def handle_key(self, key):
        if self.mode == "menu":
            names = list(DIFFICULTY)
            i = names.index(self.difficulty)
            if key in (pygame.K_LEFT, pygame.K_a):
                self.difficulty = names[(i - 1) % len(names)]
            elif key in (pygame.K_RIGHT, pygame.K_d):
                self.difficulty = names[(i + 1) % len(names)]
            elif key in (pygame.K_RETURN, pygame.K_SPACE):
                self.total_score = 0
                self.lives = self.max_lives
                self.start_level(1)



        elif self.mode == "playing":
            if key == pygame.K_r:
                self.lives -= 1
                if self.lives <= 0:
                    self.mode = "game_over"
                else:
                    self.start_level(self.level)
            elif key == pygame.K_ESCAPE:
                self.mode = "menu"
            elif key in KEY_MOVES:
                self.move_survivor(*KEY_MOVES[key])
            elif key == pygame.K_h:
                self.show_stats = not self.show_stats
            elif key == pygame.K_v:
                self.show_search = not self.show_search   
        elif self.mode == "level_complete":
            if key in (pygame.K_RETURN, pygame.K_SPACE):
                if self.level >= MAX_LEVEL:
                    self.mode = "menu"
                else:
                    self.start_level(self.level + 1)
            elif key == pygame.K_ESCAPE:
                self.mode = "menu"
        elif self.mode == "caught":
            if key in (pygame.K_r, pygame.K_RETURN):
                self.start_level(self.level)
            elif key == pygame.K_ESCAPE:
                self.mode = "menu"
        elif self.mode == "game_over":
            if key in (pygame.K_RETURN, pygame.K_r):
                self.total_score = 0
                self.lives = self.max_lives
                self.start_level(1)
            elif key == pygame.K_ESCAPE:
                self.mode = "menu"        

    def draw(self, screen, fonts):
        if self.mode == "menu":
            renderer.draw_menu(screen, fonts, self.difficulty)
            return
        self.anim.update(self.state)
        renderer.draw_grid(screen, self.state)
        if self.show_search:
            renderer.draw_search_overlay(screen, last_search["visited"], last_search["path"])
        renderer.draw_entities(screen, self.anim)
        info = {
            "level": self.level, "title": self.cfg["title"],
            "turns": self.state.turn_count, "score": self.total_score,
            "speed": self.cfg["speed"], "depth": self.cfg["depth"],
            "lives": self.lives, "max_lives": self.max_lives,
        }
        renderer.draw_hud(screen, fonts["small"], info)
        if self.show_stats:
            renderer.draw_stats_panel(screen, fonts["small"], info, self.stats)
        if self.mode == "level_complete":
             renderer.draw_level_complete(screen, fonts, self.level, self.state.turn_count,
                                    self.shortest, self.level_score,
                                    self.total_score, self.stars,
                                    self.level >= MAX_LEVEL, self.life_gain)
        elif self.mode == "caught":
            renderer.draw_caught(screen, fonts, self.level, self.total_score, self.lives)
        elif self.mode == "game_over":
            renderer.draw_game_over(screen, fonts, self.level, self.total_score)


def main():
    pygame.init()
    screen = pygame.display.set_mode((renderer.WIDTH, renderer.HEIGHT))
    pygame.display.set_caption("Vampire vs. Safe House")
    clock = pygame.time.Clock()
    fonts = {
        "small": pygame.font.SysFont("consolas", 14),
        "mid": pygame.font.SysFont("consolas", 18),
        "big": pygame.font.SysFont("consolas", 28, bold=True),
        "title": pygame.font.SysFont("consolas", 38, bold=True),
    }

    stats_logger.init_log()
    game = Game()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                game.handle_key(event.key)

        game.draw(screen, fonts)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()