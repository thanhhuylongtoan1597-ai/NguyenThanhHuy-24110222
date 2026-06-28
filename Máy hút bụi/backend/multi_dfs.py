import time
from .utils import is_vacuum_goal, apply_vacuum_action_advanced

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
                    if m1[r][c] == 1 or m2[r][c] == 1:
                        next_matrix[r][c] = 1
                        
            next_grid = tuple(tuple(row) for row in next_matrix)
            child_state = (nr1, nc1, nr2, nc2, next_grid)
            if child_state not in reached:
                reached.add(child_state)
                frontier.append((child_state, path + [action]))
                
    return None, node_count, (time.time() - start_time) * 1000
