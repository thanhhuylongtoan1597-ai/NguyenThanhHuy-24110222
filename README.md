---

- **Họ và tên:** Nguyễn Thành Huy
- **Mã số sinh viên (MSSV):** 24110222
- **Môn học:** Introduction to AI (Nhập môn Trí tuệ Nhân tạo)

---

## Tổng quan dự án

Dự án này là nơi lưu trữ các bài tập thực hành, mô hình Agent và các ứng dụng trực quan hóa thuật toán cho môn học **Nhập môn Trí tuệ Nhân tạo (Introduction to AI)**.

Hệ thống được thiết kế linh hoạt kết hợp với giao diện trực quan đồ họa (GUI) nhằm minh họa sinh động cách các thuật toán trí tuệ nhân tạo giải quyết các bài toán thực tế và bài toán kinh điển:
1. **Robot Hút Bụi (Vacuum Cleaner):** Giải bài toán di chuyển và làm sạch môi trường trong các điều kiện quan sát đầy đủ, không cảm biến (sensorless), quan sát một phần (partial observation), cũng như môi trường có vật cản phức tạp. Tích hợp các thuật toán tìm kiếm mù, heuristic, local search và môi trường phức tạp.
2. **Tô Màu Bản Đồ (Map Coloring - CSP):** Áp dụng các thuật toán thỏa mãn ràng buộc (Constraint Satisfaction Problems) như Quay lui (Backtracking), Kiểm tra trước (Forward Checking), AC-3 để tô màu bản đồ hành chính tỉnh Bà Rịa - Vũng Tàu.
3. **Cờ Caro đối kháng (Tic-Tac-Toe / Caro Game):** Triển khai các thuật toán tìm kiếm đối kháng (Adversarial Search) như Minimax, Alpha-Beta Pruning và Expectimax giúp AI đưa ra quyết định nước đi tối ưu chống lại người chơi hoặc đối thủ ngẫu nhiên.
4. **Bài toán 8-Puzzle:** Xây dựng các mô hình Simple Reflex Agent và Model-Based Reflex Agent giải bài toán xếp số 8-Puzzle.

---

## Cấu trúc thư mục dự án

```text
NguyenThanhHuy-24110222/
├── 8puzzle_model.py          # Mô hình Agent giải bài toán 8-Puzzle (Simple & Model-Based)
├── puzzle_bfs.py             # Thuật toán BFS giải bài toán 8-Puzzle
├── mayhutbui_model.py        # Mô hình Agent cho robot hút bụi đơn giản
├── mayhutbuivatcan.py        # Mô hình Agent cho robot hút bụi trong môi trường có vật cản
│
├── Máy hút bụi/              # Ứng dụng & Thuật toán tìm kiếm cho Bài toán Robot Hút Bụi
│   ├── main.py               # Điểm khởi chạy ứng dụng GUI Robot Hút Bụi
│   ├── frontend/             # Giao diện đồ họa (GUI) mô phỏng robot và lưới môi trường
│   └── backend/              # Tập hợp các thuật toán tìm kiếm cốt lõi
│       ├── bfs.py            # Breadth-First Search
│       ├── dfs.py            # Depth-First Search
│       ├── ucs.py            # Uniform Cost Search
│       ├── ids.py            # Iterative Deepening Search
│       ├── greedy.py         # Greedy Best-First Search
│       ├── astar.py          # A* Search
│       ├── idastar.py        # Iterative Deepening A*
│       ├── hill_climbing.py  # Leo đồi (Simple, Steepest Ascent, Stochastic...)
│       ├── simulated_annealing.py # Luyện kim giả lập
│       ├── beam_search.py    # Tìm kiếm chùm tia
│       ├── belief_dfs.py     # Tìm kiếm trên trạng thái niềm tin (Sensorless)
│       ├── and_or_search.py  # Tìm kiếm quan sát một phần / cây AND-OR
│       └── multi_dfs.py      # Các thuật toán hỗ trợ khác
│
├── map brvt cũ/              # Ứng dụng Thỏa mãn ràng buộc (CSP) - Tô màu bản đồ
│   ├── main.py               # Điểm khởi chạy ứng dụng GUI Tô màu bản đồ BRVT
│   ├── frontend/             # Giao diện hiển thị bản đồ và trạng thái tô màu
│   └── backend/              # Các thuật toán xử lý CSP
│       ├── pure_backtracking.py  # Quay lui thuần túy
│       ├── csp_backtracking.py   # Quay lui nâng cao
│       ├── forward_checking.py   # Kiểm tra trước (Forward Checking)
│       ├── ac3.py                # Thuật toán AC-3 (Arc Consistency)
│       ├── min_conflicts.py      # Thuật toán Min-Conflicts (Local search cho CSP)
│       ├── heuristics.py         # Các heuristic MRV, Degree Heuristic, LCV
│       └── config.py             # Cấu hình đồ thị bản đồ và dữ liệu
│
├── Caro/                     # Ứng dụng Trò chơi đối kháng Cờ Caro
│   ├── main.py               # Điểm khởi chạy trò chơi Cờ Caro
│   ├── frontend/             # Giao diện bàn cờ và tương tác người chơi
│   └── backend/              # Thuật toán trí tuệ nhân tạo đối kháng
│       ├── minimax.py        # Thuật toán Minimax
│       ├── alphabeta.py      # Cắt tỉa Alpha-Beta Pruning
│       ├── expectimax.py     # Thuật toán Expectimax (cho môi trường ngẫu nhiên)
│       ├── ai_solver.py      # Bộ giải AI tích hợp hàm đánh giá bàn cờ
│       └── board.py          # Xử lý logic bàn cờ và trạng thái thắng/thua
│
└── README.md                 # Tài liệu hướng dẫn và chi tiết thuật toán (File này)
```

