import time
from .config import VARIABLES, DOMAINS, CONSTRAINTS

def run_forward_checking():
    start_time = time.time()
    history_states = []
    
    def backtrack(assignment, domains):
        if len(assignment) == len(VARIABLES):
            history_states.append({
                "assignment": assignment.copy(),
                "domains": {v: d[:] for v, d in domains.items()},
                "msg": "THÀNH CÔNG: Đã tìm ra lời giải bằng Forward Checking"
            })
            return True
            
        var = [v for v in VARIABLES if v not in assignment][0]
        
        for color in domains[var]:
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
                        fc_msgs.append(f"Cập nhật miền giá trị của {v2}: loại bỏ '{color}'")
                        if not new_domains[v2]: fc_fail = True
                if v2 == var and v1 not in new_assignment:
                    if color in new_domains[v1]:
                        new_domains[v1].remove(color)
                        fc_msgs.append(f"Cập nhật miền giá trị của {v1}: loại bỏ '{color}'")
                        if not new_domains[v1]: fc_fail = True
            
            msg = f"Chọn vùng để tô: {var}\n  - Thử gán {var} = {color}\n  -> Hợp lệ. Assignment = {new_assignment}"
            if fc_msgs:
                msg += "\n  -> Cập nhật domain các huyện giáp ranh chưa gán:\n" + "\n".join([f"    + {m}" for m in fc_msgs])
            if fc_fail:
                msg += "\n    CẢNH BÁO: Miền giá trị của một vùng kề bị rỗng. Nhánh này bế tắc."
            
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
                "msg": f"Quay lui: Thử nghiệm vùng {var} = {color} bế tắc. Khôi phục trạng thái cũ."
            })
            
        return False

    initial_domains = {v: DOMAINS[:] for v in VARIABLES}
    backtrack({}, initial_domains)
    return history_states, (time.time() - start_time) * 1000
