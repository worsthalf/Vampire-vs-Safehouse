"""
renderer.py
Handles all Pygame drawing: the grid, obstacles, entities, and the
on-screen stats / message overlays.
"""

import pygame

CELL_SIZE = 40
GRID_SIZE = 15

COLOR_BG = (21, 21, 28)
COLOR_OBSTACLE = (58, 58, 68)
COLOR_SAFE_HOUSE = (46, 204, 113)
COLOR_SURVIVOR = (77, 166, 255)
COLOR_VAMPIRE1 = (255, 77, 109)
COLOR_VAMPIRE2 = (255, 140, 66)
COLOR_TEXT = (232, 232, 236)


def draw_grid(screen, state):
    """Draws the background grid, obstacles, and the Safe House."""
    screen.fill(COLOR_BG)
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if state.grid[y][x] == 1:
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE - 1, CELL_SIZE - 1)
                pygame.draw.rect(screen, COLOR_OBSTACLE, rect)

    sx, sy = state.safe_house
    pygame.draw.rect(
        screen, COLOR_SAFE_HOUSE,
        pygame.Rect(sx * CELL_SIZE, sy * CELL_SIZE, CELL_SIZE - 1, CELL_SIZE - 1)
    )


def draw_entity(screen, pos, color):
    """Draws a single circular entity at a grid position."""
    x, y = pos
    center = (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2)
    pygame.draw.circle(screen, color, center, CELL_SIZE // 2 - 3)


def draw_entities(screen, state):
    """Draws the Survivor and both Vampires."""
    draw_entity(screen, state.vampire1, COLOR_VAMPIRE1)
    draw_entity(screen, state.vampire2, COLOR_VAMPIRE2)
    draw_entity(screen, state.survivor, COLOR_SURVIVOR)


def draw_stats(screen, font, stats):
    """Draws the live stats overlay (states explored, timings) below the grid."""
    y_offset = GRID_SIZE * CELL_SIZE + 8
    lines = [
        f"Vampire 1 (Minimax) - states explored: {stats.get('v1_states', 0)}  "
        f"time: {stats.get('v1_time_ms', 0):.2f} ms",
        f"Vampire 2 (A*) - states explored: {stats.get('v2_states', 0)}  "
        f"time: {stats.get('v2_time_ms', 0):.2f} ms",
    ]
    for i, line in enumerate(lines):
        text_surface = font.render(line, True, COLOR_TEXT)
        screen.blit(text_surface, (8, y_offset + i * 20))


def draw_message(screen, font, message, color):
    """Draws a centered game-over / win message overlay."""
    text_surface = font.render(message, True, color)
    rect = text_surface.get_rect(center=(GRID_SIZE * CELL_SIZE // 2, GRID_SIZE * CELL_SIZE // 2))
    pygame.draw.rect(screen, (0, 0, 0), rect.inflate(20, 20))
    screen.blit(text_surface, rect)