import heapq
import time
from .utils import matrix_to_string, possible_moves, act, heuristic

def run_astar(start, sx, sy, goal):
    start_time = time.time()
    g_costs = {}
    start_state = (matrix_to_string(start), sx, sy)
    g_costs[start_state] = 0
    h_start = heuristic(start)
    frontier = [(h_start, start, sx, sy, [])]
    reached = set()
    node_count = 0

    while frontier:
        f_val, current_matrix, x, y, path = heapq.heappop(frontier)
        node_count += 1
        state = (matrix_to_string(current_matrix), x, y)
        curr_g = g_costs[state]

        if current_matrix == goal:
            return path, node_count, (time.time() - start_time) * 1000

        reached.add(state)

        for action in possible_moves(current_matrix, x, y):
            new_matrix, nx, ny = act(current_matrix, action, x, y)
            child_state = (matrix_to_string(new_matrix), nx, ny)
            
            g_new = curr_g + 1 
            
            in_frontier = any((matrix_to_string(item[1]), item[2], item[3]) == child_state for item in frontier)

            if child_state in reached:
                if g_new >= g_costs.get(child_state, float('inf')):
                    continue
                else:
                    reached.remove(child_state)
                    g_costs[child_state] = g_new
                    h_m = heuristic(new_matrix)
                    heapq.heappush(frontier, (g_new + h_m, new_matrix, nx, ny, path + [action]))
                    
            elif in_frontier:
                if g_new < g_costs.get(child_state, float('inf')):
                    g_costs[child_state] = g_new
                    h_m = heuristic(new_matrix)
                    for i, item in enumerate(frontier):
                        if (matrix_to_string(item[1]), item[2], item[3]) == child_state:
                            frontier[i] = (g_new + h_m, item[1], item[2], item[3], path + [action])
                            break
                    heapq.heapify(frontier)
                    
            elif child_state not in reached and not in_frontier:
                g_costs[child_state] = g_new
                h_m = heuristic(new_matrix)
                heapq.heappush(frontier, (g_new + h_m, new_matrix, nx, ny, path + [action]))

    return None, node_count, (time.time() - start_time) * 1000
