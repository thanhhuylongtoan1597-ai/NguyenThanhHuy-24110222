import time
from .utils import possible_moves, act

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
