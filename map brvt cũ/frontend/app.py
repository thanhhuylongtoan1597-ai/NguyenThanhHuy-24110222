import tkinter as tk
from tkinter import messagebox
import backend
from .graph_canvas import GraphCanvas
from .control_panel import ControlPanel
from .log_panel import LogPanel

class CSPBacktrackingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualizer: Graph Coloring - Ba Ria Vung Tau Province")
        self.root.geometry("1150x680")
        self.root.configure(bg="#f5f6fa")
        self.root.resizable(False, False)
        
        self.history_states = []
        self.step_index = 0
        self.is_auto_running = False
        self.current_algo = ""
        
        self.setup_layout()
        self.reset_simulation()

    def setup_layout(self):
        left_frame = tk.Frame(self.root, bg="#f5f6fa")
        left_frame.pack(side="left", fill="both", expand=True, padx=15, pady=15)

        lbl_map_title = tk.Label(left_frame, text="BẢN ĐỒ QUAN HỆ GIÁP RANH BÀ RỊA VŨNG TÀU", font=("Helvetica", 12, "bold"), fg="#2c3e50", bg="#f5f6fa")
        lbl_map_title.pack(anchor="w", pady=(0, 10))

        self.graph_canvas = GraphCanvas(left_frame)

        right_frame = tk.Frame(self.root, bg="#f5f6fa", width=460)
        right_frame.pack(side="right", fill="both", expand=False, padx=(0, 15), pady=15)
        right_frame.pack_propagate(False)

        self.control_panel = ControlPanel(
            right_frame, 
            on_algo_select_cb=self.on_algo_select, 
            reset_cb=self.reset_simulation, 
            slider_cb=self.on_slider_move
        )

        self.log_panel = LogPanel(right_frame)

    def draw_graph(self):
        self.graph_canvas.draw_graph(
            self.history_states, 
            self.step_index, 
            self.current_algo, 
            self.control_panel.lbl_step_counter
        )

    def on_algo_select(self, selected_algo):
        self.trigger_algorithm(selected_algo)

    def trigger_algorithm(self, algo_name):
        if self.is_auto_running:
            self.is_auto_running = False
            
        self.current_algo = algo_name
        self.step_index = 0
        self.log_panel.clear()
        
        if algo_name == "Backtracking":
            self.history_states, t_ms = backend.run_pure_backtracking()
            self.log_panel.insert_system_msg(f"[Hệ thống] Đang chạy tự động thuật toán Backtracking thuần túy ({t_ms:.2f} ms)...\n----------------------------------------\n")
        elif algo_name == "Forward Checking":
            self.history_states, t_ms = backend.run_forward_checking()
            self.log_panel.insert_system_msg(f"[Hệ thống] Đang chạy tự động thuật toán Forward Checking ({t_ms:.2f} ms)...\n----------------------------------------\n")
        elif algo_name == "AC-3":
            self.history_states, t_ms = backend.run_ac3_simulation()
            self.log_panel.insert_system_msg(f"[Hệ thống] Đang chạy tự động thuật toán Nhất quán cung AC-3 ({t_ms:.2f} ms)...\n----------------------------------------\n")
        elif algo_name == "Min-Conflicts":
            self.history_states, t_ms = backend.run_min_conflicts_simulation()
            self.log_panel.insert_system_msg(f"[Hệ thống] Đang chạy tự động thuật toán cục bộ Min-Conflicts ({t_ms:.2f} ms)...\n----------------------------------------\n")
        elif algo_name == "CSP":
            self.history_states, t_ms = backend.run_csp_backtracking()
            self.log_panel.insert_system_msg(f"[Hệ thống] Đang chạy tự động thuật toán CSP ({t_ms:.2f} ms)...\n----------------------------------------\n")

        if self.history_states:
            self.control_panel.set_slider_range(1, len(self.history_states), 1)

        self.is_auto_running = True
        self.auto_play()

    def on_slider_move(self, val):
        if not self.history_states:
            return
            
        target_index = int(val) - 1
        if target_index == self.step_index:
            return
            
        if self.is_auto_running and target_index != self.step_index + 1 and target_index != 0:
            self.is_auto_running = False
            
        self.step_index = target_index
        self.draw_graph()
        
        self.log_panel.clear()
        for i in range(self.step_index + 1):
            msg = self.history_states[i]["msg"].replace("✓ ", "").replace("➔ ", "").replace("↩ ", "").replace("⚠ ", "")
            self.log_panel.insert_system_msg(f"{msg}\n")
        self.log_panel.log_area.see(tk.END)

    def update_log_display(self, text_msg):
        self.log_panel.update_log_display(text_msg)

    def next_step(self):
        if self.step_index < len(self.history_states) - 1:
            self.step_index += 1
            self.control_panel.step_slider.set(self.step_index + 1)
            self.draw_graph()
            self.update_log_display(self.history_states[self.step_index]["msg"])
            return True
        else:
            self.is_auto_running = False
            messagebox.showinfo("Hoàn tất", f"Thuật toán {self.current_algo} đã hoàn thành mô phỏng!")
            return False

    def auto_play(self):
        if not self.is_auto_running:
            return
        
        if self.step_index == 0 and self.history_states:
            self.draw_graph()
            self.update_log_display(self.history_states[0]["msg"])
            self.root.after(800, self.auto_play)
            self.step_index += 1
        else:
            has_next = self.next_step()
            if has_next:
                self.root.after(800, self.auto_play)

    def reset_simulation(self):
        self.is_auto_running = False
        self.history_states = []
        self.step_index = 0
        self.current_algo = ""
        self.log_panel.clear()
        self.log_panel.insert_system_msg("Hệ thống sẵn sàng. Vui lòng bấm chọn một thuật toán để trình diễn.\n")
        
        if hasattr(self, 'control_panel'):
            self.control_panel.reset_controls()
            
        self.draw_graph()