---

## Chi tiết các Nhóm Thuật Toán

Nội dung bên dưới trình bày **6 nhóm thuật toán lớn** được triển khai trong dự án. Với mỗi thuật toán con trong các nhóm, tài liệu cung cấp **mã giả (pseudo-code)**, **ưu điểm**, **độ phức tạp thời gian** và **độ phức tạp không gian**.

---

### 1. Nhóm Thuật Toán Tìm Kiếm Mù (Uninformed Search Algorithms)

Các thuật toán tìm kiếm mù duyệt qua không gian trạng thái mà không sử dụng thêm thông tin ước lượng (heuristic) về khoảng cách tới mục tiêu.

#### 1.1. BFS (Breadth-First Search - Tìm kiếm theo chiều rộng)
* **Mã giả (Pseudo-code):**
  ```python
  def BFS(problem):
      node = Node(state=problem.initial_state)
      if problem.is_goal(node.state): return node
      frontier = Queue([node]) # Hàng đợi FIFO
      explored = Set()
      while not frontier.is_empty():
          node = frontier.pop()
          explored.add(node.state)
          for action in problem.actions(node.state):
              child = child_node(problem, node, action)
              if child.state not in explored and child.state not in frontier:
                  if problem.is_goal(child.state): return child
                  frontier.push(child)
      return None
  ```
* **Ưu điểm:** Đảm bảo tìm thấy lời giải (Complete) và tối ưu (Optimal) nếu chi phí mỗi bước đi là bằng nhau.
* **Độ phức tạp thời gian:** $O(b^d)$ (với $b$ là hệ số nhánh, $d$ là độ sâu của lời giải nông nhất).
* **Độ phức tạp không gian:** $O(b^d)$ (lưu trữ tất cả các nút trong tập frontier và explored vào bộ nhớ).

#### 1.2. DFS (Depth-First Search - Tìm kiếm theo chiều sâu)
* **Mã giả (Pseudo-code):**
  ```python
  def DFS(problem):
      frontier = Stack([Node(state=problem.initial_state)]) # Ngăn xếp LIFO
      explored = Set()
      while not frontier.is_empty():
          node = frontier.pop()
          if problem.is_goal(node.state): return node
          if node.state not in explored:
              explored.add(node.state)
              for action in problem.actions(node.state):
                  frontier.push(child_node(problem, node, action))
      return None
  ```
* **Ưu điểm:** Cực kỳ tiết kiệm bộ nhớ so với BFS khi không gian trạng thái rộng nhưng không quá sâu.
* **Độ phức tạp thời gian:** $O(b^m)$ (với $m$ là độ sâu tối đa của cây tìm kiếm).
* **Độ phức tạp không gian:** $O(b \cdot m)$ (chỉ cần lưu trữ đường đi từ gốc đến nút hiện tại cùng các nút anh em).

