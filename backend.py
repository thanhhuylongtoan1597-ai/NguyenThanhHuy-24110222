import heapq
import math
import time
from collections import deque
import random

def matrix_to_string(matrix):
    return "".join("".join(str(value) for value in row) for row in matrix)

def possible_moves(matrix, x, y):
    moves = []
    if matrix[x][y] == 1:
        moves.append("SUCK")
    if x > 0:   moves.append("UP")
    if x < 2:   moves.append("DOWN")
    if y > 0:   moves.append("LEFT")
    if y < 2:   moves.append("RIGHT")
    return moves

def act(matrix, action, x, y):
    matrix_copy = [row[:] for row in matrix]
    i, j = x, y
    if action == "UP":     i -= 1
    elif action == "DOWN":  i += 1
    elif action == "LEFT":  j -= 1
    elif action == "RIGHT": j += 1
    elif action == "SUCK":  matrix_copy[i][j] = 0
    return matrix_copy, i, j

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

def run_dfs1(start, sx, sy, goal):
    start_time = time.time()
    node = (start, sx, sy, [])
    frontier = [node]
    reached = set()
    node_count = 0

    while frontier:
        current_matrix, x, y, path = frontier.pop()
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

def run_dfs2(start, sx, sy, goal):
    start_time = time.time()
    if start == goal:
        return [], 1, (time.time() - start_time) * 1000

    node = (start, sx, sy, [])
    frontier = [node]
    reached = set()
    reached.add((matrix_to_string(start), sx, sy))
    node_count = 0

    while frontier:
        current_matrix, x, y, path = frontier.pop()
        node_count += 1

        for action in reversed(possible_moves(current_matrix, x, y)):
            new_matrix, nx, ny = act(current_matrix, action, x, y)
            child_state = (matrix_to_string(new_matrix), nx, ny)

            if child_state not in reached:
                new_path = path + [action]
                if new_matrix == goal:
                    return new_path, node_count, (time.time() - start_time) * 1000
                frontier.append((new_matrix, nx, ny, new_path))
                reached.add(child_state)

    return None, node_count, (time.time() - start_time) * 1000

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


def heuristic(matrix):
    return sum(row.count(1) for row in matrix)

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
            g_new = g_cost + 1 # Sửa g_cost đồng bộ tương tự A*
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

def run_simple_hill_climbing(start, sx, sy, goal):
    start_time = time.time()
    current_matrix = [row[:] for row in start]
    cx, cy = sx, sy
    path = []
    node_count = 0
    visited = set()

    while True:
        node_count += 1
        state = (matrix_to_string(current_matrix), cx, cy)
        if current_matrix == goal:
            return path, node_count, (time.time() - start_time) * 1000
        if state in visited:
            return None, node_count, (time.time() - start_time) * 1000
        visited.add(state)

        curr_val = -heuristic(current_matrix)
        found_next = False

        for action in possible_moves(current_matrix, cx, cy):
            new_matrix, nx, ny = act(current_matrix, action, cx, cy)
            next_val = -heuristic(new_matrix)

            if next_val > curr_val:
                current_matrix, cx, cy = new_matrix, nx, ny
                path.append(action)
                found_next = True
                break

        if not found_next:
            return None, node_count, (time.time() - start_time) * 1000

def run_steepest_hill_climbing(start, sx, sy, goal):
    start_time = time.time()
    current_matrix = [row[:] for row in start]
    cx, cy = sx, sy
    path = []
    node_count = 0

    while True:
        node_count += 1
        if current_matrix == goal:
            return path, node_count, (time.time() - start_time) * 1000

        curr_val = -heuristic(current_matrix)
        best_neighbor, best_action = None, None
        best_val = -float('inf')
        best_x, best_y = cx, cy

        for action in possible_moves(current_matrix, cx, cy):
            new_matrix, nx, ny = act(current_matrix, action, cx, cy)
            next_val = -heuristic(new_matrix)

            if next_val > best_val:
                best_val = next_val
                best_neighbor = new_matrix
                best_action = action
                best_x, best_y = nx, ny

        if best_neighbor is not None and best_val > curr_val:
            current_matrix = best_neighbor
            cx, cy = best_x, best_y
            path.append(best_action)
        else:
            return None, node_count, (time.time() - start_time) * 1000

