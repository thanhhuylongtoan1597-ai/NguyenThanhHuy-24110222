import tkinter as tk
from tkinter import ttk

class LeftPanel:
    def __init__(self, parent, app):
        self.app = app
        self.frame = tk.Frame(parent, bg="#f4f4f4", width=240, height=720)
        self.frame.pack(side="left", fill="both", expand=False, padx=15, pady=15)
        self.frame.pack_propagate(False)

        tk.Label(self.frame, text="THUẬT TOÁN", font=("Helvetica", 12, "bold"), bg="#f4f4f4").pack(pady=(0, 10))

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Vertical.TScrollbar", gripcount=0, background="#c1c1c1", troughcolor="#f4f4f4", bordercolor="#f4f4f4", lightcolor="#f4f4f4", darkcolor="#f4f4f4", arrowsize=0)

        algo_container = tk.Frame(self.frame, bg="#f4f4f4", height=380)
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

        self.buttons = {}

        algorithms = [
            ("BFS 1", "BFS 1"), ("BFS 2", "BFS 2"),
            ("DFS 1 ", "DFS 1"), ("DFS 2", "DFS 2"),
            ("UCS", "UCS"), ("IDS1", "IDS1"), ("IDS2", "IDS2"),
            ("Greedy Search", "Greedy"), ("A* Search", "A*"), ("IDA* Search", "IDA*"),
            ("Simple Hill Climbing", "Simple HC"), ("Steepest Hill Climbing", "Steepest HC"),
            ("Stochastic Hill Climbing", "Stochastic HC"), ("Random Restart HC", "Random Restart HC"),
            ("Local Beam Search", "Local Beam Search"), ("Simulated Annealing", "Simulated Annealing"),
            ("Partial Observation Search", "Partial Observation Search"), ("Sensorless Search", "Sensorless Search"),
            ("AND-OR Graph Search", "AND-OR")
        ]

        for label, algo_key in algorithms:
            btn = tk.Button(
                scrollable_frame, text=label, font=("Helvetica", 10), bg="#a9a9a9", fg="#000000",
                relief="groove", bd=1, height=2, command=lambda a=algo_key: self.app.start_search(a)
            )
            btn.pack(fill="x", pady=4)
            self.buttons[algo_key] = btn

        pos_frame = tk.LabelFrame(self.frame, text="ĐẶT VỊ TRÍ BAN ĐẦU", font=("Helvetica", 9, "bold"), bg="#f4f4f4", fg="red", padx=5, pady=5)
        pos_frame.pack(fill="x", pady=15)

        tk.Label(pos_frame, text="Hàng (0-2):", bg="#f4f4f4").grid(row=0, column=0, padx=2, pady=5, sticky="w")
        self.ent_row = tk.Entry(pos_frame, width=8, justify="center")
        self.ent_row.insert(0, str(self.app.robot_row))
        self.ent_row.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(pos_frame, text="Cột (0-2):", bg="#f4f4f4").grid(row=1, column=0, padx=2, pady=5, sticky="w")
        self.ent_col = tk.Entry(pos_frame, width=8, justify="center")
        self.ent_col.insert(0, str(self.app.robot_col))
        self.ent_col.grid(row=1, column=1, padx=5, pady=5)

        btn_update = tk.Button(pos_frame, text="Cập Nhật", font=("Helvetica", 9, "bold"), bg="#e7e7e7", command=self.app.update_initial_position)
        btn_update.grid(row=2, column=0, columnspan=2, sticky="ew", pady=5)
        
        self.btn_reset = tk.Button(self.frame, text="Reset Bàn Cờ\n(Random)", font=("Helvetica", 10, "bold"), bg="#f2dede", fg="#a94442", relief="groove", bd=1, height=2, command=self.app.reset_random)
        self.btn_reset.pack(fill="x", pady=5)

        self.btn_dual = tk.Button(self.frame, text="🤖 Mô Phỏng 2 Bàn Cờ\n(Dual Board Mode)", font=("Helvetica", 10, "bold"), bg="#d9edf7", fg="#31708f", relief="groove", bd=1, height=2, command=self.app.open_dual_board_window)
        self.btn_dual.pack(fill="x", pady=5)

    def set_controls_state(self, state):
        for btn in self.buttons.values():
            btn.config(state=state)
        self.btn_reset.config(state=state)
        self.btn_dual.config(state=state)