#### 1.3. UCS (Uniform Cost Search - Tìm kiếm chi phí đồng nhất)
* **Mã giả (Pseudo-code):**
  ```python
  def UCS(problem):
      node = Node(state=problem.initial_state)
      frontier = PriorityQueue(node, key=lambda n: n.path_cost) # Hàng đợi ưu tiên theo chi phí g(n)
      explored = Set()
      while not frontier.is_empty():
          node = frontier.pop() # Lấy nút có g(n) nhỏ nhất
          if problem.is_goal(node.state): return node
          explored.add(node.state)
          for action in problem.actions(node.state):
              child = child_node(problem, node, action)
              if child.state not in explored and child.state not in frontier:
                  frontier.push(child)
              elif child.state in frontier và child.path_cost < frontier[child.state].path_cost:
                  frontier.update(child)
      return None
  ```
* **Ưu điểm:** Đảm bảo đầy đủ và luôn tìm ra đường đi có tổng chi phí $g(n)$ nhỏ nhất ngay cả khi chi phí giữa các bước không bằng nhau.
* **Độ phức tạp thời gian:** $O(b^{1 + \lfloor C^* / \epsilon \rfloor})$ (với $C^*$ là chi phí lời giải tối ưu, $\epsilon$ là chi phí bước nhỏ nhất).
* **Độ phức tạp không gian:** $O(b^{1 + \lfloor C^* / \epsilon \rfloor})$ (lưu trữ mọi nút trong vùng biên).

#### 1.4. IDS (Iterative Deepening Search - Tìm kiếm sâu dần)
* **Mã giả (Pseudo-code):**
  ```python
  def IDS(problem):
      for depth in range(0, infinity):
          result = Depth_Limited_Search(problem, depth)
          if result != cutoff: return result

  def Depth_Limited_Search(node, problem, limit):
      if problem.is_goal(node.state): return node
      if limit == 0: return cutoff
      cutoff_occurred = False
      for action in problem.actions(node.state):
          child = child_node(problem, node, action)
          result = Depth_Limited_Search(child, problem, limit - 1)
          if result == cutoff: cutoff_occurred = True
          elif result != None: return result
      return cutoff if cutoff_occurred else None
  ```
* **Ưu điểm:** Kết hợp hoàn hảo ưu điểm của BFS (đầy đủ và tối ưu) với ưu điểm của DFS (tiết kiệm bộ nhớ).
* **Độ phức tạp thời gian:** $O(b^d)$ (chi phí ở tầng cuối $d$ chiếm đa số).
* **Độ phức tạp không gian:** $O(b \cdot d)$ (không gian tuyến tính).

---

### 2. Nhóm Thuật Toán Tìm Kiếm Thông Tin / Heuristic (Informed Search Algorithms)

Sử dụng hàm đánh giá ước lượng $h(n)$ để dẫn đường tìm kiếm thông minh hơn về phía mục tiêu.

#### 2.1. Greedy Best-First Search (Tìm kiếm tham lam)
* **Mã giả (Pseudo-code):**
  ```python
  def Greedy_Best_First(problem):
      node = Node(state=problem.initial_state)
      frontier = PriorityQueue(node, key=lambda n: heuristic(n.state)) # Sắp xếp theo h(n)
      explored = Set()
      while not frontier.is_empty():
          node = frontier.pop()
          if problem.is_goal(node.state): return node
          explored.add(node.state)
          for action in problem.actions(node.state):
              child = child_node(problem, node, action)
              if child.state not in explored and child.state not in frontier:
                  frontier.push(child)
      return None
  ```
* **Ưu điểm:** Tốc độ thực thi rất nhanh, tiếp cận mục tiêu trực tiếp nếu có hàm Heuristic chất lượng cao.
* **Độ phức tạp thời gian:** $O(b^m)$ trong trường hợp xấu nhất, nhưng trong thực tế nhanh hơn nhiều tùy thuộc hàm $h(n)$.
* **Độ phức tạp không gian:** $O(b^m)$ (lưu tất cả các nút mở rộng trong bộ nhớ).

