import tkinter as tk
from tkinter import ttk
from .styles import BG_PANEL, FG_DARK, FG_GRAY, COLOR_X, COLOR_ACCENT

class PanelView(tk.Frame):
    def __init__(self, parent, on_reset_callback, on_setting_change_callback):
        super().__init__(parent, bg=BG_PANEL, width=380, bd=0)
        self.pack_propagate(False)
        self.on_reset_callback = on_reset_callback
        self.on_setting_change_callback = on_setting_change_callback
        self.stat_widgets = {}
        
        self.build_panel()

    def build_panel(self):
        config_title = tk.Label(
            self,
            text="Cấu hình trò chơi",
            font=("Helvetica", 14, "bold"),
            bg=BG_PANEL,
            fg=COLOR_ACCENT,
            anchor="w"
        )
        config_title.pack(fill="x", padx=20, pady=(20, 10))

        algo_label = tk.Label(self, text="Thuật toán AI:", font=("Helvetica", 10), bg=BG_PANEL, fg=FG_GRAY, anchor="w")
        algo_label.pack(fill="x", padx=20)
        self.algo_var = tk.StringVar(value="Alpha-Beta Pruning")
        self.algo_combo = ttk.Combobox(
            self,
            textvariable=self.algo_var,
            values=["Minimax", "Alpha-Beta Pruning", "Expectimax"],
            state="readonly",
            font=("Helvetica", 10)
        )
        self.algo_combo.pack(fill="x", padx=20, pady=(0, 10))

        depth_label_frame = tk.Frame(self, bg=BG_PANEL)
        depth_label_frame.pack(fill="x", padx=20)
        
        depth_label = tk.Label(depth_label_frame, text="Độ sâu tối đa (Depth):", font=("Helvetica", 10), bg=BG_PANEL, fg=FG_GRAY, anchor="w")
        depth_label.pack(side="left")
        
        self.depth_val_label = tk.Label(depth_label_frame, text="9 (Tối đa)", font=("Helvetica", 10, "bold"), bg=BG_PANEL, fg=COLOR_X)
        self.depth_val_label.pack(side="right")

        self.depth_slider = ttk.Scale(
            self,
            from_=1,
            to=9,
            value=9,
            orient="horizontal",
            style='Horizontal.TScale',
            command=self.on_depth_slider_move
        )
        self.depth_slider.pack(fill="x", padx=20, pady=(0, 10))

        ai_sym_label = tk.Label(self, text="Quân cờ AI sử dụng:", font=("Helvetica", 10), bg=BG_PANEL, fg=FG_GRAY, anchor="w")
        ai_sym_label.pack(fill="x", padx=20)
        self.ai_sym_var = tk.StringVar(value="O (AI) - X (Người chơi)")
        self.ai_sym_combo = ttk.Combobox(
            self,
            textvariable=self.ai_sym_var,
            values=["O (AI) - X (Người chơi)", "X (AI) - O (Người chơi)"],
            state="readonly",
            font=("Helvetica", 10)
        )
        self.ai_sym_combo.pack(fill="x", padx=20, pady=(0, 10))
        self.ai_sym_combo.bind("<<ComboboxSelected>>", self.on_setting_change_callback)

        starter_label = tk.Label(self, text="Đi trước:", font=("Helvetica", 10), bg=BG_PANEL, fg=FG_GRAY, anchor="w")
        starter_label.pack(fill="x", padx=20)
        self.starter_var = tk.StringVar(value="Người chơi")
        self.starter_combo = ttk.Combobox(
            self,
            textvariable=self.starter_var,
            values=["Người chơi", "AI"],
            state="readonly",
            font=("Helvetica", 10)
        )
        self.starter_combo.pack(fill="x", padx=20, pady=(0, 15))
        self.starter_combo.bind("<<ComboboxSelected>>", self.on_setting_change_callback)

        self.reset_btn = tk.Button(
            self,
            text="Chơi Trận Mới",
            font=("Helvetica", 11, "bold"),
            bg=COLOR_ACCENT,
            fg="#ffffff",
            activebackground='#0b7285',
            activeforeground="#ffffff",
            relief="flat",
            bd=0,
            cursor="hand2",
            pady=8,
            command=self.on_reset_callback
        )
        self.reset_btn.pack(fill="x", padx=20, pady=(0, 15))

        divider = tk.Frame(self, height=2, bg='#dee2e6')
        divider.pack(fill="x", padx=20, pady=10)

        stats_title = tk.Label(
            self,
            text="Thống kê công cụ AI",
            font=("Helvetica", 14, "bold"),
            bg=BG_PANEL,
            fg=COLOR_ACCENT,
            anchor="w"
        )
        stats_title.pack(fill="x", padx=20, pady=(10, 10))

        stats_grid = tk.Frame(self, bg=BG_PANEL)
        stats_grid.pack(fill="both", expand=True, padx=20, pady=5)

        stats_labels = [
            ("Thuật toán vừa dùng:", "algo_lbl", "Chưa chạy"),
            ("Thời gian tìm kiếm:", "time_lbl", "0.00 ms"),
            ("Số trạng thái duyệt:", "nodes_lbl", "0"),
            ("Nước đi đề xuất:", "move_lbl", "N/A"),
        ]

        for idx, (label_text, widget_key, default_val) in enumerate(stats_labels):
            lbl_title = tk.Label(stats_grid, text=label_text, font=("Helvetica", 10), bg=BG_PANEL, fg=FG_GRAY, anchor="w")
            lbl_title.grid(row=idx, column=0, sticky="w", pady=5)

            lbl_val = tk.Label(stats_grid, text=default_val, font=("Helvetica", 10, "bold"), bg=BG_PANEL, fg=FG_DARK, anchor="e")
            lbl_val.grid(row=idx, column=1, sticky="e", pady=5)
            stats_grid.grid_columnconfigure(1, weight=1)

            self.stat_widgets[widget_key] = lbl_val

        status_bar = tk.Frame(self, bg='#e9ecef', height=45)
        status_bar.pack(side="bottom", fill="x")
        status_bar.pack_propagate(False)

        self.status_lbl = tk.Label(
            status_bar,
            text="Lượt chơi: Người chơi",
            font=("Helvetica", 11, "bold"),
            bg='#e9ecef',
            fg=COLOR_X,
            pady=10
        )
        self.status_lbl.pack(fill="both", expand=True)

    def on_depth_slider_move(self, event=None):
        val = int(float(self.depth_slider.get()))
        text = f"{val}"
        if val == 9:
            text += " (Tối đa)"
        self.depth_val_label.config(text=text)

    def update_stats(self, algorithm, elapsed, nodes, r, c):
        self.stat_widgets["algo_lbl"].config(text=algorithm, fg=COLOR_X)
        self.stat_widgets["time_lbl"].config(text=f"{elapsed:.2f} ms", fg=COLOR_X)
        self.stat_widgets["nodes_lbl"].config(text=f"{nodes:,}", fg=COLOR_X)
        self.stat_widgets["move_lbl"].config(text=f"Hàng {r+1}, Cột {c+1}", fg=COLOR_X)

    def reset_stats(self):
        self.stat_widgets["algo_lbl"].config(text="Chưa chạy", fg=FG_DARK)
        self.stat_widgets["time_lbl"].config(text="0.00 ms", fg=FG_DARK)
        self.stat_widgets["nodes_lbl"].config(text="0", fg=FG_DARK)
        self.stat_widgets["move_lbl"].config(text="N/A", fg=FG_DARK)

    def set_status(self, text, color):
        self.status_lbl.config(text=text, fg=color)
