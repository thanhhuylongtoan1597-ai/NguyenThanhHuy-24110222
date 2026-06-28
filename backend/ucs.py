import heapq
import time
from .utils import matrix_to_string, possible_moves, act

def run_ucs(start, sx, sy, goal):
    start_time = time.time()
    frontier = [(0, start, sx, sy, [])]
    reached = {}
    node_count = 0
    while frontier:
        cost, current_matrix, x, y, path = heapq.heappop(frontier)
        node_count += 1
        state = (matrix_to_string(current_matrix), x, y)
        if current_matrix == goal:
            return path, node_count, (time.time() - start_time) * 1000
        if state not in reached or cost < reached[state]:
            reached[state] = cost
            for action in possible_moves(current_matrix, x, y):
                new_matrix, nx, ny = act(current_matrix, action, x, y)
                heapq.heappush(frontier, (cost + 1, new_matrix, nx, ny, path + [action]))
    return None, node_count, (time.time() - start_time) * 1000