def run_stochastic_hill_climbing(start, sx, sy, goal):
    start_time = time.time()
    current_matrix = [row[:] for row in start]
    cx, cy = sx, sy
    path = []
    node_count = 0
    visited = set()

    while True:
        node_count += 1
        state = (matrix_to_string(current_matrix), cx, cy)
        if current_matrix == goal:
            return path, node_count, (time.time() - start_time) * 1000
        if state in visited:
            return None, node_count, (time.time() - start_time) * 1000
        visited.add(state)

        curr_val = -heuristic(current_matrix)
        better_neighbors = []

        for action in possible_moves(current_matrix, cx, cy):
            new_matrix, nx, ny = act(current_matrix, action, cx, cy)
            next_val = -heuristic(new_matrix)
            if next_val > curr_val:
                better_neighbors.append((new_matrix, nx, ny, action))

        if not better_neighbors:
            return None, node_count, (time.time() - start_time) * 1000
        else:
            current_matrix, cx, cy, chosen_action = random.choice(better_neighbors)
            path.append(chosen_action)

def run_random_restart_hc(start, sx, sy, goal, max_restart=15):
    start_time = time.time()
    
    for i in range(max_restart):
        current_matrix = [row[:] for row in start]
        cx, cy = sx, sy
        path = []
        visited = set()
        
        while True:
            if current_matrix == goal:
                return path, i + 1, (time.time() - start_time) * 1000
            
            state = (matrix_to_string(current_matrix), cx, cy)
            if state in visited: break
            visited.add(state)
            
            better_neighbors = []
            for action in possible_moves(current_matrix, cx, cy):
                new_m, nx, ny = act(current_matrix, action, cx, cy)
                if heuristic(new_m) < heuristic(current_matrix):
                    better_neighbors.append((new_m, nx, ny, action))
            
            if not better_neighbors:
                moves = possible_moves(current_matrix, cx, cy)
                action = random.choice(moves)
                current_matrix, cx, cy = act(current_matrix, action, cx, cy)
                path.append(action)
                continue
            
            current_matrix, cx, cy, action = random.choice(better_neighbors)
            path.append(action)
            
    return None, max_restart, (time.time() - start_time) * 1000

def run_local_beam_search(start, sx, sy, goal, k=3):
    start_time = time.time()
    current_state_set = [(start, sx, sy, [])] 
    
    for _ in range(100): 
        neighbor_states = []
        for matrix, x, y, path in current_state_set:
            if matrix == goal: return path, len(current_state_set), (time.time() - start_time) * 1000
            
            for action in possible_moves(matrix, x, y):
                new_m, nx, ny = act(matrix, action, x, y)
                if new_m == goal: return path + [action], len(current_state_set), (time.time() - start_time) * 1000
                neighbor_states.append((new_m, nx, ny, path + [action]))
        
        if not neighbor_states: break
        neighbor_states.sort(key=lambda item: heuristic(item[0]))
        current_state_set = neighbor_states[:k]
        
    return None, 0, (time.time() - start_time) * 1000

def run_simulated_annealing(start, sx, sy, goal):
    start_time = time.time()
    current_matrix = [row[:] for row in start]
    cx, cy = sx, sy
    path = []
    node_count = 0

    T = 100.0       
    Tmin = 1.0      
    alpha = 0.95    

    while T > Tmin:
        node_count += 1
        if current_matrix == goal:
            return path, node_count, (time.time() - start_time) * 1000

        moves = possible_moves(current_matrix, cx, cy)
        action = random.choice(moves)
        new_matrix, nx, ny = act(current_matrix, action, cx, cy)

        delta = heuristic(new_matrix) - heuristic(current_matrix)

        if delta < 0:
            current_matrix, cx, cy = new_matrix, nx, ny
            path.append(action)
        else:
            p = math.exp(-delta / T)
            if random.random() < p:
                current_matrix, cx, cy = new_matrix, nx, ny
                path.append(action)
        T = alpha * T

    return None, node_count, (time.time() - start_time) * 1000

def is_vacuum_goal(matrix):
    return sum(sum(row) for row in matrix) == 0

def apply_vacuum_action_advanced(matrix, action, x, y):
    matrix_copy = [row[:] for row in matrix]
    nx, ny = x, y
    if action == "UP":
        if x > 0: nx -= 1
        else: return None, x, y
    elif action == "DOWN":
        if x < 2: nx += 1
        else: return None, x, y
    elif action == "LEFT":
        if y > 0: ny -= 1
        else: return None, x, y
    elif action == "RIGHT":
        if y < 2: ny += 1
        else: return None, x, y
    elif action == "SUCK":
        if matrix_copy[x][y] == 1: matrix_copy[x][y] = 0
        else: return None, x, y 
    return matrix_copy, nx, ny

