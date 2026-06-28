import time
from .utils import possible_moves, act, heuristic_beam, matrix_to_string

def run_local_beam_search(start, sx, sy, goal, k=3):
    start_time = time.time()
    
    current_state_set = []
    
    start_state = (start, sx, sy, [])
    current_state_set.append(start_state)
    
    max_loops = 500
    loops = 0
    visited = set()
    node_count = 0

    while loops < max_loops:
        loops += 1
        neighbor_states = []

        for matrix, x, y, path in current_state_set:
            node_count += 1
            if matrix == goal:
                return path, node_count, (time.time() - start_time) * 1000

            for action in possible_moves(matrix, x, y):
                new_m, nx, ny = act(matrix, action, x, y)
                state_key = (nx, ny, matrix_to_string(new_m))
                
                if state_key not in visited:
                    visited.add(state_key)
                    neighbor_states.append((new_m, nx, ny, path + [action]))

        if not neighbor_states:
            best_state = min(current_state_set, key=lambda item: heuristic_beam(item[0], item[1], item[2]))
            return best_state[3], node_count, (time.time() - start_time) * 1000

        for item in neighbor_states:
            if item[0] == goal or heuristic_beam(item[0], item[1], item[2]) == 0:
                return item[3], node_count, (time.time() - start_time) * 1000

        neighbor_states.sort(key=lambda item: heuristic_beam(item[0], item[1], item[2]))
        current_state_set = neighbor_states[:k]

    best_state = min(current_state_set, key=lambda item: heuristic_beam(item[0], item[1], item[2]))
    return best_state[3], node_count, (time.time() - start_time) * 1000
