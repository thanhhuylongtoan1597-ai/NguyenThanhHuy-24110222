import tkinter as tk

class MiddlePanel:
    def __init__(self, parent, app):
        self.app = app
        self.frame = tk.Frame(parent, bg="#f4f4f4", width=420, height=720)
        self.frame.pack(side="left", fill="both", expand=False, padx=10, pady=15)
        self.frame.pack_propagate(False)

        self.canvas = tk.Canvas(self.frame, width=390, height=390, bg="white", highlightthickness=1, highlightbackground="#bdc3c7")
        self.canvas.pack(pady=5)
        self.canvas.bind("<Button-1>", self.app.on_canvas_click)

        tk.Label(self.frame, text="ĐƯỜNG ĐI TỐT NHẤT:", font=("Helvetica", 11, "bold"), bg="#f4f4f4").pack(anchor="w", pady=(15, 5))
        self.lbl_best_path = tk.Label(self.frame, text="Chua chay thuat toan", font=("Consolas", 11), bg="#ffffff", fg="#31708f", relief="solid", bd=1, padx=10, pady=15, height=3, wraplength=360, anchor="nw", justify="left")
        self.lbl_best_path.pack(fill="x", pady=5)

    def draw_all(self, matrix, robot_row, robot_col, px=None, py=None):
        self.canvas.delete("all")
        cs = 130 

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

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=bg_color, outline="#bcdbca" if text_val=="0" else "#f1b0b7")
                self.canvas.create_text(x1 + 12, y1 + 12, text=text_val, font=("Helvetica", 10, "bold"), fill="#2c3e50")

        if px is None or py is None:
            px = robot_col * cs + cs // 2 
            py = robot_row * cs + cs // 2 

        self.canvas.create_oval(px - 38, py - 38, px + 38, py + 38, fill="#3399ff", outline="white", width=2)
        self.canvas.create_text(px, py, text="🤖", font=("Helvetica", 22))
