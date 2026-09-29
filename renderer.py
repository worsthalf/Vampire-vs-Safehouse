

import pygame

CELL_SIZE = 40
GRID_SIZE = 15
HUD_HEIGHT = 30
WIDTH = GRID_SIZE * CELL_SIZE
HEIGHT = GRID_SIZE * CELL_SIZE + HUD_HEIGHT

COLOR_BG = (21, 21, 28)
COLOR_TILE_A = (26, 30, 40)
COLOR_TILE_B = (31, 35, 47)
COLOR_WALL = (78, 78, 92)
COLOR_WALL_DARK = (48, 48, 60)
COLOR_TEXT = (232, 232, 236)
COLOR_GOLD = (255, 209, 102)
SKIN = (255, 214, 170)

_cache = {}



def _new_sprite():
    s = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
    pygame.draw.ellipse(s, (0, 0, 0, 90), (9, 34, 22, 6))  # ground shadow
    return s


def _make_human():
    s = _new_sprite()
    shirt, pants = (77, 166, 255), (45, 55, 90)
    pygame.draw.rect(s, pants, (13, 29, 6, 9), border_radius=2)          # legs
    pygame.draw.rect(s, pants, (21, 29, 6, 9), border_radius=2)
    pygame.draw.rect(s, shirt, (6, 18, 5, 11), border_radius=2)          # arms
    pygame.draw.rect(s, shirt, (29, 18, 5, 11), border_radius=2)
    pygame.draw.circle(s, SKIN, (8, 30), 2)                              # hands
    pygame.draw.circle(s, SKIN, (32, 30), 2)
    pygame.draw.rect(s, shirt, (11, 16, 18, 15), border_radius=4)        # torso
    pygame.draw.circle(s, (90, 55, 30), (20, 10), 8)                     # hair
    pygame.draw.circle(s, SKIN, (20, 12), 6)                             # face
    pygame.draw.circle(s, (30, 30, 30), (18, 12), 1)                     # eyes
    pygame.draw.circle(s, (30, 30, 30), (22, 12), 1)
    pygame.draw.line(s, (170, 90, 80), (18, 15), (22, 15), 1)            # smile
    return s


def _make_vampire(cape):
    s = _new_sprite()
    dark = (25, 20, 35)
    pygame.draw.polygon(s, cape, [(20, 14), (3, 37), (37, 37)])          # cape
    pygame.draw.rect(s, dark, (14, 30, 5, 8))                            # legs
    pygame.draw.rect(s, dark, (21, 30, 5, 8))
    pygame.draw.rect(s, dark, (13, 17, 14, 14), border_radius=3)         # suit
    pygame.draw.polygon(s, (235, 235, 240), [(17, 17), (23, 17), (20, 25)])  # shirt
    pygame.draw.polygon(s, cape, [(20, 15), (9, 10), (13, 21)])          # high collar
    pygame.draw.polygon(s, cape, [(20, 15), (31, 10), (27, 21)])
    pygame.draw.circle(s, (15, 12, 20), (20, 9), 8)                      # slick hair
    pygame.draw.circle(s, (232, 232, 242), (20, 12), 6)                  # pale face
    pygame.draw.circle(s, (255, 40, 60), (18, 11), 1)                    # red eyes
    pygame.draw.circle(s, (255, 40, 60), (22, 11), 1)
    pygame.draw.line(s, (60, 20, 30), (17, 14), (23, 14), 1)             # mouth
    pygame.draw.polygon(s, (255, 255, 255), [(17, 14), (19, 14), (18, 18)])  # fangs
    pygame.draw.polygon(s, (255, 255, 255), [(21, 14), (23, 14), (22, 18)])
    return s


def get_sprite(name):
    if name not in _cache:
        if name == "survivor":
            _cache[name] = _make_human()
        elif name == "vampire1":
            _cache[name] = _make_vampire((150, 15, 40))    # crimson cape
        else:
            _cache[name] = _make_vampire((95, 45, 150))    # purple cape
    return _cache[name]




class Animator:
    

    def __init__(self):
        self.pos = {}

    def snap(self, state):
        self.pos = {
            "survivor": list(state.survivor),
            "vampire1": list(state.vampire1),
            "vampire2": list(state.vampire2),
        }

    def update(self, state):
        targets = {"survivor": state.survivor, "vampire1": state.vampire1,
                   "vampire2": state.vampire2}
        for name, (tx, ty) in targets.items():
            p = self.pos[name]
            p[0] += (tx - p[0]) * 0.35
            p[1] += (ty - p[1]) * 0.35
            if abs(tx - p[0]) < 0.01 and abs(ty - p[1]) < 0.01:
                p[0], p[1] = tx, ty




