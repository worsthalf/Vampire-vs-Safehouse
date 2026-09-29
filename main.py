import time
import pygame

from game_state import GameState, GRID_SIZE
from astar import next_step_towards
from minimax import minimax_decide
import renderer
import stats_logger

CELL_SIZE = renderer.CELL_SIZE
WINDOW_WIDTH = GRID_SIZE * CELL_SIZE
WINDOW_HEIGHT = GRID_SIZE * CELL_SIZE + 50

KEY_MOVES = {
    pygame.K_w: (0, -1), pygame.K_UP: (0, -1),
    pygame.K_s: (0, 1), pygame.K_DOWN: (0, 1),
    pygame.K_a: (-1, 0), pygame.K_LEFT: (-1, 0),
    pygame.K_d: (1, 0), pygame.K_RIGHT: (1, 0),
}


def move_survivor(state, dx, dy):
    """Attempts to move the Survivor by (dx, dy); ignored if blocked or out of bounds."""
    x, y = state.survivor
    new_pos = (x + dx, y + dy)
    if state.is_free(*new_pos):
        state.survivor = new_pos


def take_ai_turns(state, stats):
    """Runs Vampire 2 (A*) then Vampire 1 (Minimax) for one turn, and logs stats."""
    if state.check_end_conditions():
        return

    # Vampire 2: reactive A* chase toward the Survivor's current cell
    t0 = time.perf_counter()
    move, states_explored = next_step_towards(state, state.vampire2, state.survivor)
    t1 = time.perf_counter()
    state.vampire2 = move
    stats["v2_states"] = states_explored
    stats["v2_time_ms"] = (t1 - t0) * 1000
    stats_logger.log_turn(state.turn_count, "vampire2", "A*", states_explored, stats["v2_time_ms"])

    if state.check_end_conditions():
        return

    # Vampire 1: predictive Minimax + Alpha-Beta Pruning
    t0 = time.perf_counter()
    move, states_explored = minimax_decide(state)
    t1 = time.perf_counter()
    state.vampire1 = move
    stats["v1_states"] = states_explored
    stats["v1_time_ms"] = (t1 - t0) * 1000
    stats_logger.log_turn(state.turn_count, "vampire1", "Minimax+AlphaBeta", states_explored, stats["v1_time_ms"])

    state.check_end_conditions()


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Vampire vs. Safe House")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 14)
    big_font = pygame.font.SysFont("consolas", 26, bold=True)

    state = GameState()
    stats = {"v1_states": 0, "v1_time_ms": 0, "v2_states": 0, "v2_time_ms": 0}
    stats_logger.init_log()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    state = GameState()
                    stats = {"v1_states": 0, "v1_time_ms": 0, "v2_states": 0, "v2_time_ms": 0}
                elif not state.game_over and event.key in KEY_MOVES:
                    dx, dy = KEY_MOVES[event.key]
                    move_survivor(state, dx, dy)
                    state.turn_count += 1
                    take_ai_turns(state, stats)

        renderer.draw_grid(screen, state)
        renderer.draw_entities(screen, state)
        renderer.draw_stats(screen, font, stats)

        if state.game_over:
            if state.winner == "survivor":
                renderer.draw_message(screen, big_font, "SURVIVOR ESCAPED! Press R to restart", (46, 204, 113))
            else:
                renderer.draw_message(screen, big_font, "CAUGHT! Press R to restart", (255, 77, 109))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()