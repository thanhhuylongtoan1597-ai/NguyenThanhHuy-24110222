import time
from .config import VARIABLES, DOMAINS, CONSTRAINTS

def run_backtracking_heuristics():
    start_time = time.time()
    history_states = []
    initial_domains = {v: DOMAINS[:] for v in VARIABLES}

    def get_mrv_degree_variable(assignment, domains):
        unassigned_vars = [v for v in VARIABLES if v not in assignment]
        if not unassigned_vars:
            return None
            
        min_size = min(len(domains[v]) for v in unassigned_vars)
        mrv_candidates = [v for v in unassigned_vars if len(domains[v]) == min_size]
        
        if len(mrv_candidates) == 1:
            return mrv_candidates[0]
            
        best_var = mrv_candidates[0]
        max_degree = -1
        for var in mrv_candidates:
            degree = 0
            for v1, v2 in CONSTRAINTS:
                if (v1 == var and v2 not in assignment) or (v2 == var and v1 not in assignment):
                    degree += 1
            if degree > max_degree:
                max_degree = degree
                best_var = var
        return best_var

    def get_lcv_ordered_values(var, assignment, domains):
        if len(domains[var]) <= 1:
            return domains[var]
            
        value_constraints = []
        for color in domains[var]:
            count = 0
            for v1, v2 in CONSTRAINTS:
                neighbor = None
                if v1 == var and v2 not in assignment: neighbor = v2
                elif v2 == var and v1 not in assignment: neighbor = v1
                
                if neighbor and color in domains[neighbor]:
                    count += 1
            value_constraints.append((color, count))
            
        value_constraints.sort(key=lambda x: x[1])
        return [color for color, _ in value_constraints]

    def backtrack(assignment, domains):
        if len(assignment) == len(VARIABLES):
            history_states.append({
                "assignment": assignment.copy(),
                "domains": {v: d[:] for v, d in domains.items()},
                "msg": "THÀNH CÔNG: Tìm thấy lời giải tối ưu bằng Backtracking + Heuristics!"
            })
            return True
            
        var = get_mrv_degree_variable(assignment, domains)
        if var is None: return False
        
        ordered_colors = get_lcv_ordered_values(var, assignment, domains)
        
        for color in ordered_colors:
            consistent = True
            for v1, v2 in CONSTRAINTS:
                if v1 == var and v2 in assignment and assignment[v2] == color: consistent = False
                if v2 == var and v1 in assignment and assignment[v1] == color: consistent = False
                
            if not consistent:
                continue
                
            new_assignment = assignment.copy()
            new_assignment[var] = color
            
            new_domains = {v: d[:] for v, d in domains.items()}
            new_domains[var] = [color]
            
            fc_fail = False
            fc_msgs = []
            for v1, v2 in CONSTRAINTS:
                if v1 == var and v2 not in new_assignment:
                    if color in new_domains[v2]:
                        new_domains[v2].remove(color)
                        fc_msgs.append(f"Loại '{color}' khỏi {v2}")
                        if not new_domains[v2]: fc_fail = True
                if v2 == var and v1 not in new_assignment:
                    if color in new_domains[v1]:
                        new_domains[v1].remove(color)
                        fc_msgs.append(f"Loại '{color}' khỏi {v1}")
                        if not new_domains[v1]: fc_fail = True

            msg = f"Chọn biến {var} theo MRV/Degree.\n  - Thử gán giá trị tối ưu LCV: {var} = {color}"
            if fc_msgs:
                msg += f"\n  -> Lan truyền cập nhật miền giá trị hàng xóm: {', '.join(fc_msgs)}"
            if fc_fail:
                msg += "\n  -> CẢNH BÁO: Miền giá trị hàng xóm rỗng! Nhánh bế tắc."

            history_states.append({
                "assignment": new_assignment,
                "domains": {v: d[:] for v, d in new_domains.items()},
                "msg": msg
            })
            
            if not fc_fail:
                if backtrack(new_assignment, new_domains):
                    return True
                    
            history_states.append({
                "assignment": assignment.copy(),
                "domains": {v: d[:] for v, d in domains.items()},
                "msg": f"Quay lui: Thử nghiệm {var} = {color} thất bại. Khôi phục trạng thái."
            })
            
        return False

    backtrack({}, initial_domains)
    return history_states, (time.time() - start_time) * 1000
