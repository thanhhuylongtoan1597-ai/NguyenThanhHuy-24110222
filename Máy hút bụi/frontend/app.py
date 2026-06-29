import tkinter as tk
from tkinter import messagebox
import random
import backend
from .left_panel import LeftPanel
from .middle_panel import MiddlePanel
from .right_panel import RightPanel
from .dual_board_window import DualBoardWindow

class VacuumSimulationApp:

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

    def setup_layout(self):
        self.left_panel = LeftPanel(self.root, self)
        self.middle_panel = MiddlePanel(self.root, self)
        self.right_panel = RightPanel(self.root, self)

    def draw_all(self, px=None, py=None):
        self.middle_panel.draw_all(self.matrix, self.robot_row, self.robot_col, px, py)

    def on_canvas_click(self, event):
        if self.is_running: return
        c, r = event.x // 130, event.y // 130
        if 0 <= r < 3 and 0 <= c < 3:
            self.matrix[r][c] = 1 - self.matrix[r][c] 
            self.draw_all()

    def update_initial_position(self):
        if self.is_running: return
        try:
            r = int(self.left_panel.ent_row.get()) 
            c = int(self.left_panel.ent_col.get()) 
            if 0 <= r < 3 and 0 <= c < 3:
                self.robot_row = r 
                self.robot_col = c 
                self.draw_all()    
                self.right_panel.log(f"[Hệ thống] Đã cập nhật vị trí Robot về ô ({r}, {c}).\n")
            else:
                messagebox.showwarning("Lỗi tọa độ", "Vui lòng nhập chỉ số hàng và cột từ 0 đến 2.")
        except ValueError:
            messagebox.showerror("Lỗi dữ liệu", "Tọa độ nhập vào phải là số nguyên hợp lệ.")

    def reset_random(self):
        if self.is_running: return
        self.robot_row, self.robot_col = 0, 0
        self.left_panel.ent_row.delete(0, tk.END)
        self.left_panel.ent_row.insert(0, "0")
        self.left_panel.ent_col.delete(0, tk.END)
        self.left_panel.ent_col.insert(0, "0")

        self.matrix = [[random.choice([0, 1]) for _ in range(3)] for _ in range(3)]
        
        self.middle_panel.lbl_best_path.config(text="Chua chay thuat toan", fg="#31708f")
        self.right_panel.lbl_path_cost.config(text="Số bước đi (Path Cost): 0")
        self.right_panel.lbl_nodes.config(text="Số Node đã duyệt: 0")
        self.right_panel.lbl_time.config(text="Thời gian chạy: 0.00 ms")
        self.right_panel.clear_log()
        self.right_panel.log("Đã khởi tạo ngẫu nhiên bản đồ mới.\n")
        self.draw_all() 

    def open_dual_board_window(self):
        if self.is_running: return
        DualBoardWindow(self.root, self.robot_row, self.robot_col)

    def set_controls_state(self, state):

        self.left_panel.set_controls_state(state)

    def start_search(self, algo_name):
        if self.is_running: return
        
        start_matrix = [row[:] for row in self.matrix] 
        goal_matrix = [[0]*3 for _ in range(3)]        

        if start_matrix == goal_matrix:
            self.middle_panel.lbl_best_path.config(text="Sàn nhà đã sạch sẵn từ đầu!", fg="green")
            self.right_panel.log(f"[{algo_name}] Môi trường sạch, không cần xử lý.\n")
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
        
        elif algo_name == "Partial Observation Search": path, nodes, t_ms = backend.run_partial_observation_search(self.matrix, self.robot_row, self.robot_col, goal_matrix)
        elif algo_name == "Sensorless Search": path, nodes, t_ms = backend.run_sensorless_search(self.matrix, goal_matrix)
        
        elif algo_name == "AND-OR":
            path, all_paths, raw_plan, nodes, t_ms = backend.run_and_or_search(start_matrix, self.robot_row, self.robot_col, goal_matrix)
            
            if path is not None:
                self.right_panel.log("\n=== [AND-OR] TẤT CẢ CÁC ĐƯỜNG ĐI CÓ THỂ DỌN SẠCH ===\n")
                
                for idx, p in enumerate(all_paths):
                    mapping = {'U': 'UP', 'D': 'DOWN', 'L': 'LEFT', 'R': 'RIGHT', 'SUCK': 'SUCK', 
                               'UP': 'UP', 'DOWN': 'DOWN', 'LEFT': 'LEFT', 'RIGHT': 'RIGHT'}
                    p_standardized = [mapping[act] for act in p]
                    
                    path_line = " -> ".join(p_standardized)
                    self.right_panel.log(f"Đường đi {idx + 1}: {path_line}\n")
                    
                self.right_panel.log("--------------------------------------------------\n")
                self.right_panel.log(f" => Đã chọn đường đi tốt nhất (ngắn nhất - {len(path)} bước) để chạy mô phỏng.\n")

        if path is None:
            self.middle_panel.lbl_best_path.config(text="Không tìm thấy đường đi!", fg="red")
            self.right_panel.lbl_path_cost.config(text="Số bước đi (Path Cost): 0")
            self.right_panel.lbl_nodes.config(text=f"Số Node đã duyệt: {nodes}")
            self.right_panel.lbl_time.config(text=f"Thời gian chạy: {t_ms:.2f} ms")
            self.right_panel.log(f"\n--- Khởi chạy {algo_name} ---\nKhông tìm thấy giải pháp.\n")
            return

        mapping = {'U': 'UP', 'D': 'DOWN', 'L': 'LEFT', 'R': 'RIGHT', 'SUCK': 'SUCK', 
                   'UP': 'UP', 'DOWN': 'DOWN', 'LEFT': 'LEFT', 'RIGHT': 'RIGHT'}
        standardized_path = [mapping[act] for act in path]

        path_str = " ".join(standardized_path)
        self.middle_panel.lbl_best_path.config(text=path_str, fg="#3c763d")
        self.right_panel.lbl_path_cost.config(text=f"Số bước đi (Path Cost): {len(standardized_path)}")
        self.right_panel.lbl_nodes.config(text=f"Số Node đã duyệt: {nodes}")
        self.right_panel.lbl_time.config(text=f"Thời gian chạy: {t_ms:.2f} ms")

        self.right_panel.log(f"\n--- Khởi chạy {algo_name} ---\nĐường đi tìm thấy:\n{path_str}\n")

        self.is_running = True
        self.set_controls_state("disabled")

        self.anim_actions = standardized_path 
        self.anim_step_index = 0     
        self.anim_frame_index = 0    
        self.anim_robot_r = self.robot_row 
        self.anim_robot_c = self.robot_col 
        
        self.animate_frame() 

    def animate_frame(self):
        if not self.is_running: return

        if self.anim_step_index >= len(self.anim_actions):
            self.is_running = False
            self.set_controls_state("normal") 
            self.right_panel.log("=== ĐÃ HOÀN THÀNH NHIỆM VỤ ===\n")
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
                self.right_panel.log(f"Hut Bui tai: {self.anim_robot_r} {self.anim_robot_c}\n")
            else:
                self.right_panel.log(f"Move {action}: {next_r} {next_c}\n")

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
