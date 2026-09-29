import heapq

last_search = {"visited": set(), "path": []}   # renderer eta dekhe


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def _search(state, start, goal):
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
            return _reconstruct_path(came_from, current), states_explored, visited

        for neighbor in state.neighbors(current):
            tentative_g = g + 1
            if tentative_g < g_score.get(neighbor, float("inf")):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f = tentative_g + manhattan(neighbor, goal)
                heapq.heappush(open_set, (f, tentative_g, neighbor))

    return [], states_explored, visited


def _reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path


def a_star_search(state, start, goal):
    path, explored, _ = _search(state, start, goal)
    return path, explored


def next_step_towards(state, start, goal):
    
    path, explored, visited = _search(state, start, goal)
    last_search["visited"] = visited
    last_search["path"] = path
    if len(path) > 1:
        return path[1], explored
    return start, explored