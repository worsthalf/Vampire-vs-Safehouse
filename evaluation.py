from astar import manhattan

W_SURVIVOR_TO_HOME = 1.0
W_VAMPIRE_TO_SURVIVOR = 1.5
W_TERMINAL_BONUS = 500


def evaluate(state):
   
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