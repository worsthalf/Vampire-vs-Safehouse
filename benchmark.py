import csv
import os
import time

from game_state import GameState
from astar import a_star_search
from minimax import minimax_decide
from levels import _random_walls

DENSITY = {"low": 2, "medium": 5, "high": 10}   
SEEDS = range(1, 21)                            
SPEED, DEPTH, MAX_TURNS = 0.7, 3, 150


def episode(walls, prune):
    st = GameState(walls, SPEED)
    m = {"v1_states": 0, "v1_ms": 0.0, "v1_n": 0,
         "v2_states": 0, "v2_ms": 0.0, "v2_n": 0, "v2_path": 0}
    while not st.game_over and st.turn_count < MAX_TURNS:
        path, _ = a_star_search(st, st.survivor, st.safe_house)   
        if len(path) > 1:
            st.survivor = path[1]
        st.turn_count += 1
        if st.check_end_conditions():
            break
        for _ in range(st.vampire_steps_this_turn()):
            t = time.perf_counter()
            p, n = a_star_search(st, st.vampire2, st.survivor)
            m["v2_ms"] += (time.perf_counter() - t) * 1000
            m["v2_states"] += n
            m["v2_path"] += max(0, len(p) - 1)
            m["v2_n"] += 1
            if len(p) > 1:
                st.vampire2 = p[1]
            if st.check_end_conditions():
                break
            t = time.perf_counter()
            move, n = minimax_decide(st, DEPTH, prune)
            m["v1_ms"] += (time.perf_counter() - t) * 1000
            m["v1_states"] += n
            m["v1_n"] += 1
            st.vampire1 = move
            if st.check_end_conditions():
                break
    if st.winner == "vampires":
        result, by = "caught", ("vampire1" if st.survivor == st.vampire1 else "vampire2")
    elif st.winner == "survivor":
        result, by = "escaped", "-"
    else:
        result, by = "timeout", "-"
    return st, m, result, by


def main():
    os.makedirs("stats_output", exist_ok=True)
    with open("stats_output/benchmark.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["density", "seed", "alpha_beta", "result", "captured_by", "turns",
                    "v1_avg_states", "v1_avg_ms", "v2_avg_states", "v2_avg_ms", "v2_avg_path_len"])
        for name, target in DENSITY.items():
            for seed in SEEDS:
                walls = _random_walls(seed, target)
                for prune in (True, False):
                    st, m, result, by = episode(walls, prune)
                    v1n, v2n = max(1, m["v1_n"]), max(1, m["v2_n"])
                    w.writerow([name, seed, prune, result, by, st.turn_count,
                                round(m["v1_states"] / v1n, 1), round(m["v1_ms"] / v1n, 3),
                                round(m["v2_states"] / v2n, 1), round(m["v2_ms"] / v2n, 3),
                                round(m["v2_path"] / v2n, 1)])
    print("Done -> stats_output/benchmark.csv")


if __name__ == "__main__":
    main()