#### 2.2. A* Search (Tìm kiếm A*)
* **Mã giả (Pseudo-code):**
  ```python
  def A_Star(problem):
      node = Node(state=problem.initial_state)
      # Sắp xếp theo hàm f(n) = g(n) + h(n)
      frontier = PriorityQueue(node, key=lambda n: n.path_cost + heuristic(n.state))
      explored = Set()
      while not frontier.is_empty():
          node = frontier.pop()
          if problem.is_goal(node.state): return node
          explored.add(node.state)
          for action in problem.actions(node.state):
              child = child_node(problem, node, action)
              if child.state not in explored and child.state not in frontier:
                  frontier.push(child)
              elif child.state in frontier và child.f < frontier[child.state].f:
                  frontier.update(child)
      return None
  ```
* **Ưu điểm:** Là thuật toán tìm kiếm tối ưu và đầy đủ nhất nếu hàm Heuristic là chấp nhận được (Admissible) và nhất quán (Consistent).
* **Độ phức tạp thời gian:** $O(b^d)$ (tăng theo hàm mũ phụ thuộc vào độ chính xác của $h(n)$).
* **Độ phức tạp không gian:** $O(b^d)$ (phải lưu toàn bộ các nút trong bộ nhớ).

#### 2.3. IDA* (Iterative Deepening A* - A* sâu dần)
* **Mã giả (Pseudo-code):**
  ```python
  def IDA_Star(problem):
      bound = heuristic(problem.initial_state)
      path = [Node(state=problem.initial_state)]
      while True:
          t = Search(path, 0, bound, problem)
          if t == FOUND: return path[-1]
          if t == infinity: return None
          bound = t

  def Search(path, g, bound, problem):
      node = path[-1]
      f = g + heuristic(node.state)
      if f > bound: return f
      if problem.is_goal(node.state): return FOUND
      min_val = infinity
      for action in problem.actions(node.state):
          child = child_node(problem, node, action)
          if child not in path:
              path.append(child)
              t = Search(path, g + child.step_cost, bound, problem)
              if t == FOUND: return FOUND
              if t < min_val: min_val = t
              path.pop()
      return min_val
  ```
* **Ưu điểm:** Khắc phục nhược điểm tốn bộ nhớ của A* bằng cách kết hợp tư tưởng sâu dần với ngưỡng chi phí $f(n)$.
* **Độ phức tạp thời gian:** $O(b^d)$
* **Độ phức tạp không gian:** $O(b \cdot d)$ (không gian tuyến tính).

---

### 3. Nhóm Thuật Toán Tìm Kiếm Cục Bộ (Local Search Algorithms)

Tập trung vào việc tối ưu hóa trạng thái hiện tại thay vì lưu trữ đường đi từ trạng thái khởi tạo. Thích hợp cho các bài toán tối ưu hóa không gian lớn.

#### 3.1. Hill Climbing (Thuật toán Leo đồi)
* **Mã giả (Steepest-Ascent Hill Climbing):**
  ```python
  def Hill_Climbing(problem):
      current = problem.initial_state
      while True:
          neighbors = problem.neighbors(current)
          best_neighbor = max(neighbors, key=lambda n: evaluation(n))
          if evaluation(best_neighbor) <= evaluation(current):
              return current # Dừng lại khi không còn láng giềng nào tốt hơn
          current = best_neighbor
  ```
* **Ưu điểm:** Không tốn bộ nhớ, thời gian tính toán nhanh, đơn giản khi triển khai.
* **Độ phức tạp thời gian:** Phụ thuộc vào không gian trạng thái; dễ bị mắc kẹt tại các đỉnh cực trị địa phương (Local Maxima) hoặc vùng bằng phẳng (Plateau).
* **Độ phức tạp không gian:** $O(1)$ (hằng số, chỉ lưu trạng thái hiện tại).

#### 3.2. Simulated Annealing (Luyện kim giả lập)
* **Mã giả (Pseudo-code):**
  ```python
  def Simulated_Annealing(problem, schedule):
      current = problem.initial_state
      for t in range(1, infinity):
          T = schedule(t) # Giảm nhiệt độ theo thời gian
          if T == 0: return current
          next_state = random_choice(problem.neighbors(current))
          delta_E = evaluation(next_state) - evaluation(current)
          if delta_E > 0:
              current = next_state
          else:
              # Chấp nhận trạng thái xấu hơn với xác suất e^(delta_E / T)
              if random_probability() < e**(delta_E / T):
                  current = next_state
  ```
