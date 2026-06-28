import time
from .config import VARIABLES, DOMAINS, CONSTRAINTS, CSP

def run_csp_backtracking():
    start_time = time.time()
    history_states = []
    
    csp = CSP(VARIABLES, DOMAINS, CONSTRAINTS)
    
    def SELECT_UNASSIGNED_VARIABLE(variables, assignment, csp):
        unassigned = [v for v in variables if v not in assignment]
        return min(unassigned, key=lambda v: len(csp.DOMAINS[v]))
        
    def ORDER_DOMAIN_VALUES(var, assignment, csp):
        return csp.DOMAINS[var].copy()
        
    def FORWARD_CHECKING(var, value, assignment, csp):
        inferences = []
        fail = False
        for v1, v2 in csp.CONSTRAINTS:
            if v1 == var and v2 not in assignment:
                if value in csp.DOMAINS[v2]:
                    csp.DOMAINS[v2].remove(value)
                    inferences.append((v2, value))
                    if not csp.DOMAINS[v2]:
                        fail = True
            elif v2 == var and v1 not in assignment:
                if value in csp.DOMAINS[v1]:
                    csp.DOMAINS[v1].remove(value)
                    inferences.append((v1, value))
                    if not csp.DOMAINS[v1]:
                        fail = True
        return "FAILURE" if fail else inferences

    def BACKTRACK(assignment, csp):
        if len(assignment) == len(csp.VARIABLES):
            history_states.append({
                "assignment": assignment.copy(),
                "domains": {v: list(d) for v, d in csp.DOMAINS.items()},
                "msg": "THÀNH CÔNG: Đã tìm ra lời giải bằng CSP Backtracking!"
            })
            return assignment
            
        var = SELECT_UNASSIGNED_VARIABLE(csp.VARIABLES, assignment, csp)
        
        for value in ORDER_DOMAIN_VALUES(var, assignment, csp):
            consistent = True
            for v1, v2 in csp.CONSTRAINTS:
                if v1 == var and v2 in assignment and assignment[v2] == value:
                    consistent = False
                if v2 == var and v1 in assignment and assignment[v1] == value:
                    consistent = False
                    
            if not consistent:
                history_states.append({
                    "assignment": assignment.copy(),
                    "domains": {v: list(d) for v, d in csp.DOMAINS.items()},
                    "msg": f"Xung đột: Thử gán {var} = {value} thất bại do trùng màu với vùng liền kề."
                })
                continue
                
            assignment[var] = value
            local_domains = {v: list(d) for v, d in csp.DOMAINS.items()}
            
            inferences = FORWARD_CHECKING(var, value, assignment, csp)
            
            msg = f"Chọn biến: {var} (MRV).\n  - Thử gán {var} = {value}\n  - Tiến hành Forward Checking..."
            if inferences == "FAILURE":
                msg += f"\n  -> CẢNH BÁO: Miền giá trị của một vùng kề bị rỗng. Nhánh bế tắc."
            else:
                if inferences:
                    msg += f"\n  -> Cập nhật domain các vùng kề:\n" + "\n".join([f"    + Loại '{val}' khỏi {v}" for v, val in inferences])
                else:
                    msg += f"\n  -> Không có thay đổi domain của vùng kề."
                    
            history_states.append({
                "assignment": assignment.copy(),
                "domains": {v: list(d) for v, d in csp.DOMAINS.items()},
                "msg": msg
            })
            
            if inferences != "FAILURE":
                result = BACKTRACK(assignment, csp)
                if result is not None:
                    return result
                    
            if var in assignment:
                del assignment[var]
            csp.DOMAINS = local_domains
            
            history_states.append({
                "assignment": assignment.copy(),
                "domains": {v: list(d) for v, d in csp.DOMAINS.items()},
                "msg": f"Quay lui: Hủy gán {var} = {value} và khôi phục miền giá trị cũ."
            })
            
        return None

    def BACKTRACKING_SEARCH(csp):
        return BACKTRACK({}, csp)

    BACKTRACKING_SEARCH(csp)
    return history_states, (time.time() - start_time) * 1000
