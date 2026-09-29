"""
astar.py
A* Search implementation used by Vampire 2 for reactive pursuit of
the Survivor's current position.
"""

import heapq


def manhattan(a, b):
    """Manhattan distance heuristic between two grid points."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def a_star_search(state, start, goal):
    """
    Runs A* Search from start to goal on the given GameState's grid.
    Returns (path, states_explored), where path is a list of (x, y)
    coordinates from start to goal inclusive, or [] if no path exists.
    """
    open_set = [(manhattan(start, goal), 0, start)]
    came_from = {}
    g_score = {start: 0}
    visited = set()
    states_explored = 0

    while open_set:
        _, g, current = heapq.heappop(open_set)

        if current in visited:
            continue
        visited.add(current)
        states_explored += 1

        if current == goal:
            return _reconstruct_path(came_from, current), states_explored

        for neighbor in state.neighbors(current):
            tentative_g = g + 1
            if tentative_g < g_score.get(neighbor, float("inf")):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f = tentative_g + manhattan(neighbor, goal)
                heapq.heappush(open_set, (f, tentative_g, neighbor))

    return [], states_explored


def _reconstruct_path(came_from, current):
    """Rebuilds the path from the came_from map, in start-to-goal order."""
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path


def next_step_towards(state, start, goal):
    """
    Convenience wrapper: returns the next single step (x, y) an agent
    at `start` should take to move along the shortest path toward
    `goal`, plus the number of states A* explored during this call.
    """
    path, states_explored = a_star_search(state, start, goal)
    if len(path) > 1:
        return path[1], states_explored
    return start, states_explored