* **Ưu điểm:** Có khả năng thoát khỏi cực trị địa phương nhờ cơ chế chấp nhận nước đi xấu hơn với xác suất giảm dần theo nhiệt độ.
* **Độ phức tạp thời gian:** Phụ thuộc vào lịch trình hạ nhiệt (cooling schedule), có thể đạt được tối ưu toàn cục nếu hạ nhiệt đủ chậm.
* **Độ phức tạp không gian:** $O(1)$.

#### 3.3. Beam Search (Tìm kiếm chùm tia / Local Beam Search)
* **Mã giả (Pseudo-code):**
  ```python
  def Local_Beam_Search(problem, k):
      current_states = [problem.initial_state for _ in range(k)]
      while True:
          candidates = []
          for state in current_states:
              if problem.is_goal(state): return state
              candidates.extend(problem.neighbors(state))
          # Chọn k trạng thái tốt nhất từ tất cả các láng giềng sinh ra
          current_states = select_top_k(candidates, k, key=lambda s: evaluation(s))
  ```
* **Ưu điểm:** Đa dạng hóa hướng tìm kiếm bằng cách giữ song song $k$ trạng thái tốt nhất, truyền thông tin giữa các luồng tìm kiếm để tránh cực trị địa phương.
* **Độ phức tạp thời gian:** $O(k \cdot b \cdot m)$ (với $m$ là số bước tối đa).
* **Độ phức tạp không gian:** $O(k \cdot b)$.

---

### 4. Nhóm Thuật Toán Tìm Kiếm Trong Môi Trường Phức Tạp (Search in Complex / Non-Observable Environments)

Giải quyết bài toán khi robot không có cảm biến (mù hoàn toàn) hoặc chỉ quan sát được một phần môi trường (Partial Observation) bằng cách tìm kiếm trên không gian trạng thái niềm tin (Belief States).

#### 4.1. Sensorless Search (Tìm kiếm không cảm biến - Belief DFS/BFS)
* **Mã giả (Sử dụng Belief DFS/BFS):**
  ```python
  def Sensorless_Search(problem):
      start_belief = problem.initial_belief_state # Tập hợp tất cả các trạng thái thế giới có thể
      frontier = Stack([Node(start_belief)]) # Hoặc Queue cho BFS
      explored = Set()
      while not frontier.is_empty():
          node = frontier.pop()
          if problem.is_goal(node.belief_state): return node.path()
          explored.add(node.belief_state)
          for action in problem.actions:
              next_belief = predict_belief(node.belief_state, action)
              if next_belief not in explored and next_belief not in frontier:
                  frontier.push(Node(next_belief, parent=node, action=action))
  ```
* **Ưu điểm:** Tìm ra kế hoạch hành động đảm bảo đưa hệ thống về trạng thái mục tiêu dù không có bất kỳ cảm biến nào để xác định vị trí hiện tại.
* **Độ phức tạp thời gian:** $O(b^P)$ (với $P$ là số trạng thái niềm tin, trong trường hợp xấu nhất $P = 2^N$ với $N$ là số trạng thái vật lý).
* **Độ phức tạp không gian:** $O(2^N)$ (để lưu trữ các trạng thái niềm tin).

#### 4.2. Partial Observation Search (Tìm kiếm quan sát một phần / AND-OR Search)
* **Mã giả (Pseudo-code Cây AND-OR):**
  ```python
  def AND_OR_Graph_Search(problem):
      return OR_Search(problem.initial_state, problem, [])

  def OR_Search(state, problem, path):
      if problem.is_goal(state): return empty_plan
      if state in path: return failure
      for action in problem.actions(state):
          plan = AND_Search(results(state, action), problem, [state] + path)
          if plan != failure: return [action] + plan
      return failure

  def AND_Search(states, problem, path):
      plan = {}
      for s_i in states:
          plan_i = OR_Search(s_i, problem, path)
          if plan_i == failure: return failure
          plan[s_i] = plan_i
      return plan
  ```
* **Ưu điểm:** Xây dựng kế hoạch dự phòng (Contingency Plan) giúp Agent phản ứng linh hoạt dựa trên dữ liệu nhận được từ cảm biến tại mỗi bước.
* **Độ phức tạp thời gian:** Lũy thừa $O(2^N)$ trong trường hợp xấu nhất, nhưng trong thực tế nhanh hơn nhiều nhờ dữ liệu cảm biến thu hẹp trạng thái niềm tin.
* **Độ phức tạp không gian:** $O(2^N)$.

