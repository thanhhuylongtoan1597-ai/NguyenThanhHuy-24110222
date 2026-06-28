import tkinter as tk
from tkinter import scrolledtext

class RightPanel:
    def __init__(self, parent, app):
        self.app = app
        self.frame = tk.Frame(parent, bg="#f4f4f4")
        self.frame.pack(side="left", fill="both", expand=True, padx=15, pady=15)

        tk.Label(self.frame, text="THỐNG KÊ & LỊCH SỬ", font=("Helvetica", 13, "bold"), bg="#f4f4f4", fg="#2c3e50").pack(anchor="w", pady=(0, 10))

        db_frame = tk.LabelFrame(self.frame, text="Bảng Thống Kê (Dashboard)", font=("Helvetica", 10, "bold"), bg="#f4f4f4", fg="#34495e", padx=15, pady=10)
        db_frame.pack(fill="x", pady=5)

        self.lbl_path_cost = tk.Label(db_frame, text="Số bước đi (Path Cost): 0", font=("Helvetica", 10), bg="#f4f4f4", anchor="w")
        self.lbl_path_cost.pack(fill="x", pady=3)

        self.lbl_nodes = tk.Label(db_frame, text="Số Node đã duyệt: 0", font=("Helvetica", 10), bg="#f4f4f4", anchor="w")
        self.lbl_nodes.pack(fill="x", pady=3)

        self.lbl_time = tk.Label(db_frame, text="Thời gian chạy: 0.00 ms", font=("Helvetica", 10), bg="#f4f4f4", anchor="w")
        self.lbl_time.pack(fill="x", pady=3)

        log_frame = tk.LabelFrame(self.frame, text="Console Log (Lịch sử hành động)", font=("Helvetica", 10, "bold"), bg="#f4f4f4", fg="#34495e", padx=10, pady=10)
        log_frame.pack(fill="both", expand=True, pady=10)

        self.log_text = scrolledtext.ScrolledText(log_frame, font=("Consolas", 10), bg="#2c3e50", fg="#ecf0f1", wrap="word")
        self.log_text.pack(fill="both", expand=True)
        self.log_text.insert(tk.END, "Hệ thống sẵn sàng. Nhấn nút để bắt đầu giải thuật.\n")

    def log(self, text):
        self.log_text.insert(tk.END, text)
        self.log_text.see(tk.END)

    def clear_log(self):
        self.log_text.delete("1.0", tk.END)
