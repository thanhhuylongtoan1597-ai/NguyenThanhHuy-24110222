import tkinter as tk
import backend
from .config import NODE_POSITIONS, SHORT_NAMES, COLOR_MAP, DOT_COLORS

class GraphCanvas:
    def __init__(self, parent):
        self.canvas = tk.Canvas(parent, bg="#ffffff", width=620, height=580, highlightthickness=1, highlightbackground="#dcdde1")
        self.canvas.pack(fill="both", expand=True)

    def draw_graph(self, history_states, step_index, current_algo, lbl_step_counter):
        self.canvas.delete("all")
        
        if not history_states:
            curr_assign = {}
            curr_domains = {v: backend.DOMAINS[:] for v in backend.VARIABLES}
            lbl_step_counter.config(text="Trạng thái: Sẵn sàng")
        else:
            state = history_states[step_index]
            curr_assign = state["assignment"]
            curr_domains = state["domains"]
            lbl_step_counter.config(text=f"Thuật toán: {current_algo} | Bước: {step_index + 1} / {len(history_states)}")

        for v1, v2 in backend.CONSTRAINTS:
            p1 = NODE_POSITIONS[v1]
            p2 = NODE_POSITIONS[v2]
            self.canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill="#bdc3c7", width=2)

        r = 22 
        for var, pos in NODE_POSITIONS.items():
            cx, cy = pos
            color_str = curr_assign.get(var, None)
            hex_color = COLOR_MAP[color_str]
            
            self.canvas.create_text(cx, cy - (r + 12), text=var, font=("Helvetica", 9, "bold"), fill="#2c3e50")
            self.canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill=hex_color, outline="#34495e", width=2)
            
            text_color = "white" if color_str in ["Đỏ", "Xanh dương"] else "#2c3e50"
            self.canvas.create_text(cx, cy, text=SHORT_NAMES[var], font=("Helvetica", 10, "bold"), fill=text_color)
            
            available_colors = curr_domains.get(var, [])
            dot_r = 4 
            start_x = cx - ((len(available_colors) - 1) * 10) / 2 
            
            for idx, c_name in enumerate(available_colors):
                dot_x = start_x + idx * 10
                dot_y = cy + r + 10
                self.canvas.create_oval(dot_x - dot_r, dot_y - dot_r, dot_x + dot_r, dot_y + dot_r, fill=DOT_COLORS[c_name], outline="")
