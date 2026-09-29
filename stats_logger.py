"""
stats_logger.py
Logs per-turn AI performance statistics (states explored, execution
time) to a CSV file, used later for the project's evaluation report.
"""

import csv
import os

LOG_PATH = "stats_output/run_log.csv"
FIELDNAMES = ["turn", "agent", "algorithm", "states_explored", "time_ms"]


def init_log():
    """Creates the stats_output folder and CSV file with a header row."""
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    with open(LOG_PATH, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()


def log_turn(turn, agent, algorithm, states_explored, time_ms):
    """Appends one row of stats for a single agent's move this turn."""
    with open(LOG_PATH, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writerow({
            "turn": turn,
            "agent": agent,
            "algorithm": algorithm,
            "states_explored": states_explored,
            "time_ms": round(time_ms, 3),
        })