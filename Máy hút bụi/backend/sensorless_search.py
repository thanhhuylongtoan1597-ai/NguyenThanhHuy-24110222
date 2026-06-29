import time
from .utils import is_vacuum_goal, apply_vacuum_action_advanced

def run_sensorless_search(start_matrix, goal_matrix):
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

def run_sensorless_search_dual(matrix1, matrix2, goal_matrix):
    start_time = time.time()
    grid1 = tuple(tuple(row) for row in matrix1)
    grid2 = tuple(tuple(row) for row in matrix2)
    
    start_belief = frozenset(
        [(r, c, grid1) for r in range(3) for c in range(3)] +
        [(r, c, grid2) for r in range(3) for c in range(3)]
    )
    
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

