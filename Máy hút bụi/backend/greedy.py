import heapq
import time
from .utils import matrix_to_string, possible_moves, act, heuristic

def run_greedy(start, sx, sy, goal):
    start_time = time.time()
    h_start = heuristic(start)
    frontier = [(h_start, start, sx, sy, [])]
    reached = set()
    node_count = 0

    while frontier:
        _, current_matrix, x, y, path = heapq.heappop(frontier)
        node_count += 1
        state = (matrix_to_string(current_matrix), x, y)
        
        if current_matrix == goal:
            return path, node_count, (time.time() - start_time) * 1000
            
        reached.add(state)

        for action in possible_moves(current_matrix, x, y):
            new_matrix, nx, ny = act(current_matrix, action, x, y)
            child_state = (matrix_to_string(new_matrix), nx, ny)
            
            in_frontier = any((matrix_to_string(item[1]), item[2], item[3]) == child_state for item in frontier)

            if child_state not in reached and not in_frontier:
                h_m = heuristic(new_matrix)
                heapq.heappush(frontier, (h_m, new_matrix, nx, ny, path + [action]))

    return None, node_count, (time.time() - start_time) * 1000
