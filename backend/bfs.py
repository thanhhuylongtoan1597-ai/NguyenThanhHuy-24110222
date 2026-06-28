import time
from collections import deque
from .utils import matrix_to_string, possible_moves, act

def run_bfs1(start, sx, sy, goal):
    start_time = time.time()
    node = (start, sx, sy, [])
    frontier = deque([node])
    reached = set()
    node_count = 0

    while frontier:
        current_matrix, x, y, path = frontier.popleft()
        node_count += 1
        state = (matrix_to_string(current_matrix), x, y)
        reached.add(state)

        if current_matrix == goal:
            return path, node_count, (time.time() - start_time) * 1000

        for action in possible_moves(current_matrix, x, y):
            new_matrix, nx, ny = act(current_matrix, action, x, y)
            child_state = (matrix_to_string(new_matrix), nx, ny)

            if child_state not in reached:
                in_frontier = False
                for item in frontier:
                    if (matrix_to_string(item[0]), item[1], item[2]) == child_state:
                        in_frontier = True
                        break
                if not in_frontier:
                    frontier.append((new_matrix, nx, ny, path + [action]))

    return None, node_count, (time.time() - start_time) * 1000

def run_bfs2(start, sx, sy, goal):
    start_time = time.time()
    if start == goal:
        return [], 1, (time.time() - start_time) * 1000

    node = (start, sx, sy, [])
    frontier = deque([node])
    reached = set()
    reached.add((matrix_to_string(start), sx, sy))
    node_count = 0

    while frontier:
        current_matrix, x, y, path = frontier.popleft()
        node_count += 1

        for action in possible_moves(current_matrix, x, y):
            new_matrix, nx, ny = act(current_matrix, action, x, y)
            child_state = (matrix_to_string(new_matrix), nx, ny)

            if child_state not in reached:
                new_path = path + [action]
                if new_matrix == goal:
                    return new_path, node_count, (time.time() - start_time) * 1000
                frontier.append((new_matrix, nx, ny, new_path))
                reached.add(child_state)

    return None, node_count, (time.time() - start_time) * 1000
