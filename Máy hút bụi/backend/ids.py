import time
from .utils import matrix_to_string, possible_moves, act

def run_ids_1(start, sx, sy, goal):
    start_time = time.time()
    def dls(matrix, x, y, goal, limit, path):
        if matrix == goal: return path
        if limit <= 0: return None
        for action in possible_moves(matrix, x, y):
            new_m, nx, ny = act(matrix, action, x, y)
            res = dls(new_m, nx, ny, goal, limit - 1, path + [action])
            if res is not None: return res
        return None
    for limit in range(50):
        res = dls(start, sx, sy, goal, limit, [])
        if res is not None:
            return res, limit * 10, (time.time() - start_time) * 1000
    return None, 0, (time.time() - start_time) * 1000

def run_ids_2(start, sx, sy, goal):
    start_time = time.time()
    def dls_with_cycle_check(matrix, x, y, goal, limit, path, visited_in_path):
        state = (matrix_to_string(matrix), x, y)
        if state in visited_in_path:
            return None
        if matrix == goal: 
            return path
        if limit <= 0: 
            return None
            
        visited_in_path.add(state)
        for action in possible_moves(matrix, x, y):
            new_m, nx, ny = act(matrix, action, x, y)
            res = dls_with_cycle_check(new_m, nx, ny, goal, limit - 1, path + [action], visited_in_path)
            if res is not None: 
                return res
        visited_in_path.remove(state) 
        return None

    for limit in range(50):
        res = dls_with_cycle_check(start, sx, sy, goal, limit, [], set())
        if res is not None:
            return res, limit * 15, (time.time() - start_time) * 1000
    return None, 0, (time.time() - start_time) * 1000