---

### 5. Nhóm Thuật Toán Thỏa Mãn Ràng Buộc - CSP (Constraint Satisfaction Problems)

Giải quyết các bài toán định cấu hình và phân bổ tài nguyên (như Tô màu bản đồ) bằng cách gán giá trị cho các biến sao cho thỏa mãn tất cả các ràng buộc.

#### 5.1. Backtracking Search (Quay lui thuần túy)
* **Mã giả (Pseudo-code):**
  ```python
  def Backtracking_Search(csp):
      return Backtrack({}, csp)

  def Backtrack(assignment, csp):
      if len(assignment) == len(csp.variables): return assignment
      var = select_unassigned_variable(csp, assignment)
      for value in order_domain_values(var, assignment, csp):
          if is_consistent(var, value, assignment, csp):
              assignment[var] = value
              result = Backtrack(assignment, csp)
              if result != failure: return result
              del assignment[var] # Quay lui (Backtrack)
      return failure
  ```
* **Ưu điểm:** Thuật toán nền tảng đơn giản, đảm bảo tìm thấy lời giải hợp lệ nếu tồn tại.
* **Độ phức tạp thời gian:** $O(d^n)$ (với $n$ là số biến và $d$ là kích thước miền giá trị lớn nhất).
* **Độ phức tạp không gian:** $O(n)$ (độ sâu đệ quy tối đa bằng số lượng biến).

#### 5.2. Forward Checking (Kiểm tra trước)
* **Mã giả (Pseudo-code):**
  ```python
  def Forward_Checking_Backtrack(assignment, csp):
      if len(assignment) == len(csp.variables): return assignment
      var = select_unassigned_variable(csp, assignment)
      for value in order_domain_values(var, assignment, csp):
          if is_consistent(var, value, assignment, csp):
              assignment[var] = value
              saved_domains = copy_domains(csp)
              # Loại bỏ các giá trị không hợp lệ ở các biến láng giềng chưa gán
              if keep_consistent(var, value, csp, assignment):
                  result = Forward_Checking_Backtrack(assignment, csp)
                  if result != failure: return result
              restore_domains(csp, saved_domains)
              del assignment[var]
      return failure
  ```
* **Ưu điểm:** Phát hiện sớm các nhánh cụt ngay khi gán giá trị cho một biến, cắt tỉa không gian tìm kiếm hiệu quả hơn nhiều so với Backtracking thuần túy.
* **Độ phức tạp thời gian:** Nhỏ hơn đáng kể so với $O(d^n)$ trong thực tế.
* **Độ phức tạp không gian:** $O(n \cdot d)$ (lưu vết miền giá trị của các biến tại mỗi cấp độ sâu).

#### 5.3. AC-3 (Arc Consistency Algorithm #3) / Min-Conflicts
* **Mã giả (AC-3 Algorithm):**
  ```python
  def AC3(csp):
      queue = Queue(all_arcs_in_csp)
      while not queue.is_empty():
          (Xi, Xj) = queue.pop()
          if Revise(csp, Xi, Xj):
              if len(csp.domains[Xi]) == 0: return False
              for Xk in csp.neighbors[Xi] - {Xj}:
                  queue.push((Xk, Xi))
      return True

  def Revise(csp, Xi, Xj):
      revised = False
      for x in csp.domains[Xi]:
          if not satisfies_constraint(x, y) for any y in csp.domains[Xj]:
              csp.domains[Xi].remove(x)
              revised = True
      return revised
  ```
* **Ưu điểm:** Duy trì tính nhất quán cung (Arc Consistency) trên toàn bộ đồ thị ràng buộc, loại bỏ tối đa các giá trị thừa trước hoặc trong quá trình tìm kiếm.
* **Độ phức tạp thời gian:** $O(c \cdot d^3)$ (với $c$ là số lượng cung/cặp ràng buộc và $d$ là kích thước miền giá trị lớn nhất).
* **Độ phức tạp không gian:** $O(c)$ hoặc $O(n \cdot d)$.

---

### 6. Nhóm Thuật Toán Đối Kháng (Adversarial Search / Games)