def draw_house(screen, cell):
    x, y = cell[0] * CELL_SIZE, cell[1] * CELL_SIZE
    glow = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
    pygame.draw.circle(glow, (46, 204, 113, 60), (20, 20), 20)
    screen.blit(glow, (x, y))
    pygame.draw.rect(screen, (222, 196, 150), (x + 7, y + 18, 26, 18))         # walls
    pygame.draw.polygon(screen, (170, 60, 50),
                        [(x + 3, y + 19), (x + 20, y + 4), (x + 37, y + 19)])  # roof
    pygame.draw.rect(screen, (90, 60, 40), (x + 16, y + 25, 8, 11))            # door
    pygame.draw.rect(screen, (255, 230, 120), (x + 9, y + 22, 5, 5))           # windows
    pygame.draw.rect(screen, (255, 230, 120), (x + 26, y + 22, 5, 5))


def draw_grid(screen, state):
    screen.fill(COLOR_BG)
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            r = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if state.grid[y][x] == 1:
                pygame.draw.rect(screen, COLOR_WALL_DARK, r)
                pygame.draw.rect(screen, COLOR_WALL, r.inflate(-3, -3), border_radius=3)
                pygame.draw.line(screen, COLOR_WALL_DARK, (r.x + 3, r.centery),
                                 (r.right - 4, r.centery), 1)
            else:
                pygame.draw.rect(screen, COLOR_TILE_A if (x + y) % 2 == 0 else COLOR_TILE_B, r)
    draw_house(screen, state.safe_house)


def draw_entities(screen, anim):
    for name in ("vampire1", "vampire2", "survivor"):
        px, py = anim.pos[name]
        screen.blit(get_sprite(name), (px * CELL_SIZE, py * CELL_SIZE))


