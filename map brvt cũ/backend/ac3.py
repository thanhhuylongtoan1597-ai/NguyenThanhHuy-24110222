import time
from .config import VARIABLES, DOMAINS, CONSTRAINTS

def run_ac3_simulation():
    start_time = time.time()
    history_states = []
    
    domains = {v: DOMAINS[:] for v in VARIABLES}

    def ac3_search(assignment, current_domains):
        if len(assignment) == len(VARIABLES):
            history_states.append({
                "assignment": assignment.copy(),
                "domains": {v: d[:] for v, d in current_domains.items()},
                "msg": "THANH CONG: AC-3 phoi hop Tim kiem da to mau thanh cong toan bo ban do!"
            })
            return True

        var = [v for v in VARIABLES if v not in assignment][0]

        for color in current_domains[var]:
            new_assignment = assignment.copy()
            new_assignment[var] = color

            new_domains = {v: d[:] for v, d in current_domains.items()}
            new_domains[var] = [color]

            history_states.append({
                "assignment": new_assignment.copy(),
                "domains": {v: d[:] for v, d in new_domains.items()},
                "msg": f"TO MAU: Thu gan {var} = {color}.\n[He thong] Bat dau goi AC-3 de kiem tra nhat quan cung..."
            })

            queue = []
            for v1, v2 in CONSTRAINTS:
                queue.append((v1, v2))
                queue.append((v2, v1))

            ac3_failed = False
            while queue:
                vi, vj = queue.pop(0)
                
                removed = False
                new_vi_domain = new_domains[vi][:]
                
                for x in new_domains[vi]:
                    has_valid_y = any(y != x for y in new_domains[vj])
                    
                    if not has_valid_y:
                        new_vi_domain.remove(x)
                        removed = True
                        history_states.append({
                            "assignment": new_assignment.copy(),
                            "domains": {v: (new_vi_domain[:] if v == vi else d[:]) for v, d in new_domains.items()},
                            "msg": f"  [AC-3] Xet cung ({vi} - {vj}): Xoa mau '{x}' khoi {vi} vi be tac."
                        })

                if removed:
                    new_domains[vi] = new_vi_domain
                    if not new_domains[vi]:
                        ac3_failed = True
                        history_states.append({
                            "assignment": new_assignment.copy(),
                            "domains": {v: d[:] for v, d in new_domains.items()},
                            "msg": f"  [AC-3 Canh bao] Mien gia tri cua {vi} bi rong! Dung nhanh AC-3 nay."
                        })
                        break

                    for v1, v2 in CONSTRAINTS:
                        if v1 == vi and v2 != vj and (v2, vi) not in queue: queue.append((v2, vi))
                        if v2 == vi and v1 != vj and (v1, vi) not in queue: queue.append((v1, vi))

            if not ac3_failed:
                history_states.append({
                    "assignment": new_assignment.copy(),
                    "domains": {v: d[:] for v, d in new_domains.items()},
                    "msg": f"[AC-3 Dat] Do thi nhat quan cung sau khi gan {var}={color}. Tien hanh vung tiep theo."
                })
                if ac3_search(new_assignment, new_domains):
                    return True

            history_states.append({
                "assignment": assignment.copy(),
                "domains": {v: d[:] for v, d in current_domains.items()},
                "msg": f"QUAY LUI: Nhanh gan {var} = {color} gay be tac he thong. Khoi phuc trang thai cu."
            })

        return False

    ac3_search({}, domains)
    return history_states, (time.time() - start_time) * 1000
