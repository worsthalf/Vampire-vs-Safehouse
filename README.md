<div align="center">

# 🧛 Vampire vs. Safe House

### A Multi-Agent AI Search Engine & 3-Player Survival Strategy Game

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=flat-square&logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-2.5%2B-00d084?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)
![Status](https://img.shields.io/badge/Status-In%20Development-orange?style=flat-square)

Artificial Intelligence (CSE 3318) — Course Project, Premier University

<!-- TODO: replace with real gameplay GIF once playable -->
<!-- ![demo](assets/demo.gif) -->

</div>

---

## 📖 Table of Contents

- [Overview](#-overview)
- [Problem Statement](#-problem-statement)
- [Game Rules & Mechanics](#-game-rules--mechanics)
- [Features](#-features)
- [How the AI Works](#-how-the-ai-works)
- [Installation](#️-installation)
- [How to Run](#️-how-to-run)
- [Controls](#-controls)
- [Project Structure](#-project-structure)
- [File-by-File Explanation](#-file-by-file-explanation)
- [Evaluation Plan & Results](#-evaluation-plan--results)
- [Roadmap](#-roadmap)
- [Contributions](#-contributions)
- [References](#-references)
- [License](#-license)

---

## 🎮 Overview

**Vampire vs. Safe House** is a Python + Pygame grid-survival game built to demonstrate, in a real and interactive environment, how classical **informed search** and **adversarial game-theory** algorithms behave when pitted against each other.

The game is played on a `15 × 15` grid. One human-controlled **Survivor** must cross the grid — weaving around static obstacles — to reach the **Safe House** in the bottom-right corner. Two AI-controlled **Vampires**, each using a *different* search strategy, try to intercept the Survivor before they escape.

The core idea of the project is to show, side by side, how a **reactive** agent (one that always chases where the target currently is) behaves differently from a **predictive** agent (one that reasons about where the target is *going to be*).

---

## ❓ Problem Statement

In most simple 2D grid games, enemy characters move using either random movement or fixed, hardcoded routines. This makes their behavior predictable and easy to exploit, and it does not demonstrate any real decision-making intelligence.

This project addresses that gap by building a small multi-agent system in which:

- The **Survivor** moves purely on human input — no AI, no automation. This keeps a real, unpredictable "opponent" for the AI agents to react to, instead of a scripted dummy.
- **Vampire 2** uses **A\* Search** to reactively recompute the shortest path to the Survivor's current cell every turn.
- **Vampire 1** uses **Minimax with Alpha-Beta Pruning** to look several moves ahead and predict where the Survivor is likely to go, so it can cut off the escape route instead of simply following.

Comparing these two pursuit styles — reactive vs. predictive — inside the same game space is the central experiment of the project.

---

## 🕹 Game Rules & Mechanics

| Element | Description |
|---|---|
| **Grid** | `15 × 15` cells, some permanently blocked as obstacles (walls) |
| **Start positions** | Survivor `(0, 0)`, Vampire 1 `(14, 0)`, Vampire 2 `(0, 14)` |
| **Goal (Survivor)** | Reach the Safe House at `(14, 14)` |
| **Loss condition** | Either Vampire occupies the same cell as the Survivor |
| **Win condition** | Survivor reaches the Safe House before being caught |
| **Actions** | Up, Down, Left, Right — one cell per turn, diagonal moves are not allowed |
| **Move cost** | Every valid move between adjacent cells costs `1` (used by A*'s `g(n)`) |
| **Turn order** | Survivor moves (keypress) → Vampire 2 moves (A*) → Vampire 1 moves (Minimax) → repeat |

This is a **turn-based** design rather than real-time: each Survivor keypress triggers exactly one response move from each Vampire. This keeps the AI computation (especially Minimax) from ever causing input lag, and makes the states-explored / time measurements clean and comparable between turns.

---

## ✨ Features

- [x] `15 × 15` interactive grid with static obstacles
- [x] Fully manual Survivor movement (WASD / Arrow keys) — zero AI involvement
- [x] Vampire 2 — A* Search pathfinding (reactive pursuit)
- [x] Vampire 1 — Minimax with Alpha-Beta Pruning (predictive interception)
- [x] Live stats overlay — states explored & execution time per algorithm, per turn
- [x] Win / loss detection with on-screen message and instant restart (`R` key)
- [x] Per-turn CSV logging of algorithm performance for the evaluation report
- [ ] Difficulty levels (Easy / Medium / Hard) — obstacle density, spawn distance, Minimax depth
- [ ] Bar-chart visualization of states-explored comparison (Matplotlib, for the report)

---

## 🧠 How the AI Works

### Vampire 2 — A* Search (Reactive Pursuit)

Every turn, Vampire 2 re-runs A* Search from its own current position to the Survivor's **current** cell. It evaluates each candidate node using:

```
f(n) = g(n) + h(n)
```

- `g(n)` — the actual number of steps taken so far from the start
- `h(n)` — the estimated remaining distance to the goal, using the **Manhattan distance** heuristic:

```
h(n) = |x1 - x2| + |y1 - y2|
```

A* guarantees the shortest possible path around obstacles, but because it always targets the Survivor's *current* position, it is fundamentally reactive: if the Survivor keeps moving, Vampire 2 is always chasing a moving target and tends to trail one step behind.

### Vampire 1 — Minimax + Alpha-Beta Pruning (Predictive Interception)

Vampire 1 does not aim at the Survivor's current cell. Instead, it builds a short game tree (default depth `3`) that alternates between:

- **MAX layer** — Vampire 1's turn, trying to pick the move that **maximizes** its score
- **MIN layer** — the Survivor's (simulated) turn, assumed to always play the move that **minimizes** Vampire 1's score (i.e., the worst case for Vampire 1)

At each leaf of the tree, the position is scored by an **evaluation function**:

```
score =  (weight_A × distance(Survivor, SafeHouse))
        − (weight_B × distance(Vampire1, Survivor))
```

- A **higher** distance from Survivor to the Safe House is good for Vampire 1 (the Survivor is being kept away from the goal).
- A **lower** distance from Vampire 1 to the Survivor is good for Vampire 1 (it is closing in).
- Reaching the same cell as the Survivor, or the Survivor reaching the Safe House, are scored as large terminal bonuses/penalties so the search always prioritizes an actual capture or correctly avoids an inevitable escape.

**Alpha-Beta Pruning** is layered on top of this search: while exploring the tree, it keeps track of the best score the maximizer (`alpha`) and minimizer (`beta`) can already guarantee, and stops exploring a branch the moment it proves that branch cannot change the final decision. This does not change the move Vampire 1 picks — it only removes wasted computation, which is exactly what the **Evaluation Plan** below measures (states explored *with* vs. *without* pruning).

### Why two different Vampires?

> Vampire 2 pressures the Survivor from behind, while Vampire 1 tries to get ahead and block the path to the Safe House. Running both at once naturally produces a simple pincer effect, and comparing their individual capture rates is what makes the "reactive vs. predictive" comparison meaningful in the final report.

---

## ⚙️ Installation

```bash
git clone https://github.com/<your-username>/vampire-vs-safehouse.git
cd vampire-vs-safehouse
pip install -r requirements.txt
```

> Requires Python 3.9 or newer. If `pip install` fails on Linux, you may first need `sudo apt install python3-pip`.

## ▶️ How to Run

```bash
python main.py
```

A separate game window will open (not inside the terminal or your editor) — this is normal Pygame behavior, since it renders its own OS window.

## 🎹 Controls

| Key | Action |
|:---:|:---|
| `W` / `↑` | Move Survivor up |
| `S` / `↓` | Move Survivor down |
| `A` / `←` | Move Survivor left |
| `D` / `→` | Move Survivor right |
| `R` | Restart the game at any time |

---

## 🗂 Project Structure

```
vampire-vs-safehouse/
├── main.py             # Game loop, Pygame init, input handling, turn sequencing
├── game_state.py        # Grid, obstacle layout, GameState class, win/loss checks
├── astar.py             # A* Search — used by Vampire 2
├── minimax.py            # Minimax + Alpha-Beta Pruning — used by Vampire 1
├── evaluation.py          # Scoring function used inside Minimax
├── renderer.py             # All Pygame drawing (grid, entities, stats overlay)
├── stats_logger.py          # CSV logging of states explored / execution time
├── requirements.txt
├── .gitignore
└── README.md
```

## 📄 File-by-File Explanation

| File | Responsibility |
|---|---|
| `game_state.py` | Defines the `15×15` grid and obstacle walls, and the `GameState` class that holds every entity's position, whose `neighbors()` and `is_free()` methods are shared by both A* and Minimax so obstacle rules stay consistent everywhere. |
| `astar.py` | Implements A* Search with a min-heap (`heapq`) open set and Manhattan-distance heuristic; exposes `next_step_towards()`, which Vampire 2 calls once per turn. |
| `evaluation.py` | A standalone scoring function so the "intelligence" of Vampire 1 lives in one place, separate from the tree-search mechanics — makes it easy to tune weights without touching `minimax.py`. |
| `minimax.py` | Implements the recursive Minimax search with Alpha-Beta Pruning, alternating MAX (Vampire 1) and MIN (simulated Survivor) layers, and returns both the chosen move and the number of states explored. |
| `renderer.py` | Pure drawing code — no game logic — so the visuals can be restyled without touching how the game behaves. |
| `stats_logger.py` | Writes one CSV row per AI move (`turn`, `agent`, `algorithm`, `states_explored`, `time_ms`) to `stats_output/run_log.csv`, which becomes the raw data behind the Evaluation Plan table. |
| `main.py` | Wires everything together: reads keyboard input, advances the turn order (Survivor → Vampire 2 → Vampire 1), and redraws the screen every frame. |

---

## 📊 Evaluation Plan & Results

The project measures each algorithm on:

- **States/nodes explored** — how many grid cells the search actually visited
- **Execution time (ms)** — wall-clock time per decision
- **Path optimality** — whether the chosen path is guaranteed shortest

<!-- TODO: paste final measured numbers here after running several test sessions -->

| Algorithm | States Explored | Time (ms) | Optimality |
|:---|:---:|:---:|:---:|
| A* Search (Vampire 2) | _TBD_ | _TBD_ | Optimal |
| Minimax (no pruning) | _TBD_ | _TBD_ | Strategic |
| Minimax + Alpha-Beta (Vampire 1) | _TBD_ | _TBD_ | Strategic (optimized) |

All raw per-turn data is written automatically to `stats_output/run_log.csv` while the game runs — this is the source data for the table above and for any charts in the final report.

---

## 🗺 Roadmap

- [ ] Add selectable difficulty levels (obstacle density, spawn distance, Minimax depth)
- [ ] Add a "Minimax without pruning" toggle for a direct pruning-benefit comparison
- [ ] Generate a Matplotlib bar chart from `run_log.csv` for the final report
- [ ] Record a gameplay GIF for this README

---

## 👥 Contributions

| Student ID | Name | Role |
|:---|:---|:---|
| 0222410005101066 | MD Afzalul Hossain | <!-- e.g. Game engine, A* & Minimax implementation --> |
| 0222410005101061 | A K M Asadujjaman Jahed | <!-- e.g. Evaluation design, testing, report --> |
| 0222410005101070 | Suchana Barua | <!-- e.g. Documentation, presentation, benchmarking --> |

*Repository setup and code integration handled by [your name]; all members contributed to design, algorithm logic, testing, and the final report as detailed above.*

**Course:** Artificial Intelligence (CSE 3318)
**Instructor:** Ms. Tashin Hossain
**Department:** Computer Science and Engineering, Premier University

---

## 📚 References

1. Russell, S., & Norvig, P. *Artificial Intelligence: A Modern Approach*, 4th Edition, Pearson.
2. Hart, P. E., Nilsson, N. J., & Raphael, B. (1968). "A Formal Basis for the Heuristic Determination of Minimum Cost Paths." *IEEE Transactions on Systems Science and Cybernetics*.
3. Korf, R. E. (1990). "Real-time heuristic search." *Artificial Intelligence*, 42(2-3), 189–211.
4. Shannon, C. E. (1950). "Programming a Computer for Playing Chess." *Philosophical Magazine*.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
