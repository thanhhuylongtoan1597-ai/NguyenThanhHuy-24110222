import tkinter as tk
from tkinter import messagebox, scrolledtext
import random
import backend

class DualBoardWindow:
    def __init__(self, parent, robot_row, robot_col):
        self.top = tk.Toplevel(parent)
        self.top.title("🤖 Mô Phỏng 2 Bàn Cờ (Partial Observation & Sensorless Search)")
        self.top.geometry("980x740")
        self.top.configure(bg="#f4f4f4")
        self.top.resizable(False, False)

        self.robot_row = robot_row
        self.robot_col = robot_col

        self.matrix1 = [[random.choice([0, 1]) for _ in range(3)] for _ in range(3)]
        self.matrix2 = [[random.choice([0, 1]) for _ in range(3)] for _ in range(3)]

        self.is_running = False
        self.anim_actions = []
        self.anim_step_index = 0
        self.anim_frame_index = 0
        self.anim_robot_r1 = robot_row
        self.anim_robot_c1 = robot_col
        self.anim_robot_r2 = robot_row
        self.anim_robot_c2 = robot_col

        self.setup_ui()
        self.draw_boards()

    def setup_ui(self):
        # Header controls
        ctrl_frame = tk.Frame(self.top, bg="#f4f4f4", pady=10)
        ctrl_frame.pack(fill="x")

        tk.Label(ctrl_frame, text=f"Vị trí Robot chung: ({self.robot_row}, {self.robot_col})", font=("Helvetica", 11, "bold"), bg="#f4f4f4", fg="#2c3e50").pack(side="left", padx=15)

        self.btn_random = tk.Button(ctrl_frame, text="🎲 Random Bụi Mới", font=("Helvetica", 10, "bold"), bg="#f2dede", fg="#a94442", relief="groove", bd=1, padx=10, command=self.reset_random_dirt)
        self.btn_random.pack(side="left", padx=10)

        self.btn_partial = tk.Button(ctrl_frame, text="🔍 Chạy Partial Observation Search", font=("Helvetica", 10, "bold"), bg="#d9edf7", fg="#31708f", relief="groove", bd=1, padx=10, command=lambda: self.start_dual_search("Partial Observation Search"))
        self.btn_partial.pack(side="left", padx=10)

        self.btn_sensorless = tk.Button(ctrl_frame, text="🙈 Chạy Sensorless Search", font=("Helvetica", 10, "bold"), bg="#dff0d8", fg="#3c763d", relief="groove", bd=1, padx=10, command=lambda: self.start_dual_search("Sensorless Search"))
        self.btn_sensorless.pack(side="left", padx=10)

        # Boards Frame (Side by side)
        boards_frame = tk.Frame(self.top, bg="#f4f4f4")
        boards_frame.pack(pady=10)

        # Board 1
        b1_frame = tk.Frame(boards_frame, bg="#f4f4f4")
        b1_frame.grid(row=0, column=0, padx=20)
        tk.Label(b1_frame, text="BÀN CỜ 1 (Môi trường A)", font=("Helvetica", 11, "bold"), bg="#f4f4f4", fg="#2980b9").pack(pady=5)
        self.canvas1 = tk.Canvas(b1_frame, width=330, height=330, bg="white", highlightthickness=1, highlightbackground="#bdc3c7")
        self.canvas1.pack()

        # Board 2
        b2_frame = tk.Frame(boards_frame, bg="#f4f4f4")
        b2_frame.grid(row=0, column=1, padx=20)
        tk.Label(b2_frame, text="BÀN CỜ 2 (Môi trường B)", font=("Helvetica", 11, "bold"), bg="#f4f4f4", fg="#8e44ad").pack(pady=5)
        self.canvas2 = tk.Canvas(b2_frame, width=330, height=330, bg="white", highlightthickness=1, highlightbackground="#bdc3c7")
        self.canvas2.pack()

        # Dashboard & Log Frame
        bottom_frame = tk.Frame(self.top, bg="#f4f4f4", padx=15, pady=5)
        bottom_frame.pack(fill="both", expand=True)

        stats_frame = tk.Frame(bottom_frame, bg="#f4f4f4")
        stats_frame.pack(fill="x", pady=2)

        self.lbl_path_cost = tk.Label(stats_frame, text="Số bước đi (Path Cost): 0", font=("Helvetica", 10, "bold"), bg="#f4f4f4", fg="#333333")
        self.lbl_path_cost.pack(side="left", padx=15)

        self.lbl_nodes = tk.Label(stats_frame, text="Số Node đã duyệt: 0", font=("Helvetica", 10, "bold"), bg="#f4f4f4", fg="#333333")
        self.lbl_nodes.pack(side="left", padx=15)

        self.lbl_time = tk.Label(stats_frame, text="Thời gian chạy: 0.00 ms", font=("Helvetica", 10, "bold"), bg="#f4f4f4", fg="#333333")
        self.lbl_time.pack(side="left", padx=15)

        self.lbl_path = tk.Label(bottom_frame, text="Đường đi: Chưa chạy thuật toán", font=("Consolas", 10), bg="#ffffff", fg="#27ae60", relief="solid", bd=1, padx=10, pady=5, anchor="w")
        self.lbl_path.pack(fill="x", pady=5)

        log_box_frame = tk.LabelFrame(bottom_frame, text="Console Log Đồng Bộ Dual-Board", font=("Helvetica", 9, "bold"), bg="#f4f4f4", fg="#34495e", padx=5, pady=5)
        log_box_frame.pack(fill="both", expand=True, pady=5)

        self.log_text = scrolledtext.ScrolledText(log_box_frame, font=("Consolas", 9), bg="#2c3e50", fg="#ecf0f1", height=8, wrap="word")
        self.log_text.pack(fill="both", expand=True)
        self.log_text.insert(tk.END, "Đã mở cửa sổ Dual-Board Mô Phỏng Song Song. Nhấn nút thuật toán để chạy.\n")

    def log(self, text):
        self.log_text.insert(tk.END, text)
        self.log_text.see(tk.END)

    def reset_random_dirt(self):
        if self.is_running: return
        self.matrix1 = [[random.choice([0, 1]) for _ in range(3)] for _ in range(3)]
        self.matrix2 = [[random.choice([0, 1]) for _ in range(3)] for _ in range(3)]
        self.lbl_path_cost.config(text="Số bước đi (Path Cost): 0")
        self.lbl_nodes.config(text="Số Node đã duyệt: 0")
        self.lbl_time.config(text="Thời gian chạy: 0.00 ms")
        self.lbl_path.config(text="Đường đi: Chưa chạy thuật toán")
        self.log_text.delete("1.0", tk.END)
        self.log("Đã khởi tạo ngẫu nhiên vị trí bụi mới cho 2 Bàn cờ (Robot giữ nguyên vị trí).\n")
        self.draw_boards()

    def draw_boards(self, px1=None, py1=None, px2=None, py2=None):
        self._draw_single_board(self.canvas1, self.matrix1, self.robot_row, self.robot_col, px1, py1)
        self._draw_single_board(self.canvas2, self.matrix2, self.robot_row, self.robot_col, px2, py2)

    def _draw_single_board(self, canvas, matrix, r_row, r_col, px, py):
        canvas.delete("all")
        cs = 110
        for r in range(3):
            for c in range(3):
                x1, y1 = c * cs, r * cs
                x2, y2 = x1 + cs, y1 + cs
                if matrix[r][c] == 1:
                    bg_color = "#f5c6cb"
                    text_val = "1"
                else:
                    bg_color = "#c3e6cb"
                    text_val = "0"
                canvas.create_rectangle(x1, y1, x2, y2, fill=bg_color, outline="#bcdbca" if text_val=="0" else "#f1b0b7")
                canvas.create_text(x1 + 10, y1 + 10, text=text_val, font=("Helvetica", 9, "bold"), fill="#2c3e50")

        if px is None or py is None:
            px = r_col * cs + cs // 2
            py = r_row * cs + cs // 2

        canvas.create_oval(px - 32, py - 32, px + 32, py + 32, fill="#3399ff", outline="white", width=2)
        canvas.create_text(px, py, text="🤖", font=("Helvetica", 18))

    def set_controls_state(self, state):
        self.btn_random.config(state=state)
        self.btn_partial.config(state=state)
        self.btn_sensorless.config(state=state)

    def start_dual_search(self, algo_name):
        if self.is_running: return
        goal_matrix = [[0]*3 for _ in range(3)]

        if algo_name == "Partial Observation Search":
            path, nodes, t_ms = backend.run_partial_observation_search_dual(self.matrix1, self.matrix2, self.robot_row, self.robot_col, goal_matrix)
        elif algo_name == "Sensorless Search":
            path, nodes, t_ms = backend.run_sensorless_search_dual(self.matrix1, self.matrix2, goal_matrix)
        else:
            return

        if path is None:
            self.lbl_path.config(text="Không tìm thấy đường đi giải quyết cả 2 bảng!")
            self.log(f"\n--- Khởi chạy {algo_name} trên 2 Bảng ---\nKhông tìm thấy giải pháp chung.\n")
            return

        mapping = {'U': 'UP', 'D': 'DOWN', 'L': 'LEFT', 'R': 'RIGHT', 'SUCK': 'SUCK', 
                   'UP': 'UP', 'DOWN': 'DOWN', 'LEFT': 'LEFT', 'RIGHT': 'RIGHT'}
        standardized_path = [mapping[act] for act in path]
        path_str = " -> ".join(standardized_path)

        self.lbl_path.config(text=f"Đường đi đồng bộ: {path_str}")
        self.lbl_path_cost.config(text=f"Số bước đi (Path Cost): {len(standardized_path)}")
        self.lbl_nodes.config(text=f"Số Node đã duyệt: {nodes}")
        self.lbl_time.config(text=f"Thời gian chạy: {t_ms:.2f} ms")

        self.log(f"\n=== KHỞI CHẠY {algo_name.upper()} DUAL-BOARD ===\nĐường đi tìm thấy ({len(standardized_path)} bước):\n{path_str}\n")

        self.is_running = True
        self.set_controls_state("disabled")

        self.anim_actions = standardized_path
        self.anim_step_index = 0
        self.anim_frame_index = 0
        self.anim_robot_r1 = self.robot_row
        self.anim_robot_c1 = self.robot_col
        self.anim_robot_r2 = self.robot_row
        self.anim_robot_c2 = self.robot_col

        self.animate_frame()

    def animate_frame(self):
        if not self.is_running: return

        if self.anim_step_index >= len(self.anim_actions):
            self.is_running = False
            self.set_controls_state("normal")
            self.log("=== ĐÃ HOÀN THÀNH DỌN SẠCH CẢ 2 BÀN CỜ ===\n")
            self.draw_boards()
            return

        action = self.anim_actions[self.anim_step_index]
        k = self.anim_frame_index
        total_frames = 12
        cs = 110

        start_px1 = self.anim_robot_c1 * cs + cs // 2
        start_py1 = self.anim_robot_r1 * cs + cs // 2
        start_px2 = self.anim_robot_c2 * cs + cs // 2
        start_py2 = self.anim_robot_r2 * cs + cs // 2

        next_r1, next_c1 = self.anim_robot_r1, self.anim_robot_c1
        next_r2, next_c2 = self.anim_robot_r2, self.anim_robot_c2

        if action == "UP":
            next_r1, next_r2 = next_r1 - 1, next_r2 - 1
        elif action == "DOWN":
            next_r1, next_r2 = next_r1 + 1, next_r2 + 1
        elif action == "LEFT":
            next_c1, next_c2 = next_c1 - 1, next_c2 - 1
        elif action == "RIGHT":
            next_c1, next_c2 = next_c1 + 1, next_c2 + 1

        next_r1, next_c1 = max(0, min(2, next_r1)), max(0, min(2, next_c1))
        next_r2, next_c2 = max(0, min(2, next_r2)), max(0, min(2, next_c2))

        end_px1 = next_c1 * cs + cs // 2
        end_py1 = next_r1 * cs + cs // 2
        end_px2 = next_c2 * cs + cs // 2
        end_py2 = next_r2 * cs + cs // 2

        if k == 0:
            if action == "SUCK":
                self.log(f"Hành động [SUCK] đồng thời trên Bảng 1 & Bảng 2\n")
            else:
                self.log(f"Hành động [MOVE {action}] đồng thời trên cả 2 Bảng\n")

        if action == "SUCK":
            curr_px1, curr_py1 = start_px1, start_py1
            curr_px2, curr_py2 = start_px2, start_py2
            if k == total_frames:
                self.matrix1[self.anim_robot_r1][self.anim_robot_c1] = 0
                self.matrix2[self.anim_robot_r2][self.anim_robot_c2] = 0
        else:
            curr_px1 = start_px1 + (end_px1 - start_px1) * k / total_frames
            curr_py1 = start_py1 + (end_py1 - start_py1) * k / total_frames
            curr_px2 = start_px2 + (end_px2 - start_px2) * k / total_frames
            curr_py2 = start_py2 + (end_py2 - start_py2) * k / total_frames

        self._draw_single_board(self.canvas1, self.matrix1, self.anim_robot_r1, self.anim_robot_c1, curr_px1, curr_py1)
        self._draw_single_board(self.canvas2, self.matrix2, self.anim_robot_r2, self.anim_robot_c2, curr_px2, curr_py2)

        if k < total_frames:
            self.anim_frame_index += 1
            self.top.after(25, self.animate_frame)
        else:
            self.anim_robot_r1, self.anim_robot_c1 = next_r1, next_c1
            self.anim_robot_r2, self.anim_robot_c2 = next_r2, next_c2
            self.anim_step_index += 1
            self.anim_frame_index = 0
            self.top.after(100, self.animate_frame)