Được áp dụng trong các trò chơi hai người chơi đối kháng (như Cờ Caro / Tic-Tac-Toe), nơi mỗi bên nỗ lực tối đa hóa điểm số của mình và tối thiểu hóa điểm số của đối thủ.

#### 6.1. Minimax Algorithm (Thuật toán Minimax)
* **Mã giả (Pseudo-code):**
  ```python
  def Minimax_Decision(state):
      return argmax(Actions(state), key=lambda a: Min_Value(Result(state, a)))

  def Max_Value(state):
      if Terminal_Test(state): return Utility(state)
      v = -infinity
      for a in Actions(state):
          v = max(v, Min_Value(Result(state, a)))
      return v

  def Min_Value(state):
      if Terminal_Test(state): return Utility(state)
      v = +infinity
      for a in Actions(state):
          v = min(v, Max_Value(Result(state, a)))
      return v
  ```
* **Ưu điểm:** Đưa ra nước đi tối ưu tuyệt đối giả định đối thủ cũng thi đấu tối ưu theo lý thuyết trò chơi.
* **Độ phức tạp thời gian:** $O(b^m)$ (với $b$ là hệ số nhánh nước đi và $m$ là độ sâu tối đa của cây trò chơi).
* **Độ phức tạp không gian:** $O(b \cdot m)$ (tìm kiếm theo chiều sâu).

#### 6.2. Alpha-Beta Pruning (Cắt tỉa Alpha-Beta)
* **Mã giả (Pseudo-code):**
  ```python
  def Alpha_Beta_Search(state):
      v = Max_Value(state, -infinity, +infinity)
      return action_with_value(v)

  def Max_Value(state, alpha, beta):
      if Terminal_Test(state): return Utility(state)
      v = -infinity
      for a in Actions(state):
          v = max(v, Min_Value(Result(state, a), alpha, beta))
          if v >= beta: return v # Cắt tỉa nhánh Beta
          alpha = max(alpha, v)
      return v

  def Min_Value(state, alpha, beta):
      if Terminal_Test(state): return Utility(state)
      v = +infinity
      for a in Actions(state):
          v = min(v, Max_Value(Result(state, a), alpha, beta))
          if v <= alpha: return v # Cắt tỉa nhánh Alpha
          beta = min(beta, v)
      return v
  ```
* **Ưu điểm:** Giảm số lượng nút cần duyệt bằng cách bỏ qua các nhánh không ảnh hưởng đến quyết định cuối cùng mà vẫn thu được nước đi hoàn toàn tương đương Minimax.
* **Độ phức tạp thời gian:** Trong trường hợp thứ tự sắp xếp nước đi tốt nhất, độ phức tạp đạt $O(b^{m/2})$ (cho phép duyệt sâu gấp đôi Minimax).
* **Độ phức tạp không gian:** $O(b \cdot m)$.

#### 6.3. Expectimax Algorithm (Thuật toán Expectimax)
* **Mã giả (Pseudo-code):**
  ```python
  def Expectimax_Decision(state):
      return argmax(Actions(state), key=lambda a: Expect_Value(Result(state, a)))

  def Expect_Value(state):
      if Terminal_Test(state): return Utility(state)
      v = 0
      actions = Actions(state)
      prob = 1.0 / len(actions) # Giả định xác suất phân bố đều của đối thủ
      for a in actions:
          v += prob * Max_Value(Result(state, a))
      return v
  ```
* **Ưu điểm:** Hoạt động vượt trội hơn Minimax khi đối thủ không chơi hoàn hảo mà có tính ngẫu nhiên hoặc khi môi trường mang yếu tố xác suất.
* **Độ phức tạp thời gian:** $O(b^m)$.
* **Độ phức tạp không gian:** $O(b \cdot m)$.

---

## Hướng dẫn chạy các ứng dụng trực quan (GUI)

Để khởi chạy các module giao diện đồ họa trong dự án, di chuyển vào thư mục tương ứng và thực hiện lệnh:

1. **Ứng dụng Robot Hút Bụi:**
   ```bash
   cd "Máy hút bụi"
   python main.py
   ```

2. **Ứng dụng Tô màu bản đồ BRVT (CSP):**
   ```bash
   cd "map brvt cũ"
   python main.py
   ```

3. **Trò chơi Cờ Caro đối kháng (AI):**
   ```bash
   cd Caro
   python main.py
   ```
