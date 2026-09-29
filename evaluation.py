"""
evaluation.py
Evaluation function used by Vampire 1's Minimax search to score
non-terminal and terminal game states.
"""

from astar import manhattan

W_SURVIVOR_TO_HOME = 1.0
W_VAMPIRE_TO_SURVIVOR = 1.5
W_TERMINAL_BONUS = 500


def evaluate(state):
    """
    Higher scores favor Vampire 1. Rewards:
      - keeping the Survivor far from the Safe House,
      - Vampire 1 staying close to the Survivor,
      - an outright capture (best possible outcome for Vampire 1),
    and heavily penalizes the Survivor reaching the Safe House.
    """
    if state.survivor == state.vampire1 or state.survivor == state.vampire2:
        return W_TERMINAL_BONUS

    if state.survivor == state.safe_house:
        return -W_TERMINAL_BONUS

    dist_survivor_home = manhattan(state.survivor, state.safe_house)
    dist_vampire_survivor = manhattan(state.vampire1, state.survivor)

    score = (
        W_SURVIVOR_TO_HOME * dist_survivor_home
        - W_VAMPIRE_TO_SURVIVOR * dist_vampire_survivor
    )
    return score