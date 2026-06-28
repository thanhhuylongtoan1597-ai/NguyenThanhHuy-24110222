import time
from .config import VARIABLES, DOMAINS, CONSTRAINTS

def run_pure_backtracking():
    start_time = time.time()
    history_states = []
    static_domains = {v: DOMAINS[:] for v in VARIABLES}

    def backtrack(assignment):
        if len(assignment) == len(VARIABLES):
            history_states.append({
                "assignment": assignment.copy(),
                "domains": static_domains.copy(),
                "msg": "THÀNH CÔNG: Đã tìm ra lời giải bằng Backtracking"
            })
            return True
            
        var = [v for v in VARIABLES if v not in assignment][0]
        
        for color in DOMAINS:
            consistent = True
            for v1, v2 in CONSTRAINTS:
                if v1 == var and v2 in assignment and assignment[v2] == color: consistent = False
                if v2 == var and v1 in assignment and assignment[v1] == color: consistent = False
            
            if not consistent:
                history_states.append({
                    "assignment": assignment.copy(),
                    "domains": get_display_domains(assignment, var, color),
                    "msg": f"Xung đột: Thử gán {var} = {color} thất bại do trùng màu với vùng liền kề"
                })
                continue
            
            new_assignment = assignment.copy()
            new_assignment[var] = color
            
            history_states.append({
                "assignment": new_assignment,
                "domains": get_display_domains(new_assignment, var, color),
                "msg": f"Chọn vùng để tô: {var}\n  - Thử gán {var} = {color}\n  -> Hợp lệ. Thử vùng tiếp theo."
            })
            
            if backtrack(new_assignment):
                return True
                
            history_states.append({
                "assignment": assignment.copy(),
                "domains": get_display_domains(assignment, var, color),
                "msg": f"Quay lui: Nhánh sau của {var} = {color} bị bế tắc. Thử màu khác."
            })
            
        return False

    def get_display_domains(current_assign, active_var, active_color):
        display_doms = {}
        for v in VARIABLES:
            if v in current_assign: display_doms[v] = [current_assign[v]]
            elif v == active_var: display_doms[v] = [active_color]
            else: display_doms[v] = DOMAINS[:]
        return display_doms

    backtrack({})
    return history_states, (time.time() - start_time) * 1000
