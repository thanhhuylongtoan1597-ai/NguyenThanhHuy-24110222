import tkinter as tk
from tkinter import scrolledtext, messagebox
import random
import backend

class VacuumSimulationApp:
    # 1. KHỔI TẠO ỨNG DỤNG & TRẠNG THÁI BAN ĐẦU
    
    # Hàm khởi tạo cấu hình cửa sổ và các biến trạng thái ban đầu
    def __init__(self, root):
        self.root = root
        self.root.title("Chương Trình Mô Phỏng Robot Hút Bụi AI")
        self.root.geometry("1150x750")
        self.root.configure(bg="#f4f4f4")
        self.root.resizable(False, False)

        self.robot_row = 0
        self.robot_col = 1
        self.matrix = [[1, 0, 0], [0, 1, 0], [0, 0, 1]] 
        self.is_running = False

        self.anim_actions = []
        self.anim_step_index = 0
        self.anim_frame_index = 0
        self.anim_robot_r = 0
        self.anim_robot_c = 0

        self.setup_layout()
        self.draw_all()

    # 2. THIẾT LẬP BỐ CỤC GIAO DIỆN (LAYOUT)
    
    # Hàm xây dựng bố cục các khung (frames), nút bấm và phân chia cột giao diện
    def setup_layout(self):
        #  CỘT TRÁI: THUẬT TOÁN & THIẾT LẬP 
        left_frame = tk.Frame(self.root, bg="#f4f4f4", width=240, height=720)
        left_frame.pack(side="left", fill="both", expand=False, padx=15, pady=15)
        left_frame.pack_propagate(False)

        tk.Label(left_frame, text="THUẬT TOÁN", font=("Helvetica", 12, "bold"), bg="#f4f4f4").pack(pady=(0, 10))

        # Cấu hình phong cách thanh cuộn tối giản giống hệ thống
        from tkinter import ttk
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Vertical.TScrollbar", gripcount=0, background="#c1c1c1", troughcolor="#f4f4f4", bordercolor="#f4f4f4", lightcolor="#f4f4f4", darkcolor="#f4f4f4", arrowsize=0)

        # Khung container và vùng cuộn tối giản cho danh sách thuật toán
        algo_container = tk.Frame(left_frame, bg="#f4f4f4", height=380)
        algo_container.pack(fill="x", expand=False)
        algo_container.pack_propagate(False)

        algo_canvas = tk.Canvas(algo_container, bg="#f4f4f4", highlightthickness=0, bd=0)
        algo_scrollbar = ttk.Scrollbar(algo_container, orient="vertical", command=algo_canvas.yview, style="Vertical.TScrollbar")

        scrollable_frame = tk.Frame(algo_canvas, bg="#f4f4f4")
        scrollable_frame.bind("<Configure>", lambda e: algo_canvas.configure(scrollregion=algo_canvas.bbox("all")))

        algo_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=215)
        algo_canvas.configure(yscrollcommand=algo_scrollbar.set)

        algo_canvas.pack(side="left", fill="both", expand=True)
        algo_scrollbar.pack(side="right", fill="y")

        algo_canvas.bind_all("<MouseWheel>", lambda e: algo_canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))

        # Các nút bấm thuật toán được giữ nguyên code, chỉ chuyển sang đặt vào scrollable_frame
        self.btn_bfs1 = tk.Button(scrollable_frame, text="BFS 1", font=("Helvetica", 10), bg="#a9a9a9", fg="#000000", relief="groove", bd=1, height=2, command=lambda: self.start_search("BFS 1"))
        self.btn_bfs1.pack(fill="x", pady=4)

        self.btn_bfs2 = tk.Button(scrollable_frame, text="BFS 2", font=("Helvetica", 10), bg="#a9a9a9", fg="#000000", relief="groove", bd=1, height=2, command=lambda: self.start_search("BFS 2"))
        self.btn_bfs2.pack(fill="x", pady=4)

        self.btn_dfs1 = tk.Button(scrollable_frame, text="DFS 1 ", font=("Helvetica", 10), bg="#a9a9a9", fg="#000000", relief="groove", bd=1, height=2, command=lambda: self.start_search("DFS 1"))
        self.btn_dfs1.pack(fill="x", pady=4)

        self.btn_dfs2 = tk.Button(scrollable_frame, text="DFS 2", font=("Helvetica", 10), bg="#a9a9a9", fg="#000000", relief="groove", bd=1, height=2, command=lambda: self.start_search("DFS 2"))
        self.btn_dfs2.pack(fill="x", pady=4)

        self.btn_ucs = tk.Button(scrollable_frame, text="UCS", font=("Helvetica", 10), bg="#a9a9a9", fg="#000000", relief="groove", bd=1, height=2, command=lambda: self.start_search("UCS"))
        self.btn_ucs.pack(fill="x", pady=4)

        self.btn_ids_1 = tk.Button(scrollable_frame, text="IDS1", font=("Helvetica", 10), bg="#a9a9a9", fg="#000000", relief="groove", bd=1, height=2, command=lambda: self.start_search("IDS1"))
        self.btn_ids_1.pack(fill="x", pady=4)

        self.btn_ids_2 = tk.Button(scrollable_frame, text="IDS2", font=("Helvetica", 10), bg="#a9a9a9", fg="#000000", relief="groove", bd=1, height=2, command=lambda: self.start_search("IDS2"))
        self.btn_ids_2.pack(fill="x", pady=4)

        self.btn_greedy = tk.Button(scrollable_frame, text="Greedy Search", font=("Helvetica", 10), bg="#a9a9a9", fg="#000000", relief="groove", bd=1, height=2, command=lambda: self.start_search("Greedy"))
        self.btn_greedy.pack(fill="x", pady=4)

        self.btn_astar = tk.Button(scrollable_frame, text="A* Search", font=("Helvetica", 10), bg="#a9a9a9", fg="#000000", relief="groove", bd=1, height=2, command=lambda: self.start_search("A*"))
        self.btn_astar.pack(fill="x", pady=4)
        
        self.btn_idastar = tk.Button(scrollable_frame, text="IDA* Search", font=("Helvetica", 10), bg="#a9a9a9", fg="#000000", relief="groove", bd=1, height=2, command=lambda: self.start_search("IDA*"))
        self.btn_idastar.pack(fill="x", pady=4)

        self.btn_simple_hc = tk.Button(scrollable_frame, text="Simple Hill Climbing", font=("Helvetica", 10), bg="#a9a9a9", fg="#000000", relief="groove", bd=1, height=2, command=lambda: self.start_search("Simple HC"))
        self.btn_simple_hc.pack(fill="x", pady=4)

        self.btn_steepest_hc = tk.Button(scrollable_frame, text="Steepest Hill Climbing", font=("Helvetica", 10), bg="#a9a9a9", fg="#000000", relief="groove", bd=1, height=2, command=lambda: self.start_search("Steepest HC"))
        self.btn_steepest_hc.pack(fill="x", pady=4)

        self.btn_stochastic_hc = tk.Button(scrollable_frame, text="Stochastic Hill Climbing", font=("Helvetica", 10), bg="#a9a9a9", fg="#000000", relief="groove", bd=1, height=2, command=lambda: self.start_search("Stochastic HC"))
        self.btn_stochastic_hc.pack(fill="x", pady=4)

        self.btn_rand_restart_hc = tk.Button(scrollable_frame, text="Random Restart HC", font=("Helvetica", 10), bg="#a9a9a9", command=lambda: self.start_search("Random Restart HC"))
        self.btn_rand_restart_hc.pack(fill="x", pady=4)

        self.btn_beam_search = tk.Button(scrollable_frame, text="Local Beam Search", font=("Helvetica", 10), bg="#a9a9a9", command=lambda: self.start_search("Local Beam Search"))
        self.btn_beam_search.pack(fill="x", pady=4)

        self.btn_simulated_annealing = tk.Button(scrollable_frame, text="Simulated Annealing", font=("Helvetica", 10), bg="#a9a9a9", command=lambda: self.start_search("Simulated Annealing"))
        self.btn_simulated_annealing.pack(fill="x", pady=4)
        
        self.btn_multi_dfs = tk.Button(scrollable_frame, text="Multi-State DFS", font=("Helvetica", 10), bg="#a9a9a9", fg="#000000", relief="groove", bd=1, height=2, command=lambda: self.start_search("Multi DFS"))
        self.btn_multi_dfs.pack(fill="x", pady=4)

        self.btn_belief_dfs = tk.Button(scrollable_frame, text="Belief State DFS", font=("Helvetica", 10), bg="#a9a9a9", fg="#000000", relief="groove", bd=1, height=2, command=lambda: self.start_search("Belief DFS"))
        self.btn_belief_dfs.pack(fill="x", pady=4)

        self.btn_and_or_search = tk.Button(scrollable_frame, text="AND-OR Graph Search", font=("Helvetica", 10), bg="#a9a9a9", fg="#000000", relief="groove", bd=1, height=2, command=lambda: self.start_search("AND-OR"))
        self.btn_and_or_search.pack(fill="x", pady=4)

        pos_frame = tk.LabelFrame(left_frame, text="ĐẶT VỊ TRÍ BAN ĐẦU", font=("Helvetica", 9, "bold"), bg="#f4f4f4", fg="red", padx=5, pady=5)
        pos_frame.pack(fill="x", pady=15)

        tk.Label(pos_frame, text="Hàng (0-2):", bg="#f4f4f4").grid(row=0, column=0, padx=2, pady=5, sticky="w")
        self.ent_row = tk.Entry(pos_frame, width=8, justify="center")
        self.ent_row.insert(0, str(self.robot_row))
        self.ent_row.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(pos_frame, text="Cột (0-2):", bg="#f4f4f4").grid(row=1, column=0, padx=2, pady=5, sticky="w")
        self.ent_col = tk.Entry(pos_frame, width=8, justify="center")
        self.ent_col.insert(0, str(self.robot_col))
        self.ent_col.grid(row=1, column=1, padx=5, pady=5)

        btn_update = tk.Button(pos_frame, text="Cập Nhật", font=("Helvetica", 9, "bold"), bg="#e7e7e7", command=self.update_initial_position)
        btn_update.grid(row=2, column=0, columnspan=2, sticky="ew", pady=5)
        
        self.btn_reset = tk.Button(left_frame, text="Reset Bàn Cờ\n(Random)", font=("Helvetica", 10, "bold"), bg="#f2dede", fg="#a94442", relief="groove", bd=1, height=2, command=self.reset_random)
        self.btn_reset.pack(fill="x", pady=10)

        # CỘT GIỮA: TRỰC QUAN LƯỚI & ĐƯỜNG ĐI
        middle_frame = tk.Frame(self.root, bg="#f4f4f4", width=420, height=720)
        middle_frame.pack(side="left", fill="both", expand=False, padx=10, pady=15)
        middle_frame.pack_propagate(False)

        self.canvas = tk.Canvas(middle_frame, width=390, height=390, bg="white", highlightthickness=1, highlightbackground="#bdc3c7")
        self.canvas.pack(pady=5)
        self.canvas.bind("<Button-1>", self.on_canvas_click)

        tk.Label(middle_frame, text="ĐƯỜNG ĐI TỐT NHẤT:", font=("Helvetica", 11, "bold"), bg="#f4f4f4").pack(anchor="w", pady=(15, 5))
        self.lbl_best_path = tk.Label(middle_frame, text="Chua chay thuat toan", font=("Consolas", 11), bg="#ffffff", fg="#31708f", relief="solid", bd=1, padx=10, pady=15, height=3, wraplength=360, anchor="nw", justify="left")
        self.lbl_best_path.pack(fill="x", pady=5)

        # CỘT PHẢI: THỐNG KÊ & LỊCH SỬ
        right_frame = tk.Frame(self.root, bg="#f4f4f4")
        right_frame.pack(side="left", fill="both", expand=True, padx=15, pady=15)

        tk.Label(right_frame, text="THỐNG KÊ & LỊCH SỬ", font=("Helvetica", 13, "bold"), bg="#f4f4f4", fg="#2c3e50").pack(anchor="w", pady=(0, 10))

        db_frame = tk.LabelFrame(right_frame, text="Bảng Thống Kê (Dashboard)", font=("Helvetica", 10, "bold"), bg="#f4f4f4", fg="#34495e", padx=15, pady=10)
        db_frame.pack(fill="x", pady=5)

        self.lbl_path_cost = tk.Label(db_frame, text="Số bước đi (Path Cost): 0", font=("Helvetica", 10), bg="#f4f4f4", anchor="w")
        self.lbl_path_cost.pack(fill="x", pady=3)

        self.lbl_nodes = tk.Label(db_frame, text="Số Node đã duyệt: 0", font=("Helvetica", 10), bg="#f4f4f4", anchor="w")
        self.lbl_nodes.pack(fill="x", pady=3)

        self.lbl_time = tk.Label(db_frame, text="Thời gian chạy: 0.00 ms", font=("Helvetica", 10), bg="#f4f4f4", anchor="w")
        self.lbl_time.pack(fill="x", pady=3)

        log_frame = tk.LabelFrame(right_frame, text="Console Log (Lịch sử hành động)", font=("Helvetica", 10, "bold"), bg="#f4f4f4", fg="#34495e", padx=10, pady=10)
        log_frame.pack(fill="both", expand=True, pady=10)

        self.log_text = scrolledtext.ScrolledText(log_frame, font=("Consolas", 10), bg="#2c3e50", fg="#ecf0f1", wrap="word")
        self.log_text.pack(fill="both", expand=True)
        self.log_text.insert(tk.END, "Hệ thống sẵn sàng. Nhấn nút để bắt đầu giải thuật.\n")
        
    # 3. XỬ LÝ ĐỒ HỌA & CANVAS TƯƠNG TÁC
    
    # Hàm vẽ toàn bộ lưới ô vuông (Xanh/Đỏ) và vẽ Robot lên màn hình Canvas
    def draw_all(self, px=None, py=None):
        self.canvas.delete("all")
        cs = 130 

        for r in range(3):       
            for c in range(3):   
                x1, y1 = c * cs, r * cs
                x2, y2 = x1 + cs, y1 + cs

                if self.matrix[r][c] == 1:
                    bg_color = "#f5c6cb" 
                    text_val = "1"       
                else:
                    bg_color = "#c3e6cb" 
                    text_val = "0"       

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=bg_color, outline="#bcdbca" if text_val=="0" else "#f1b0b7")
                self.canvas.create_text(x1 + 12, y1 + 12, text=text_val, font=("Helvetica", 10, "bold"), fill="#2c3e50")

        if px is None or py is None:
            px = self.robot_col * cs + cs // 2 
            py = self.robot_row * cs + cs // 2 

        self.canvas.create_oval(px - 38, py - 38, px + 38, py + 38, fill="#3399ff", outline="white", width=2)
        self.canvas.create_text(px, py, text="🤖", font=("Helvetica", 22))

    # Hàm xử lý sự kiện click chuột trái trên ô lưới để thay đổi trạng thái Sạch/Bụi
    def on_canvas_click(self, event):
        if self.is_running: return
        c, r = event.x // 130, event.y // 130
        if 0 <= r < 3 and 0 <= c < 3:
            self.matrix[r][c] = 1 - self.matrix[r][c] 
            self.draw_all()

    # 4. CÁC HÀM CHỨC NĂNG BỔ TRỢ (RESET, CẬP NHẬT VỊ TRÍ, KHÓA CONTROL)
    
    # Hàm đọc dữ liệu từ ô nhập để thay đổi vị trí xuất phát tĩnh của Robot
    def update_initial_position(self):
        if self.is_running: return
        try:
            r = int(self.ent_row.get()) 
            c = int(self.ent_col.get()) 
            if 0 <= r < 3 and 0 <= c < 3:
                self.robot_row = r 
                self.robot_col = c 
                self.draw_all()    
                self.log_text.insert(tk.END, f"[Hệ thống] Đã cập nhật vị trí Robot về ô ({r}, {c}).\n")
                self.log_text.see(tk.END)
            else:
                messagebox.showwarning("Lỗi tọa độ", "Vui lòng nhập chỉ số hàng và cột từ 0 đến 2.")
        except ValueError:
            messagebox.showerror("Lỗi dữ liệu", "Tọa độ nhập vào phải là số nguyên hợp lệ.")

    # Hàm reset hệ thống, đưa robot về ô (0,0) và tạo ma trận bụi ngẫu nhiên
    def reset_random(self):
        if self.is_running: return
        self.robot_row, self.robot_col = 0, 0
        self.ent_row.delete(0, tk.END)
        self.ent_row.insert(0, "0")
        self.ent_col.delete(0, tk.END)
        self.ent_col.insert(0, "0")

        self.matrix = [[random.choice([0, 1]) for _ in range(3)] for _ in range(3)]
        
        self.lbl_best_path.config(text="Chua chay thuat toan", fg="#31708f")
        self.lbl_path_cost.config(text="Số bước đi (Path Cost): 0")
        self.lbl_nodes.config(text="Số Node đã duyệt: 0")
        self.lbl_time.config(text="Thời gian chạy: 0.00 ms")
        self.log_text.delete("1.0", tk.END)
        self.log_text.insert(tk.END, "Đã khởi tạo ngẫu nhiên bản đồ mới.\n")
        self.draw_all() 

    # Hàm bật/tắt (khóa) trạng thái tương tác của các nút bấm điều khiển
    def set_controls_state(self, state):
        self.btn_bfs1.config(state=state)
        self.btn_bfs2.config(state=state)
        self.btn_dfs1.config(state=state)
        self.btn_dfs2.config(state=state)
        self.btn_ucs.config(state=state) 
        self.btn_ids_1.config(state=state)
        self.btn_ids_2.config(state=state)
        self.btn_reset.config(state=state)
        self.btn_greedy.config(state=state)
        self.btn_astar.config(state=state)
        self.btn_idastar.config(state=state)
        self.btn_simple_hc.config(state=state)
        self.btn_steepest_hc.config(state=state)
        self.btn_stochastic_hc.config(state=state)
        self.btn_rand_restart_hc.config(state=state)
        self.btn_beam_search.config(state=state)
        self.btn_simulated_annealing.config(state=state)
        self.btn_multi_dfs.config(state=state)
        self.btn_belief_dfs.config(state=state)
        self.btn_and_or_search.config(state=state)

    # 5. LIÊN KẾT BACKEND & ENGINE MÔ PHỎNG HOẠT HÌNH
    
    # Hàm tiếp nhận lệnh thuật toán, gọi xử lý từ backend và chuẩn bị dữ liệu chạy hoạt hình
    def start_search(self, algo_name):
        if self.is_running: return
        
        start_matrix = [row[:] for row in self.matrix] 
        goal_matrix = [[0]*3 for _ in range(3)]        

        if start_matrix == goal_matrix:
            self.lbl_best_path.config(text="Sàn nhà đã sạch sẵn từ đầu!", fg="green")
            self.log_text.insert(tk.END, f"[{algo_name}] Môi trường sạch, không cần xử lý.\n")
            return

        if algo_name == "BFS 1":   path, nodes, t_ms = backend.run_bfs1(start_matrix, self.robot_row, self.robot_col, goal_matrix)
        elif algo_name == "BFS 2": path, nodes, t_ms = backend.run_bfs2(start_matrix, self.robot_row, self.robot_col, goal_matrix)
        elif algo_name == "DFS 1": path, nodes, t_ms = backend.run_dfs1(start_matrix, self.robot_row, self.robot_col, goal_matrix)
        elif algo_name == "DFS 2": path, nodes, t_ms = backend.run_dfs2(start_matrix, self.robot_row, self.robot_col, goal_matrix)
        elif algo_name == "UCS": path, nodes, t_ms = backend.run_ucs(self.matrix, self.robot_row, self.robot_col, goal_matrix)
        elif algo_name == "IDS1": path, nodes, t_ms = backend.run_ids_1(self.matrix, self.robot_row, self.robot_col, goal_matrix)
        elif algo_name == "IDS2": path, nodes, t_ms = backend.run_ids_2(self.matrix, self.robot_row, self.robot_col, goal_matrix)
        elif algo_name == "Greedy": path, nodes, t_ms = backend.run_greedy(self.matrix, self.robot_row, self.robot_col, goal_matrix)
        elif algo_name == "A*": path, nodes, t_ms = backend.run_astar(self.matrix, self.robot_row, self.robot_col, goal_matrix)
        elif algo_name == "IDA*": path, nodes, t_ms = backend.run_idastar(self.matrix, self.robot_row, self.robot_col, goal_matrix)
        elif algo_name == "Simple HC": path, nodes, t_ms = backend.run_simple_hill_climbing(self.matrix, self.robot_row, self.robot_col, goal_matrix)
        elif algo_name == "Steepest HC": path, nodes, t_ms = backend.run_steepest_hill_climbing(self.matrix, self.robot_row, self.robot_col, goal_matrix)
        elif algo_name == "Stochastic HC": path, nodes, t_ms = backend.run_stochastic_hill_climbing(self.matrix, self.robot_row, self.robot_col, goal_matrix)
        elif algo_name == "Random Restart HC": path, nodes, t_ms = backend.run_random_restart_hc(self.matrix, self.robot_row, self.robot_col, goal_matrix)
        elif algo_name == "Local Beam Search": path, nodes, t_ms = backend.run_local_beam_search(self.matrix, self.robot_row, self.robot_col, goal_matrix)
        elif algo_name == "Simulated Annealing": path, nodes, t_ms = backend.run_simulated_annealing(self.matrix, self.robot_row, self.robot_col, goal_matrix)
        
        elif algo_name == "Multi DFS": path, nodes, t_ms = backend.run_multi_dfs(self.matrix, self.robot_row, self.robot_col, goal_matrix)
        elif algo_name == "Belief DFS": path, nodes, t_ms = backend.run_belief_dfs(self.matrix, goal_matrix)
        
        elif algo_name == "AND-OR":
            path, all_paths, raw_plan, nodes, t_ms = backend.run_and_or_search(start_matrix, self.robot_row, self.robot_col, goal_matrix)
            
            if path is not None:
                self.log_text.insert(tk.END, f"\n=== [AND-OR] TẤT CẢ CÁC ĐƯỜNG ĐI CÓ THỂ DỌN SẠCH ===\n")
                
                for idx, p in enumerate(all_paths):
                    mapping = {'U': 'UP', 'D': 'DOWN', 'L': 'LEFT', 'R': 'RIGHT', 'SUCK': 'SUCK', 
                               'UP': 'UP', 'DOWN': 'DOWN', 'LEFT': 'LEFT', 'RIGHT': 'RIGHT'}
                    p_standardized = [mapping[act] for act in p]
                    
                    path_line = " -> ".join(p_standardized)
                    self.log_text.insert(tk.END, f"Đường đi {idx + 1}: {path_line}\n")
                    
                self.log_text.insert(tk.END, f"--------------------------------------------------\n")
                self.log_text.insert(tk.END, f" => Đã chọn đường đi tốt nhất (ngắn nhất - {len(path)} bước) để chạy mô phỏng.\n")

        # Ánh xạ ký tự viết tắt ('U', 'D', 'L', 'R') sang định dạng chuỗi đầy đủ của Frontend
        mapping = {'U': 'UP', 'D': 'DOWN', 'L': 'LEFT', 'R': 'RIGHT', 'SUCK': 'SUCK', 
                   'UP': 'UP', 'DOWN': 'DOWN', 'LEFT': 'LEFT', 'RIGHT': 'RIGHT'}
        standardized_path = [mapping[act] for act in path]

        path_str = " ".join(standardized_path)
        self.lbl_best_path.config(text=path_str, fg="#3c763d")
        self.lbl_path_cost.config(text=f"Số bước đi (Path Cost): {len(standardized_path)}")
        self.lbl_nodes.config(text=f"Số Node đã duyệt: {nodes}")
        self.lbl_time.config(text=f"Thời gian chạy: {t_ms:.2f} ms")

        self.log_text.insert(tk.END, f"\n--- Khởi chạy {algo_name} ---\nĐường đi tìm thấy:\n{path_str}\n")
        self.log_text.see(tk.END)

        self.is_running = True
        self.set_controls_state("disabled")

        # Nạp danh sách bước đi đã chuẩn hóa vào bộ engine đồ họa
        self.anim_actions = standardized_path 
        self.anim_step_index = 0     
        self.anim_frame_index = 0    
        self.anim_robot_r = self.robot_row 
        self.anim_robot_c = self.robot_col 
        
        self.animate_frame() 

    # Hàm đệ quy thời gian chia nhỏ bước đi lớn để cập nhật pixel trượt mượt mà cho Robot
    def animate_frame(self):
        if not self.is_running: return

        if self.anim_step_index >= len(self.anim_actions):
            self.is_running = False
            self.set_controls_state("normal") 
            self.log_text.insert(tk.END, "=== ĐÃ HOÀN THÀNH NHIỆM VỤ ===\n")
            self.log_text.see(tk.END)
            self.draw_all() 
            return

        action = self.anim_actions[self.anim_step_index]
        k = self.anim_frame_index 
        total_frames = 15  

        cs = 130
        start_px = self.anim_robot_c * cs + cs // 2
        start_py = self.anim_robot_r * cs + cs // 2

        next_r, next_c = self.anim_robot_r, self.anim_robot_c
        if action == "UP":     next_r -= 1
        elif action == "DOWN":  next_r += 1
        elif action == "LEFT":  next_c -= 1
        elif action == "RIGHT": next_c += 1

        next_r = max(0, min(2, next_r))
        next_c = max(0, min(2, next_c))

        end_px = next_c * cs + cs // 2
        end_py = next_r * cs + cs // 2

        if k == 0:
            if action == "SUCK":
                self.log_text.insert(tk.END, f"Hut Bui tai: {self.anim_robot_r} {self.anim_robot_c}\n")
            else:
                self.log_text.insert(tk.END, f"Move {action}: {next_r} {next_c}\n")
            self.log_text.see(tk.END)

        if action == "SUCK":
            curr_px, curr_py = start_px, start_py
            if k == total_frames:
                self.matrix[self.anim_robot_r][self.anim_robot_c] = 0
        else:
            curr_px = start_px + (end_px - start_px) * (k / total_frames)
            curr_py = start_py + (end_py - start_py) * (k / total_frames)

        self.draw_all(curr_px, curr_py)

        if k < total_frames:
            self.anim_frame_index += 1 
        else:
            self.robot_row, self.robot_col = next_r, next_c
            self.anim_robot_r, self.anim_robot_c = next_r, next_c
            self.anim_step_index += 1 
            self.anim_frame_index = 0 

        self.root.after(20, self.animate_frame)