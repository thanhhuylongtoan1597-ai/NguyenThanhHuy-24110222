import time
from .utils import matrix_to_string, possible_moves, act, heuristic

def run_idastar(start, sx, sy, goal):
    start_time = time.time()
    node_count = [0]

    def dls_astar(matrix, x, y, goal, g_cost, threshold, path, visited_in_path):
        node_count[0] += 1
        h_cost = heuristic(matrix)
        f_cost = g_cost + h_cost
        
        if f_cost > threshold: return f_cost, None
        if matrix == goal: return f_cost, path
            
        state = (matrix_to_string(matrix), x, y)
        if state in visited_in_path: return float('inf'), None
            
        visited_in_path.add(state)
        min_cutoff_threshold = float('inf')
        
        for action in possible_moves(matrix, x, y):
            new_m, nx, ny = act(matrix, action, x, y)
            g_new = g_cost + 1
            res_f, res_path = dls_astar(new_m, nx, ny, goal, g_new, threshold, path + [action], visited_in_path)
            
            if res_path is not None: return res_f, res_path
            if res_f < min_cutoff_threshold: min_cutoff_threshold = res_f
                
        visited_in_path.remove(state)
        return min_cutoff_threshold, None

    threshold = heuristic(start)
    while threshold != float('inf'):
        res_f, path = dls_astar(start, sx, sy, goal, 0, threshold, [], set())
        if path is not None:
            return path, node_count[0], (time.time() - start_time) * 1000
        if res_f == float('inf'): break
        threshold = res_f
    return None, node_count[0], (time.time() - start_time) * 1000
