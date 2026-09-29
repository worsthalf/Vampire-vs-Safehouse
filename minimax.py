"""
minimax.py
Minimax with Alpha-Beta Pruning used by Vampire 1 for predictive
interception of the Survivor.
"""

import copy
from evaluation import evaluate

MAX_DEPTH = 3


def minimax_decide(state, depth=MAX_DEPTH):
    """
    Chooses Vampire 1's next move by running Minimax with Alpha-Beta
    Pruning. Vampire 1 is the maximizing player; the Survivor is
    modeled as the minimizing (assumed-optimal) opponent.
    Returns (best_move, states_explored).
    """
    stats = {"states_explored": 0}
    _, best_move = _minimax(
        state, depth, float("-inf"), float("inf"),
        maximizing=True, stats=stats
    )
    return best_move or state.vampire1, stats["states_explored"]


def _minimax(state, depth, alpha, beta, maximizing, stats):
    stats["states_explored"] += 1

    if depth == 0 or state.check_end_conditions():
        return evaluate(state), None

    if maximizing:
        # Vampire 1's turn: maximize its advantage
        best_score = float("-inf")
        best_move = None
        for move in state.neighbors(state.vampire1) or [state.vampire1]:
            child = _apply_vampire1_move(state, move)
            score, _ = _minimax(child, depth - 1, alpha, beta, False, stats)
            if score > best_score:
                best_score = score
                best_move = move
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break  # beta cut-off
        return best_score, best_move
    else:
        # Survivor's turn: assumed optimal, minimizes Vampire 1's score
        best_score = float("inf")
        for move in state.neighbors(state.survivor) or [state.survivor]:
            child = _apply_survivor_move(state, move)
            score, _ = _minimax(child, depth - 1, alpha, beta, True, stats)
            if score < best_score:
                best_score = score
            beta = min(beta, best_score)
            if beta <= alpha:
                break  # alpha cut-off
        return best_score, None


def _apply_vampire1_move(state, move):
    """Returns a shallow copy of state with Vampire 1 moved to `move`."""
    new_state = copy.copy(state)
    new_state.vampire1 = move
    return new_state


def _apply_survivor_move(state, move):
    """Returns a shallow copy of state with the Survivor moved to `move`."""
    new_state = copy.copy(state)
    new_state.survivor = move
    return new_state