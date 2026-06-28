import tkinter as tk
from tkinter import scrolledtext

class LogPanel:
    def __init__(self, parent):
        self.log_box = tk.LabelFrame(parent, text="NHẬT KÝ THUẬT TOÁN", font=("Helvetica", 10, "bold"), bg="#f5f6fa", fg="#2c3e50", padx=5, pady=5)
        self.log_box.pack(fill="both", expand=True)

        self.log_area = scrolledtext.ScrolledText(self.log_box, font=("Consolas", 9), bg="#1e1e1e", fg="#ffffff", insertbackground="white", wrap="word")
        self.log_area.pack(fill="both", expand=True)

    def clear(self):
        self.log_area.delete("1.0", tk.END)

    def insert_system_msg(self, msg):
        self.log_area.insert(tk.END, msg)

    def update_log_display(self, text_msg):
        cleaned_msg = text_msg.replace("✓ ", "").replace("➔ ", "").replace("↩ ", "").replace("⚠ ", "")
        self.log_area.insert(tk.END, f"{cleaned_msg}\n")
        self.log_area.see(tk.END)
