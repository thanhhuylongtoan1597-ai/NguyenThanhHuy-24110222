import math
import random
import time
from .utils import possible_moves, act, heuristic_beam

def run_simulated_annealing(start, sx, sy, goal, T0=100.0, Tmin=0.01, alpha=0.95):
    start_time = time.time()
    current_matrix = [row[:] for row in start]
    cx, cy = sx, sy
    path = []
    node_count = 0

    T = T0

    while T > Tmin:
        node_count += 1
        if current_matrix == goal:
            return path, node_count, (time.time() - start_time) * 1000

        moves = possible_moves(current_matrix, cx, cy)
        if not moves:
            break
        action = random.choice(moves)
        new_matrix, nx, ny = act(current_matrix, action, cx, cy)

        curr_h = heuristic_beam(current_matrix, cx, cy)
        next_h = heuristic_beam(new_matrix, nx, ny)
        delta = next_h - curr_h

        if delta < 0:
            current_matrix, cx, cy = new_matrix, nx, ny
            path.append(action)
        else:
            p = math.exp(-delta / T) if T != 0 else 0
            if random.uniform(0, 1) < p:
                current_matrix, cx, cy = new_matrix, nx, ny
                path.append(action)
        T = alpha * T

    return path, node_count, (time.time() - start_time) * 1000
