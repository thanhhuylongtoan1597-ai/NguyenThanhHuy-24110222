import random
import time
from .utils import possible_moves, act, get_value

def run_simple_hill_climbing(start, sx, sy, goal):
    """
    Mã giả Slide 1: Simple Hill Climbing
    """
    start_time = time.time()
    current_matrix = [row[:] for row in start]
    cx, cy = sx, sy
    path = []
    node_count = 0
    max_loops = 1000

    for _ in range(max_loops):
        node_count += 1
        if current_matrix == goal:
            return path, node_count, (time.time() - start_time) * 1000

        curr_val = get_value(current_matrix, cx, cy)
        found_better = False

        for action in possible_moves(current_matrix, cx, cy):
            new_matrix, nx, ny = act(current_matrix, action, cx, cy)
            next_val = get_value(new_matrix, nx, ny)

            if next_val > curr_val:
                current_matrix, cx, cy = new_matrix, nx, ny
                path.append(action)
                found_better = True
                break

        if not found_better:
            return path, node_count, (time.time() - start_time) * 1000

    return path, node_count, (time.time() - start_time) * 1000

def run_steepest_hill_climbing(start, sx, sy, goal):
    """
    Mã giả Slide 2: Steepest Ascent Hill Climbing
    """
    start_time = time.time()
    current_matrix = [row[:] for row in start]
    cx, cy = sx, sy
    path = []
    node_count = 0
    max_loops = 1000

    for _ in range(max_loops):
        node_count += 1
        if current_matrix == goal:
            return path, node_count, (time.time() - start_time) * 1000

        curr_val = get_value(current_matrix, cx, cy)
        best_neighbor = None
        best_val = curr_val
        best_action = None
        best_x, best_y = cx, cy

        for action in possible_moves(current_matrix, cx, cy):
            new_matrix, nx, ny = act(current_matrix, action, cx, cy)
            next_val = get_value(new_matrix, nx, ny)

            if next_val > best_val:
                best_val = next_val
                best_neighbor = new_matrix
                best_action = action
                best_x, best_y = nx, ny

        if best_neighbor is not None:
            current_matrix = best_neighbor
            cx, cy = best_x, best_y
            path.append(best_action)
        else:
            return path, node_count, (time.time() - start_time) * 1000

    return path, node_count, (time.time() - start_time) * 1000

def run_stochastic_hill_climbing(start, sx, sy, goal):
    """
    Mã giả Slide 3: Stochastic Hill Climbing
    """
    start_time = time.time()
    current_matrix = [row[:] for row in start]
    cx, cy = sx, sy
    path = []
    node_count = 0
    max_loops = 1000

    for _ in range(max_loops):
        node_count += 1
        if current_matrix == goal:
            return path, node_count, (time.time() - start_time) * 1000

        curr_val = get_value(current_matrix, cx, cy)
        better_neighbors = []

        for action in possible_moves(current_matrix, cx, cy):
            new_matrix, nx, ny = act(current_matrix, action, cx, cy)
            next_val = get_value(new_matrix, nx, ny)
            if next_val > curr_val:
                better_neighbors.append((new_matrix, nx, ny, action))

        if not better_neighbors:
            return path, node_count, (time.time() - start_time) * 1000
        else:
            chosen = random.choice(better_neighbors)
            current_matrix, cx, cy, chosen_action = chosen
            path.append(chosen_action)

    return path, node_count, (time.time() - start_time) * 1000

def run_random_restart_hc(start, sx, sy, goal, max_restart=20):
    """
    Random Restart Hill Climbing
    """
    start_time = time.time()
    total_node_count = 0
    
    for i in range(1, max_restart + 1):
        if i == 1:
            current_matrix = [row[:] for row in start]
            cx, cy = sx, sy
        else:
            current_matrix = [row[:] for row in start]
            cx = random.randint(0, len(start) - 1)
            cy = random.randint(0, len(start[0]) - 1)
            
        path = []
        while True:
            total_node_count += 1
            if current_matrix == goal:
                return path, total_node_count, (time.time() - start_time) * 1000
            
            curr_val = get_value(current_matrix, cx, cy)
            better_neighbors = []
            
            for action in possible_moves(current_matrix, cx, cy):
                new_m, nx, ny = act(current_matrix, action, cx, cy)
                next_val = get_value(new_m, nx, ny)
                if next_val > curr_val:
                    better_neighbors.append((next_val, new_m, nx, ny, action))
            
            if not better_neighbors:
                break
            else:
                best_neighbor = max(better_neighbors, key=lambda item: item[0])
                _, current_matrix, cx, cy, action = best_neighbor
                path.append(action)
                
    return [], total_node_count, (time.time() - start_time) * 1000
