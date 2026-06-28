import time
import random
from .config import VARIABLES, DOMAINS, CONSTRAINTS

def run_min_conflicts_simulation(max_steps=100):
    start_time = time.time()
    history_states = []
    
    current_assignment = {v: random.choice(DOMAINS) for v in VARIABLES}
    
    def count_conflicts(var, color, assignment):
        conflicts = 0
        for v1, v2 in CONSTRAINTS:
            if v1 == var and assignment.get(v2) == color:
                conflicts += 1
            if v2 == var and assignment.get(v1) == color:
                conflicts += 1
        return conflicts

    def get_all_conflicted_vars(assignment):
        conflicted = []
        for v1, v2 in CONSTRAINTS:
            if assignment.get(v1) == assignment.get(v2):
                if v1 not in conflicted: conflicted.append(v1)
                if v2 not in conflicted: conflicted.append(v2)
        return conflicted

    static_domains = {v: DOMAINS[:] for v in VARIABLES}
    
    history_states.append({
        "assignment": current_assignment.copy(),
        "domains": static_domains.copy(),
        "msg": f"KHOI TAO: Gan ngau nhien trang thai ban dau cho tat ca cac vung."
    })

    for step in range(1, max_steps + 1):
        conflicted_vars = get_all_conflicted_vars(current_assignment)
        
        if not conflicted_vars:
            history_states.append({
                "assignment": current_assignment.copy(),
                "domains": static_domains.copy(),
                "msg": f"THANH CONG: Tim thay loi giai phu hop tai buoc {step}!"
            })
            return history_states, (time.time() - start_time) * 1000

        var = random.choice(conflicted_vars)
        
        min_conflict_count = float('inf')
        best_colors = []
        
        for color in DOMAINS:
            num_conflicts = count_conflicts(var, color, current_assignment)
            if num_conflicts < min_conflict_count:
                min_conflict_count = num_conflicts
                best_colors = [color]
            elif num_conflicts == min_conflict_count:
                best_colors.append(color)
                
        chosen_color = random.choice(best_colors)
        current_assignment[var] = chosen_color
        
        history_states.append({
            "assignment": current_assignment.copy(),
            "domains": static_domains.copy(),
            "msg": f"BUOC {step}: Chon ngau nhien vung xung dot {var}.\n  - Thay doi sang mau {chosen_color} (so xung dot thap nhat: {min_conflict_count})."
        })

    history_states.append({
        "assignment": current_assignment.copy(),
        "domains": static_domains.copy(),
        "msg": f"THAT BAI: Khong tim thay loi giai sau {max_steps} buoc lap."
    })
    return history_states, (time.time() - start_time) * 1000