def run_multi_dfs(start_matrix, sx, sy, goal_matrix):
    start_time = time.time()
    r2, c2 = (2, 2) if (sx, sy) != (2, 2) else (0, 0)
    start_grid = tuple(tuple(row) for row in start_matrix)
    start_state = (sx, sy, r2, c2, start_grid)
    
    frontier = [(start_state, [])]
    reached = set([start_state])
    node_count = 0
    actions = ["SUCK", "UP", "DOWN", "LEFT", "RIGHT"]
    
    while frontier:
        (r1, c1, r2, c2, current_grid), path = frontier.pop()
        node_count += 1
        current_matrix = [list(row) for row in current_grid]
        
        if is_vacuum_goal(current_matrix):
            return path, node_count, (time.time() - start_time) * 1000
            
        for action in actions:
            res1, nr1, nc1 = apply_vacuum_action_advanced(current_matrix, action, r1, c1)
            res2, nr2, nc2 = apply_vacuum_action_advanced(current_matrix, action, r2, c2)
            
            if res1 is None and res2 is None: continue
                
            m1 = res1 if res1 is not None else current_matrix
            m2 = res2 if res2 is not None else current_matrix
            
            next_matrix = [[0]*3 for _ in range(3)]
            for r in range(3):
                for c in range(3):
                    if m1[r][c] == 1 or m2[r][c] == 1: # Sửa logic giao thoa trạng thái bụi (OR)
                        next_matrix[r][c] = 1
                        
            next_grid = tuple(tuple(row) for row in next_matrix)
            child_state = (nr1, nc1, nr2, nc2, next_grid)
            if child_state not in reached:
                reached.add(child_state)
                frontier.append((child_state, path + [action]))
                
    return None, node_count, (time.time() - start_time) * 1000

def run_belief_dfs(start_matrix, goal_matrix):
    start_time = time.time()
    grid_tuple = tuple(tuple(row) for row in start_matrix)
    start_belief = frozenset((r, c, grid_tuple) for r in range(3) for c in range(3))
    
    frontier = [(start_belief, [])]
    reached = set([start_belief])
    node_count = 0
    actions = ["SUCK", "UP", "DOWN", "LEFT", "RIGHT"]
    
    while frontier:
        current_belief, path = frontier.pop()
        node_count += 1
        
        if all(is_vacuum_goal([list(row) for row in s[2]]) for s in current_belief):
            return path, node_count, (time.time() - start_time) * 1000
            
        for action in actions:
            next_belief_list = []
            has_changed = False 
            
            for (r, c, grid) in current_belief:
                matrix_state = [list(row) for row in grid]
                res_m, nr, nc = apply_vacuum_action_advanced(matrix_state, action, r, c)
                if res_m is not None:
                    has_changed = True
                    next_belief_list.append((nr, nc, tuple(tuple(row) for row in res_m)))
                else:
                    next_belief_list.append((r, c, grid))
                    
            if not has_changed: continue 
            next_belief = frozenset(next_belief_list)
            if next_belief not in reached:
                reached.add(next_belief)
                frontier.append((next_belief, path + [action]))
                
    return None, node_count, (time.time() - start_time) * 1000

def run_and_or_search(start_matrix, sx, sy, goal_matrix):
    start_time = time.time()
    node_count = [0]
    
    def to_tuple(m):
        return tuple(tuple(row) for row in m)

    def or_search(state, path):
        node_count[0] += 1
        matrix, cx, cy = state
        
        if matrix == to_tuple(goal_matrix):
            return []
            
        if state in path:
            return None
            
        moves = possible_moves([list(r) for r in matrix], cx, cy)
        
        for action in moves:
            next_m, nx, ny = act([list(r) for r in matrix], action, cx, cy)
            next_state = (to_tuple(next_m), nx, ny)
            result_states = [next_state] 
            plan = and_search(result_states, path + [state])
            if plan is not None:
                return [action, plan]
                
        return None

    def and_search(states, path):
        plans = {}
        
        for s in states:
            plan_s = or_search(s, path)
            
            if plan_s is None:
                return None
                
            plans[s] = plan_s
            
        return plans

    initial_state = (to_tuple(start_matrix), sx, sy)
    conditional_plan = or_search(initial_state, [])
    
    all_executable_paths = []
    
    def extract_paths(plan, current_path):
        if plan == []:
            all_executable_paths.append(current_path)
            return
        if plan is None or not isinstance(plan, list) or len(plan) < 2:
            return
            
        action = plan[0]
        next_and_plans = plan[1]  
        
        for s, sub_plan in next_and_plans.items():
            extract_paths(sub_plan, current_path + [action])

    if conditional_plan is not None:
        extract_paths(conditional_plan, [])
    
    best_path = min(all_executable_paths, key=len) if all_executable_paths else None
    elapsed_time = (time.time() - start_time) * 1000
    
    return best_path, all_executable_paths, conditional_plan, node_count[0], elapsed_time
