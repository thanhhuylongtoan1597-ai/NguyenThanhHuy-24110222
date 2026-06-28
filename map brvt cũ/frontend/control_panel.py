import tkinter as tk

class ControlPanel:
    def __init__(self, parent, on_algo_select_cb, reset_cb, slider_cb):
        self.ctrl_box = tk.LabelFrame(parent, text="ĐIỀU KHIỂN THUẬT TOÁN", font=("Helvetica", 10, "bold"), bg="#f5f6fa", fg="#2c3e50", padx=10, pady=10)
        self.ctrl_box.pack(fill="x", pady=(0, 10))

        lbl_info = tk.Label(self.ctrl_box, text="Số màu mặc định: 3 màu (Đỏ, Xanh lá, Xanh dương)", font=("Helvetica", 9, "italic"), bg="#f5f6fa", fg="#7f8c8d")
        lbl_info.pack(anchor="w", pady=(0, 10))

        algo_frame = tk.Frame(self.ctrl_box, bg="#f5f6fa")
        algo_frame.pack(fill="x", pady=(0, 5))

        tk.Label(algo_frame, text="Chọn thuật toán:", font=("Helvetica", 10, "bold"), bg="#f5f6fa", fg="#2c3e50").pack(side="left", padx=5)

        self.algo_var = tk.StringVar(value="Chọn...")
        algorithms = ["Backtracking", "Forward Checking", "AC-3", "Min-Conflicts", "CSP"]
        
        self.algo_menu = tk.OptionMenu(
            algo_frame, 
            self.algo_var, 
            *algorithms, 
            command=on_algo_select_cb
        )
        self.algo_menu.config(font=("Helvetica", 10), bg="#ffffff", fg="#2c3e50", activebackground="#eceff1", relief="flat", width=20)
        self.algo_menu.pack(side="right", padx=5, fill="x", expand=True)

        bottom_ctrl = tk.Frame(self.ctrl_box, bg="#f5f6fa")
        bottom_ctrl.pack(fill="x", pady=(10, 0))

        self.btn_reset = tk.Button(bottom_ctrl, text="Reset bản đồ", font=("Helvetica", 9, "bold"), bg="#e74c3c", fg="white", relief="flat", command=reset_cb)
        self.btn_reset.pack(side="left", padx=5)

        self.lbl_step_counter = tk.Label(bottom_ctrl, text="Trạng thái: Chọn thuật toán", font=("Helvetica", 10, "bold"), bg="#f5f6fa", fg="#2c3e50")
        self.lbl_step_counter.pack(side="right", padx=5)

        slider_frame = tk.Frame(self.ctrl_box, bg="#f5f6fa")
        slider_frame.pack(fill="x", pady=(10, 0))
        
        self.step_slider = tk.Scale(
            slider_frame, 
            from_=0, 
            to=0, 
            orient="horizontal", 
            bg="#f5f6fa", 
            highlightthickness=0,
            command=slider_cb
        )
        self.step_slider.pack(fill="x", expand=True)

    def set_slider_range(self, from_val, to_val, current_val):
        self.step_slider.config(from_=from_val, to=to_val)
        self.step_slider.set(current_val)

    def reset_controls(self):
        self.algo_var.set("Chọn...")
        self.step_slider.config(from_=0, to=0)
        self.step_slider.set(0)
