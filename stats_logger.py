import csv
import os

LOG_PATH = "stats_output/run_log.csv"
FIELDNAMES = ["level", "turn", "agent", "algorithm", "states_explored", "time_ms"]


def init_log():
    
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    with open(LOG_PATH, "w", newline="") as f:
        csv.DictWriter(f, fieldnames=FIELDNAMES).writeheader()


def log_turn(level, turn, agent, algorithm, states_explored, time_ms):
    
    with open(LOG_PATH, "a", newline="") as f:
        csv.DictWriter(f, fieldnames=FIELDNAMES).writerow({
            "level": level,
            "turn": turn,
            "agent": agent,
            "algorithm": algorithm,
            "states_explored": states_explored,
            "time_ms": round(time_ms, 3),
        })