def draw_heart(screen, cx, cy, r, color):
    """Small heart shape made from two circles and a triangle."""
    pygame.draw.circle(screen, color, (cx - r // 2, cy - r // 4), r // 2 + 1)
    pygame.draw.circle(screen, color, (cx + r // 2, cy - r // 4), r // 2 + 1)
    pygame.draw.polygon(screen, color, [(cx - r, cy - r // 4 + 1),
                                        (cx + r, cy - r // 4 + 1),
                                        (cx, cy + r)])


def draw_lives(screen, lives, max_lives, top):
    """Hearts in the bottom-right corner of the HUD bar."""
    spacing = 24
    x = WIDTH - 12 - max_lives * spacing + spacing // 2
    cy = top + HUD_HEIGHT // 2
    for i in range(max_lives):
        if i < lives:
            draw_heart(screen, x + i * spacing, cy, 8, (255, 77, 109))
        else:
            draw_heart(screen, x + i * spacing, cy, 8, (55, 40, 52))


def draw_hud(screen, font, info):
    top = GRID_SIZE * CELL_SIZE
    pygame.draw.rect(screen, (14, 14, 20), (0, top, WIDTH, HUD_HEIGHT))
    text = (f"Lv {info['level']}: {info['title']}   Turns: {info['turns']}   "
            f"Score: {info['score']}   Spd x{info['speed']}")
    surf = font.render(text, True, COLOR_GOLD)
    screen.blit(surf, surf.get_rect(midleft=(8, top + HUD_HEIGHT // 2)))
    draw_lives(screen, info["lives"], info["max_lives"], top)

def draw_stats_panel(screen, font, info, stats):
    lines = [
        f"Minimax depth: {info['depth']}",
        f"V1 Minimax: {stats['v1_states']} states, {stats['v1_time_ms']:.2f} ms",
        f"V2 A*:      {stats['v2_states']} states, {stats['v2_time_ms']:.2f} ms",
    ]
    box = pygame.Surface((330, 12 + len(lines) * 20), pygame.SRCALPHA)
    box.fill((0, 0, 0, 180))
    screen.blit(box, (8, 8))
    for i, text in enumerate(lines):
        screen.blit(font.render(text, True, COLOR_TEXT), (16, 14 + i * 20))    

def _center(screen, font, text, y, color):
    surf = font.render(text, True, color)
    screen.blit(surf, surf.get_rect(center=(WIDTH // 2, y)))

def draw_menu(screen, fonts):
    screen.fill(COLOR_BG)
    for y in range(0, HEIGHT, CELL_SIZE):
        for x in range(0, WIDTH, CELL_SIZE):
            if (x // CELL_SIZE + y // CELL_SIZE) % 2 == 0:
                pygame.draw.rect(screen, COLOR_TILE_A, (x, y, CELL_SIZE, CELL_SIZE))
    _center(screen, fonts["title"], "VAMPIRE vs. SAFE HOUSE", 110, (255, 77, 109))
    _center(screen, fonts["mid"], "Reach the Safe House before the vampires catch you!", 165, COLOR_TEXT)
    for name, cx in (("survivor", WIDTH // 2), ("vampire1", WIDTH // 2 - 150),
                     ("vampire2", WIDTH // 2 + 150)):
        big = pygame.transform.scale(get_sprite(name), (CELL_SIZE * 3, CELL_SIZE * 3))
        screen.blit(big, big.get_rect(center=(cx, 290)))
    draw_house(screen, (7, 9))
    _center(screen, fonts["big"], "Press ENTER to Start", 430, (46, 204, 113))
    _center(screen, fonts["mid"], "Move: W A S D / Arrow keys (one step per press)", 490, COLOR_TEXT)
    _center(screen, fonts["mid"], "Every level: new map, faster vampires", 520, COLOR_TEXT)


def _panel(screen, fonts, title, title_color, lines, footer):
    dim = pygame.Surface((WIDTH, GRID_SIZE * CELL_SIZE), pygame.SRCALPHA)
    dim.fill((0, 0, 0, 170))
    screen.blit(dim, (0, 0))
    box = pygame.Rect(0, 0, 460, 300)
    box.center = (WIDTH // 2, GRID_SIZE * CELL_SIZE // 2)
    pygame.draw.rect(screen, (18, 18, 26), box, border_radius=12)
    pygame.draw.rect(screen, title_color, box, 3, border_radius=12)
    _center(screen, fonts["big"], title, box.top + 45, title_color)
    for i, (text, color) in enumerate(lines):
        _center(screen, fonts["mid"], text, box.top + 100 + i * 32, color)
    _center(screen, fonts["mid"], footer, box.bottom - 30, COLOR_GOLD)


def draw_level_complete(screen, fonts, level, turns, shortest, level_score, total,
                        stars, is_last=False, life_gain=0):
    star_text = "*" * stars + "-" * (3 - stars)
    title = "YOU WIN!" if is_last else "CONGRATULATIONS!"
    footer = "ESC: menu" if is_last else "ENTER: next level   ESC: menu"
    life_text = f"+{life_gain} life regained!" if life_gain > 0 else "Lives: no change"
    _panel(screen, fonts, title, (46, 204, 113), [
        (f"Level {level} complete!   [{star_text}]", COLOR_GOLD),
        (f"Turns: {turns}  (best possible: {shortest})", COLOR_TEXT),
        (f"Level score: {level_score}", COLOR_TEXT),
        (f"Total score: {total}", COLOR_TEXT),
        (life_text, (255, 77, 109) if life_gain > 0 else COLOR_TEXT),
    ], footer)


def draw_caught(screen, fonts, level, total, lives):
    _panel(screen, fonts, "CAUGHT!", (255, 77, 109), [
        ("The vampires got you...", COLOR_TEXT),
        (f"Lives left: {lives}", COLOR_GOLD),
        (f"Level {level}   Total score: {total}", COLOR_TEXT),
    ], "R: retry level   ESC: menu")

def draw_game_over(screen, fonts, level, total):
    _panel(screen, fonts, "GAME OVER", (255, 77, 109), [
        ("You ran out of lives...", COLOR_TEXT),
        (f"Reached level {level}", COLOR_TEXT),
        (f"Final score: {total}", COLOR_GOLD),
    ], "ENTER: restart from level 1   ESC: menu")

def draw_search_overlay(screen, visited, path):
    explored = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
    explored.fill((150, 60, 220, 70))
    for (x, y) in visited:
        screen.blit(explored, (x * CELL_SIZE, y * CELL_SIZE))
    route = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
    route.fill((255, 209, 102, 120))
    for (x, y) in path:
        screen.blit(route, (x * CELL_SIZE, y * CELL_SIZE))